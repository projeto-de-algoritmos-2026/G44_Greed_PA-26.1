import tkinter as tk
from tkinter import ttk
from typing import Iterable, Optional

from src.config import (
    BACKGROUND,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    GOLD,
    GRID,
    MUTED,
    NEIGHBORHOOD,
    PANEL_BG,
    ROAD,
    ROUTE,
    SERVED,
    TEXT,
    TRUCK,
)
from src.models import Candidate, Road
from src.planner import ReliefRoutePlanner


class ReliefRouteUI:
    def __init__(self, planner: ReliefRoutePlanner) -> None:
        self.planner = planner
        self.root = tk.Tk()
        self.root.title("Rota Solidaria")
        self.root.configure(bg=BACKGROUND)

        self._build_layout()
        self._bind_keys()
        self.render()

    def _build_layout(self) -> None:
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Metric.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))

        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=PANEL_BG,
            highlightthickness=1,
            highlightbackground=GRID,
        )
        self.canvas.grid(row=0, column=0, padx=18, pady=18)

        panel = ttk.Frame(self.root, padding=18)
        panel.grid(row=0, column=1, padx=(0, 18), pady=18, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Rota Solidaria", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            panel,
            text="Um caminhao, pouco combustivel e bairros esperando marmitas.",
            wraplength=340,
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        self.metric_var = tk.StringVar()
        self.choice_var = tk.StringVar()
        ttk.Label(panel, textvariable=self.metric_var, style="Metric.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Label(panel, textvariable=self.choice_var, wraplength=340).grid(row=3, column=0, sticky="w", pady=(8, 16))

        buttons = ttk.Frame(panel)
        buttons.grid(row=4, column=0, sticky="ew", pady=(0, 16))
        buttons.columnconfigure((0, 1, 2), weight=1)
        ttk.Button(buttons, text="Passo guloso", command=self.step, style="Action.TButton").grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(buttons, text="Resolver", command=self.solve, style="Action.TButton").grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(buttons, text="Resetar", command=self.reset).grid(row=0, column=2, sticky="ew", padx=(5, 0))

        drive_pad = ttk.Frame(panel)
        drive_pad.grid(row=5, column=0, pady=(0, 16))
        ttk.Button(drive_pad, text="↑", width=5, command=lambda: self.manual_move(0, -1)).grid(row=0, column=1, padx=4, pady=2)
        ttk.Button(drive_pad, text="←", width=5, command=lambda: self.manual_move(-1, 0)).grid(row=1, column=0, padx=4, pady=2)
        ttk.Button(drive_pad, text="→", width=5, command=lambda: self.manual_move(1, 0)).grid(row=1, column=2, padx=4, pady=2)
        ttk.Button(drive_pad, text="↓", width=5, command=lambda: self.manual_move(0, 1)).grid(row=2, column=1, padx=4, pady=2)

        ttk.Label(panel, text="Diario da rota", style="Metric.TLabel").grid(row=6, column=0, sticky="w")
        self.log_box = tk.Text(
            panel,
            width=46,
            height=15,
            bg="#fffaf0",
            fg=TEXT,
            relief="solid",
            borderwidth=1,
            wrap="word",
            font=("Consolas", 9),
        )
        self.log_box.grid(row=7, column=0, sticky="nsew", pady=(8, 0))
        self.log_box.configure(state="disabled")

        ttk.Label(
            panel,
            text="Manual: use setas ou WASD. Guloso: maior familias/distancia.",
            wraplength=340,
        ).grid(row=8, column=0, sticky="w", pady=(12, 0))
        panel.rowconfigure(7, weight=1)

    def _bind_keys(self) -> None:
        bindings = {
            "<Up>": (0, -1),
            "<Down>": (0, 1),
            "<Left>": (-1, 0),
            "<Right>": (1, 0),
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
            "W": (0, -1),
            "S": (0, 1),
            "A": (-1, 0),
            "D": (1, 0),
        }
        for key, direction in bindings.items():
            self.root.bind(key, lambda _event, move=direction: self.manual_move(*move))
        self.root.bind("<space>", lambda _event: self.step())
        self.root.bind("r", lambda _event: self.reset())
        self.root.bind("R", lambda _event: self.reset())

    def step(self) -> None:
        self.planner.step()
        self.render()

    def solve(self) -> None:
        self.planner.solve_all()
        self.render()

    def reset(self) -> None:
        self.planner.reset()
        self.render()

    def manual_move(self, delta_x: int, delta_y: int) -> None:
        self.planner.move_by_direction(delta_x, delta_y)
        self.render()

    def render(self) -> None:
        self.canvas.delete("all")
        self._draw_background()
        self._draw_roads()
        self._draw_neighborhoods()
        self._draw_truck()
        self._update_panel()

    def _draw_background(self) -> None:
        for x in range(40, CANVAS_WIDTH, 80):
            self.canvas.create_line(x, 30, x, CANVAS_HEIGHT - 30, fill="#eadfce")
        for y in range(40, CANVAS_HEIGHT, 70):
            self.canvas.create_line(30, y, CANVAS_WIDTH - 30, y, fill="#eadfce")
        self.canvas.create_text(
            24,
            24,
            anchor="w",
            text="Mapa de entregas: numeros nas ruas indicam km",
            fill=MUTED,
            font=("Segoe UI", 10, "bold"),
        )

    def _draw_roads(self) -> None:
        route_edges = self.planner.route_edges()
        last_edges = self.planner.last_path_edges()
        locations = self.planner.neighborhood_by_name

        for road in self.planner.roads:
            a = locations[road.a]
            b = locations[road.b]
            edge_key = frozenset((road.a, road.b))
            color = ROAD
            width = 2
            if edge_key in route_edges:
                color = ROUTE
                width = 5
            if edge_key in last_edges:
                color = GOLD
                width = 7

            self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color, width=width)
            self._draw_distance_label(road, a.x, a.y, b.x, b.y)

    def _draw_distance_label(self, road: Road, x1: int, y1: int, x2: int, y2: int) -> None:
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        self.canvas.create_rectangle(mx - 13, my - 10, mx + 13, my + 10, fill=PANEL_BG, outline="")
        self.canvas.create_text(mx, my, text=str(road.distance), fill=TEXT, font=("Segoe UI", 9, "bold"))

    def _draw_neighborhoods(self) -> None:
        for neighborhood in self.planner.neighborhoods:
            if neighborhood.name == self.planner.current:
                fill = TRUCK
                outline = TEXT
                text_fill = "white"
            elif neighborhood.name in self.planner.served:
                fill = "#d9f3f7"
                outline = SERVED
                text_fill = TEXT
            elif neighborhood.families == 0:
                fill = "#f2dfbd"
                outline = TEXT
                text_fill = TEXT
            else:
                fill = NEIGHBORHOOD
                outline = TEXT
                text_fill = TEXT

            self.canvas.create_oval(
                neighborhood.x - 25,
                neighborhood.y - 25,
                neighborhood.x + 25,
                neighborhood.y + 25,
                fill=fill,
                outline=outline,
                width=3,
            )
            label = "BASE" if neighborhood.families == 0 else str(neighborhood.families)
            self.canvas.create_text(neighborhood.x, neighborhood.y, text=label, fill=text_fill, font=("Segoe UI", 9, "bold"))
            self.canvas.create_text(
                neighborhood.x,
                neighborhood.y + 36,
                text=neighborhood.name,
                fill=TEXT,
                font=("Segoe UI", 9),
            )

    def _draw_truck(self) -> None:
        current = self.planner.neighborhood_by_name[self.planner.current]
        x = current.x
        y = current.y - 38
        self.canvas.create_rectangle(x - 18, y - 8, x + 13, y + 10, fill=TRUCK, outline=TEXT, width=2)
        self.canvas.create_rectangle(x + 3, y - 16, x + 22, y + 10, fill=TRUCK, outline=TEXT, width=2)
        self.canvas.create_oval(x - 14, y + 7, x - 6, y + 15, fill=TEXT, outline=TEXT)
        self.canvas.create_oval(x + 9, y + 7, x + 17, y + 15, fill=TEXT, outline=TEXT)

    def _update_panel(self) -> None:
        self.metric_var.set(
            f"Combustivel: {self.planner.fuel}/{self.planner.initial_fuel} km | "
            f"Familias atendidas: {self.planner.total_families}"
        )
        choice = self.planner.best_choice()
        self.choice_var.set(self._choice_text(choice))
        self._write_log(self.planner.log)

    def _choice_text(self, choice: Optional[Candidate]) -> str:
        if choice is None:
            return "Proxima escolha: nenhum bairro cabe no combustivel restante."
        route = " -> ".join(choice.path)
        return (
            f"Proxima escolha: {choice.neighborhood.name}, "
            f"{choice.neighborhood.families} familias em {choice.distance} km "
            f"({choice.ratio:.2f} familias/km). Rota: {route}."
        )

    def _write_log(self, lines: Iterable[str]) -> None:
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.insert(tk.END, "\n".join(lines[-18:]))
        self.log_box.configure(state="disabled")
        self.log_box.see(tk.END)

    def run(self) -> None:
        self.root.mainloop()
