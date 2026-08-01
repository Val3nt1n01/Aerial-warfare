import pygame
import random
from personaje import cubo
from enemigo import Enemigo
from bala import bala

pygame.init()

# --- CONFIGURACIÓN DE PANTALLA ---
ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aerial Warfare")
FPS = 60
relog = pygame.time.Clock()

# --- FONDO DEL MENÚ ---
# Reemplaza "fondo_menu.png" por la ruta/nombre de tu imagen
fondo_menu_original = pygame.image.load("fondo_menu.jpg")
fondo_menu = pygame.transform.scale(fondo_menu_original, (ANCHO, ALTO))

fondo_game_original = pygame.image.load("fondo_game.jpg")
fondo_game = pygame.transform.scale(fondo_game_original, (ANCHO, ALTO))

# --- FUENTES Y TIPOGRAFÍAS ---
FUENTE_HUD = pygame.font.SysFont("AmeriGarmnd_BT", 36)
FUENTE_TITULO = pygame.font.SysFont("AmeriGarmnd_BT", 72, bold=True)
FUENTE_BOTON = pygame.font.SysFont("AmeriGarmnd_BT", 36)

# --- BOTONES ---
boton_play = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 40, 200, 60)
boton_exit = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 40, 200, 60)

boton_continuar = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 - 40, 240, 60)
boton_menu = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 + 40, 240, 60)

# --- VARIABLES DE ESTADO Y JUEGO ---
jugando = True
estado = "MENU"
nombre_jugador = ""

vida = 5
puntos = 0
tiempo_pasado = 0
tiempo_entre_enemigos = 500  

cubo = cubo(ANCHO / 2, ALTO - 100)
enemigos = []
balas = []

ultima_bala = 0
tiempo_entre_balas = 250  

# --- FUNCIONES AUXILIARES ---
def crear_bala():
    global ultima_bala
    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(bala(cubo.rect.centerx, cubo.rect.top))
        ultima_bala = pygame.time.get_ticks()

def gestionar_teclas(teclas):
    if teclas[pygame.K_a]:
        cubo.x -= cubo.velocidad
    if teclas[pygame.K_d]:
        cubo.x += cubo.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()

    if cubo.x < 0:
        cubo.x = 0
    if cubo.x > ANCHO - cubo.ancho:
        cubo.x = ANCHO - cubo.ancho

def reiniciar_partida():
    global vida, puntos, enemigos, balas, tiempo_pasado
    vida = 5
    puntos = 0
    enemigos.clear()
    balas.clear()
    tiempo_pasado = 0
    cubo.x = ANCHO / 2
    cubo.y = ALTO - 100

def guardar_puntaje(nombre_final, puntos_finales):
    nombre_clean = nombre_final.strip() if nombre_final.strip() else "Anonimo"
    puntajes_guardados = {}
    
    try:
        with open("puntajes.txt", "r") as archivo:
            for linea in archivo:
                if ":" in linea:
                    usuario, pts = linea.strip().split(":", 1)
                    puntajes_guardados[usuario.strip()] = int(pts.strip())
    except FileNotFoundError:
        pass

    if nombre_clean in puntajes_guardados:
        if puntos_finales > puntajes_guardados[nombre_clean]:
            puntajes_guardados[nombre_clean] = puntos_finales
    else:
        puntajes_guardados[nombre_clean] = puntos_finales

    with open("puntajes.txt", "w") as archivo:
        for usuario, pts in puntajes_guardados.items():
            archivo.write(f"{usuario}: {pts}\n")

