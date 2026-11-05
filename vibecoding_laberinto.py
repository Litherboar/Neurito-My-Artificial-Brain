"""Compara DFS, BFS y A* en los retos de Neurito.

Este archivo corresponde al punto 7 del laboratorio. Ejecuta:

    uv run vibecoding_laberinto.py
"""
from collections import deque
import heapq
from statistics import mean

from laberinto_mundo import MAPAS, DIRECCIONES, valido
from laberinto_red import generar_datos


def vecinos(mapa, posicion):
    for accion, (df, dc) in enumerate(DIRECCIONES):
        siguiente = (posicion[0] + df, posicion[1] + dc)
        if valido(mapa, siguiente):
            yield accion, siguiente


def distancia_manhattan(origen, meta):
    return abs(origen[0] - meta[0]) + abs(origen[1] - meta[1])


def buscar(mapa, inicio, meta, algoritmo):
    """Devuelve la ruta y el número de celdas que revisó el algoritmo."""
    anteriores = {inicio: None}
    acciones = {}
    costes = {inicio: 0}
    contador = 0

    if algoritmo == "dfs":
        pendientes = [inicio]
    elif algoritmo == "bfs":
        pendientes = deque([inicio])
    else:
        pendientes = [(distancia_manhattan(inicio, meta), 0, inicio)]

    while pendientes:
        if algoritmo == "dfs":
            actual = pendientes.pop()
        elif algoritmo == "bfs":
            actual = pendientes.popleft()
        else:
            _, _, actual = heapq.heappop(pendientes)
        contador += 1

        if actual == meta:
            break

        for accion, siguiente in vecinos(mapa, actual):
            coste = costes[actual] + 1
            if siguiente in anteriores:
                if algoritmo != "astar" or coste >= costes[siguiente]:
                    continue
            anteriores[siguiente] = actual
            acciones[siguiente] = accion
            costes[siguiente] = coste

            if algoritmo == "astar":
                prioridad = coste + distancia_manhattan(siguiente, meta)
                heapq.heappush(pendientes, (prioridad, coste, siguiente))
            else:
                pendientes.append(siguiente)

    if meta not in anteriores:
        return [], contador

    ruta = []
    actual = meta
    while anteriores[actual] is not None:
        ruta.append(acciones[actual])
        actual = anteriores[actual]
    ruta.reverse()
    return ruta, contador


def comparar():
    """Compara los tres algoritmos usando los 716 casos de prueba del proyecto."""
    (_, _), (_, _), casos = generar_datos(semilla=42)
    resultados = {}
    for algoritmo in ("dfs", "bfs", "astar"):
        rutas = [
            buscar(MAPAS[indice], inicio, meta, algoritmo)
            for indice, inicio, meta, _ in casos
        ]
        resultados[algoritmo] = {
            "exito": sum(bool(ruta) for ruta, _ in rutas) / len(rutas),
            "movimientos": mean(len(ruta) for ruta, _ in rutas if ruta),
            "celdas": mean(celdas for _, celdas in rutas),
        }
    return resultados


def main():
    nombres = {"dfs": "DFS", "bfs": "BFS", "astar": "A*"}
    print("Comparación DFS, BFS y A*")
    print("Casos de prueba: 716")
    print()
    for algoritmo, datos in comparar().items():
        print(
            f"{nombres[algoritmo]}: "
            f"éxito={datos['exito']:.1%}, "
            f"movimientos promedio={datos['movimientos']:.1f}, "
            f"celdas revisadas={datos['celdas']:.1f}"
        )


if __name__ == "__main__":
    main()
