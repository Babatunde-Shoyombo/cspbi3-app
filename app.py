import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io

# ==========================================
# PAGE CONFIGURATION & HEADER
# ==========================================
st.set_page_config(page_title="CsPbI3 Thermodynamic Suite", layout="wide")

st.title("🔬 CsPbI$_3$ Thermodynamic & Phase Predictor Suite")
st.markdown("""
**Author:** [Your Name] | **Institution:** [Your University]  
An interactive, Machine Learning-derived thermodynamic dashboard for predicting the phase stability of CsPbI$_3$ under thermal, strain, and nanoscale surface perturbations.
""")

# ==========================================
# PHYSICAL CONSTANTS (From your ML/DFT Data)
# ==========================================
phases = ['delta', 'gamma', 'beta', 'alpha']
labels = ['Yellow (Non-Perovskite)', 'Black (Orthorhombic)', 'Black (Tetragonal)', 'Black (Cubic)']
colors = ['#FFD700', '#404040', '#606060', '#808080']

E0 = {'delta': 0.0, 'gamma': 0.05, 'beta': 0.08, 'alpha': 0.15} # Base Energy (eV)
S_slopes = {'delta': 0.0001, 'gamma': 0.0003, 'beta': 0.0004, 'alpha': 0.0006} # Entropy slopes
Surf_E = {'delta': 0.136, 'gamma': 0.100, 'beta': 0.085, 'alpha': 0.072} # Surface Energies (J/m^2)

# Convert Surface Energy from J/m^2 to eV/A^2 (1 J = 6.242e18 eV, 1 m^2 = 1e20 A^2)
conversion_factor = 6.242e18 / 1e20
for p in phases: Surf_E[p] = Surf_E[p] * conversion_factor

def get_strain_penalty(phase, s):
    return 0.005 * (s**2) if phase == 'delta' else 0.015 * (s**2)

# ==========================================
# APP LAYOUT: TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Bulk Strain Analysis", "📏 Nanoscale Thin Films", "🗺️ 2D Phase Diagram", "📄 How to Cite"])

# ------------------------------------------
# TAB 1: BULK STRAIN ANALYSIS
# ------------------------------------------
with tab1:
    st.header("Bulk Material Stability")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Control Panel")
        temp = st.slider("Temperature (K)", 0, 800, 300, 10, key="t1")
        strain = st.slider("Biaxial Strain (%)", -4.0, 4.0, 0.0, 0.1, key="s1")
        
        free_energies = {p: E0[p] - (S_slopes[p] * temp) + get_strain_penalty(p, strain) for p in phases}
        stable_p = min(free_energies, key=free_energies.get)
        
        st.write("### 🏆 Ground State:")
        st.success(f"**{stable_p.upper()} Phase** is currently the most stable.")
        
        # Data export
        df = pd.DataFrame({"Phase": phases, "Relative Free Energy (eV)": list(free_energies.values())})
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data as CSV", data=csv, file_name="bulk_thermo_data.csv", mime="text/csv")

    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([labels[i] for i,p in enumerate(phases)], list(free_energies.values()), color=colors, edgecolor='black')
        ax.set_ylabel("Relative Free Energy (eV/FU)")
        ax.set_title(f"Bulk Stability at {temp} K and {strain}% Strain")
        ax.axhline(0, color='black')
        st.pyplot(fig)

# ------------------------------------------
# TAB 2: NANOSCALE THIN FILMS
# ------------------------------------------
with tab2:
    st.header("Surface Energy & Nanoscale Stability")
    st.markdown("At the nanoscale, surface area dominates over volume. Adjust the thickness of the film to see how surface energy stabilizes the Black phase!")
    
    col3, col4 = st.columns([1, 2])
    with col3:
        thickness = st.slider("Film Thickness (Nanometers)", 1.0, 50.0, 10.0, 1.0)
        temp_nano = st.slider("Temperature (K)", 0, 800, 300, 10, key="t2")
        
        # Thickness in Angstroms
        t_angstrom = thickness * 10
        # Total Energy = Bulk Energy + (2 * Surface Energy / thickness)
        nano_energies = {p: (E0[p] - (S_slopes[p] * temp_nano)) + (2 * Surf_E[p] / t_angstrom) for p in phases}
        stable_nano = min(nano_energies, key=nano_energies.get)
        
        st.write("### 🏆 Ground State at this Thickness:")
        if stable_nano == 'delta': st.warning("Yellow Phase Dominates.")
        else: st.success(f"Black Phase ({stable_nano.upper()}) is Stabilized!")

    with col4:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.bar([labels[i] for i,p in enumerate(phases)], list(nano_energies.values()), color=colors, edgecolor='black')
        ax2.set_ylabel("Total Energy (Bulk + Surface) (eV)")
        ax2.set_title(f"Nanoscale Stability for {thickness} nm Film at {temp_nano} K")
        st.pyplot(fig2)

# ------------------------------------------
# TAB 3: 2D PHASE DIAGRAM
# ------------------------------------------
with tab3:
    st.header("🗺️ Temperature-Strain Phase Diagram")
    st.markdown("This contour map shows the most stable phase across all temperatures and strains simultaneously.")
    
    T_range = np.linspace(0, 800, 100)
    S_range = np.linspace(-4.0, 4.0, 100)
    T_mesh, S_mesh = np.meshgrid(T_range, S_range)
    
    # Create phase map: 0=delta, 1=gamma, 2=beta, 3=alpha
    Z_map = np.zeros_like(T_mesh)
    
    for i in range(100):
        for j in range(100):
            t_val = T_mesh[i, j]
            s_val = S_mesh[i, j]
            e_vals = [E0[p] - (S_slopes[p] * t_val) + get_strain_penalty(p, s_val) for p in phases]
            Z_map[i, j] = np.argmin(e_vals)
            
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    contour = ax3.contourf(T_mesh, S_mesh, Z_map, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], colors=colors)
    ax3.set_xlabel("Temperature (K)")
    ax3.set_ylabel("Biaxial Strain (%)")
    ax3.set_title("Global Phase Diagram of CsPbI3")
    st.pyplot(fig3)

# ------------------------------------------
# TAB 4: HOW TO CITE (SECURITY & IP)
# ------------------------------------------
with tab4:
    st.header("📄 Copyright, Citation & Methodology")
    st.markdown("""
    **Developer:** [Your Name]  
    **License:** MIT Open Source License  
    
    This application is the result of a Master's Thesis investigating the thermodynamic degradation of CsPbI$_3$. Data was generated using Quantum ESPRESSO (DFT) and MACE-MP-0 Machine Learning potentials coupled with Phonopy.
    
    ### 📝 How to Cite this Software:
    If you use this tool to generate graphs or data for an academic publication, please cite:
    
    > **[Your Last Name, Initial.], (2026). *CsPbI3 Thermodynamic & Phase Predictor Suite*. [GitHub Repository / Zenodo DOI link to be inserted here].**
    """)
