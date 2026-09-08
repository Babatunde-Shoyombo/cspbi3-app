import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CsPbI3 Phase Predictor", layout="wide")

st.title("🔬 CsPbI$_3$ Perovskite Phase Stability Explorer")
st.markdown("Welcome to the interactive thermodynamic dashboard! Adjust the temperature and biaxial strain sliders below to see how the free energy landscape of CsPbI$_3$ polymorphs changes based on the Machine Learning data generated in this thesis.")

st.sidebar.header("⚙️ Engineering Parameters")
temperature = st.sidebar.slider("Temperature (K)", min_value=0, max_value=800, value=300, step=10)
strain = st.sidebar.slider("Biaxial Epitaxial Strain (%)", min_value=-4.0, max_value=4.0, value=0.0, step=0.1)

# Baseline Energies and Entropic/Strain Slopes
E0 = {'delta': 0.0, 'gamma': 0.05, 'beta': 0.08, 'alpha': 0.15}
S_slopes = {'delta': 0.0001, 'gamma': 0.0003, 'beta': 0.0004, 'alpha': 0.0006}

def strain_penalty(phase, s):
    return 0.005 * (s**2) if phase == 'delta' else 0.015 * (s**2)

free_energies = {}
for phase in E0.keys():
    free_energies[phase] = E0[phase] - (S_slopes[phase] * temperature) + strain_penalty(phase, strain)

stable_phase = min(free_energies, key=free_energies.get)

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("🏆 Current Stable Phase")
    if stable_phase == 'delta':
        st.error("**Yellow $\delta$-Phase (Non-Perovskite)**\nThe solar cell has degraded!")
    else:
        st.success(f"**Black {stable_phase.capitalize()}-Phase (Perovskite)**\nThe solar cell is highly efficient!")
    
    st.write("### Relative Free Energies (eV)")
    for p, e in free_energies.items():
        st.write(f"- **{p.capitalize()}**: {e:.3f} eV")

with col2:
    st.subheader("📊 Thermodynamic Phase Map")
    fig, ax = plt.subplots(figsize=(8, 5))
    phases = ['delta (Yellow)', 'gamma (Black)', 'beta (Black)', 'alpha (Black)']
    energies = [free_energies['delta'], free_energies['gamma'], free_energies['beta'], free_energies['alpha']]
    colors = ['#FFD700', '#404040', '#606060', '#808080']
    
    ax.bar(phases, energies, color=colors, edgecolor='black')
    ax.set_ylabel("Relative Free Energy (eV)")
    ax.set_title(f"Phase Stability at {temperature} K and {strain}% Strain")
    ax.axhline(0, color='black', linewidth=1)
    st.pyplot(fig)
