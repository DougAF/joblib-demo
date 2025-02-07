"""Tools to implement caching."""

# pylint: disable=too-few-public-methods

import functools


def _make_key(args, kwargs):
    """Creates a hashable key. A simplified version of functools._make_key."""

    # create a key for the memo from args and kwargs
    key = args

    if kwargs:
        # marks the start of the keyword arguments in key
        key += (object(),)
        for item in kwargs.items():
            key += item

    return key


class MemoizedFunction:
    """Takes a function and returns a callable that is a memoized version of that function."""

    def __init__(self, func):
        self.func = func
        self.cache = dict()
        self.cache_hits = 0
        self.n_calls = 0

    def __call__(self, *args, **kwargs):

        key = _make_key(args, kwargs)

        self.n_calls += 1
        if not self.cache.get(key):
            self.cache[key] = self.func(*args, **kwargs)
        else:
            self.cache_hits += 1
        return self.cache[key]


def memoize(func):
    """Decorates a function to implement a memo.
    A simpler, less optimized version of functools.cache."""

    memo = {}

    @functools.wraps(func)
    def memorize_closure(*args, **kwargs):

        key = _make_key(args, kwargs)

        if not memo.get(key):
            memo[key] = func(*args, **kwargs)

        return memo[key]

    return memorize_closure
