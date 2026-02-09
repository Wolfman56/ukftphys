import wgpu
# import wgpu.backends.rs  <- Removed, let auto-discovery handle it
import numpy as np
import logging
import struct

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# WGSL SHADERS
# -----------------------------------------------------------------------------

SHADER_SOURCE = """
struct Particle {
    pos: vec3<f32>,
    vel: vec3<f32>,
};

struct Source {
    pos: vec3<f32>,
    mass: f32,
};

struct SimulationParams {
    n_particles: u32,
    n_sources: u32,
    sigma: f32,
    alpha: f32,
    dt: f32,
    damping: f32,
    pad1: f32, 
    pad2: f32,
};

@group(0) @binding(0)
var<storage, read_write> particles: array<Particle>;

@group(0) @binding(1)
var<storage, read> sources: array<Source>;

@group(0) @binding(2)
var<uniform> params: SimulationParams;

@compute @workgroup_size(64)
fn update_particles(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let i = global_id.x;
    if (i >= params.n_particles) {
        return;
    }

    var pos = particles[i].pos;
    var vel = particles[i].vel;
    
    var rho = 0.0;
    var grad_rho = vec3<f32>(0.0, 0.0, 0.0);
    let sigma_sq = params.sigma * params.sigma;

    // Iterate over sources (Entropic Gravity)
    for (var j = 0u; j < params.n_sources; j = j + 1u) {
        let s_pos = sources[j].pos;
        let s_mass = sources[j].mass;
        
        let delta = pos - s_pos;
        let dist_sq = dot(delta, delta);
        
        let gauss = s_mass * exp(-dist_sq / (2.0 * sigma_sq));
        
        rho = rho + gauss;
        // Gradient of exp(-r^2/2s^2) is exp(...) * (-r/s^2)
        // Correcting direction: gradient points UP density (towards source)
        // But (pos - s_pos) points AWAY from source.
        // So derivative wrt pos is: gauss * (-1.0/sigma_sq) * (pos - s_pos)
        // Which is gauss * (s_pos - pos) / sigma_sq
        // So a negative delta term.
        grad_rho = grad_rho + (gauss * (-delta) / sigma_sq);
    }
    
    // Entropic Force: alpha * grad(rho) / rho
    let eps = 1e-12;
    let acc = (params.alpha * grad_rho) / (rho + eps);
    
    // Update Dynamics
    vel = vel * params.damping + acc * params.dt;
    pos = pos + vel * params.dt;
    
    // Store back
    particles[i].pos = pos;
    particles[i].vel = vel;
}
"""

DENSITY_SHADER_SOURCE = """
struct Source {
    pos: vec3<f32>,
    mass: f32,
};

struct GridParams {
    width: u32,
    height: u32,
    n_sources: u32,
    sigma: f32,
    min_x: f32,
    max_x: f32,
    min_y: f32,
    max_y: f32,
};

@group(0) @binding(0)
var<storage, read_write> grid_density: array<f32>;

@group(0) @binding(1)
var<storage, read> sources: array<Source>;

@group(0) @binding(2)
var<uniform> params: GridParams;

@compute @workgroup_size(8, 8)
fn compute_density(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let ix = global_id.x;
    let iy = global_id.y;
    
    if (ix >= params.width || iy >= params.height) {
        return;
    }
    
    let w_f = f32(params.width);
    let h_f = f32(params.height);
    
    // Map index to physical coordinate
    let t_x = f32(ix) / (w_f - 1.0);
    let t_y = f32(iy) / (h_f - 1.0);
    
    let x = params.min_x + t_x * (params.max_x - params.min_x);
    let y = params.min_y + t_y * (params.max_y - params.min_y);
    let pos = vec3<f32>(x, y, 0.0);
    
    var rho = 0.0;
    let sigma_sq = params.sigma * params.sigma;
    
    for (var j = 0u; j < params.n_sources; j = j + 1u) {
        let s_pos = sources[j].pos;
        let s_mass = sources[j].mass;
        
        let delta = pos - s_pos;
        let dist_sq = dot(delta, delta);
        rho = rho + s_mass * exp(-dist_sq / (2.0 * sigma_sq));
    }
    
    let flat_idx = iy * params.width + ix;
    grid_density[flat_idx] = rho;
}
"""

