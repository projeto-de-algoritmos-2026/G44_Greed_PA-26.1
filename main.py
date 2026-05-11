import argparse

from src.planner import ReliefRoutePlanner
from src.ui import ReliefRouteUI


def run_terminal() -> None:
    planner = ReliefRoutePlanner()
    print("Rota Solidaria")
    print(f"Combustivel inicial: {planner.initial_fuel} km")
    print()

    planner.solve_all()
    for line in planner.log:
        print(f"- {line}")
    print()
    print(planner.summary())


def main() -> None:
    parser = argparse.ArgumentParser(description="Rota Solidaria")
    parser.add_argument(
        "--terminal",
        action="store_true",
        help="executa a simulacao automatica no terminal",
    )
    args = parser.parse_args()

    if args.terminal:
        run_terminal()
        return

    app = ReliefRouteUI(ReliefRoutePlanner())
    app.run()


if __name__ == "__main__":
    main()
