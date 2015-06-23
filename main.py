
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
DISPLAY_INFO = pygame.display.Info()

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
SNAKE_SPEED = 2


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
        return Box(randint(0, DISPLAY_INFO.current_w), randint(0, DISPLAY_INFO.current_h), COLOR_BLACK)


class Snake(list):

    def __init__(self, x, y):
        super().__init__()

        self.append(Box(x, y, COLOR_SNAKE))

        # Store the directions
        self.direction = None
        self.last_direction = None

        # Store the box to eat
        self.to_eat = Box.generate_random()

        self.frame_count = 0

    def draw(self, surface):

        box = self[0]
        box.draw(surface)

        x = box.x
        y = box.y

        for box in self[1:]:
            if self.last_direction == pygame.K_LEFT:

                if self.direction == pygame.K_UP:
                    box.x = x
                    box.y = y + BOX_SIZE

            box.draw(surface)

        if self.frame_count == len(self):
            self.frame_count = 0

        """for i in range(0, len(self)):
            box = self[i]
            x = box.x
            y = box.y

            if self.direction == pygame.K_LEFT:
                x += BOX_SIZE * i

            elif self.direction == pygame.K_RIGHT:
                x -= BOX_SIZE * i

            elif self.direction == pygame.K_UP:
                y += BOX_SIZE * i

            elif self.direction == pygame.K_DOWN:
                y -= BOX_SIZE * i

            box.draw(surface, x, y)"""

    def handle_direction(self):
        """Changes the direction according to LEFT, RIGHT, UP and DOWN keys pressed."""
        # Has the player decided yet?
        if self.direction is None:

            # If not, don't go any further
            return

        # If yes, handle the keys pressed...
        box = self[0]

        if self.direction == pygame.K_LEFT:
            box.x -= SNAKE_SPEED

        elif self.direction == pygame.K_RIGHT:
            box.x += SNAKE_SPEED

        elif self.direction == pygame.K_UP:
            box.y -= SNAKE_SPEED

        elif self.direction == pygame.K_DOWN:
            box.y += SNAKE_SPEED

    def hit_wall(self):
        """Returns whether the snake has hit any wall."""
        # Grab the first box
        box = self[0]

        # Check coordinates and return whether the head hits the wall
        return box.x <= -box.width or box.x >= DISPLAY_INFO.current_w \
            or box.y <= -box.height or box.y >= DISPLAY_INFO.current_h

    def hit_box(self):
        """Returns whether the snake has hit the box to eat."""
        # Grab the first box
        box = self[0]

        # Call the other box's hit() method
        return self.to_eat.hit(box.x, box.y)


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

        # Get the first box
        box = snake[0]

        # Append a box to the snake's tail
        snake.append(Box(box.x, box.y, COLOR_SNAKE))

        # Generate another box for the snake
        snake.to_eat = Box.generate_random()

    # Set a white background
    surface.fill(COLOR_WHITE)

    # Draw the snake with its tail (reddish box)
    snake.draw(surface)

    # Draw the box to eat (black box)
    pygame.draw.rect(surface, COLOR_BLACK, (snake.to_eat.x, snake.to_eat.y, BOX_SIZE, BOX_SIZE))

    # Don't quit the main loop
    return True


def game_start():
    """Configure PyGame and start the main loop."""
    # Set a caption
    pygame.display.set_caption('Snake')

    # Get the display's surface
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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
