import pygame

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 75
        self.alto = 75
        self.velocidad = 5
        self.color = "purple"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.vida = 3
        self.imagen = pygame.image.load("nave_sin_fondo.png")  # Carga la imagen del cubo
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        self.imagen = pygame.transform.rotate(self.imagen, 180)  # Rota la imagen 180 grados
        

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))  # Dibuja la imagen del cubo

    def movimiento(self):
        self.y += self.velocidad