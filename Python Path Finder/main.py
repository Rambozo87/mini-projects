from asyncio.windows_events import NULL
import pygame
import sys
import random

from pygame.constants import K_SPACE

sys.setrecursionlimit(500000)

# Directions for movement: (dx, dy)
DIRECTIONS = [
    (0, 2),  # North
    (0, -2), # South
    (2, 0),  # East
    (-2, 0)  # West
]

pygame.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)
window_width = 1920
window_height = 1080
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
clock = pygame.time.Clock()
dt = 0

cell_count = 13

cell_size = window_height//cell_count

cell_data = [[0 for _ in range(cell_count)] for _ in range(cell_count)]

bg = (15, 15, 15)
grid = (75, 75, 75)
fg = (115, 115, 115)

maze_path = None

def main():
    running = True

    maze_status = NULL

    generate_maze()

    start_time_ms = pygame.time.get_ticks()
    last_help_press = start_time_ms

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time_ms = pygame.time.get_ticks()
        elapsed_time_ms = current_time_ms - start_time_ms

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_h]:
            last_help_press = current_time_ms
        if keys[K_SPACE]:
            maze_status = crawler_driver()



        draw_cells()

        if(elapsed_time_ms - last_help_press < 2000):
            help_text = my_font.render("Press H for this Help Screen", False, (210, 185, 150))
            quit_text = my_font.render("To quit press Q or ESC", False, (210, 185, 150))
            screen.blit(help_text, (50, 50))
            screen.blit(quit_text, (50, 70))

        if(maze_status):
            maze_text = my_font.render(maze_status, False, (210, 185, 150))
            screen.blit(maze_text, (window_width/2, window_height/2))

        pygame.display.update()

def draw_cells():
    screen.fill((0,0,0))

    if window_width < window_height:
        x_offset = (window_height - window_width)/2
        y_offset = (window_width - cell_size*cell_count)/2
    elif window_width > window_height:
        x_offset = (window_width - window_height)/2
        y_offset = (window_height - cell_size*cell_count)/2
    else:
        x_offset = 0
        y_offset = 0

    for x, row in enumerate(cell_data):
        for y, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, fg, (x*cell_size+x_offset, y*cell_size+y_offset, cell_size, cell_size))
            if cell == 2:
                pygame.draw.rect(screen, (255,0,0), (x*cell_size+x_offset, y*cell_size+y_offset, cell_size, cell_size))
            if cell == -1:
                pygame.draw.rect(screen, (0,255,0), (x*cell_size+x_offset, y*cell_size+y_offset, cell_size, cell_size))

def is_valid(x, y):
    """Checks if coordinates are within the inner bounds (1 to cell_count-2)."""
    return 1 <= x < cell_count - 1 and 1 <= y < cell_count - 1

def generate_maze():
    # 1. Initialize all inner cells to WALL (1)
    for x in range(1, cell_count - 1):
        for y in range(1, cell_count - 1):
            cell_data[x][y] = 1

    # 2. Set the outer boundary to WALL (1) - Your initial logic
    for x, row in enumerate(cell_data):
        for y, cell in enumerate(row):
            if x == 0 or y == 0 or x == cell_count-1 or y == cell_count-1:
                cell_data[x][y] = 1

    # 3. Choose a random starting point for the algorithm
    # Start must be on an inner cell, typically an odd coordinate for a perfect maze.
    start_x = random.randrange(1, cell_count - 1, 2)
    start_y = random.randrange(1, cell_count - 1, 2)

    # Set the starting cell to PATH (0)
    cell_data[start_x][start_y] = 0

    # 4. Run the Recursive Backtracker Algorithm
    recursive_backtracker(start_x, start_y)

    # 5. Set the final START (-1) and FINISH (2) points

    # START (-1): Must be on the edge wall. We'll use the left wall (x=0)
    # We choose an inner y-coordinate that is even (ensures connection to the maze path)
    start_y_final = random.randrange(1, cell_count - 1, 2)
    cell_data[1][start_y_final] = -1 # Set the adjacent path to start
    cell_data[0][start_y_final] = 1 # Keep the boundary wall

    # FINISH (2): Must be on the edge wall, opposite side (x=cell_count-1).
    # We choose a different y-coordinate that is also odd.
    finish_y_final = random.randrange(1, cell_count - 1, 2)
    # Ensure start and finish are not too close or identical for a meaningful maze
    while abs(finish_y_final - start_y_final) < 2 and cell_count > 5:
         finish_y_final = random.randrange(1, cell_count - 1, 2)

    cell_data[cell_count - 2][finish_y_final] = 2 # Set the adjacent path to finish
    cell_data[cell_count - 1][finish_y_final] = 1 # Keep the boundary wall

def recursive_backtracker(cx, cy):
    """Depth-First Search (DFS) based maze generation."""

    # Shuffle the directions to ensure randomness
    random.shuffle(DIRECTIONS)

    for dx, dy in DIRECTIONS:
        nx, ny = cx + dx, cy + dy  # Next cell (2 steps away)
        wall_x, wall_y = cx + dx // 2, cy + dy // 2  # Wall between current and next cell

        if is_valid(nx, ny) and cell_data[nx][ny] == 1:
            # Found an unvisited wall cell

            # 1. Carve the path in the next cell
            cell_data[nx][ny] = 0

            # 2. Carve the wall between current and next cell
            cell_data[wall_x][wall_y] = 0

            # 3. Recursively call the function from the new cell
            recursive_backtracker(nx, ny)

def crawler_driver():
    crawler_pos = [0,0]

    return crawler(crawler_pos, 0, 0, 0)

def crawler(crawler_pos, distance_between_spots, open_spots, index):
# # This method recursively crawls through a maze by checking by first checking if any of the three spots are avaliable to go through.
#
# #open spots array will be a 6x* array, first two columns will be open paths position, the third colume will be which paths are open represented by a 4 bit number 0000
#   a 0 will represent open path and a 1 will represent a closed path. the bit order is like this: 1,0,0,1 -> north(closed), east(open), south(open), west(closed). It will also mark the path it just came from as closed. North being the top of the screen.
#
#
# case:
#   If two or three new open paths mark cell a open spot by adding it to the array then have the crawler take the lest most path from the crawlers point of view. Mark that patha seen(closed) and mark the other open paths as unseen(open)
# case:
#   If one only one new path is open move continue on it.
# case:
#   If no new paths are avliable move to the last open_spot with multiple paths on the list. If the open spot has all paths marks as closed, remove the sport from the
#   list and then move to the new last open sport on the list (Test efficieny by starting from beginning, middle, and end of list).
# case:
#   Reached end point which will be marked as a 2 in the maze array. The crawler will only know it has reach the end once it has made at that spot,
#   the crawler is only aware of the open paths and the last spots that had open paths
# case:
#   if crawler has reached an impass and there are no mark spots display bad maze message

main()
