import secrets

import jax
from jax import Array


def jax_prng_key(random_seed: int | Array | None) -> Array:
    if isinstance(random_seed, Array):
        return random_seed
    return jax.random.key(secrets.randbits(64) if random_seed is None else random_seed)
