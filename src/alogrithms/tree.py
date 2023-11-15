from typing import List, Optional, Set

from src.structures import FilmId
from dataclasses import dataclass


@dataclass
class Tree:
    current_level: List[FilmId]
    vertexes: Set[FilmId]


def intersect_trees(t1: Tree, t2: Tree) -> Optional[List[FilmId]]:
    intersection = t1.vertexes & t2.vertexes
    if not intersection:
        return None
    return list(intersection)