RENDER_SHADER_SOURCE = """
struct Particle {
    pos: vec3<f32>,
    vel: vec3<f32>,
};

struct Camera {
    view_proj: mat4x4<f32>,
    width: f32,
    height: f32,
    point_size: f32,
};

@group(0) @binding(0)
var<storage, read> particles: array<Particle>;

@group(0) @binding(1)
var<storage, read_write> screen: array<atomic<u32>>;

@group(0) @binding(2)
var<uniform> cam: Camera;

@compute @workgroup_size(64)
fn render_points(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let i = global_id.x;
    if (i >= arrayLength(&particles)) { return; }
    
    let pos_world = vec4<f32>(particles[i].pos, 1.0);
    var clip = cam.view_proj * pos_world;
    
    // Perspective Division
    let ndc = clip.xyz / clip.w;
    
    // Check if inside frustum
    if (clip.w > 0.0 && ndc.x >= -1.0 && ndc.x <= 1.0 && ndc.y >= -1.0 && ndc.y <= 1.0 && ndc.z >= 0.0 && ndc.z <= 1.0) {
        
        // Map to Screen Coords [0, W]
        // NDC Y is up in WGPU (or Vulkan -1 to 1)
        // Screen Y usually top-down or bottom-up depending on format. Let's do standard.
        let x = u32((ndc.x * 0.5 + 0.5) * cam.width);
        let y = u32((1.0 - (ndc.y * 0.5 + 0.5)) * cam.height); // Flip Y
        
        let w = u32(cam.width);
        let h = u32(cam.height);
        
        if (x < w && y < h) {
            let idx = y * w + x;
            atomicAdd(&screen[idx], 1u);
        }
    }
}
"""

# -----------------------------------------------------------------------------
# UKFT GPU ACCELERATOR
# -----------------------------------------------------------------------------

