import matplotlib.pyplot as plt
import numpy as np

def parse_decay_block(file_path, particle_id=25):
    """
    Parses the DECAY block for a specific particle from a MadGraph param_card.dat.
    """
    decay_data = {
        'total_width': 0.0,
        'channels': []
    }
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    in_decay_block = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split()
        
        # Check for DECAY 25 header
        if parts[0] == 'DECAY':
            if int(parts[1]) == particle_id:
                decay_data['total_width'] = float(parts[2])
                in_decay_block = True
            else:
                in_decay_block = False
            continue
            
        if in_decay_block:
            # If line starts with a new block or decay, stop
            if parts[0] == 'BLOCK' or parts[0] == 'DECAY':
                break
                
            # Parse decay channel
            # Format: BR  NDA  ID1 ID2 ... # Comment
            try:
                br = float(parts[0])
                nda = int(parts[1])
                ids = [int(p) for p in parts[2:2+nda]]
                
                # Map IDs to names
                name_map = {
                    5: 'b', -5: 'b~',
                    15: 'tau-', -15: 'tau+',
                    21: 'g',
                    22: 'gamma'
                }
                
                channel_name = " ".join([name_map.get(pid, str(pid)) for pid in ids])
                
                # Combine particle/antiparticle names into more readable format
                if "b" in channel_name and "b~" in channel_name:
                    channel_name = r"$b \bar{b}$"
                elif "tau-" in channel_name and "tau+" in channel_name:
                    channel_name = r"$\tau^- \tau^+$"
                elif "g g" in channel_name:
                    channel_name = r"$g g$"
                elif "gamma gamma" in channel_name:
                    channel_name = r"$\gamma \gamma$"
                
                decay_data['channels'].append({
                    'br': br,
                    'ids': ids,
                    'name': channel_name
                })
            except ValueError:
                continue
                
    return decay_data

def plot_branching_ratios(decay_data):
    """
    Plots the branching ratios as a pie chart and a bar chart.
    """
    channels = decay_data['channels']
    
    # Sort by BR
    channels.sort(key=lambda x: x['br'], reverse=True)
    
    labels = [c['name'] for c in channels]
    sizes = [c['br'] for c in channels]
    
    # Pie Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart for dominant modes
    # If there are very small modes, maybe group them? 
    # Here they are 95%, 5%, 0.3%, 0.007%. The last two are tiny.
    
    # Explode the 2nd slice (tau) slightly for visibility
    explode = [0] * len(sizes)
    if len(sizes) > 1:
        explode[1] = 0.1
    
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       shadow=False, startangle=20, pctdistance=0.85)
    
    # Draw circle for donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax1.add_artist(centre_circle)
    
    ax1.axis('equal')  
    ax1.set_title(f'Entropic Monopole (30 GeV) Decay Channels\nTotal Width $\Gamma = {decay_data["total_width"]*1000:.2f}$ MeV', fontsize=14)
    
    # Bar Chart (Log Scale for visibility of rare modes)
    bars = ax2.bar(labels, sizes, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax2.set_yscale('log')
    ax2.set_ylabel('Branching Ratio (Log Scale)')
    ax2.set_title('Branching Ratios by Channel')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add text labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height*1.1,
                f'{height:.2%}',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('experiments/48_entropic_monopole_decay_plot.png')
    print("Plot saved to experiments/48_entropic_monopole_decay_plot.png")

def calculate_lifetime(width_gev):
    """
    Calculates lifetime in seconds from width in GeV.
    tau = hbar / Gamma
    hbar = 6.582119569e-25 GeV s
    """
    hbar = 6.582119569e-25 # GeV s
    return hbar / width_gev

if __name__ == "__main__":
    param_card_path = "experiments/48_entropic_monopole_madgraph/monopole_process/Cards/param_card.dat"
    data = parse_decay_block(param_card_path)
    
    print(f"Total Width: {data['total_width']} GeV")
    lifetime = calculate_lifetime(data['total_width'])
    print(f"Lifetime: {lifetime:.2e} s")
    
    print("\nBranching Ratios:")
    for c in data['channels']:
        print(f"  {c['name']}: {c['br']:.4%}")
        
    plot_branching_ratios(data)
