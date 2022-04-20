#---------------------------------------------------------#
# Universidad Nacional Autónoma de México
# Facultad de Ingeniería
# Semestre 2022-2
# Asignatura: Sistemas Distribuidos
# Grupo: 01 
# Nombre del alumno: López Hernández Emanuel 
# Programa: Juego de la vida
# Versión: 4.7.2
# Fecha: 19 de abril de 2022
#---------------------------------------------------------#

#Libreria para la creación de juegos en 2D
import pygame
#Libreria para análisis de datos, creación de matrices y funciones matemáticas
import numpy
#Libreria para el control del tiempo
import time
#Inicializa todos los modulos de pygame
pygame.init()
#Inicialización del tamaño de la ventana (ancho, alto)
ancho, alto = 800, 800
#Inicialización del color de la ventana
colorPantalla = 25, 25 ,25
#Despliegue de la ventana
screen  = pygame.display.set_mode((alto, ancho))
screen.fill(colorPantalla)

# Tamaño de nuestra matriz cuadrada nxn para valores mayores a 50 
nxC, nyC = 90, 90

# Estado de las celdas. Viva = 1 / Muerta = 0
gameState = numpy.zeros((nxC,  nyC))

# Dimensiones de cada celda individual
dimCW = ancho / nxC
dimCH = alto / nyC

# Modelos en gameState previamente definidos y que se usan para inicializar el juego

# Oscilador.
gameState[38, 20] = 1
gameState[39, 20] = 1
gameState[40, 20] = 1

# Runner 1
gameState[10,5] = 1
gameState[12,5] = 1
gameState[11,6] = 1
gameState[12,6] = 1
gameState[11,7] = 1

# Runner 2
gameState[5,10] = 1
gameState[5,12] = 1
gameState[6,11] = 1
gameState[6,12] = 1
gameState[7,11] = 1

# Box
gameState[18,15] = 1
gameState[17,16] = 1
gameState[17,15] = 1
gameState[18,16] = 1

#Serpent 1
gameState[30,20] = 1
gameState[31,20] = 1
gameState[32,20] = 1
gameState[32,19] = 1
gameState[33,19] = 1
gameState[34,19] = 1

pauseExect = False

# Bucle de ejecución
while True:

    # Copiamos la matriz del estado anterior
    # para representar la matriz en el nuevo estado
    newGameState = numpy.copy(gameState)

    # Ralentizamos la ejecución a 0.1 segundos
    time.sleep(0.1)

    # Limpiamos la pantalla
    screen.fill(colorPantalla)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    # Cada vez que identificamos un evento lo procesamos
    for event in ev:
        # Detectamos si se presiona una tecla.
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se presiona el ratón.
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(numpy.floor(posX / dimCW)), int(numpy.floor(posY / dimCH))
            newGameState[celX, celY] = 1
    # Recorrido según el tamaño de la ventana
    for y in range(0, nxC):
        for x in range (0, nyC):

            if not pauseExect:

                # Calculamos el número de vecinos cercanos.
                n_neigh =   gameState[(x - 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x)     % nxC, (y - 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x - 1) % nxC, (y)      % nyC] + \
                            gameState[(x + 1) % nxC, (y)      % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1)  % nyC] + \
                            gameState[(x)     % nxC, (y + 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1)  % nyC]

                # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".

                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla #2 : Una celda viva con menos de 2 o más 3 vecinas vinas, "muere".

                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Calculamos el polígono que forma la celda.
            poly = [((x)   * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

            # Si la celda está "muerta" pintamos un recuadro con borde gris
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (40, 40, 40), poly, 1)
           # Si la celda está "viva" pintamos un recuadro relleno de color
            else:
                pygame.draw.polygon(screen, (200, 100, 100), poly, 0)

    # Actualizamos el estado del juego.
    gameState = numpy.copy(newGameState)

    # Mostramos el resultado
    pygame.display.flip()
