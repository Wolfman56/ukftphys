import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_heatmap_with_contours(trajectory_data, rho_history, alpha_entropic=0.2, filename="results/ukft_choice_guided.html"):
    """
    Plots empirical particle density heatmap with theoretical wavefunction contours.
    """
    T_ticks, M_particles = trajectory_data.shape
    N = rho_history.shape[1]
    
    # Empirical heatmap (density over time)
    fig = make_subplots()
    hist_data = go.Histogram2d(x=np.repeat(np.arange(T_ticks), M_particles),
                              y=trajectory_data.flatten(),
                              nbinsx=T_ticks, nbinsy=N,
                              colorscale='Magma',
                              colorbar=dict(title="Empirical Density"))
    fig.add_trace(hist_data)
    
    # Theoretical contours
    contour = go.Contour(z=rho_history.T, # Transpose to align (Rows=Space=Y, Cols=Time=X)
                        x=np.arange(T_ticks),
                        y=np.arange(N),
                        contours_coloring='lines',
                        line_color='lime',
                        line_width=1.5,
                        contours=dict(showlabels=True))
    fig.add_trace(contour)
    
    # Sample trajectories overlay
    samples = 50
    # Guard against fewer particles
    actual_samples = min(samples, M_particles)
    
    for i in range(actual_samples):
        fig.add_trace(go.Scatter(x=np.arange(T_ticks),
                                 y=trajectory_data[:, i],
                                 mode='lines',
                                 line=dict(color='white', width=0.8),
                                 opacity=0.15,
                                 name=f"T_{i}"))
    
    fig.update_layout(title=f"Entropic Double Slit: Choice-Guided Trajectories + |ψ|² Contours (α_entropic={alpha_entropic})",
                      xaxis_title="Choice Tick / Emergent Time",
                      yaxis_title="Lattice Site",
                      height=800,
                      template="plotly_dark")
    
    # Save PNG
    png_filename = filename.replace(".html", ".png")
    fig.write_image(png_filename)
    print(f"Saved plot image to {png_filename}")

    fig.write_html(filename)
    # fig.show() # Commented out to prevent blocking in some environments, or keep it if running interactively

def plot_simulation_results(x_grid, choice_indices, history_rho, history_pos, history_time, L_phys, alpha_entropic, dt_base, title_prefix="UKFT Simulation"):
    """
    Generates interactive plots for UKFT simulation results.
    """
    # Grid for plotting
    # Y-Axis is now Choice Event (n), not Physical Time
    X, N_ticks = np.meshgrid(x_grid, choice_indices)

    # Figure 1: The "Knowledge Landscape" - 3D Surface of Density
    fig = go.Figure()

    # Add Surface: Probability Density
    fig.add_trace(go.Surface(
        z=history_rho,
        x=x_grid,
        y=choice_indices,
        colorscale='Magma',
        name='Knowledge Density |ψ|²',
        opacity=0.9,
        colorbar=dict(title='Density')
    ))

    # Update layout
    fig.update_layout(
        title=f'{title_prefix}: Universal Knowledge Field Evolution (Density vs Choice Event)',
        scene=dict(
            xaxis_title='Position (Lattice)',
            yaxis_title='Choice Event (n)',
            zaxis_title='Density',
        ),
        width=900,
        height=600,
    )

    # Figure 2: Trajectories and Potentials (2D Animation/Static Hybrid)
    # Plotting against Choice Event on Y-axis
    fig2 = go.Figure()

    # Background: Density Contour
    fig2.add_trace(go.Contour(
        z=history_rho,
        x=x_grid,
        y=choice_indices,
        colorscale='Viridis',
        name='Density',
        contours=dict(showlines=False),
        colorbar=dict(title='Density')
    ))

    # Overlay Trajectories (Plot just 50 for clarity)
    num_plot_paths = 50
    # Guard against having fewer particles than 50
    actual_num_paths = min(num_plot_paths, history_pos.shape[1])
    
    # We plot all segments at once for performance if possible, but here line-by-line is okay for 50
    for i in range(actual_num_paths):
        fig2.add_trace(go.Scatter(
            x=x_grid[history_pos[:, i]], # Map indices to x_grid
            y=choice_indices,
            mode='lines',
            opacity=0.3,
            line=dict(color='white', width=1),
            showlegend=False,
            name='Conscious Agent'
        ))

    # Add Physical Time as a secondary annotation or axis?
    # Let's add a trace on the right side showing Physical Time evolution
    fig2.add_trace(go.Scatter(
        x=np.full_like(history_time, L_phys/2 + 2), # Draw line on right edge
        y=choice_indices,
        mode='lines',
        line=dict(color='red', width=3),
        name='Physical Time',
        hovertext=[f"t_phys={t:.2f}" for t in history_time]
    ))

    fig2.update_layout(
        title=f'{title_prefix}: Choice-Guided Trajectories (Y=Choice Event, Z=Density)',
        xaxis_title='Position',
        yaxis_title='Choice Event (n)',
        width=900,
        height=600
    )

    # Figure 3: Time Dilaton (Physical Time vs Choice Event)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=choice_indices,
        y=history_time,
        mode='lines+markers',
        name='Emergent Time'
    ))
    fig3.update_layout(
        title='Emergent Physical Time from Choice Events',
        xaxis_title='Choice Event (n)',
        yaxis_title='Physical Time t',
        width=600,
        height=400
    )
    
    return fig, fig2, fig3

def save_plots_to_html(filename, figs, title, description):
    # Save PNGs for each figure
    base_filename = filename.replace(".html", "")
    for i, fig in enumerate(figs):
        png_name = f"{base_filename}_fig{i+1}.png"
        try:
            fig.write_image(png_name)
            print(f"Saved plot image to {png_name}")
        except Exception as e:
            print(f"Failed to save PNG {png_name}: {e}")

    with open(filename, 'w') as f:
        f.write(f"<h1>{title}</h1>")
        f.write(f"<h2>{description}</h2>")
        f.write(f"<p>Note: Y-axis represents discrete Choice Events. Physical time emerges dynamically based on field density.</p>")
        for fig in figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
