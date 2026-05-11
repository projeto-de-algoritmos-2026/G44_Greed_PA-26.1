import heapq
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Set, Tuple

from src.models import Candidate, Neighborhood, Road


Graph = Dict[str, List[Tuple[str, int]]]


def build_graph(roads: List[Road]) -> Graph:
    graph: DefaultDict[str, List[Tuple[str, int]]] = defaultdict(list)
    for road in roads:
        graph[road.a].append((road.b, road.distance))
        graph[road.b].append((road.a, road.distance))
    return dict(graph)


def shortest_path(graph: Graph, start: str, goal: str) -> Tuple[int, List[str]]:
    queue: List[Tuple[int, str]] = [(0, start)]
    distances: Dict[str, int] = {start: 0}
    previous: Dict[str, Optional[str]] = {start: None}

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current == goal:
            break
        if current_distance > distances[current]:
            continue

        for neighbor, weight in graph.get(current, []):
            new_distance = current_distance + weight
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    if goal not in distances:
        return 10**9, []

    path = [goal]
    while path[-1] != start:
        parent = previous[path[-1]]
        if parent is None:
            break
        path.append(parent)
    path.reverse()
    return distances[goal], path


def build_candidates(
    graph: Graph,
    neighborhoods: List[Neighborhood],
    current: str,
    served: Set[str],
    fuel: int,
) -> List[Candidate]:
    candidates: List[Candidate] = []

    for neighborhood in neighborhoods:
        if neighborhood.families <= 0 or neighborhood.name in served:
            continue

        distance, path = shortest_path(graph, current, neighborhood.name)
        if not path or distance > fuel:
            continue

        candidates.append(
            Candidate(
                neighborhood=neighborhood,
                distance=distance,
                path=path,
                ratio=neighborhood.families / distance,
            )
        )

    return sorted(
        candidates,
        key=lambda candidate: (
            -candidate.ratio,
            -candidate.neighborhood.families,
            candidate.distance,
            candidate.neighborhood.name,
        ),
    )


def choose_next_delivery(
    graph: Graph,
    neighborhoods: List[Neighborhood],
    current: str,
    served: Set[str],
    fuel: int,
) -> Optional[Candidate]:
    candidates = build_candidates(graph, neighborhoods, current, served, fuel)
    if not candidates:
        return None
    return candidates[0]
