
## Brain Modeling Project 2024/2025

# Comparison of Cerebellar Spiking Neural Networks
This project investigates the differences between two spiking neural network (SNN) models of the cerebellum. Using the NEST simulator, we implement a biologically inspired Leaky Integrate-and-Fire (LIF) network and compare its dynamics with a more detailed model that incorporates spatial information.

## Objectives
The goal of this project is to examine how different levels of abstraction in neural modeling influence network behavior. Specifically, we:

1. Implement a Spiking Neural Network (SNN) in NEST:
   - Construct a network of excitatory and inhibitory LIF neurons.
   - Define synaptic connectivity and external inputs.
   - Analyze neural activity using spike trains, raster plots, and average firing rates.
2. Compare Network Dynamics:
   - Measure steady-state firing rates across models.
   - Identify transition points (e.g., shifts between low/high activity or asynchronous/synchronized states).
   - Examine temporal patterns, including oscillations and fluctuations.

## Requirements
To set up the environment, it is recommended to use Conda and install dependencies from the `requirements.txt` file.
Software & Libraries:
- NEST Simulator for SNN simulations.

## Authors
- [@22cav](https://www.github.com/22cav)
