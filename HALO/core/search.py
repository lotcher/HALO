from typing import List, Tuple
from functools import reduce
from operator import add

import numpy as np
from bools.log import Logger

from HALO.data import TelemetryData, Pair, Combination
from HALO.config import Config


class Searcher:
    @classmethod
    def search(cls, telemetry_data: TelemetryData, search_paths: List[str]):
        Logger.info(f'搜索路径：{"->".join(search_paths)}')

        def find(comb: Combination, paths):
            if not paths:
                return
            combs_with_scores = []
            for v in telemetry_data.values(paths[0]):
                current_comb = comb + Pair(paths[0], v)
                election_score = telemetry_data.election_score(current_comb)
                combs_with_scores.append(
                    (current_comb, election_score)
                )
                if telemetry_data.damping_score(current_comb) > Config.damping_score_threshold:
                    yield current_comb, election_score
            for c in cls.next_search_combs(combs_with_scores):
                yield from find(c, paths[1:])

        root_attr = search_paths[0]
        return cls.reverse_truncation(reduce(add, [
            list(find(Combination([Pair(root_attr, root)]), search_paths[1:]))
            for root in telemetry_data.values(root_attr)
        ]))

    @classmethod
    def next_search_combs(cls, combs_with_scores: List[Tuple[Combination, float]]):
        combs_with_scores.sort(key=lambda _: _[1])
        combs, scores = zip(*combs_with_scores)

        def std(li):
            return np.std(li) if li else 0

        return combs[min([(std(scores[:i]) + std(scores[i:]), i) for i in range(len(scores))])[1]:]

    @classmethod
    def reverse_truncation(cls, root_cause_combs):
        return root_cause_combs
