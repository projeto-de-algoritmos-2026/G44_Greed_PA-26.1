from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Neighborhood:
    name: str
    x: int
    y: int
    families: int


@dataclass(frozen=True)
class Road:
    a: str
    b: str
    distance: int


@dataclass(frozen=True)
class Candidate:
    neighborhood: Neighborhood
    distance: int
    path: List[str]
    ratio: float


@dataclass(frozen=True)
class DeliveryStep:
    target: Neighborhood
    distance: int
    path: List[str]
    families: int
    ratio: float


Point = Tuple[int, int]