# --- BUCLE PRINCIPAL ---
while jugando:
    relog.tick(FPS)
    eventos = pygame.event.get()
    pos_mouse = pygame.mouse.get_pos()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            if estado == "JUEGO":
                estado = "PAUSA"
            elif estado == "PAUSA":
                estado = "JUEGO"

        if estado == "GAME_OVER" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                guardar_puntaje(nombre_jugador, puntos)
                estado = "MENU"
            elif evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            else:
                if len(nombre_jugador) < 12 and evento.unicode.isprintable():
                    nombre_jugador += evento.unicode

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado == "MENU":
                if boton_play.collidepoint(evento.pos):
                    reiniciar_partida()
                    estado = "JUEGO"
                elif boton_exit.collidepoint(evento.pos):
                    jugando = False

            elif estado == "PAUSA":
                if boton_continuar.collidepoint(evento.pos):
                    estado = "JUEGO"
                elif boton_menu.collidepoint(evento.pos):
                    estado = "MENU"

    # ==========================================
    # 1. PANTALLA: MENÚ PRINCIPAL
    # ==========================================
    if estado == "MENU":
        # Dibujar la imagen de fondo en la esquina superior izquierda (0,0)
        VENTANA.blit(fondo_menu, (0, 0))

        txt_titulo = FUENTE_TITULO.render("AERIAL WARFARE", True, "white")
        VENTANA.blit(txt_titulo, txt_titulo.get_rect(center=(ANCHO // 2, ALTO // 4)))

        col_play = (70, 70, 70) if boton_play.collidepoint(pos_mouse) else (30, 30, 30)
        pygame.draw.rect(VENTANA, col_play, boton_play, border_radius=10)
        pygame.draw.rect(VENTANA, "white", boton_play, width=3, border_radius=10)
        txt_play = FUENTE_BOTON.render("PLAY", True, "white")
        VENTANA.blit(txt_play, txt_play.get_rect(center=boton_play.center))

        col_exit = (70, 70, 70) if boton_exit.collidepoint(pos_mouse) else (30, 30, 30)
        pygame.draw.rect(VENTANA, col_exit, boton_exit, border_radius=10)
        pygame.draw.rect(VENTANA, "red", boton_exit, width=3, border_radius=10)
        txt_exit = FUENTE_BOTON.render("EXIT", True, "white")
        VENTANA.blit(txt_exit, txt_exit.get_rect(center=boton_exit.center))

    # ==========================================
    # 2. PANTALLA: EN JUEGO
    # ==========================================
    elif estado == "JUEGO":
        tiempo_pasado += relog.get_time()

        if tiempo_pasado > tiempo_entre_enemigos:
            enemigos.append(Enemigo(random.randint(0, ANCHO - 50), -100))
            tiempo_pasado = 0

        teclas = pygame.key.get_pressed()
        gestionar_teclas(teclas)

        # Fondo estático durante el juego
        VENTANA.blit(fondo_game, (0, 0))

        cubo.dibujar(VENTANA)

        for b in balas[:]:
            b.movimiento()
            b.dibujar(VENTANA)
            if b.y < -20:
                balas.remove(b)

        for enemigo in enemigos[:]:
            enemigo.dibujar(VENTANA)
            enemigo.movimiento()

            if cubo.rect.colliderect(enemigo.rect):
                vida -= 1
                enemigos.remove(enemigo)
                if vida <= 0:
                    estado = "GAME_OVER"
                    nombre_jugador = ""
                continue

            if enemigo.y > ALTO:
                enemigos.remove(enemigo)
                continue

            for b in balas[:]:
                if b.rect.colliderect(enemigo.rect):
                    balas.remove(b)
                    enemigos.remove(enemigo)
                    puntos += 1
                    break

        txt_vida = FUENTE_HUD.render(f"Vidas: {vida}", True, "white")
        txt_puntos = FUENTE_HUD.render(f"Puntos: {puntos}", True, "white")
        VENTANA.blit(txt_vida, (20, 20))
        VENTANA.blit(txt_puntos, (20, 50))

    # ==========================================
    # 3. PANTALLA: PAUSA
    # ==========================================
    elif estado == "PAUSA":
        sombra = pygame.Surface((ANCHO, ALTO))
        sombra.set_alpha(150)
        sombra.fill((0, 0, 0))
        VENTANA.blit(sombra, (0, 0))

        txt_pausa = FUENTE_TITULO.render("PAUSA", True, "yellow")
        VENTANA.blit(txt_pausa, txt_pausa.get_rect(center=(ANCHO // 2, ALTO // 4)))

        col_cont = (70, 70, 70) if boton_continuar.collidepoint(pos_mouse) else (30, 30, 30)
        pygame.draw.rect(VENTANA, col_cont, boton_continuar, border_radius=10)
        pygame.draw.rect(VENTANA, "white", boton_continuar, width=3, border_radius=10)
        txt_cont = FUENTE_BOTON.render("CONTINUAR", True, "white")
        VENTANA.blit(txt_cont, txt_cont.get_rect(center=boton_continuar.center))

        col_men = (70, 70, 70) if boton_menu.collidepoint(pos_mouse) else (30, 30, 30)
        pygame.draw.rect(VENTANA, col_men, boton_menu, border_radius=10)
        pygame.draw.rect(VENTANA, "white", boton_menu, width=3, border_radius=10)
        txt_menu = FUENTE_BOTON.render("MENÚ", True, "white")
        VENTANA.blit(txt_menu, txt_menu.get_rect(center=boton_menu.center))

    # ==========================================
    # 4. PANTALLA: GAME OVER
    # ==========================================
    elif estado == "GAME_OVER":
        VENTANA.fill("black")

        txt_go = FUENTE_TITULO.render("GAME OVER", True, "red")
        VENTANA.blit(txt_go, txt_go.get_rect(center=(ANCHO // 2, ALTO // 4)))

        txt_pts = FUENTE_HUD.render(f"Puntaje Final: {puntos}", True, "white")
        VENTANA.blit(txt_pts, txt_pts.get_rect(center=(ANCHO // 2, ALTO // 3 + 20)))

        txt_indicacion = FUENTE_BOTON.render("Escribe tu nombre y presiona ENTER:", True, "yellow")
        VENTANA.blit(txt_indicacion, txt_indicacion.get_rect(center=(ANCHO // 2, ALTO // 2)))

        caja_texto = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 300, 50)
        pygame.draw.rect(VENTANA, (40, 40, 40), caja_texto, border_radius=8)
        pygame.draw.rect(VENTANA, "white", caja_texto, width=2, border_radius=8)

        txt_nombre = FUENTE_BOTON.render(nombre_jugador + "_", True, "cyan")
        VENTANA.blit(txt_nombre, txt_nombre.get_rect(center=caja_texto.center))

    pygame.display.update()

pygame.quit()
quit()