import numpy as np
from scipy.integrate import quad
from scipy.special import erf
from scipy.optimize import least_squares
from src.config import *

# ======================
# UTILITIES
# ======================

def validate_parameters():
    """Check parameter biological plausibility"""
    assert 0 < GRANULE_CELL_PARAMS["tau_m"] < 50, "Granule cell tau_m out of range"
    assert -80 < GRANULE_CELL_PARAMS["V_th"] < -40, "Granule threshold unrealistic"
    assert abs(SYN_MF_TO_GRANULE["weight"]) < 10, "MF-GrC weight too large"
    # Add similar checks for other parameters
    # CONTINUE ...

def find_steady_state(mf_rate, cf_rate):
    """Robust steady-state solver"""
    # Initial guess based on biological expectations
    initial_guess = np.array([
        max(1, 0.1 * mf_rate),  # GrC ~10% of MF input
        max(1, 0.2 * mf_rate),  # GoC 
        50.0,  # PC base rate
        20.0   # MLI
    ])
    
    # Bounds to prevent negative rates
    bounds = ([1e-3, 1e-3, 1e-3, 1e-3], [1e4, 1e4, 1e3, 1e3])
    
    # Use trust-region reflective method
    result = least_squares(
        lambda x: cerebellar_mean_field(x, mf_rate, cf_rate),
        initial_guess,
        bounds=bounds,
        ftol=1e-6,
        xtol=1e-6,
        max_nfev=1000
    )
    return result.x


# ======================
# NETWORK ARCHITECTURE
# ======================

NEURON_POPULATIONS = [
    "granule", "golgi", "purkinje", 
    "interneurons", "mossy_fibers", 
    "climbing_fibers", "dcn"
]

SYNAPTIC_CONNECTIONS = {
    # Mossy fiber projections
    ('mossy_fibers', 'granule'): (
        abs(SYN_MF_TO_GRANULE['weight']), 
        4   # int(MOSSY_FIBER_NUM * CONN_MF_TO_GRANULE['p'])
    ),
    ('mossy_fibers', 'golgi'): (
        SYN_MF_TO_GOLGI['weight'], 
        int(MOSSY_FIBER_NUM * CONN_MF_TO_GOLGI['p'])
    ),
    ('mossy_fibers', 'dcn'): (
        SYN_MF_TO_DCN['weight'],
        int(MOSSY_FIBER_NUM * DEEP_CEREBELLAR_NUCLEI_NUM * 0.01)
    ),
    
    # Granule cell projections
    ('granule', 'golgi'): (
        SYN_GRANULE_TO_GOLGI['weight'], 
        int(GRANULE_CELL_NUM * CONN_GRANULE_TO_GOLGI['p'])
    ),
    ('granule', 'purkinje'): (
        SYN_PARALLEL['weight'], 
        int(GRANULE_CELL_NUM * CONN_GRANULE_TO_PURKINJE['p'])
    ),
    ('granule', 'interneurons'): (
        SYN_GRANULE_TO_INTERNEURON['weight'], 
        int(GRANULE_CELL_NUM * CONN_GRANULE_TO_INTERNEURON['p'])
    ),
    
    # Golgi cell projections
    ('golgi', 'granule'): (
        abs(SYN_GOLGI_TO_GRANULE['weight']), 
        int(GOLGI_CELL_NUM * CONN_GOLGI_TO_GRANULE['p'])
    ),
    ('golgi', 'golgi'): (
        abs(SYN_GOLGI_TO_GOLGI['weight']), 
        int(GOLGI_CELL_NUM * CONN_GOLGI_TO_GOLGI['p'])
    ),
    
    # Interneuron projections
    ('interneurons', 'purkinje'): (
        abs(SYN_INTERNEURON_TO_PURKINJE['weight']), 
        int(INTERNEURON_NUM * CONN_INTERNEURON_TO_PURKINJE['p'])
    ),
    ('interneurons', 'interneurons'): (
        abs(SYN_INTERNEURON_TO_INTERNEURON['weight']), 
        int(INTERNEURON_NUM * CONN_INTERNEURON_TO_INTERNEURON['p'])
    ),
    
    # Climbing fiber projections
    ('climbing_fibers', 'purkinje'): (
        SYN_CLIMBING['weight'], 
        int(CLIMBING_FIBER_NUM)
    ),
    
    # Purkinje cell projections
    ('purkinje', 'dcn'): (
        abs(SYN_PURKINJE_TO_DCN['weight']), 
        PURKINJE_CELL_NUM
    )
}

