
try:
    import wgpu
    print("wgpu is available")
    import wgpu.backends.rs
    print("wgpu backend is available")
except ImportError:
    print("wgpu is NOT available")

try:
    import torch
    print(f"torch is available: {torch.__version__}")
    if torch.cuda.is_available():
        print("torch.cuda is available")
    elif torch.backends.mps.is_available():
        print("torch.mps is available (macOS)")
    else:
        print("torch cpu only")
except ImportError:
    print("torch is NOT available")
