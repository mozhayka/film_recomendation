from typing import List, Optional, Set

from src.structures import FilmId, Answer
from dataclasses import dataclass


@dataclass
class Tree:
    current_level: List[FilmId]
    vertexes: Set[FilmId]


def intersect_trees(t1: Tree, t2: Tree) -> Optional[List[FilmId]]:
    intersection = t1.vertexes & t2.vertexes
    if intersection.__sizeof__() == 0:
        return None
    return list(intersection)
