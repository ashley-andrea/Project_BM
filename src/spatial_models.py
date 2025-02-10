# src/spatial_models.py
import nest
import nest.spatial as spt
import src.config as config

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": config.DT, "print_time": True, "rng_seed": config.SEED})

def create_mossy_fibers(n):
    """Create a population of mossy fibers (input to granule cells) with spatial information."""
    mossy_fibers = nest.Create("poisson_generator", n, params=config.MOSSY_FIBER_PARAMS)
    print(f"Created {n} mossy fibers.")
    return mossy_fibers