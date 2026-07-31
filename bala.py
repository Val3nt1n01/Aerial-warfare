import pygame

class bala:
    def __init__(self, x, y): # (mantén tus parámetros actuales)
        self.x = x
        self.y = y
        self.ancho = 20
        self.alto = 20
        self.velocidad = 15
        self.color = "white"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, ventana):
        # Eliminamos la línea que recreaba el Rect aquí
        pygame.draw.rect(ventana, self.color, self.rect)

    def movimiento(self):
        self.y -= self.velocidad
        self.rect.y = self.y  # <--- ¡ESTO ACTUALIZA EL RECTÁNGULO FÍSICO!