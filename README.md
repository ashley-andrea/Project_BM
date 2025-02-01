
## Brain Modeling Project 2024/2025

# Comparison of Cerebellar Spiking Neural Networks and Mean-Field Models
This project explores the differences between a spiking neural network (SNN) and a mean-field model of the cerebellum. Using the NEST simulator, we construct a biologically inspired Leaky Integrate-and-Fire (LIF) network and compare its dynamics to a rate-based approximation.

## Objectives
The goal of this project is to analyze how the level of abstraction in neural modeling affects network behavior. We implement:
1. Spiking Neural Network (SNN) in NEST:
    - Construct a network of excitatory and inhibitory LIF neurons.
    - Define synaptic connectivity and external inputs.
    - Record neural activity via spike trains, raster plots, and average firing rates.
2. Mean-Field Model Representation:
    - Develop a simplified differential equation-based model.
    - Capture the average firing rates of excitatory and inhibitory populations.
    - Comparison of the Two Approaches.
3. Steady-state firing rates across models.
    - Transition points (e.g., shifts between low/high activity or asynchronous/synchronized states).
    - Temporal patterns, including oscillations and fluctuations.

## Requirements
To set up the environment, it is recommended to use Conda and install dependencies from the `requirements.txt` file.
Software & Libraries:
- NEST Simulator for SNN simulations.

## Authors
- [@22cav](https://www.github.com/22cav)
