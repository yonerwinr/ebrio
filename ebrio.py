import random
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación del Borracho")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Configuración del borracho
radio_borracho = 10
posicion_borracho = [ANCHO // 2, ALTO // 2]

# Cargar la imagen del borracho
imagen_borracho = pygame.image.load('borracho.png')
imagen_borracho = pygame.transform.scale(imagen_borracho, (100, 100))  # Ajustar el tamaño de la imagen

# Fuente para el texto
fuente = pygame.font.SysFont(None, 36)

# Función para simular el paseo del borracho
def simular_paseo():
    x, y = ANCHO // 2, ALTO // 2
    trayectoria = [(x, y, '')]
    for _ in range(10):  # Número de pasos en el paseo
        paso = random.choice(['norte', 'sur', 'este', 'oeste'])
        if paso == 'norte':
            y -= 50
        elif paso == 'sur':
            y += 50
        elif paso == 'este':
            x += 50
        elif paso == 'oeste':
            x -= 50
        trayectoria.append((x, y, paso))
    return trayectoria

# Función para estimar la probabilidad
def estimar_probabilidad(num_simulaciones):
    exito = 0
    for _ in range(num_simulaciones):
        trayectoria = simular_paseo()
        x_final, y_final, _ = trayectoria[-1]
        distancia = abs(x_final - ANCHO // 2) // 50 + abs(y_final - ALTO // 2) // 50
        if distancia == 2:
            exito += 1
    return exito / num_simulaciones

# Función para dibujar las calles
def dibujar_calles():
    for x in range(0, ANCHO, 50):
        pygame.draw.line(pantalla, BLANCO, (x, 0), (x, ALTO))
    for y in range(0, ALTO, 50):
        pygame.draw.line(pantalla, BLANCO, (0, y), (ANCHO, y))

# Función para dibujar al borracho
def dibujar_borracho(posicion):
    pantalla.blit(imagen_borracho, (posicion[0] - 20, posicion[1] - 20))  # Ajustar la posición para centrar la imagen

# Función para dibujar texto en la pantalla
def dibujar_texto(texto, posicion):
    imagen_texto = fuente.render(texto, True, BLANCO)
    pantalla.blit(imagen_texto, posicion)

# Función para dibujar un botón
def dibujar_boton(texto, posicion, tamano):
    rect = pygame.Rect(posicion, tamano)
    pygame.draw.rect(pantalla, VERDE, rect)
    imagen_texto = fuente.render(texto, True, NEGRO)
    pantalla.blit(imagen_texto, (posicion[0] + 10, posicion[1] + 10))
    return rect

# Función principal
def main():
    num_simulaciones = 1000
    probabilidad = estimar_probabilidad(num_simulaciones)
    trayectoria = simular_paseo()
    indice_paso = 0
    reloj = pygame.time.Clock()
    mostrar_probabilidad = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if mostrar_probabilidad and boton.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pantalla.fill(NEGRO)
        dibujar_calles()

        if indice_paso < len(trayectoria):
            posicion_borracho[0], posicion_borracho[1], direccion = trayectoria[indice_paso]
            indice_paso += 1
        else:
            direccion = ''
            mostrar_probabilidad = True

        dibujar_borracho(posicion_borracho)
        dibujar_texto(f"Dirección: {direccion}", (10, 10))

        if mostrar_probabilidad:
            dibujar_texto(f"Probabilidad: {probabilidad * 100:.2f}%", (10, 50))
            boton = dibujar_boton("Finalizar", (10, 100), (150, 50))

        pygame.display.flip()
        reloj.tick(1)  # Controlar la velocidad de la animación

if __name__ == "__main__":
    main()
    