class EntropicGPUAccelerator:
    def __init__(self):
        self.device = wgpu.utils.get_default_device()
        self.queue = self.device.queue
        self.adapter = self.device.adapter
        
        logger.info(f"Initialized GPU Accelerator: {self.adapter.summary}")
        
        # Pipelines (Lazily created)
        self.sim_pipeline = None
        self.grid_pipeline = None
        self.render_pipeline = None
        
    def _create_sim_pipeline(self):
        shader = self.device.create_shader_module(code=SHADER_SOURCE)
        
        # Define Binding Layouts
        # 0: Particles (RW), 1: Sources (R), 2: Params (Uniform)
        entries = [
            {"binding": 0, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.storage}},
            {"binding": 1, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.read_only_storage}},
            {"binding": 2, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.uniform}},
        ]
        bind_group_layout = self.device.create_bind_group_layout(entries=entries)
        pipeline_layout = self.device.create_pipeline_layout(bind_group_layouts=[bind_group_layout])
        
        compute_pipeline = self.device.create_compute_pipeline(
            layout=pipeline_layout,
            compute={"module": shader, "entry_point": "update_particles"},
        )
        return compute_pipeline, bind_group_layout

    def _create_grid_pipeline(self):
        shader = self.device.create_shader_module(code=DENSITY_SHADER_SOURCE)
        entries = [
            {"binding": 0, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.storage}},
            {"binding": 1, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.read_only_storage}},
            {"binding": 2, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.uniform}},
        ]
        bind_group_layout = self.device.create_bind_group_layout(entries=entries)
        pipeline_layout = self.device.create_pipeline_layout(bind_group_layouts=[bind_group_layout])
        
        compute_pipeline = self.device.create_compute_pipeline(
            layout=pipeline_layout,
            compute={"module": shader, "entry_point": "compute_density"},
        )
        return compute_pipeline, bind_group_layout

    def _create_render_pipeline(self):
        shader = self.device.create_shader_module(code=RENDER_SHADER_SOURCE)
        entries = [
            {"binding": 0, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.read_only_storage}},
            {"binding": 1, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.storage}}, # Atomic needs standard storage
            {"binding": 2, "visibility": wgpu.ShaderStage.COMPUTE, "buffer": {"type": wgpu.BufferBindingType.uniform}},
        ]
        bind_group_layout = self.device.create_bind_group_layout(entries=entries)
        pipeline_layout = self.device.create_pipeline_layout(bind_group_layouts=[bind_group_layout])
        
        compute_pipeline = self.device.create_compute_pipeline(
            layout=pipeline_layout,
            compute={"module": shader, "entry_point": "render_points"},
        )
        return compute_pipeline, bind_group_layout

    def run_simulation_step(self, particles_pos, particles_vel, sources, sim_params):
        """
        Runs one time step of the particle simulation on GPU.
        Returns updated (pos, vel).
        """
        N = len(particles_pos)
        M = len(sources)
        
        # 1. Prepare Data
        # Particle Struct: vec3 pos, f32 pad, vec3 vel, f32 pad (Total 8 floats = 32 bytes)
        # We need to interleave pos and vel
        p_data = np.zeros((N, 8), dtype=np.float32)
        p_data[:, 0:3] = particles_pos.astype(np.float32)
        p_data[:, 4:7] = particles_vel.astype(np.float32)
        # padding is zero
        
        # Source Struct: vec3 pos, f32 mass (4 floats = 16 bytes)
        s_data = np.zeros((M, 4), dtype=np.float32)
        for i, (pos, mass) in enumerate(sources):
            s_data[i, 0:3] = pos
            s_data[i, 3] = mass
            
        # Param Struct Matching Shader:
        # n_particles(u32), n_sources(u32), sigma(f32), alpha(f32)
        # dt(f32), damping(f32), pad1(f32), pad2(f32)
        # Total 32 bytes (8 * 4)
        
        params_bytes = struct.pack(
            'IIffffff',
            N, M, 
            sim_params['sigma'], 
            sim_params['alpha'], 
            sim_params['dt'], 
            sim_params['damping'],
            0.0, 0.0
        )
        # Note: struct.pack returns bytes. We can wrap in np.frombuffer if needed, 
        # but create_buffer_with_data accepts bytes if we handle it or pass numpy array.
        # wgpu-py expects memoryview-compatible.
        params_np = np.frombuffer(params_bytes, dtype=np.uint8)

        # 2. Create Buffers
        p_buffer = self.device.create_buffer_with_data(data=p_data, usage=wgpu.BufferUsage.STORAGE | wgpu.BufferUsage.COPY_SRC)
        s_buffer = self.device.create_buffer_with_data(data=s_data, usage=wgpu.BufferUsage.STORAGE)
        u_buffer = self.device.create_buffer_with_data(data=params_np, usage=wgpu.BufferUsage.UNIFORM)
        
        # 3. Pipeline
        if not self.sim_pipeline:
            self.sim_pipeline, self.sim_bg_layout = self._create_sim_pipeline()
            
        bind_group = self.device.create_bind_group(
            layout=self.sim_bg_layout,
            entries=[
                {"binding": 0, "resource": {"buffer": p_buffer, "offset": 0, "size": p_buffer.size}},
                {"binding": 1, "resource": {"buffer": s_buffer, "offset": 0, "size": s_buffer.size}},
                {"binding": 2, "resource": {"buffer": u_buffer, "offset": 0, "size": u_buffer.size}},
            ]
        )
        
        # 4. Discrete Dispatch
        command_encoder = self.device.create_command_encoder()
        compute_pass = command_encoder.begin_compute_pass()
        compute_pass.set_pipeline(self.sim_pipeline)
        compute_pass.set_bind_group(0, bind_group, [], 0, 999999) # dynamic offsets
        
        workgroups = (N + 63) // 64
        compute_pass.dispatch_workgroups(workgroups, 1, 1)
        compute_pass.end()
        
        # 5. Readback
        # We need a staging buffer or just read_buffer (wgpu-py convenience)
        # But create_buffer_with_data returns a mapped buffer? No, usually device local.
        # Use queue.submit and then read
        self.queue.submit([command_encoder.finish()])
        
        # Read back particles
        result_bytes = self.device.queue.read_buffer(p_buffer)
        result_data = np.frombuffer(result_bytes, dtype=np.float32).reshape((N, 8))
        
        new_pos = result_data[:, 0:3]
        new_vel = result_data[:, 4:7]
        
        return new_pos, new_vel


    def render_density_view(self, particles_pos, width, height, mvp_matrix):
        """
        Renders particles to a density map (heatmap) on GPU using Atomic Add.
        Returns a (H, W) numpy float32 array used for visualization.
        """
        N = len(particles_pos)
        
        # 1. Prepare Particles
        # We generally re-use the format from simulation but simplified: Just POS is needed.
        # But our shader expects Particle struct {pos, vel}. We can reuse the sim buffer if we kept it alive.
        # For simplicity, we upload again (transfer overhead is small compared to plotting).
        p_data = np.zeros((N, 8), dtype=np.float32)
        p_data[:, 0:3] = particles_pos.astype(np.float32)
        
        # 2. Prepare Camera Uniforms
        # Mat4 (16 floats) + w, h, point_size, pad (4 floats) = 20 floats
        cam_data = np.zeros(20, dtype=np.float32)
        cam_data[0:16] = mvp_matrix.flatten()
        cam_data[16] = float(width)
        cam_data[17] = float(height)
        cam_data[18] = 1.0 # point size (unused in atomic accumulation)
        
        # 3. Create Buffers
        p_buffer = self.device.create_buffer_with_data(data=p_data, usage=wgpu.BufferUsage.STORAGE)
        
        # Screen Buffer: Atomic U32. Initialized to zero.
        screen_size = width * height * 4 # 4 bytes per pixel
        screen_buffer = self.device.create_buffer(size=screen_size, usage=wgpu.BufferUsage.STORAGE | wgpu.BufferUsage.COPY_SRC)
        
        cam_buffer = self.device.create_buffer_with_data(data=cam_data, usage=wgpu.BufferUsage.UNIFORM)
        
        # 4. Pipeline
        if not self.render_pipeline:
            self.render_pipeline, self.render_bg_layout = self._create_render_pipeline()
            
        bind_group = self.device.create_bind_group(
            layout=self.render_bg_layout,
            entries=[
                {"binding": 0, "resource": {"buffer": p_buffer, "offset": 0, "size": p_buffer.size}},
                {"binding": 1, "resource": {"buffer": screen_buffer, "offset": 0, "size": screen_buffer.size}},
                {"binding": 2, "resource": {"buffer": cam_buffer, "offset": 0, "size": cam_buffer.size}},
            ]
        )
        
        # 5. Dispatch
        command_encoder = self.device.create_command_encoder()
        
        # Clear screen buffer (technically create_buffer zeros it, but good practice if reusing)
        # command_encoder.clear_buffer(screen_buffer, 0, screen_size) 
        
        compute_pass = command_encoder.begin_compute_pass()
        compute_pass.set_pipeline(self.render_pipeline)
        compute_pass.set_bind_group(0, bind_group, [], 0, 999999)
        
        workgroups = (N + 63) // 64
        compute_pass.dispatch_workgroups(workgroups, 1, 1)
        compute_pass.end()
        
        self.queue.submit([command_encoder.finish()])
        
        # 6. Readback
        result_bytes = self.device.queue.read_buffer(screen_buffer)
        result_data = np.frombuffer(result_bytes, dtype=np.uint32).reshape((height, width))
        
        return result_data.astype(np.float32)

    def compute_density_grid(self, width, height, x_range, y_range, sources, sigma):
        """
        Computes 2D density grid on GPU.
        """
        M = len(sources)
        s_data = np.zeros((M, 4), dtype=np.float32)
        for i, (pos, mass) in enumerate(sources):
            s_data[i, 0:3] = pos
            s_data[i, 3] = mass
            
        params_arr = np.array([
            width, height, M, 0, # u32 part (need to act as if viewed as u32)
            sigma, x_range[0], x_range[1], y_range[0], y_range[1],
            0.0, 0.0 # padding
        ], dtype=np.float32)
        
        # FIX: The struct has mixed types (u32, f32). Python numpy array must be byte-exact.
        # Struct: u32, u32, u32, f32 ... 
        # Actually WGSL Uniforms align to 16 bytes.
        # Let's use specific packing.
        # struct GridParams { width(u32), height(u32), n_sources(u32), sigma(f32) } -> 16 bytes perfect.
        # min_x(f32), max_x(f32), min_y(f32), max_y(f32) -> 16 bytes perfect.
        # Total 32 bytes.
        
        import struct
        packed_params = struct.pack(
            'IIIfffff', 
            width, height, M, sigma,
            float(x_range[0]), float(x_range[1]), float(y_range[0]), float(y_range[1])
        )
        
        # Buffers
        n_pixels = width * height
        grid_bytes_size = n_pixels * 4 # f32
        
        # Output buffer
        grid_buffer = self.device.create_buffer(size=grid_bytes_size, usage=wgpu.BufferUsage.STORAGE | wgpu.BufferUsage.COPY_SRC)
        
        s_buffer = self.device.create_buffer_with_data(data=s_data, usage=wgpu.BufferUsage.STORAGE)
        u_buffer = self.device.create_buffer_with_data(data=packed_params, usage=wgpu.BufferUsage.UNIFORM)
        
        if not self.grid_pipeline:
            self.grid_pipeline, self.grid_bg_layout = self._create_grid_pipeline()
            
        bind_group = self.device.create_bind_group(
            layout=self.grid_bg_layout,
            entries=[
                {"binding": 0, "resource": {"buffer": grid_buffer, "offset": 0, "size": grid_buffer.size}},
                {"binding": 1, "resource": {"buffer": s_buffer, "offset": 0, "size": s_buffer.size}},
                {"binding": 2, "resource": {"buffer": u_buffer, "offset": 0, "size": u_buffer.size}},
            ]
        )
        
        command_encoder = self.device.create_command_encoder()
        compute_pass = command_encoder.begin_compute_pass()
        compute_pass.set_pipeline(self.grid_pipeline)
        compute_pass.set_bind_group(0, bind_group, [], 0, 999999)
        
        gx = (width + 7) // 8
        gy = (height + 7) // 8
        compute_pass.dispatch_workgroups(gx, gy, 1)
        compute_pass.end()
        
        self.queue.submit([command_encoder.finish()])
        
        result_bytes = self.device.queue.read_buffer(grid_buffer)
        grid_vals = np.frombuffer(result_bytes, dtype=np.float32).reshape((height, width))
        
        return grid_vals

