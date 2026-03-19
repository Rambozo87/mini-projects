import pygame

pygame.init()
window_width = 1920
window_height = 1080
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0

cell_size = 8
cell_data = [[[0] * 240] * 135]

def main():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #######

        screen.fill((25, 25, 35))

        for i in range(round(window_width / cell_size) + 1):
            x = round(cell_size * i)

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (x, 0),
                (x, 1080),
                2,
            )

        for i in range(round(window_height / cell_size) + 1):
            y = round(cell_size * i)

            pygame.draw.line(
                screen,
                (215, 215, 205),
                (0, y),
                (1920, y),
                2,
            )

        pygame.display.flip()

        #######

        dt = clock.tick(60) / 1000

    pygame.quit()


def mouse_to_col()
    x = pygame.mouse.get_pos()[0]
    return round(x/cell_size)

def mouse_to_row()
    y = pygame.mouse.get_pos()[1]
