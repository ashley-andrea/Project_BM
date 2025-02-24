
## Brain Modeling Project 2024/2025

# Comparison of Cerebellar Spiking Neural Networks
This project investigates the differences between two spiking neural network (SNN) models of the cerebellum. Using the NEST simulator, we implement a biologically inspired Leaky Integrate-and-Fire (LIF) network and compare its dynamics with a more detailed model that incorporates spatial information.
The simplest way to inspect the code and its functioning is through Colab: check below for the link.

## Colab compatibility
If you want to open and run this project with colab, follow this link: 
[Colab Link](https://colab.research.google.com/github/22cav/Project_BM/blob/main/cerebellum_simulation(Colab).ipynb)

## Objectives
The goal of this project is to examine how different levels of abstraction in neural modeling influence network behavior. Specifically, we:

1. Implement a Spiking Neural Network (SNN) in NEST:
   - Construct a network of excitatory and inhibitory LIF neurons.
   - Define synaptic connectivity and external inputs.
   - Analyze neural activity using spike trains, raster plots, and average firing rates.
2. Compare Network Dynamics:
   - Measure firing rates across models.
   - Examine temporal patterns, including oscillations and fluctuations.
   - Compare some variables extracted from the results (e.g. Correlation coefficients)

## Requirements
To set up the environment, it is recommended to use Conda and install dependencies from the `requirements.txt` file.
Software & Libraries:
- NEST Simulator for SNN simulations.

## Authors
- [@22cav](https://www.github.com/22cav)
- [@ashley-andrea](https://www.github.com/ashley-andrea)
- [@SofiaFormenti](https://www.github.com/SofiaFormenti)
