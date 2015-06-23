
"""Snake game written in PyGame (Python 3)"""


# ================================================
# >> IMPORTS
# ================================================
# Python Imports
#   Random
from random import randint

# PyGame Imports
#   Core
import pygame


# Initialize PyGame
pygame.init()


# ================================================
# >> CONSTANTS
# ================================================
# Store display info
_DISPLAY_INFO = pygame.display.Info()
DISPLAY_WIDTH = _DISPLAY_INFO.current_w
DISPLAY_HEIGHT = _DISPLAY_INFO.current_h

if DISPLAY_WIDTH > 1024 and DISPLAY_HEIGHT > 768:
    DISPLAY_FLAGS = 0
else:
    DISPLAY_FLAGS = pygame.FULLSCREEN

# Store opposite keys
OPPOSITE_KEYS = {
    pygame.K_RIGHT: pygame.K_LEFT,
    pygame.K_LEFT: pygame.K_RIGHT,
    pygame.K_UP: pygame.K_DOWN,
    pygame.K_DOWN: pygame.K_UP
}

# Store colors
COLOR_BLACK = (0, 0, 0)
COLOR_SNAKE = (170, 60, 0)
COLOR_WHITE = (255, 255, 255)

# Store the size of a box
BOX_SIZE = 10

# Store the snake's speed
SNAKE_SPEED = 3


# ================================================
# >> CLASSES
# ================================================
class Box(object):

    """Stores information about a box and handles hit events."""

    def __init__(self, x, y, color):
        """Called on instantiation."""
        # Store X and Y coordinates
        self.x = x
        self.y = y

        # Store width and height
        self.width = BOX_SIZE
        self.height = BOX_SIZE

        # Store the color
        self.color = color

    def hit(self, x, y):
        """Returns whether the two coordinates hit this box."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def draw(self, surface):
        """Draws the box on the surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, BOX_SIZE, BOX_SIZE))

    @property
    def min_x(self):
        """Returns the smallest X coordinate."""
        return self.x - self.width

    @property
    def max_x(self):
        """Returns the largest X coordinate."""
        return self.x + self.width

    @property
    def min_y(self):
        """Returns the smallest Y coordinate."""
        return self.y - self.height

    @property
    def max_y(self):
        """Returns the largest Y coordinate."""
        return self.y + self.height

    @staticmethod
    def generate_random():
        """Returns a random box."""
        return Box(randint(0, DISPLAY_WIDTH), randint(0, DISPLAY_HEIGHT), COLOR_BLACK)


class Snake(Box):

    """Adds snake logic to a box."""

    def __init__(self, x, y):
        """Called on instantiation."""
        # Call Box's constructor
        super().__init__(x, y, COLOR_SNAKE)

        # Store the directions
        self.direction = None
        self.last_direction = None

        # Store the box to eat
        self.to_eat = Box.generate_random()

        # Store the tail
        self.tail = list()

    def draw(self, surface, font):
        """Draws the snake with its tail to the surface."""
        # First, draw the box of the snake
        super().draw(surface)

        # Draw the tail...
        for box in self.tail:

            # Get the box's index
            index = self.tail.index(box) + 1

            # Handle the box's coordinates according to the snake's direction...
            if self.direction == pygame.K_LEFT:
                box.x = self.x + BOX_SIZE * index
                box.y = self.y

            elif self.direction == pygame.K_RIGHT:
                box.x = self.x - BOX_SIZE * index
                box.y = self.y

            elif self.direction == pygame.K_UP:
                box.x = self.x
                box.y = self.y + BOX_SIZE * index

            elif self.direction == pygame.K_DOWN:
                box.x = self.x
                box.y = self.y - BOX_SIZE * index

            # Draw the box to the surface
            box.draw(surface)

        # Draw the scoreboard
        text = font.render('SCORE: {0}'.format(len(self.tail)), 1, COLOR_BLACK)
        pos = text.get_rect()
        pos.centerx = 50
        pos.centery += 20

        surface.blit(text, pos)

    def handle_direction(self):
        """Changes the direction according to LEFT, RIGHT, UP and DOWN keys pressed."""
        # Has the player decided yet?
        if self.direction is None:

            # If not, don't go any further
            return

        # If yes, handle the keys pressed...
        if self.direction == pygame.K_LEFT:
            self.x -= SNAKE_SPEED

        elif self.direction == pygame.K_RIGHT:
            self.x += SNAKE_SPEED

        elif self.direction == pygame.K_UP:
            self.y -= SNAKE_SPEED

        elif self.direction == pygame.K_DOWN:
            self.y += SNAKE_SPEED

    def hit_wall(self):
        """Returns whether the snake has hit any wall."""
        return self.x <= -self.width or self.x >= DISPLAY_WIDTH \
            or self.y <= -self.height or self.y >= DISPLAY_HEIGHT

    def hit_box(self):
        """Returns whether the snake has hit the box to eat."""
        return self.to_eat.hit(self.x, self.y)


# ================================================
# >> FUNCTIONS
# ================================================
def game_on(surface, font, snake):
    """The game's main loop."""
    # Handle events...
    for event in pygame.event.get():

        # Quit the main loop?
        if event.type == pygame.QUIT:
            return False

        # Was a key pressed?
        if event.type == pygame.KEYDOWN:

            # Quit if ESC was pressed
            if event.key == pygame.K_ESCAPE:
                return False

            # Was LEFT, RIGHT, UP or DOWN pressed?
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_UP or event.key == pygame.K_DOWN:

                # If yes, change the snake's direction accordingly
                if snake.direction != OPPOSITE_KEYS[event.key]:
                    snake.last_direction = snake.direction
                    snake.direction = event.key

    # Handle the snake's direction changes
    snake.handle_direction()

    # Did we it any wall?
    if snake.hit_wall():

        # If yes, quit the game
        return False

    # Did it hit another box?
    if snake.hit_box():

        # Append a box to the snake's tail
        snake.tail.append(Box(snake.x, snake.y, COLOR_SNAKE))

        # Generate another box for the snake
        snake.to_eat = Box.generate_random()

    # Set a white background
    surface.fill(COLOR_WHITE)

    # Draw the snake with its tail (reddish box)
    snake.draw(surface, font)

    # Draw the box to eat (black box)
    pygame.draw.rect(surface, COLOR_BLACK, (snake.to_eat.x, snake.to_eat.y, BOX_SIZE, BOX_SIZE))

    # Don't quit the main loop
    return True


def game_start():
    """Configure PyGame and start the main loop."""
    # Set a caption
    pygame.display.set_caption('Snake')

    # Create a font
    font = pygame.font.Font(None, 20)

    # Get the display's surface
    surface = pygame.display.set_mode((0, 0) if not DISPLAY_FLAGS else (DISPLAY_WIDTH, DISPLAY_HEIGHT), DISPLAY_FLAGS)

    # Get a Snake object
    snake = Snake(300, 300)

    # Update the display while the game is running...
    while game_on(surface, font, snake):
        pygame.display.update()

    # Quit PyGame
    pygame.quit()

    # Quit Python
    quit()


# Was this file imported?
if __name__ == '__main__':

    # If not, start the game!
    game_start()
