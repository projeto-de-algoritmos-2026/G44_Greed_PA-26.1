import math
from typing import Dict, List, Optional, Set, Tuple

from src.algorithms import Graph, build_candidates, build_graph, choose_next_delivery
from src.data import INITIAL_FUEL, NEIGHBORHOODS, ROADS, START
from src.models import Candidate, DeliveryStep, Neighborhood


class ReliefRoutePlanner:
    def __init__(self) -> None:
        self.neighborhoods = list(NEIGHBORHOODS)
        self.roads = list(ROADS)
        self.graph: Graph = build_graph(self.roads)
        self.road_distance: Dict[frozenset, int] = {
            frozenset((road.a, road.b)): road.distance for road in self.roads
        }
        self.initial_fuel = INITIAL_FUEL
        self.neighborhood_by_name: Dict[str, Neighborhood] = {
            neighborhood.name: neighborhood for neighborhood in self.neighborhoods
        }
        self.reset()

    def reset(self) -> None:
        self.current = START
        self.fuel = self.initial_fuel
        self.served: Set[str] = set()
        self.steps: List[DeliveryStep] = []
        self.last_path: List[str] = []
        self.log: List[str] = [
            "Caminhao saiu da Cozinha Central.",
            "Regra: escolher o bairro com maior familias atendidas por km.",
            "Modo manual: use setas ou WASD para dirigir pelas ruas.",
        ]
        self.finished = False

    @property
    def total_families(self) -> int:
        return sum(step.families for step in self.steps)

    def candidates(self) -> List[Candidate]:
        return build_candidates(self.graph, self.neighborhoods, self.current, self.served, self.fuel)

    def best_choice(self) -> Optional[Candidate]:
        return choose_next_delivery(self.graph, self.neighborhoods, self.current, self.served, self.fuel)

    def step(self) -> bool:
        if self.finished:
            return False

        choice = self.best_choice()
        if choice is None:
            self.finished = True
            self.last_path = []
            self.log.append("Fim: nenhum bairro restante cabe no combustivel atual.")
            self.log.append(self.summary())
            return False

        self.current = choice.neighborhood.name
        self.fuel -= choice.distance
        self.served.add(choice.neighborhood.name)
        self.last_path = choice.path
        self.steps.append(
            DeliveryStep(
                target=choice.neighborhood,
                distance=choice.distance,
                path=choice.path,
                families=choice.neighborhood.families,
                ratio=choice.ratio,
            )
        )
        self.log.append(
            f"Atendeu {choice.neighborhood.name}: {choice.neighborhood.families} familias, "
            f"{choice.distance} km, eficiencia {choice.ratio:.2f}."
        )

        if self.best_choice() is None:
            self.finished = True
            self.log.append("Fim: todos os bairros possiveis foram atendidos com o combustivel disponivel.")
            self.log.append(self.summary())

        return True

    def solve_all(self) -> None:
        while self.step():
            pass

    def manual_neighbors(self) -> List[Tuple[Neighborhood, int]]:
        neighbors: List[Tuple[Neighborhood, int]] = []
        for neighbor_name, distance in self.graph[self.current]:
            neighbors.append((self.neighborhood_by_name[neighbor_name], distance))
        return neighbors

    def move_to(self, destination_name: str) -> bool:
        if self.finished:
            return False

        edge_key = frozenset((self.current, destination_name))
        if edge_key not in self.road_distance:
            self.log.append(f"Nao existe rua direta ate {destination_name}.")
            return False

        distance = self.road_distance[edge_key]
        if distance > self.fuel:
            self.log.append(f"Combustivel insuficiente para ir ate {destination_name}: precisa de {distance} km.")
            return False

        origin = self.current
        self.current = destination_name
        self.fuel -= distance
        self.last_path = [origin, destination_name]
        destination = self.neighborhood_by_name[destination_name]

        if destination.families > 0 and destination.name not in self.served:
            self.served.add(destination.name)
            self.steps.append(
                DeliveryStep(
                    target=destination,
                    distance=distance,
                    path=[origin, destination_name],
                    families=destination.families,
                    ratio=destination.families / distance,
                )
            )
            self.log.append(
                f"Movimento manual: atendeu {destination.name}, "
                f"{destination.families} familias por {distance} km."
            )
        else:
            self.log.append(f"Movimento manual: foi para {destination.name} por {distance} km.")

        if self.best_choice() is None:
            self.finished = True
            self.log.append("Fim: nenhum bairro restante cabe no combustivel atual.")
            self.log.append(self.summary())

        return True

    def move_by_direction(self, delta_x: int, delta_y: int) -> bool:
        current = self.neighborhood_by_name[self.current]
        best_name: Optional[str] = None
        best_alignment: Optional[float] = None
        best_distance: Optional[float] = None

        for neighbor, _distance in self.manual_neighbors():
            vector_x = neighbor.x - current.x
            vector_y = neighbor.y - current.y
            dot = (vector_x * delta_x) + (vector_y * delta_y)
            if dot <= 0:
                continue

            screen_distance = math.hypot(vector_x, vector_y)
            alignment = dot / screen_distance
            if (
                best_alignment is None
                or alignment > best_alignment
                or (alignment == best_alignment and screen_distance < (best_distance or screen_distance))
            ):
                best_alignment = alignment
                best_distance = screen_distance
                best_name = neighbor.name

        if best_name is None:
            self.log.append("Nao ha rua nessa direcao.")
            return False

        return self.move_to(best_name)

    def route_edges(self) -> Set[frozenset]:
        selected: Set[frozenset] = set()
        for step in self.steps:
            for first, second in zip(step.path, step.path[1:]):
                selected.add(frozenset((first, second)))
        return selected

    def last_path_edges(self) -> Set[frozenset]:
        return {frozenset((first, second)) for first, second in zip(self.last_path, self.last_path[1:])}

    def summary(self) -> str:
        return (
            f"Resumo: {self.total_families} familias atendidas, "
            f"{self.initial_fuel - self.fuel} km usados, {self.fuel} km restantes."
        )


__all__ = ["Neighborhood", "ReliefRoutePlanner"]
