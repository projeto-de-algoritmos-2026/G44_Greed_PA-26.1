from src.models import Neighborhood, Road


START = "Cozinha Central"
INITIAL_FUEL = 46

NEIGHBORHOODS = [
    Neighborhood("Cozinha Central", 360, 235, 0),
    Neighborhood("Vila Sol", 155, 105, 38),
    Neighborhood("Morro Azul", 120, 330, 64),
    Neighborhood("Jardim Norte", 350, 70, 32),
    Neighborhood("Parque Verde", 360, 395, 44),
    Neighborhood("Ribeirao", 585, 395, 58),
    Neighborhood("Hospital", 570, 110, 72),
    Neighborhood("Escola Nova", 215, 220, 26),
    Neighborhood("Distrito Leste", 610, 240, 46),
]

ROADS = [
    Road("Cozinha Central", "Escola Nova", 6),
    Road("Cozinha Central", "Jardim Norte", 7),
    Road("Cozinha Central", "Parque Verde", 6),
    Road("Cozinha Central", "Distrito Leste", 8),
    Road("Escola Nova", "Vila Sol", 5),
    Road("Escola Nova", "Morro Azul", 7),
    Road("Vila Sol", "Jardim Norte", 6),
    Road("Jardim Norte", "Hospital", 6),
    Road("Hospital", "Distrito Leste", 5),
    Road("Distrito Leste", "Ribeirao", 4),
    Road("Ribeirao", "Parque Verde", 8),
    Road("Parque Verde", "Morro Azul", 7),
    Road("Morro Azul", "Escola Nova", 6),
    Road("Hospital", "Cozinha Central", 10),
    Road("Distrito Leste", "Parque Verde", 6),
]
