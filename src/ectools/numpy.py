import numpy as np


def np_prng_key(random_seed: int | np.random.SeedSequence | None) -> np.random.SeedSequence:
    if isinstance(random_seed, np.random.SeedSequence):
        return random_seed
    return np.random.SeedSequence(random_seed)
