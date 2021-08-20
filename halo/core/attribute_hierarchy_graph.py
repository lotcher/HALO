from typing import List, OrderedDict as Dict
from dataclasses import dataclass, field
from itertools import combinations
from collections import OrderedDict
from functools import lru_cache

from halo.data import Attr, TelemetryData

from bools.log import Logger


@dataclass
class AHG:
    attrs: List[Attr]
    skeleton: List[Attr] = field(default=list)
    remaining_attrs: Dict[str, Attr] = field(default=dict)

    def __post_init__(self):
        skeleton_heads = sorted(
            [attr for attr in self.attrs if attr.strict_children and attr.strict_in_degree == 0],
            key=lambda attr: len(attr.strict_children)
        )
        # 如果存在多个不相关的包含关系，选择最“复杂”的关系
        # 选择最长的strict path作为骨架（即使多条strict path不存在公共子节点）
        self.skeleton = sorted(skeleton_heads[0].strict_paths(), key=lambda _: -len(_))[0] if skeleton_heads else []
        [attr.set_level(level) for level, attr in enumerate(self.skeleton, start=1)]

        self.remaining_attrs = OrderedDict([(attr.name, attr) for attr in self.attrs if attr not in self.skeleton])

    def get_attrs_by_level(self, level):
        return [attr for attr in self.attrs if attr.level == level]

    def minimize_obj(self, attr: Attr, change_level, telemetry_data):
        ahg = AHG(TelemetryData(telemetry_data.df, telemetry_data.failure_col, telemetry_data.success_col).attrs)
        ahg.remaining_attrs.get(attr.name).set_level(change_level)
        skeleton_len = len(self.skeleton)

        @lru_cache(maxsize=skeleton_len)
        def attrs_and_count_by_level(level):
            current_attrs = ahg.get_attrs_by_level(level)
            current_count, next_count = len(current_attrs), len(ahg.get_attrs_by_level(level + 1))
            return current_attrs, current_count, next_count

        def i(level):
            current_attrs, current_count, _ = attrs_and_count_by_level(level)
            # 如果某一层只有一个节点，分母可能为0
            return sum([
                telemetry_data.hi(*[_.name for _ in combs]) for combs in combinations(current_attrs, 2)
            ]) / (current_count * (current_count - 1) / 2 + 1)

        def c(level):
            current_attrs, current_count, next_count = attrs_and_count_by_level(level)
            return sum([
                telemetry_data.hi(current_attr.name, next_attr.name)
                for current_attr in current_attrs for next_attr in self.attrs if next_attr.level == change_level + 1
            ]) / (current_count * next_count)

        return sum(map(i, range(1, skeleton_len + 1))) - sum(map(c, range(1, skeleton_len)))

    def extract(self, telemetry_data):
        Logger.info(f'skeleton: {"->".join([attr.name for attr in self.skeleton])}')
        for remaining_attr in self.remaining_attrs.values():
            objs = [
                (self.minimize_obj(remaining_attr, level, telemetry_data), level)
                for level in range(1, len(self.skeleton) + 1)
            ]
            Logger.info(f'{remaining_attr.name}各层obj分数: {objs}，{remaining_attr.name} set level={min(objs)[1]}')
            min_obj_level = min(objs)[1]
            remaining_attr.set_level(min_obj_level)

    def random_walk(self, telemetry_data: TelemetryData):
        def walk(path: Attr):
            yield path.name
            children = list(path.children)
            if children:
                max_score_index = max(
                    enumerate([telemetry_data.random_score(_.name) for _ in children]),
                    key=lambda _: _[1]
                )[0]
                yield from walk(children[max_score_index])

        return list(walk(self.attrs[0]))