# ======================
# CORE FUNCTIONS
# ======================

def get_synaptic_parameters(source_population, target_population, sign=1.0):
    """
    Retrieve synaptic parameters from configuration
    
    Args:
        source_population (str): Presynaptic population name
        target_population (str): Postsynaptic population name
        sign (float): Sign multiplier for inhibitory connections
    
    Returns:
        tuple: (synaptic_weight, connection_count)
    """
    connection_key = (source_population, target_population)
    
    if connection_key not in SYNAPTIC_CONNECTIONS:
        raise ValueError(f"Undefined connection: {connection_key}")
    
    base_weight, connection_count = SYNAPTIC_CONNECTIONS[connection_key]
    return sign * base_weight, connection_count
 
def improved_integrand(x):
    """
    Enhanced integrand with sophisticated handling of numerical edge cases.
    
    Key improvements:
    - Advanced asymptotic approximations
    - Precise handling of overflow scenarios
    - Continuous behavior across different x ranges
    """
    # Extreme negative x: asymptotic approximation
    if x < -10:
        return 1.0 / (np.sqrt(np.pi) * np.abs(x))
    
    # Extreme positive x: specialized high-precision approximation
    if x > 10:
        return np.exp(x**2) * (2 - np.exp(-x**2) / (np.sqrt(np.pi) * x))
    
    # Standard case with robust error function handling
    try:
        return np.exp(x**2) * (1 + erf(x))
    except OverflowError:
        # Fallback strategy for unexpected numerical issues
        return np.sign(x) * np.inf if x > 0 else 0.0

def siegert_integral(mean_potential, potential_std, 
                     membrane_time_constant, threshold_potential, 
                     reset_potential, refractory_period,
                     adaptive_integration=True):
    """
    Robust and precise Siegert integral calculation.
    
    Enhanced features:
    - Adaptive integration strategy
    - Multiple numerical stability mechanisms
    - Flexible integration approach
    """
    # Normalize potentials to standard units
    lower_bound = (reset_potential - mean_potential) / potential_std
    upper_bound = (threshold_potential - mean_potential) / potential_std
    
    # Early termination for negligible integration range
    if np.abs(upper_bound - lower_bound) < 1e-12:
        return 0.0
    
    # Advanced integration strategy
    if adaptive_integration and lower_bound * upper_bound < 0:
        # Split integration around zero for enhanced precision
        try:
            int1, err1 = quad(improved_integrand, lower_bound, 0, 
                              limit=300, epsabs=1e-10, epsrel=1e-10)
            int2, err2 = quad(improved_integrand, 0, upper_bound, 
                              limit=300, epsabs=1e-10, epsrel=1e-10)
            integral_value = int1 + int2
            integration_error = err1 + err2
        except Exception:
            # Fallback to standard integration
            integral_value, integration_error = quad(
                improved_integrand, lower_bound, upper_bound, 
                limit=300, epsabs=1e-10, epsrel=1e-10
            )
    else:
        # Standard single-range integration
        integral_value, integration_error = quad(
            improved_integrand, lower_bound, upper_bound, 
            limit=300, epsabs=1e-10, epsrel=1e-10
        )
    
    # Final computation with enhanced numerical stability
    denominator = (refractory_period + 
                   membrane_time_constant * np.sqrt(np.pi) * integral_value)
    
    # Handle potential division by near-zero scenarios
    result = 1.0 / denominator if denominator > 1e-12 else 0.0
    
    return result


def create_transfer_function(cell_parameters):
    """
    Generate population-specific rate transfer function
    
    Args:
        cell_parameters (dict): Physiological parameters for cell type
    
    Returns:
        function: Rate calculation function (mu, sigma) -> rate
    """
    def transfer_function(mean_input, std_input):
        return siegert_integral(
            mean_input, std_input,
            cell_parameters["tau_m"],
            cell_parameters["V_th"],
            cell_parameters["V_reset"],
            cell_parameters["t_ref"]
        )
    return transfer_function

# ======================
# POPULATION INTERACTIONS
# ======================

