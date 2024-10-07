# -*- coding: utf-8 -*-
"""Montecarlo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a2m9dhA_BIqNsopjQnRaxe9qFzEhXOCR
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import copy
from collections import Counter

# Parámetros de la simulación
# Cantidad de simulaciones

equipo_size = 5

# Habilidades
resistencia_mean = 35
resistencia_std = 10
experiencia_inicial = 10
suerte_min = 1
suerte_max = 3

# Probabilidades de acierto
prob_diana_mujer = [0.30, 0.38, 0.27, 0.05]  # Central, intermedia, exterior, error
prob_diana_hombre = [0.20, 0.33, 0.40, 0.07]

# generos

generos = ["hombre", "mujer"]

# Puntos por diana
puntos_diana = [10, 9, 8, 0]  # Central, intermedia, exterior, error

# Datos a guardar por juego
mejor_suerte_por_juego = []
mejor_experiencia_por_juego = []
equipo_ganador_por_juego = []
genero_mas_victorias_por_juego = []
puntajes_total_equipo_1 = []
puntajes_total_equipo_2 = []
jugador_mas_suerte_juego = []

puntos_jugadores_por_juego = {
    f"jugador{i+1}": [] for i in range(equipo_size * 2)
}  # Un diccionario para almacenar los puntajes de todos los jugadores


def graficar_puntos(puntos_jugadores_por_juego):
    plt.figure(figsize=(10, 6))

    for jugador, puntos in puntos_jugadores_por_juego.items():
        plt.plot(range(1, len(puntos) + 1), puntos, marker="o", label=jugador)

    plt.title("Puntos obtenidos por cada jugador vs Juegos")
    plt.xlabel("Juego")
    plt.ylabel("Puntos obtenidos")
    plt.xticks(range(1, len(puntos_jugadores_por_juego["jugador1"]) + 1))
    plt.legend()
    plt.grid()
    plt.show()


# Función para crear un jugador
def crear_jugador(genero):
    resistencia = max(1, int(np.random.normal(resistencia_mean, resistencia_std)))
    resistencia_aux = resistencia
    experiencia = experiencia_inicial
    suerte = np.random.uniform(suerte_min, suerte_max)
    return {
        "nombre_jugador": "n/n",
        "resistencia": resistencia,
        "resistencia_aux": resistencia_aux,
        "experiencia": experiencia,
        "suerte": suerte,
        "genero": genero,
        "puntos_individual": 0,
        "rondas_ganadas": 0,
    }


def recolectar_jugador_mas_suerte(jugadores):
    # Encuentra al jugador con más suerte
    jugador_mas_suerte = max(jugadores, key=lambda j: j["suerte"])
    mejor_suerte_por_juego.append(jugador_mas_suerte)
    print(
        f"Jugador con más suerte en este juego: {jugador_mas_suerte['nombre_jugador']} con suerte {jugador_mas_suerte['suerte']}"
    )


def recolectar_jugador_mas_experiencia(jugadores):
    # Encuentra al jugador con más experiencia
    jugador_mas_experiencia = max(jugadores, key=lambda j: j["experiencia"])
    mejor_experiencia_por_juego.append(jugador_mas_experiencia)
    print(
        f"Jugador con más experiencia en este juego: {jugador_mas_experiencia['nombre_jugador']} con experiencia {jugador_mas_experiencia['experiencia']}"
    )


def actualizar_suerte(jugadores):
    # Actualiza la suerte de cada jugador
    for jugador in jugadores:
        jugador["suerte"] = np.random.uniform(suerte_min, suerte_max)


# Función para realizar un lanzamiento
def lanzar(jugador):
    # Reducción de resistencia por lanzamiento
    jugador["resistencia"] -= 5

    # Probabilidad de acierto en función del género
    prob_diana = prob_diana_mujer if jugador["genero"] == "mujer" else prob_diana_hombre
    # Lanzamiento
    # resultado = seleccionar_con_probabilidades(puntos_diana, prob_diana)
    resultado = random.choices(puntos_diana, weights=prob_diana)[0]

    return resultado


def lanzar_desempate(jugador):

    # Probabilidad de acierto en función del género
    prob_diana = prob_diana_mujer if jugador["genero"] == "mujer" else prob_diana_hombre

    # Lanzamiento
    # resultado = seleccionar_con_probabilidades(puntos_diana, prob_diana)
    resultado = random.choices(puntos_diana, weights=prob_diana)[0]

    return resultado


def registrar_genero_con_mas_victorias(jugador):
    if jugador["genero"] == "hombre":
        genero_mas_victorias_por_juego.append("hombre")
    else:
        genero_mas_victorias_por_juego.append("mujer")


def reiniciar_puntajes(jugadores):
    for jugador in jugadores:
        jugador["puntos_individual"] = 0  # Reinicia el puntaje individual a 0


def registrar_genero_con_mas_victorias_por_juego(equipo_ganador):
    # Sumar las rondas ganadas por los hombres y mujeres en el equipo ganador
    rondas_hombres = sum(
        jugador["rondas_ganadas"]
        for jugador in equipo_ganador
        if jugador["genero"] == "hombre"
    )
    rondas_mujeres = sum(
        jugador["rondas_ganadas"]
        for jugador in equipo_ganador
        if jugador["genero"] == "mujer"
    )

    # Comparar las rondas ganadas entre hombres y mujeres
    if rondas_hombres > rondas_mujeres:
        genero_mas_victorias_por_juego.append("hombre")
        print(
            f"El género con más victorias en este juego es: hombre con {rondas_hombres} rondas ganadas"
        )
    elif rondas_mujeres > rondas_hombres:
        genero_mas_victorias_por_juego.append("mujer")
        print(
            f"El género con más victorias en este juego es: mujer con {rondas_mujeres} rondas ganadas"
        )
    else:
        genero_mas_victorias_por_juego.append("empate")
        print(
            f"El género con más victorias en este juego es: empate con {rondas_hombres} rondas ganadas por cada género"
        )


def most_lucky(players):
    most_lucky_player = max(players, key=lambda player: player["suerte"])
    return most_lucky_player


def encontrar_suertudos(list):
    contador = Counter(list)
    for valor, cuenta in contador.items():
        if cuenta == 3:
            return valor  # Devuelve el valor que se repite 3 veces
    return None  # Si no hay ningún valor con 3 repeticiones


def simulacion_monte_carlo():
    condition = True
    cantidad_juegos = 0
    resistencia_inicial_jugador_1 = 0
    resistencia_inicial_jugador_2 = 0
    cansacio_one = 1
    cansacio_two = 2
    valor_repetido = ""
    valor_repetido2 = ""
    lucky_list = []
    lucky_list2 = []

    equipo_1 = [
        crear_jugador("mujer") if i % 2 == 0 else crear_jugador("hombre")
        for i in range(equipo_size)
    ]
    equipo_2 = [
        crear_jugador("mujer") if i % 2 == 0 else crear_jugador("hombre")
        for i in range(equipo_size)
    ]
    equipo_1_copia = copy.deepcopy(equipo_1)
    equipo_2_copia = copy.deepcopy(equipo_2)

    def desempate_juegos(jugadores):
        puntajes = {jugador["nombre_jugador"]: 0 for jugador in jugadores}

        # Jugar 5 juegos
        for juego in range(1):

            for jugador in jugadores:
                resultado = lanzar_desempate(jugador)
                puntajes[jugador["nombre_jugador"]] += resultado

        # Obtener el puntaje máximo y verificar si hay empate
        max_puntaje = max(puntajes.values())
        jugadores_max_puntos = [
            jugador
            for jugador in jugadores
            if puntajes[jugador["nombre_jugador"]] == max_puntaje
        ]

        return jugadores_max_puntos, max_puntaje

    def calculos_individuales():
        calcular_ganador_ronda_individual()
        recolectar_jugador_mas_suerte(equipo_1 + equipo_2)
        recolectar_jugador_mas_experiencia(equipo_1 + equipo_2)
        for jugador in equipo_1 + equipo_2:
            puntos_jugadores_por_juego[jugador["nombre_jugador"]].append(
                jugador["puntos_individual"]
            )

        reiniciar_puntajes(equipo_1)
        reiniciar_puntajes(equipo_2)

    def contar_victorias_totales():
        total_hombres = genero_mas_victorias_por_juego.count("hombre")
        total_mujeres = genero_mas_victorias_por_juego.count("mujer")

        if total_hombres > total_mujeres:
            print(
                f"El género con más victorias totales es: hombre con {total_hombres} victorias"
            )
        elif total_mujeres > total_hombres:
            print(
                f"El género con más victorias totales es: mujer con {total_mujeres} victorias"
            )
        else:
            print(
                f"Ambos géneros tienen el mismo número de victorias: {total_hombres} para hombres y {total_mujeres} para mujeres"
            )

    def calcular_ganador_ronda_individual():
        # Agrupar todos los jugadores de ambos equipos en una lista combinada
        todos_los_jugadores = equipo_1 + equipo_2

        # Obtener el puntaje máximo de todos los jugadores
        max_puntos = max(
            jugador["puntos_individual"] for jugador in todos_los_jugadores
        )

        # Obtener todos los jugadores con el puntaje máximo
        jugadores_max_puntos = [
            jugador
            for jugador in todos_los_jugadores
            if jugador["puntos_individual"] == max_puntos
        ]

        # Si hay empate, realizar un desempate con el método de lanzar
        if len(jugadores_max_puntos) > 1:

            # Repetir el desempate hasta que haya un solo ganador
            while len(jugadores_max_puntos) > 1:

                jugadores_max_puntos, max_puntaje_final = desempate_juegos(
                    jugadores_max_puntos
                )

            # Declarar al ganador
            jugador_ganador = jugadores_max_puntos[0]
            jugador_ganador["experiencia"] += 3
            jugador_ganador["rondas_ganadas"] += 1
            registrar_genero_con_mas_victorias(jugador_ganador)
        else:
            jugador_ganador = jugadores_max_puntos[0]
            jugador_ganador["experiencia"] += 3
            jugador_ganador["rondas_ganadas"] += 1
            registrar_genero_con_mas_victorias(jugador_ganador)

    contador = 1
    for jugador in equipo_1:
        jugador["nombre_jugador"] = f"jugador{contador}"
        contador += 1

    # Cambiar los nombres de los jugadores para el segundo equipo
    for jugador in equipo_2:
        jugador["nombre_jugador"] = f"jugador{contador}"
        contador += 1

    print(equipo_1)
    print(equipo_2)

    #  for juego in range(n_juegos):
    puntos_equipo_1 = 0
    puntos_equipo_2 = 0
    puntos_ronda_1 = 0
    puntos_ronda_2 = 0
    n_juegos = 5
    tiro_bonus = False

    # Simulación de las rondas
    count = 0
    cantidad_juegos = 0
    while cantidad_juegos < n_juegos:
        # Lanzamientos para cada jugador de ambos equipos
        for jugador_1, jugador_2 in zip(equipo_1, equipo_2):
            resistencia_inicial_jugador_1 = jugador_1["resistencia_aux"]
            resistencia_inicial_jugador_2 = jugador_2["resistencia_aux"]

            if tiro_bonus:
                jugador_suertudo = most_lucky(equipo_1)
                puntos_equipo_1 += lanzar(jugador_suertudo)
                lucky_list.append(most_lucky(equipo_1)["nombre_jugador"])

                jugador_suertudo2 = most_lucky(equipo_2)
                puntos_equipo_2 += lanzar(jugador_suertudo2)
                lucky_list2.append(most_lucky(equipo_2)["nombre_jugador"])

                valor_repetido = encontrar_suertudos(lucky_list)
                valor_repetido2 = encontrar_suertudos(lucky_list2)

                print("")
                tiro_bonus = False

            # Tiro Extra
            if valor_repetido == most_lucky(equipo_1)["nombre_jugador"]:
                puntos_equipo_1 += lanzar(most_lucky(equipo_1))

            if valor_repetido2 == most_lucky(equipo_2)["nombre_jugador"]:
                puntos_equipo_2 += lanzar(most_lucky(equipo_2))

            if jugador_1["resistencia"] <= 4:

                count += 1
                resistencia_inicial_jugador_1 -= max(
                    1, int(np.random.normal(cansacio_one, cansacio_two))
                )
                jugador_1["resistencia"] = resistencia_inicial_jugador_1
                tiro_bonus = True
            else:
                puntos_jugador_1 = lanzar(jugador_1)
                puntos_equipo_1 += puntos_jugador_1
                jugador_1["puntos_individual"] = (
                    jugador_1["puntos_individual"] + puntos_jugador_1
                )
                tiro_bonus = False

            if jugador_2["resistencia"] <= 4:
                count += 1
                resistencia_inicial_jugador_2 -= max(
                    1, int(np.random.normal(cansacio_one, cansacio_two))
                )
                jugador_2["resistencia"] = resistencia_inicial_jugador_2
                tiro_bonus = True
            else:
                puntos_jugador_2 = lanzar(jugador_2)
                puntos_equipo_2 += puntos_jugador_2
                jugador_2["puntos_individual"] = (
                    jugador_2["puntos_individual"] + puntos_jugador_2
                )
                tiro_bonus = False

            if count == 10:

                cantidad_juegos += 1
                tiro_bonus = True
                print("Juego: ", cantidad_juegos)
                calculos_individuales()
                jugador_1["resistencia"] = jugador_1["resistencia_aux"]
                jugador_2["resistencia"] = jugador_2["resistencia_aux"]

                if puntos_equipo_1 > puntos_equipo_2:
                    print("Equipo uno ganador: ", puntos_equipo_1)
                    print("Equipo Dos perdedor: ", puntos_equipo_2)
                    equipo_ganador_por_juego.append(1)

                else:
                    print("Equido dos ganador: ", puntos_equipo_2)
                    print("Equipo uno perdedor: ", puntos_equipo_1)
                    equipo_ganador_por_juego.append(2)

                registrar_genero_con_mas_victorias_por_juego(equipo_1 + equipo_2)
                count = 0
                actualizar_suerte(equipo_1)
                actualizar_suerte(equipo_2)

    contar_victorias_totales()
    # Guardar los resultados del juego


simulacion_monte_carlo()
graficar_puntos(puntos_jugadores_por_juego)