import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Experimento de Monty Hall")

# Colores y fuentes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

# Propiedades de las puertas
door_width = 150
door_height = 300
door_gap = 50

# Calcular posiciones de las 3 puertas
door_positions = []
start_x = (WIDTH - (3 * door_width + 2 * door_gap)) // 2
y = (HEIGHT - door_height) // 2
for i in range(3):
    x = start_x + i * (door_width + door_gap)
    door_positions.append(pygame.Rect(x, y, door_width, door_height))

# Botones para la decisión de cambiar o mantener
button_switch = pygame.Rect(WIDTH // 4 - 75, HEIGHT - 100, 150, 50)
button_stay = pygame.Rect(3 * WIDTH // 4 - 75, HEIGHT - 100, 150, 50)

# Estados del juego:
# "waiting_choice": esperando que el jugador elija una puerta.
# "switch_choice": se ha revelado una puerta y se pregunta si se quiere cambiar.
# "result": se muestran los resultados.
state = "waiting_choice"
player_choice = None
prize_door = None
host_opened = None
final_choice = None

def reset_game():
    global state, player_choice, prize_door, host_opened, final_choice
    state = "waiting_choice"
    player_choice = None
    prize_door = random.randint(0, 2)
    host_opened = None
    final_choice = None

reset_game()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if state == "waiting_choice":
                # El jugador elige una puerta
                for i, door_rect in enumerate(door_positions):
                    if door_rect.collidepoint(mouse_pos):
                        player_choice = i
                        # El presentador revela una puerta que no es la elegida ni tiene el premio.
                        posibles = [d for d in range(3) if d != player_choice and d != prize_door]
                        if player_choice == prize_door:
                            host_opened = random.choice(posibles)
                        else:
                            host_opened = posibles[0]
                        state = "switch_choice"
                        break
            elif state == "switch_choice":
                # El jugador decide si cambiar o no usando los botones
                if button_switch.collidepoint(mouse_pos):
                    final_choice = [d for d in range(3) if d not in (player_choice, host_opened)][0]
                    state = "result"
                elif button_stay.collidepoint(mouse_pos):
                    final_choice = player_choice
                    state = "result"
            elif state == "result":
                # Cualquier clic reinicia el juego
                reset_game()

    # Dibujo de la pantalla
    screen.fill(WHITE)
    
    # Mensajes según el estado
    if state == "waiting_choice":
        text = big_font.render("Elige una puerta", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    elif state == "switch_choice":
        text = big_font.render("¿Quieres cambiar?", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    elif state == "result":
        if final_choice == prize_door:
            outcome_text = "¡Ganaste!"
            outcome_color = GREEN
        else:
            outcome_text = "Perdiste..."
            outcome_color = RED
        text = big_font.render(outcome_text, True, outcome_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
        subtext = font.render("Haz clic para jugar de nuevo", True, BLACK)
        screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, 100))
    
    # Dibujar las puertas
    for i, door_rect in enumerate(door_positions):
        door_color = GRAY
        # Si la puerta fue abierta por el presentador, se muestra como abierta
        if state in ("switch_choice", "result") and i == host_opened:
            door_color = WHITE
        pygame.draw.rect(screen, door_color, door_rect)
        pygame.draw.rect(screen, BLACK, door_rect, 3)
        label = font.render(f"Puerta {i+1}", True, BLACK)
        screen.blit(label, (door_rect.centerx - label.get_width() // 2, door_rect.bottom + 5))
        
        # Durante el estado "result", se revela lo que hay detrás de las puertas
        if state == "result":
            if i == final_choice or i == host_opened:
                contenido = "Premio" if i == prize_door else "Cabra"
                reveal = font.render(contenido, True, BLUE)
                screen.blit(reveal, (door_rect.centerx - reveal.get_width() // 2, door_rect.centery - reveal.get_height() // 2))
        elif state == "switch_choice" and i == host_opened:
            # Se marca la puerta abierta
            reveal = font.render("Abierta", True, BLUE)
            screen.blit(reveal, (door_rect.centerx - reveal.get_width() // 2, door_rect.centery - reveal.get_height() // 2))
    
    # Resaltar la elección inicial del jugador
    if player_choice is not None:
        pygame.draw.rect(screen, YELLOW, door_positions[player_choice], 5)
    
    # En el estado de decisión se muestran los botones para cambiar o mantener
    if state == "switch_choice":
        pygame.draw.rect(screen, GREEN, button_switch)
        switch_text = font.render("Cambiar", True, BLACK)
        screen.blit(switch_text, (button_switch.centerx - switch_text.get_width() // 2,
                                  button_switch.centery - switch_text.get_height() // 2))
        pygame.draw.rect(screen, RED, button_stay)
        stay_text = font.render("Mantener", True, BLACK)
        screen.blit(stay_text, (button_stay.centerx - stay_text.get_width() // 2,
                                button_stay.centery - stay_text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
