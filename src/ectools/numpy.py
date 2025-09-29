from collections.abc import Callable

import numpy as np
from cytoolz import compose as cmp


def np_prng_key(random_seed: int | np.random.SeedSequence | None) -> np.random.SeedSequence:
    if isinstance(random_seed, np.random.SeedSequence):
        return random_seed
    return np.random.SeedSequence(random_seed)


def np_prng(random_seed: int | np.random.SeedSequence | None) -> np.random.Generator:
    return np.random.default_rng(np_prng_key(random_seed))


# np_prng: Callable[[int | np.random.SeedSequence | None], np.random.Generator] = cmp(
#     np.random.default_rng, np_prng_key
# )