# Initialize transfer functions
granule_rate = create_transfer_function(GRANULE_CELL_PARAMS)
golgi_rate = create_transfer_function(GOLGI_CELL_PARAMS)
purkinje_rate = create_transfer_function(PURKINJE_CELL_PARAMS)
interneuron_rate = create_transfer_function(INTERNEURON_PARAMS)

# Retrieve synaptic parameters
mf_to_granule_weight, mf_to_granule_count = get_synaptic_parameters('mossy_fibers', 'granule')
mf_to_golgi_weight, mf_to_golgi_count = get_synaptic_parameters('mossy_fibers', 'golgi')
cf_to_purkinje_weight, cf_to_purkinje_count = get_synaptic_parameters('climbing_fibers', 'purkinje')
granule_to_golgi_weight, granule_to_golgi_count = get_synaptic_parameters('granule', 'golgi')
golgi_to_granule_weight, golgi_to_granule_count = get_synaptic_parameters('golgi', 'granule', -1)
golgi_to_golgi_weight, golgi_to_golgi_count = get_synaptic_parameters('golgi', 'golgi', -1)
granule_to_interneuron_weight, granule_to_interneuron_count = get_synaptic_parameters('granule', 'interneurons')
granule_to_purkinje_weight, granule_to_purkinje_count = get_synaptic_parameters('granule', 'purkinje')
interneuron_to_interneuron_weight, interneuron_to_interneuron_count = get_synaptic_parameters('interneurons', 'interneurons', -1)
interneuron_to_purkinje_weight, interneuron_to_purkinje_count = get_synaptic_parameters('interneurons', 'purkinje', -1)
purkinje_to_dcn_weight, purkinje_to_dcn_count = get_synaptic_parameters('purkinje', 'dcn', -1)
mf_to_dcn_weight, mf_to_dcn_count = get_synaptic_parameters('mossy_fibers', 'dcn')


# ======================
# INPUT CALCULATIONS
# ======================

def calculate_synaptic_input(weight_count_pairs):
    """Sum weighted synaptic inputs"""
    return sum(weight * count * rate for weight, count, rate in weight_count_pairs)

def calculate_synaptic_variance(weight_count_pairs):
    """Sum squared synaptic variances"""
    return sum((weight**2) * count * rate for weight, count, rate in weight_count_pairs)

def granule_inputs(golgi_rate, mossy_fiber_rate, verbose=False):
    """Calculate granule cell input statistics"""
    normalization_factor = 1
    mean = normalization_factor * calculate_synaptic_input([
        (mf_to_granule_weight, mf_to_granule_count, mossy_fiber_rate),
        (golgi_to_granule_weight, golgi_to_granule_count, golgi_rate)
    ])
    variance = normalization_factor * calculate_synaptic_variance([
        (mf_to_granule_weight, mf_to_granule_count, mossy_fiber_rate),
        (golgi_to_granule_weight, golgi_to_granule_count, golgi_rate)
    ])
    # DEBUG
    if verbose:
        print("Granule inputs params:")
        print("     golgi_rate:", golgi_rate)
        print("     mossy_fiber_rate:", mossy_fiber_rate)
    return mean, np.sqrt(variance)

def golgi_inputs(granule_rate, mossy_fiber_rate, current_golgi_rate, verbose=False):
    """Calculate golgi cell input statistics"""
    normalization_factor = 1
    mean = normalization_factor * calculate_synaptic_input([
        (mf_to_golgi_weight, mf_to_golgi_count, mossy_fiber_rate),
        (granule_to_golgi_weight, granule_to_golgi_count, granule_rate),
        (golgi_to_golgi_weight, golgi_to_golgi_count, current_golgi_rate)
    ])
    variance = normalization_factor * calculate_synaptic_variance([
        (mf_to_golgi_weight, mf_to_golgi_count, mossy_fiber_rate),
        (granule_to_golgi_weight, granule_to_golgi_count, granule_rate),
        (golgi_to_golgi_weight, golgi_to_golgi_count, current_golgi_rate)
    ])
    # DEBUG
    if verbose:
        print("Golgi inputs params:")
        print("     granule_rate:", granule_rate)
        print("     mossy_fiber_rate:", mossy_fiber_rate)
        print("     current_golgi_rate:", current_golgi_rate)
    return mean, np.sqrt(variance)

