import asyncio
from typing import List, Optional

from src.structures import FilmId, Answer
from dataclasses import dataclass


@dataclass
class Tree:
    current_level: asyncio.Queue[FilmId]
    vertexes: List[FilmId]

def intersect_trees(t1: Tree, t2: Tree) -> Optional[List[FilmId]]:
    pass
