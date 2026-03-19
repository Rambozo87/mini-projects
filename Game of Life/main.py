import pygame

pygame.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)
window_width = 1920
window_height = 1080
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
dt = 0

cell_size = 70

rows = window_height // cell_size
cols = window_width // cell_size

cell_data = [[0 for _ in range(cols)] for _ in range(rows)]


generation = 0
population = 0


def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            cell_data[mouse_to_row()][mouse_to_col()] = 1
        if pygame.mouse.get_pressed()[2]:
            cell_data[mouse_to_row()][mouse_to_col()] = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            update_cells()

        draw_grid()
        draw_cells()

        generation_counter = my_font.render(
            f"Generation: {generation}", False, (210, 185, 150)
        )
        pop_counter = my_font.render(
            f"Population: {population}", False, (210, 185, 150)
        )
        screen.blit(generation_counter, (50, 50))
        screen.blit(pop_counter, (50, 80))

        pygame.display.update()

        dt = clock.tick(10) / 1000

    pygame.quit()


def draw_grid():
    screen.fill((25, 25, 35))

    for i in range(cols + 1):
        x = i * cell_size
        pygame.draw.line(screen, (115, 115, 105), (x, 0), (x, 1080), 2)

    for i in range(rows + 1):
        y = i * cell_size
        pygame.draw.line(screen, (115, 115, 105), (0, y), (1920, y), 2)


def mouse_to_col():
    return min(pygame.mouse.get_pos()[0] // cell_size, cols - 1)


def mouse_to_row():
    return min(pygame.mouse.get_pos()[1] // cell_size, rows - 1)


def draw_cells():
    global population
    population_counter = 0

    for i in range(rows):
        for j in range(cols):
            alive = cell_data[i][j]
            if alive:
                population_counter += 1
            color = (175, 175, 165) if alive else (25, 25, 35)

            pygame.draw.rect(
                screen,
                color,
                (
                    j * cell_size + 2,
                    i * cell_size + 2,
                    cell_size - 2,
                    cell_size - 2,
                ),
            )

    population = population_counter


def update_cells():
    global cell_data, generation, population

    new_data = [[0 for _ in range(cols)] for _ in range(rows)]
    population_counter = 0

    for i in range(rows):
        for j in range(cols):
            alive = cell_data[i][j]
            neighbours = 0

            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue

                    ni = i + di
                    nj = j + dj

                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbours += cell_data[ni][nj]

            if alive:
                new_data[i][j] = 1 if neighbours in (2, 3) else 0
            else:
                new_data[i][j] = 1 if neighbours == 3 else 0

            if new_data[i][j] == 1:
                population_counter += 1

    cell_data = new_data
    generation += 1
    population = population_counter


main()
