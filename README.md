# 🔬 CsPbI3 Thermodynamic & Phase Predictor Suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23370541.svg)](https://doi.org/10.5281/zenodo.23370541)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://babatunde-shoyombo-cspbi3-predictor.streamlit.app/)

**Developers:** Babatunde H. Shoyombo & Dr. A. D. Adewoyin  
**Institution:** University of Lagos, Nigeria.  

This repository contains the computational workflow, Machine Learning validation scripts, and the source code for the **CsPbI3 Phase Predictor**—an interactive web application developed as part of a Master's Thesis investigating the thermodynamic degradation of all-inorganic perovskite solar cells.

## 📖 Project Overview
Cesium Lead Iodide CsPbI3) is a highly promising material for next-generation solar cells. However, its photoactive "black" perovskite phases ($\alpha, \beta, \gamma$) spontaneously degrade into an inactive "yellow" non-perovskite phase ($\delta$) at room temperature. 

Simulating this degradation using traditional Ab Initio Molecular Dynamics (AIMD) requires prohibitive supercomputing resources. This project overcomes that hardware bottleneck by deploying a **Hybrid First-Principles and Machine Learning (ML)** methodology:
1. **Density Functional Theory (DFT):** Used to establish a rigorous 0 K energetic baseline.
2. **Machine Learning (MACE-MP-0):** An equivariant graph neural network used to accelerate structural relaxations, finite-temperature phonons, and perturbation engineering by a factor of >1000x.

## ⚙️ Repository Structure
* `/01_DFT_Baseline/` - Scripts for high-precision static SCF calculations (Quantum ESPRESSO).
* `/02_ML_Validation/` - AI-driven geometric relaxations validating the MACE model against DFT.
* `/03_Thermodynamics/` - Finite-displacement phonon coupling via `phonopy` to map Helmholtz Free Energy (0 K to 800 K).
* `/04_Perturbations/` - Engineering simulations evaluating biaxial epitaxial strain (-4% to +4%) and (100) surface facet cleavage.
* `app.py` - The source code for the interactive Streamlit web application.
* `requirements.txt` - Python dependencies required to run the application.

## 🚀 Live Web Application
The computational data generated in this study has been translated into an open-source, interactive predictive tool for experimental researchers. 
**Access the live app here:** [CsPbI3 Phase Predictor Suite](https://babatunde-shoyombo-cspbi3-predictor.streamlit.app/)

## 📝 How to Cite
If you use this software, datasets, or methodology in your academic research, please cite:

> **Shoyombo, B. H., & Adewoyin, A. D. (2026). *CsPbI3 Thermodynamic & Phase Predictor Suite (v1.0)*. Zenodo. DOI: [10.5281/zenodo.23370541](https://doi.org/10.5281/zenodo.23370541)**

## 🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.
