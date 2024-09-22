import pygame


class Box:
    COLOR_BLACK = (0, 0, 0)
    COLOR_BLUE = (52, 31, 151)
    COLOR_RED = (255, 0, 0)

    def __init__(self, val, row, col):
        self.value = val  # Current box value
        self.row = row
        self.col = col
        self.selected = False  # To mark whether this box is selected

    # To draw this box
    def draw(self, screen, original):
        font = pygame.font.SysFont('Comic Sans MS', 35)
        gap = 50

        # Calculate drawing position relative to this box in board
        x = (self.col + 1) * gap
        y = (self.row + 1) * gap

        num_color = self.COLOR_BLACK
        if original is True:
            num_color = self.COLOR_BLUE
        if self.value != 0:
            text = font.render(str(self.value), True, num_color)
            screen.blit(text, (x + 15, y))  # Draw number in the middle

        if self.selected:
            pygame.draw.rect(screen, self.COLOR_RED, (x, y, gap + 4, gap + 4), 4)  # If this box selected, draw red box

    def set(self, val):
        self.value = val