def purkinje_inputs(interneuron_rate, granule_rate, climbing_fiber_rate, verbose=False):
    """Calculate purkinje cell input statistics"""
    mean = calculate_synaptic_input([
        (granule_to_purkinje_weight, granule_to_purkinje_count, granule_rate),
        (interneuron_to_purkinje_weight, interneuron_to_purkinje_count, interneuron_rate),
        (cf_to_purkinje_weight, cf_to_purkinje_count, climbing_fiber_rate)
    ])
    variance = calculate_synaptic_variance([
        (granule_to_purkinje_weight, granule_to_purkinje_count, granule_rate),
        (interneuron_to_purkinje_weight, interneuron_to_purkinje_count, interneuron_rate),
        (cf_to_purkinje_weight, cf_to_purkinje_count, climbing_fiber_rate)
    ])
    # DEBUG
    if verbose:
        print("Purkinje inputs params:")
        print("     interneuron_rate:", interneuron_rate)
        print("     granule_rate:", granule_rate)
        print("     climbing_fiber_rate:", climbing_fiber_rate)
    return mean, np.sqrt(variance)

def interneuron_inputs(granule_rate, current_interneuron_rate, verbose=False):
    """Calculate interneuron input statistics"""
    mean = calculate_synaptic_input([
        (granule_to_interneuron_weight, granule_to_interneuron_count, granule_rate),
        (interneuron_to_interneuron_weight, interneuron_to_interneuron_count, current_interneuron_rate)
    ])
    variance = calculate_synaptic_variance([
        (granule_to_interneuron_weight, granule_to_interneuron_count, granule_rate),
        (interneuron_to_interneuron_weight, interneuron_to_interneuron_count, current_interneuron_rate)
    ])
    # DEBUG
    if verbose:
        print("Interneuron inputs params:")
        print("     granule_rate:", granule_rate)
        print("     current_interneuron_rate:", current_interneuron_rate)
    return mean, np.sqrt(variance)

# ======================
# MEAN-FIELD MODEL
# ======================

def cerebellar_mean_field(current_rates, mossy_fiber_rate, climbing_fiber_rate, verbose=False):
    """
    Calculate residuals between current rates and mean-field predictions
    
    Args:
        current_rates (list): Current population rates [granule, golgi, purkinje, interneuron]
        mossy_fiber_rate (float): Mossy fiber input rate (Hz)
        climbing_fiber_rate (float): Climbing fiber input rate (Hz)
    
    Returns:
        list: Residuals for each population [granule_res, golgi_res, purkinje_res, interneuron_res]
    """
    current_granule, current_golgi, current_purkinje, current_interneuron = current_rates
    
    # Granule cell calculations
    granule_mean, granule_std = granule_inputs(current_golgi, mossy_fiber_rate, verbose=verbose)
    if verbose:
        print("     Granule mean input:", granule_mean)
        print("     Granule std input:", granule_std)
    granule_residual = current_granule - granule_rate(granule_mean, granule_std)
    
    # Golgi cell calculations
    golgi_mean, golgi_std = golgi_inputs(current_granule, mossy_fiber_rate, current_golgi, verbose=verbose)
    if verbose:
        print("     Golgi mean input:", golgi_mean)
        print("     Golgi std input:", golgi_std)
    golgi_residual = current_golgi - golgi_rate(golgi_mean, golgi_std)
    
    # Purkinje cell calculations
    purkinje_mean, purkinje_std = purkinje_inputs(current_interneuron, current_granule, climbing_fiber_rate, verbose=verbose)
    if verbose:
        print("     Purkinje mean input:", purkinje_mean)
        print("     Purkinje std input:", purkinje_std)
    purkinje_residual = current_purkinje - purkinje_rate(purkinje_mean, purkinje_std)
    
    # Interneuron calculations
    interneuron_mean, interneuron_std = interneuron_inputs(current_granule, current_interneuron, verbose=verbose)
    if verbose:
        print("     Interneuron mean input:", interneuron_mean)
        print("     Interneuron std input:", interneuron_std)
    interneuron_residual = current_interneuron - interneuron_rate(interneuron_mean, interneuron_std)
    
    return [granule_residual, golgi_residual, purkinje_residual, interneuron_residual]



