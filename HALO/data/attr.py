from dataclasses import dataclass, field
from typing import List, Set
from bools.log import Logger


@dataclass(unsafe_hash=True)
class Attr:
    name: str
    entropy: float = field(hash=False)
    parents: Set['Attr'] = field(default_factory=set, hash=False)
    children: Set['Attr'] = field(default_factory=set, hash=False)
    strict_children: Set['Attr'] = field(default_factory=set, hash=False)
    in_degree: int = field(default=0, hash=False)
    strict_in_degree: int = field(default=0, hash=False)
    level: int = field(default=0, hash=False)

    def add_child(self, child: 'Attr', hi=0):
        self.children.add(child)
        child.parents.add(self)
        child.in_degree += 1
        if hi > 0.9:
            self.strict_children.add(child)
            child.strict_in_degree += 1

    def find_paths(self):
        for child in self.strict_children:
            if child.strict_children:
                yield [child] + list(child.find_paths())
            else:
                yield [child]

    def strict_paths(self):
        def flatten(path: List):
            for item in path:
                yield from flatten(item) if isinstance(item, list) else [item]

        return [[self, *flatten(path)] for path in self.find_paths()]

    def set_level(self, level):
        self.level = level
        drop_parents = {parent for parent in self.parents if parent.level < level - 1 and parent.level != 0}
        self.parents -= drop_parents
        Logger.debug(f'{self.name} set level={level}, drop parents: {[p.name for p in drop_parents]}')
        for attr in drop_parents:
            attr.children = attr.children - {self}
            attr.strict_children -= {self}

    def __repr__(self):
        return f'{self.name}(entropy={self.entropy}, parents={[p.name for p in self.parents]}, ' \
               f'children={[c.name for c in self.children]}, level={self.level})'
