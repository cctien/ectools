from collections.abc import Sequence

import numpy as np


def np_prng_key(random_seed: int | np.random.SeedSequence | None) -> np.random.SeedSequence:
    if isinstance(random_seed, np.random.SeedSequence):
        return random_seed
    return np.random.SeedSequence(random_seed)


def np_prng(random_seed: int | np.random.SeedSequence | None) -> np.random.Generator:
    return np.random.default_rng(np_prng_key(random_seed))


def np_generalized_concat(arrays: Sequence[np.ndarray], axis: int = 0, **kwargs) -> np.ndarray:
    try:
        return np.concatenate(arrays, axis=axis, **kwargs)
    except ValueError:
        return np.stack(arrays, axis=axis, **kwargs)


# np_prng: Callable[[int | np.random.SeedSequence | None], np.random.Generator] = cmp(
#     np.random.default_rng, np_prng_key
# )
