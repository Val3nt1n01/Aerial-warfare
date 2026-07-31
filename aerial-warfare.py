import pygame
from personaje import cubo
from enemigo import Enemigo
from bala import bala

import random
#py -m pip install pygame

pygame.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
FPS = 60
FUENTE = pygame.font.SysFont("AmeriGarmnd_BT", 36)

jugando = True

relog = pygame.time.Clock()

vida = 5
puntos = 0

tiempo_pasado = 0

tiempo_entre_enemigos = 500  # Tiempo en milisegundos entre la aparición de enemigos

cubo = cubo(ANCHO/2, ALTO-100)

enemigos = []
balas = []

ultima_bala = 0
tiempo_entre_balas = 100  # Tiempo en milisegundos entre disparos

enemigos.append(Enemigo(ANCHO/2, 100))

def crear_bala():
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(bala(cubo.rect.centerx, cubo.rect.top))
        ultima_bala = pygame.time.get_ticks()

def gestionar_teclas(teclas):
    #if teclas[pygame.K_w]:
        #cubo.y -= cubo.velocidad
    #if teclas[pygame.K_s]:
        #cubo.y += cubo.velocidad
    if teclas[pygame.K_a]:
        cubo.x -= cubo.velocidad
    if teclas[pygame.K_d]:
        cubo.x += cubo.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()

while jugando:

    tiempo_pasado += relog.tick(FPS)

    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0, ANCHO), -100))
        tiempo_pasado = 0
 
    eventos = pygame.event.get()

    teclas = pygame.key.get_pressed()

    texto_vida = FUENTE.render(f"Vidas: {vida}", True, "white")
    texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "white")
    gestionar_teclas(teclas)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False

    VENTANA.fill("black")
    cubo.dibujar(VENTANA)

    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()

        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            vida -= 1
            print(f"Te quedan {vida} vidas")
            enemigos.remove(enemigo)
        if vida <= 0:
            print("Game Over")
            jugando = False

        if enemigo.y > ALTO:
            enemigos.remove(enemigo)
            puntos += 1

        for b in balas[:]:
            if b.rect.colliderect(enemigo.rect):  # <--- Sintaxis corregida
                balas.remove(b)
                enemigo.vida -= 1
        if enemigo.vida <= 0:
            enemigos.remove(enemigo)
            puntos += 1
            

    for b in balas[:]:
        b.dibujar(VENTANA)
        b.movimiento()

               

    VENTANA.blit(texto_vida, (20, 20))
    VENTANA.blit(texto_puntos, (20, 50))


    pygame.display.update()
pygame.quit()

nombre = input("Ingrese su nombre: ")

with open("puntajes.txt", "a") as archivo:
    archivo.write(f"{nombre}: {puntos}\n")

quit()