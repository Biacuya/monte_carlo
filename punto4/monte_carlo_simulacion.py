import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la simulación
#Cantidad de simulaciones
n_juegos = 5
n_rondas = 10
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

generos = ['hombre', 'mujer']

# Puntos por diana
puntos_diana = [10, 9, 8, 0] # Central, intermedia, exterior, error

# Datos a guardar por juego
mejor_suerte_por_juego = []
mas_experiencia_por_juego = []
equipo_ganador_por_juego = []
genero_mas_victorias_por_juego = []
puntajes_total_equipo_1 = []
puntajes_total_equipo_2 = []

# Función para crear un jugador
def crear_jugador(genero):
    resistencia = max(1, int(np.random.normal(resistencia_mean, resistencia_std)))
    resistencia_aux = resistencia
    experiencia = experiencia_inicial
    suerte = np.random.uniform(suerte_min, suerte_max)
    return {"resistencia": resistencia, "resistencia_aux": resistencia_aux, "experiencia": experiencia, "suerte": suerte, "genero": genero}

# Función para realizar un lanzamiento
def lanzar(genero, jugador):
    # Reducción de resistencia por lanzamiento
    jugador['resistencia'] -= 5

    # Probabilidad de acierto en función del género
    prob_diana = prob_diana_mujer if jugador['genero'] == 'mujer' else prob_diana_hombre

    # Lanzamiento
    resultado = np.random.choice(puntos_diana, p=prob_diana)
    return resultado




# Simulación de 20,000 juegos



def simulacion_monte_carlo():
  condition = True
  cantidad_juegos = 0
  resistencia_inicial_jugador_1 = 0;
  resistencia_inicial_jugador_2 = 0;
  cansacio_one = 1
  cansacio_two = 2
  count = 0

  equipo_1 = [crear_jugador('mujer') if i % 2 == 0 else crear_jugador('hombre') for i in range(equipo_size)]
  equipo_2 = [crear_jugador('mujer') if i % 2 == 0 else crear_jugador('hombre') for i in range(equipo_size)]

  print(equipo_1)
  print(equipo_2)


  for juego in range(n_juegos):
        puntos_equipo_1 = 0
        puntos_equipo_2 = 0
        puntos_ronda_1 = 0
        puntos_ronda_2 = 0

        # Simulación de las rondas
        while condition:
            # Lanzamientos para cada jugador de ambos equipos
            for jugador_1, jugador_2 in zip(equipo_1, equipo_2):
                resistencia_inicial_jugador_1 = jugador_1['resistencia_aux']
                resistencia_inicial_jugador_2 = jugador_2['resistencia_aux']

                if jugador_1['resistencia'] <= 4:
                  count +=1
                  print("count ", count)
                  resistencia_inicial_jugador_1 -= max(1, int(np.random.normal(cansacio_one, cansacio_two)))
                  jugador_1['resistencia'] = resistencia_inicial_jugador_1
                else:
                  puntos_equipo_1 += lanzar(jugador_1['genero'], jugador_1)

                if jugador_2['resistencia'] <= 4:
                  count +=1
                  print("count ", count)
                  resistencia_inicial_jugador_2 -= max(1, int(np.random.normal(cansacio_one, cansacio_two)))
                  jugador_2['resistencia'] = resistencia_inicial_jugador_2
                  
                else:
                  puntos_equipo_2 += lanzar(jugador_2['genero'], jugador_2)
                  
                if count == 10:
                  cantidad_juegos +=1
                  print("Juegos: ", cantidad_juegos)
                  print(f"Antes de reiniciar la resistencia: {jugador_1['genero']}, suerte: {jugador_1['suerte']}, exp: {jugador_1['experiencia']}, resistencia: {jugador_1['resistencia']}")
                  jugador_1['resistencia'] = jugador_1['resistencia_aux']
                  print(f"Depués de reiniciar la resistencia: {jugador_1['genero']}, suerte: {jugador_1['suerte']}, exp: {jugador_1['experiencia']}, resistencia: {jugador_1['resistencia']}")
                  print(equipo_1)
                  jugador_2['resistencia'] = jugador_2['resistencia_aux']

                  if puntos_equipo_1 > puntos_equipo_2:
                    print('Equipo uno ganador: ', puntos_equipo_1)
                    print('Equipo Dos perdedor: ', puntos_equipo_2)
                    equipo_ganador_por_juego.append(1)
                  else:
                    print('Equido dos ganador: ', puntos_equipo_2)
                    print('Equipo uno perdedor: ', puntos_equipo_1)
                    equipo_ganador_por_juego.append(2)

                if cantidad_juegos >= n_juegos:
                  condition = False;
                  


        # Guardar los resultados del juego
        mejor_suerte_por_juego.append(max(equipo_1 + equipo_2, key=lambda x: x['suerte']))
        mas_experiencia_por_juego.append(max(equipo_1 + equipo_2, key=lambda x: x['experiencia']))
        puntajes_total_equipo_1.append(puntos_equipo_1)
        puntajes_total_equipo_2.append(puntos_equipo_2)

simulacion_monte_carlo()




#print(mejor_suerte_por_juego)
#print(mas_experiencia_por_juego)
print('Equipo ganador: ', equipo_ganador_por_juego)
print('Puntaje equipo 1:', puntajes_total_equipo_1)
print('Puntaje equipo 2:', puntajes_total_equipo_2)
# Graficar resultados de los puntajes
plt.figure(figsize=(10, 6))
#La grafica es para cada jugador en el juego
#plt.plot(puntajes_total_equipo_1[:20000], label="Equipo 1")
#plt.plot(puntajes_total_equipo_2[:20000], label="Equipo 2")
plt.title('Puntos obtenidos por cada equipo en los primeros 20000 juegos')
plt.xlabel('Juego')
plt.ylabel('Puntos Totales')
plt.legend()
plt.grid(True)
plt.show()
