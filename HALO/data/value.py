from dataclasses import dataclass, field
from typing import List


@dataclass(unsafe_hash=True)
class Pair:
    attr_name: str
    value: str


@dataclass(unsafe_hash=True)
class Combination:
    pairs: List[Pair] = field(hash=False)

    def query_str(self):
        return ' and '.join([f'{pair.attr_name}=="{pair.value}"' for pair in self.pairs])

    def reverse(self):
        return Combination(*reversed(self.pairs))

    def __add__(self, other):
        if isinstance(other, Pair):
            return Combination(self.pairs + [other])

    def __repr__(self):
        return f'Combination({", ".join([f"{pair.attr_name}={pair.value}" for pair in self.pairs])})'
