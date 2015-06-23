
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
#   Display
from pygame import display
#   Event
from pygame import event as events
#   Draw
from pygame.draw import rect
#   Font
from pygame.font import Font

# Initialize PyGame
pygame.init()


# ================================================
# >> CONSTANTS
# ================================================
# Store display info
_display_info = pygame.display.Info()

if _display_info.current_w > 1248:
    DISPLAY_WIDTH = 1248
else:
    DISPLAY_WIDTH = _display_info.current_w

if _display_info.current_h > 768:
    DISPLAY_HEIGHT = 768
else:
    DISPLAY_HEIGHT = _display_info.current_h

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

        # Store the color
        self.color = color

        # Store an indicator if it already hit the last vector
        self.move_accordingly = False

    def hit(self, x, y):
        """Returns whether the two coordinates hit this box."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def draw(self, surface):
        """Draws the box on the surface."""
        rect(surface, self.color, (self.x, self.y, BOX_SIZE, BOX_SIZE))

    @property
    def min_x(self):
        """Returns the smallest X coordinate."""
        return self.x - BOX_SIZE

    @property
    def max_x(self):
        """Returns the largest X coordinate."""
        return self.x + BOX_SIZE

    @property
    def min_y(self):
        """Returns the smallest Y coordinate."""
        return self.y - BOX_SIZE

    @property
    def max_y(self):
        """Returns the largest Y coordinate."""
        return self.y + BOX_SIZE

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

        self.last_vector = None

        # Store the tail
        self.tail = list()

        # Store the box to eat
        self.to_eat = Box.generate_random()

    def draw(self, surface):
        """Draws the snake with its tail to the surface."""
        # First, draw this box
        super().draw(surface)

        # Draw the tail...
        for box in self.tail:

            # Generate a size
            size = (self.tail.index(box) + 1) * BOX_SIZE

            # TODO: get this to work..
            if box.move_accordingly:

                if self.direction == pygame.K_LEFT:
                    box.x = self.x + size
                    box.y = self.y

                elif self.direction == pygame.K_RIGHT:
                    box.x = self.x - size
                    box.y = self.y

                elif self.direction == pygame.K_UP:
                    box.x = self.x
                    box.y = self.y + size

                elif self.direction == pygame.K_DOWN:
                    box.x = self.x
                    box.y = self.y - size

            else:

                if self.direction == pygame.K_LEFT:

                    if self.last_direction == pygame.K_UP:
                        y = self.y + size
                    else:
                        y = self.y - size

                    if (box.x, y) == self.last_vector:
                        box.y = y
                        box.move_accordingly = True

                elif self.direction == pygame.K_RIGHT:

                    if self.last_direction == pygame.K_UP:
                        y = self.y + size
                    else:
                        y = self.y - size

                    if (box.x, y) == self.last_vector:
                        box.y = y
                        box.move_accordingly = True

                elif self.direction == pygame.K_UP:

                    if self.last_direction == pygame.K_LEFT:
                        x = self.x - size
                    else:
                        x = self.x + size

                    if (x, box.y) == self.last_vector:
                        box.x = x
                        box.move_accordingly = True

                else:

                    if self.last_direction == pygame.K_LEFT:
                        x = self.x + size
                    else:
                        x = self.x - size

                    if (x, box.y) == self.last_vector:
                        box.x = x
                        box.move_accordingly = True

            # Draw the box to the surface
            box.draw(surface)

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
        return self.x <= -BOX_SIZE or self.x >= DISPLAY_WIDTH \
            or self.y <= -BOX_SIZE or self.y >= DISPLAY_HEIGHT

    def hit_box(self):
        """Returns whether the snake has hit the box to eat."""
        return self.to_eat.hit(self.x, self.y)


# ================================================
# >> FUNCTIONS
# ================================================
def game_on(surface, font, snake):
    """The game's main loop."""
    # Handle events...
    for event in events.get():

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

                # If yes, was an opposite key or the same key as last time pressed?
                if snake.direction != OPPOSITE_KEYS[event.key] and snake.direction != event.key:

                    # If no, change the snake's direction values
                    snake.last_direction = snake.direction
                    snake.direction = event.key
                    snake.last_vector = (snake.x, snake.y)

                    for box in snake.tail:
                        box.move_accordingly = False

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
    snake.draw(surface)

    # Draw the box to eat (black box)
    snake.to_eat.draw(surface)

    # Render a font surface
    text = font.render('SCORE: {0}'.format(len(snake.tail)), 1, COLOR_BLACK)

    # Gets its current position
    pos = text.get_rect()

    # Change X and Y coordinates to top-left
    pos.centerx = 50
    pos.centery += 20

    # Draw the scoreboard to the surface
    surface.blit(text, pos)

    # Don't quit the main loop
    return True


def game_start():
    """Configure PyGame and start the main loop."""
    # Set a caption
    display.set_caption('Snake')

    # Create a font
    font = Font(None, 20)

    # Get the display's surface
    surface = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # Get a Snake object
    snake = Snake(300, 300)

    # Update the display while the game is running...
    while game_on(surface, font, snake):
        display.update()

    # Quit PyGame
    pygame.quit()

    # Quit Python
    quit()


# Was this file imported?
if __name__ == '__main__':

    # If not, start the game!
    game_start()
