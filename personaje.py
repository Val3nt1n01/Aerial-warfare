import pygame

class cubo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 100
        self.alto = 100
        self.velocidad = 10
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load("cubo_sin_fondo.png")  # Carga la imagen del cubo
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))  # Dibuja la imagen del cubo