import time
import numpy as np
import pygame


class GameOfLife:
    def __init__(self, width, height, cell_size, grid=None):
        pygame.init()
        self.board_size = (self.width, self.height) = (width, height)
        self.dead_cell_color = (0, 0, 0)
        self.live_cell_color = (255, 255, 255)
        self.cell_size = cell_size
        self.rows = self.height//self.cell_size
        self.columns = self.width//self.cell_size
        self.grid_size = (self.rows, self.columns)
        self.screen = pygame.display.set_mode(self.board_size)
        self.screen.fill(self.dead_cell_color)
        self.grid = grid
        self.randomize_grid()
        pygame.display.flip()

    def randomize_grid(self):
        if not self.grid:
            self.grid = np.random.choice(a=(0, 1), size=self.grid_size, replace=True, p=(0.50, 0.50))

    def calculate_live_neighbors(self, i, j):
        temp_sum = 0
        if i == 0 and j == 0:
            temp_sum += self.grid[i + 1][j]
            temp_sum += self.grid[i][j + 1]
            temp_sum += self.grid[i + 1][j + 1]
        elif i == 0 and j == self.columns - 1:
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i + 1][j - 1]
            temp_sum += self.grid[i + 1][j]
        elif i == self.rows - 1 and j == 0:
            temp_sum += self.grid[i - 1][j]
            temp_sum += self.grid[i - 1][j + 1]
            temp_sum += self.grid[i][j + 1]
        elif i == self.rows - 1 and j == self.columns - 1:
            temp_sum += self.grid[i - 1][j - 1]
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i - 1][j]
        elif i == 0:
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i + 1][j - 1]
            temp_sum += self.grid[i + 1][j]
            temp_sum += self.grid[i][j + 1]
            temp_sum += self.grid[i + 1][j + 1]
        elif i == self.rows - 1:
            temp_sum += self.grid[i - 1][j - 1]
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i - 1][j]
            temp_sum += self.grid[i - 1][j + 1]
            temp_sum += self.grid[i][j + 1]
        elif j == 0:
            temp_sum += self.grid[i - 1][j]
            temp_sum += self.grid[i + 1][j]
            temp_sum += self.grid[i - 1][j + 1]
            temp_sum += self.grid[i][j + 1]
            temp_sum += self.grid[i + 1][j + 1]
        elif j == self.columns - 1:
            temp_sum += self.grid[i - 1][j - 1]
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i + 1][j - 1]
            temp_sum += self.grid[i - 1][j]
            temp_sum += self.grid[i + 1][j]
        else:
            temp_sum += self.grid[i - 1][j - 1]
            temp_sum += self.grid[i][j - 1]
            temp_sum += self.grid[i + 1][j - 1]
            temp_sum += self.grid[i - 1][j]
            temp_sum += self.grid[i + 1][j]
            temp_sum += self.grid[i - 1][j + 1]
            temp_sum += self.grid[i][j + 1]
            temp_sum += self.grid[i + 1][j + 1]
        return temp_sum

    def update_generation(self):
        new_generation = np.zeros(shape=self.grid_size)
        for i in range(self.rows):
            for j in range(self.columns):
                neighbors = self.calculate_live_neighbors(i, j)
                if self.grid[i][j] == 0 and neighbors == 3:
                    new_generation[i][j] = 1
                elif self.grid[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                    new_generation[i][j] = 0
                else:
                    new_generation[i][j] = self.grid[i][j]
        self.grid = new_generation

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, self.live_cell_color, (j*self.cell_size, i*self.cell_size,
                                                                         self.cell_size-1, self.cell_size-1))
                else:
                    pygame.draw.rect(self.screen, self.dead_cell_color, (j*self.cell_size, i*self.cell_size,
                                                                         self.cell_size-1, self.cell_size-1))
        pygame.display.flip()

    def run(self):
        paused = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_p:
                        paused = not paused
            if not paused:
                self.draw_grid()
                self.update_generation()
                time.sleep(0)


if __name__ == '__main__':
    GameOfLife(1000, 500, 5).run()
