
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


# ================================================
# >> CONSTANTS
# ================================================
# Window size
WINDOW_SIZE = (1024, 768)

# Store colors
COLOR_BLACK = (0, 0, 0)
COLOR_SNAKE = (170, 60, 0)
COLOR_WHITE = (255, 255, 255)

# Store the size of a box
BOX_SIZE = 10

# Store the starting speed of the snake
SNAKE_SPEED = 3


# ================================================
# >> CLASSES
# ================================================
class Box(object):

    """Stores information about a box and handles hit events."""

    def __init__(self, x, y):
        """Called on instantiation."""
        # Store X and Y coordinates
        self.x = x
        self.y = y

        # Store width and height
        self.width = BOX_SIZE
        self.height = BOX_SIZE

    def hit(self, x, y):
        """Returns whether the two coordinates hit this box."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    @property
    def min_x(self):
        """Returns the smalles X coordinate."""
        return self.x - self.width

    @property
    def max_x(self):
        """Returns the largest X coordinate."""
        return self.x + self.width

    @property
    def min_y(self):
        """Returns the smalles Y coordinate."""
        return self.y - self.height

    @property
    def max_y(self):
        """Returns the largest Y coordinate."""
        return self.y + self.height


class Snake(Box):

    """Adds Snake logic to a box."""

    def __init__(self, x, y):
        """Called on instantiation."""
        # Call Box's constructor
        super().__init__(x, y)

        # Store the direction
        self.direction = None

        # Store the speed
        self.speed = SNAKE_SPEED

        # Store the box to eat
        self.to_eat = Box(randint(0, WINDOW_SIZE[0]), randint(0, WINDOW_SIZE[1]))

    def handle_movement(self):
        """Changes the direction according to LEFT, RIGHT, UP and DOWN keys pressed."""
        # Has the player decided yet?
        if self.direction is None:

            # If not, don't go any further
            return

        # If yes, handle the LEFT key...
        if self.direction == pygame.K_LEFT:
            self.x -= self.speed

        # ... the RIGHT key...
        elif self.direction == pygame.K_RIGHT:
            self.x += self.speed

        # ... the UP key...
        elif self.direction == pygame.K_UP:
            self.y -= self.speed

        # ... the DOWN key...
        elif self.direction == pygame.K_DOWN:
            self.y += self.speed

    def hit_wall(self):
        """Returns whether the snake has hit any wall."""
        return self.x <= -self.width or self.x >= WINDOW_SIZE[0] or self.y <= -self.height or self.y >= WINDOW_SIZE[1]

    def hit_box(self):
        """Returns whether the snake has hit the other box."""
        return self.to_eat.hit(self.x, self.y)


# ================================================
# >> FUNCTIONS
# ================================================
def game_on(surface, snake):
    """The game's main loop."""
    # Handle events...
    for event in pygame.event.get():

        # Quit the main loop?
        if event.type == pygame.QUIT:
            return False

        # Was a key pressed?
        if event.type == pygame.KEYDOWN:

            # If yes, set the direction to move the snake
            snake.direction = event.key

    # Handle the snake's movement
    snake.handle_movement()

    # Did we hit any wall?
    if snake.hit_wall():

        # If yes, quit the game
        return False

    # Did we hit another box?
    if snake.hit_box():

        # If yes, speed up the snake by 1
        snake.speed += 1

        # And generate another box for the snake
        snake.to_eat = Box(randint(0, WINDOW_SIZE[0]), randint(0, WINDOW_SIZE[1]))

    # Set a white background
    surface.fill(COLOR_WHITE)

    # Draw the snake (reddish box)
    pygame.draw.rect(surface, COLOR_SNAKE, (snake.x, snake.y, snake.width, snake.height))

    # Draw the box to eat (black box)
    pygame.draw.rect(surface, COLOR_BLACK, (snake.to_eat.x, snake.to_eat.y, BOX_SIZE, BOX_SIZE))

    # Don't quit the main loop
    return True


def game_start():
    """Initialize PyGame and start the main loop."""
    # Initialize PyGame
    pygame.init()

    # Set a caption
    pygame.display.set_caption('Snake')

    # Get the display's surface
    surface = pygame.display.set_mode(WINDOW_SIZE)

    # Get a Snake object
    snake = Snake(300, 300)

    # Update the display while the game is running...
    while game_on(surface, snake):
        pygame.display.update()

    # Quit PyGame
    pygame.quit()

    # Quit Python
    quit()


# Was this file imported?
if __name__ == '__main__':

    # If not, start the game!
    game_start()
