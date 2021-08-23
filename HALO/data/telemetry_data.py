from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations

import numpy as np
import pandas as pd

from .attr import Attr
from .value import Combination
from HALO.config import Config


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
        self.fail_count = self.df[self.failure_col].sum()

    def pdf(self, attr_names):
        return self.df[attr_names].value_counts() / self.df.shape[0]

    def values(self, attr_name):
        return self.df[attr_name].unique()

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

    def random_score(self, attr_name, sampling=Config.sampling):
        sample = self.df.iloc[self.df[attr_name].sample(sampling).index].sum()
        return int(sample[self.failure_col]) / int(sample[self.success_col])

    @lru_cache
    def metric_values(self, comb: Combination):
        return self.df.query(comb.query_str())[[self.failure_col, self.success_col]]

    def _election_score(self, f_count, s_count):
        recall, precision = f_count / self.fail_count, f_count / (f_count + s_count)
        return 2 * recall * precision / (recall + precision) if recall + precision != 0 else 0

    def election_score(self, comb: Combination):
        f_count, s_count = self.metric_values(comb).sum()
        if f_count == 0:
            return 0
        return self._election_score(f_count, s_count)

    def damping_score(self, comb: Combination):
        metric_values = self.metric_values(comb)
        election_scores = np.array([self._election_score(f, s) for f, s in metric_values.itertuples(index=False)])
        if metric_values.empty or election_scores.sum() == 0:
            return 0
        all_counts = metric_values.sum(axis=1)

        def kl(p, q):
            return sum([i * np.log2(i / j) for i, j in zip(p, q) if i != 0])

        def js(p, q):
            m = [(i + j) / 2 for i, j in zip(p, q)]
            return 1 / 2 * kl(p, m) + 1 / 2 * kl(q, m)

        return 1 - js(election_scores / sum(election_scores), all_counts / sum(all_counts))
