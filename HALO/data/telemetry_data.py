from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations

import numpy as np
import pandas as pd

from .attr import Attr


@dataclass(unsafe_hash=True)
class TelemetryData:
    df: pd.DataFrame = field(hash=False)
    failure_col: str
    success_col: str

    def __post_init__(self):
        self.attr_cols = list(set(self.df.columns) - {self.failure_col, self.success_col})
        attrs = sorted([
            Attr(attr_name, self.entropy(attr_name))
            for attr_name in self.attr_cols
        ], key=lambda attr: attr.entropy)

        for combs in combinations(attrs, 2):
            father, child = combs  # type:Attr
            hi = self.hi(father.name, child.name)
            father.add_child(child, hi)
        self.attrs = attrs

    def pdf(self, attr_names):
        return self.df[attr_names].value_counts() / self.df.shape[0]

    @lru_cache(maxsize=32)
    def entropy(self, attr_name):
        pdf = self.pdf(attr_name)
        return -(np.log2(pdf) * pdf).sum()

    def conditional_entropy(self, an1, an2):
        conditional_pdf = self.pdf([an1, an2])
        pj = np.array([conditional_pdf[:, indices[1]].sum() for indices in conditional_pdf.index])
        return -(np.log2(conditional_pdf / pj) * conditional_pdf).sum()

    @lru_cache(maxsize=256)
    def hi(self, an1, an2):
        return 1 - (self.conditional_entropy(an1, an2) / self.entropy(an1)) \
            if self.entropy(an1) < self.entropy(an2) else -np.inf

    def random_score(self, attr_name, sampling=2):
        sample = self.df.iloc[self.df[attr_name].sample(sampling).index].sum()
        return int(sample[self.failure_col]) / int(sample[self.success_col])
