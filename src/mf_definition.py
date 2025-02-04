import nest
import numpy as np
from simulation import run_simulation
from config import *

# Run the simulation
network = run_simulation()

# Select the population of interest
grc_pop = network["granule"]
goc_pop = network["golgi"]
pc_pop = network["purkinje"]
mli_pop = network["interneurons"]
mf_input = network["mossy_fibers"]
cf_input = network["climbing_fibers"]
dcn_output = network["dcn"]

# Define Siegert function
def siegert(mean, sigma, tau_m, V_th, V_reset, tau_ref):
    def integrand(x):
        return np.exp(x**2) * (1 + np.erf(x))
    lower = (V_reset - mean) / sigma
    upper = (V_th - mean) / sigma
    integral, _ = np.quad(integrand, lower, upper)
    return 1.0 / (tau_ref + tau_m * np.sqrt(np.pi) * integral)

# Population-specific parameters
grc_pam = GRANULE_CELL_PARAMS
goc_pam = GOLGI_CELL_PARAMS
pc_pam = PURKINJE_CELL_PARAMS
mli_pam = INTERNEURON_PARAMS

# Connection weights and in-degrees
conn_ext_grc = nest.GetConnections(mf_input, grc_pop)
J_ext_grc = np.mean(nest.GetStatus(conn_ext_grc, 'weight'))
N_ext_grc = len(conn_ext_grc) // len(grc_pop)

conn_ext_go = nest.GetConnections(mf_input, goc_pop)
J_ext_go = np.mean(nest.GetStatus(conn_ext_go, 'weight'))
N_ext_go = len(conn_ext_go) // len(goc_pop)

conn_ext_pc = nest.GetConnections(cf_input, pc_pop)
J_ext_pc = np.mean(nest.GetStatus(conn_ext_pc, 'weight'))
N_ext_pc = len(conn_ext_pc) // len(pc_pop)

conn_grc_goc = nest.GetConnections(grc_pop, goc_pop)
J_grc_goc = np.mean(nest.GetStatus(conn_grc_goc, 'weight'))
N_grc_goc = len(conn_grc_goc) // len(goc_pop)  

conn_goc_grc = nest.GetConnections(goc_pop, grc_pop)
J_goc_grc = -np.abs(np.mean(nest.GetStatus(conn_goc_grc, 'weight')))
N_goc_grc = len(conn_goc_grc) // len(grc_pop)

conn_goc_goc = nest.GetConnections(goc_pop, goc_pop)
J_goc_goc = -np.abs(np.mean(nest.GetStatus(conn_goc_goc, 'weight')))
N_goc_goc = len(conn_goc_goc) // len(goc_pop) 

conn_grc_mli = nest.GetConnections(grc_pop, mli_pop)
J_grc_mli = np.mean(nest.GetStatus(conn_grc_mli, 'weight'))
N_grc_mli = len(conn_grc_mli) // len(mli_pop)

conn_grc_pc = nest.GetConnections(grc_pop, pc_pop)
J_grc_pc = np.mean(nest.GetStatus(conn_grc_pc, 'weight'))
N_grc_pc = len(conn_grc_pc) // len(pc_pop)

conn_mli_mli = nest.GetConnections(mli_pop, mli_pop)
J_mli_mli = -np.abs(np.mean(nest.GetStatus(conn_mli_mli, 'weight')))
N_mli_mli = len(conn_mli_mli) // len(mli_pop)

conn_mli_pc = nest.GetConnections(mli_pop, pc_pop)
J_mli_pc = -np.abs(np.mean(nest.GetStatus(conn_mli_pc, 'weight')))
N_mli_pc = len(conn_mli_pc) // len(pc_pop)

conn_pc_ext = nest.GetConnections(pc_pop, dcn_output)
J_pc_ext = -np.abs(np.mean(nest.GetStatus(conn_pc_ext, 'weight')))
N_pc_ext = len(conn_pc_ext) // len(dcn_output)

# Population-specific transfer functions
def nu_grc(mu, sigma):
    return siegert(mu, sigma, grc_pam["tau_m"], grc_pam["V_th"], grc_pam["V_reset"], grc_pam["t_ref"])

def nu_goc(mu, sigma):
    return siegert(mu, sigma, goc_pam["tau_m"], goc_pam["V_th"], goc_pam["V_reset"], goc_pam["t_ref"])

def nu_pc(mu, sigma):
    return siegert(mu, sigma, pc_pam["tau_m"], pc_pam["V_th"], pc_pam["V_reset"], pc_pam["t_ref"])

def nu_mli(mu, sigma):
    return siegert(mu, sigma, mli_pam["tau_m"], mli_pam["V_th"], mli_pam["V_reset"], mli_pam["t_ref"])

# Population-specific mean and variance of inputs

# Input to grc: external (mossy fibers) - inhibition from goc
def mu_grc(nu_goc, nu_ext):
    return J_ext_grc * N_ext_grc * nu_ext + J_goc_grc * N_goc_grc * nu_goc

def sigma2_grc(nu_goc, nu_ext):
    return (J_ext_grc**2 * N_ext_grc * nu_ext) + (J_goc_grc**2 * N_goc_grc * nu_goc)

# Input to goc: external (mossy fibers) - excitation from grc
def mu_goc(nu_gr, nu_ext, nu_goc):
    return J_ext_go * N_ext_go * nu_ext + J_grc_goc * N_grc_goc * nu_gr + J_goc_goc * N_goc_goc * nu_goc

def sigma2_goc(nu_gr, nu_ext, nu_goc):
    return (J_ext_go**2 * N_ext_go * nu_ext) + (J_grc_goc**2 * N_grc_goc * nu_gr) + (J_goc_goc**2 * N_goc_goc * nu_goc)

### CONTINUE HERE ###

# Input to pc: excitation from cf - inhibition from mli