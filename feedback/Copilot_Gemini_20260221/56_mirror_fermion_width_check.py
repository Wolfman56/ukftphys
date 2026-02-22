
import numpy as np

def verify_5_9_rule():
    print("Verifying the '5/9 Rule' from UKFT Paper 35...")
    
    # 1. Inputs
    alpha_em_inv = 137.035999  # Fine Structure Constant at low energy
    alpha_em = 1.0 / alpha_em_inv
    
    mirror_mass_gev = 320.0
    
    # 2. The Prediction: Gamma/M = (5/9) * alpha_em
    predicted_ratio = (5.0/9.0) * alpha_em
    predicted_width = predicted_ratio * mirror_mass_gev
    
    print(f"Alpha_EM: {alpha_em:.6e} (1/{alpha_em_inv:.2f})")
    print(f"Predicted Ratio (Gamma/M): {predicted_ratio:.6e}")
    print(f"Predicted Width (Gamma) for M={mirror_mass_gev} GeV: {predicted_width:.4f} GeV")
    
    # 3. The "GUT" Interpretation Check
    # Claim: 5/9 * alpha_em = 5/24 * alpha_gut IF alpha_em = 3/8 * alpha_gut
    # Let's check the algebra
    # 5/24 * alpha_gut = 5/24 * (8/3 * alpha_em) = (5*8)/(24*3) * alpha_em
    # = 40/72 * alpha_em = 5/9 * alpha_em
    
    lhs = (5.0/9.0)
    rhs_factor = (5.0/24.0) * (8.0/3.0)
    
    print("-" * 30)
    print("Algebraic Check:")
    print(f"LHS Factor (Pheno): 5/9 = {lhs:.6f}")
    print(f"RHS Factor (GUT): 5/24 * 8/3 = {rhs_factor:.6f}")
    
    if abs(lhs - rhs_factor) < 1e-9:
        print(">> Algebraic Derivation: CONSISTENT")
    else:
        print(">> Algebraic Derivation: INCONSISTENT")
        
    print("-" * 30)
    print("Conclusion:")
    print(f"The Mirror Fermion at {mirror_mass_gev} GeV should have a width of ~{predicted_width:.2f} GeV.")
    
if __name__ == "__main__":
    verify_5_9_rule()
