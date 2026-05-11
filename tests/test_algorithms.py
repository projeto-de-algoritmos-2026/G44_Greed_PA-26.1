import unittest

from src.algorithms import build_candidates, build_graph, choose_next_delivery, shortest_path
from src.data import INITIAL_FUEL, NEIGHBORHOODS, ROADS, START
from src.planner import ReliefRoutePlanner


class ReliefRouteTests(unittest.TestCase):
    def test_shortest_path_uses_weighted_roads(self) -> None:
        graph = build_graph(ROADS)
        distance, path = shortest_path(graph, START, "Hospital")
        self.assertEqual(distance, 10)
        self.assertEqual(path, ["Cozinha Central", "Hospital"])

    def test_first_greedy_choice_maximizes_families_per_km(self) -> None:
        graph = build_graph(ROADS)
        choice = choose_next_delivery(graph, NEIGHBORHOODS, START, set(), INITIAL_FUEL)
        self.assertIsNotNone(choice)
        self.assertEqual(choice.neighborhood.name, "Parque Verde")

    def test_candidates_respect_available_fuel(self) -> None:
        graph = build_graph(ROADS)
        candidates = build_candidates(graph, NEIGHBORHOODS, START, set(), fuel=5)
        self.assertEqual(candidates, [])

    def test_full_route_never_spends_more_than_initial_fuel(self) -> None:
        planner = ReliefRoutePlanner()
        planner.solve_all()
        spent = planner.initial_fuel - planner.fuel
        self.assertLessEqual(spent, planner.initial_fuel)
        self.assertGreater(planner.total_families, 0)

    def test_manual_move_spends_fuel_and_serves_neighborhood(self) -> None:
        planner = ReliefRoutePlanner()
        moved = planner.move_by_direction(0, 1)
        self.assertTrue(moved)
        self.assertEqual(planner.current, "Parque Verde")
        self.assertEqual(planner.fuel, planner.initial_fuel - 6)
        self.assertIn("Parque Verde", planner.served)

    def test_manual_direction_can_enter_ribeirao_from_distrito_leste(self) -> None:
        planner = ReliefRoutePlanner()
        planner.move_to("Distrito Leste")
        moved = planner.move_by_direction(0, 1)
        self.assertTrue(moved)
        self.assertEqual(planner.current, "Ribeirao")

    def test_manual_routes_between_parque_ribeirao_and_distrito(self) -> None:
        planner = ReliefRoutePlanner()
        planner.move_to("Parque Verde")

        self.assertTrue(planner.move_by_direction(1, 0))
        self.assertEqual(planner.current, "Ribeirao")

        self.assertTrue(planner.move_by_direction(-1, 0))
        self.assertEqual(planner.current, "Parque Verde")

        self.assertTrue(planner.move_by_direction(1, -1))
        self.assertEqual(planner.current, "Distrito Leste")

        self.assertTrue(planner.move_by_direction(-1, 1))
        self.assertEqual(planner.current, "Parque Verde")


if __name__ == "__main__":
    unittest.main()
