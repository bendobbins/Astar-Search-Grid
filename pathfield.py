import pygame
import sys
# Initiate pygame
pygame.init()
pygame.font.init()

from textinput import Input
from Astar import handle_input, shortest_path

# Sizing constants
WINDOWWIDTH = 700
WINDOWHEIGHT = 775
BOXSIZE = 11
FIELDSIZE = 50
GAP = 2
XMARGIN = 25
YMARGIN = 40

# Style constants
WHITE = (255, 255, 255)
LIGHTGREY = (225, 225, 225)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BUTTONFONT = pygame.font.SysFont("Courier", 16)
SMALLFONT = pygame.font.SysFont("Courier", 13)

# Set mode for display
DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def draw_field(clicked, endpoints, path):
    """
    Draws the boxes for the GUI grid.

    clicked -- Boxes that should be walls (black)
    endpoints -- Boxes that should be blue
    path -- Boxes that should be green
    """
    for box_x in range(FIELDSIZE):
        for box_y in range(FIELDSIZE):
            left, top = get_box_placement(box_x, box_y)
            if (box_x, box_y) not in clicked:
                pygame.draw.rect(DISPLAY, LIGHTGREY, (left, top, BOXSIZE, BOXSIZE))
            if (box_x, box_y) in endpoints:
                pygame.draw.rect(DISPLAY, BLUE, (left, top, BOXSIZE, BOXSIZE))
            if (box_x, box_y) in path:
                pygame.draw.rect(DISPLAY, GREEN, (left, top, BOXSIZE, BOXSIZE))
                


def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = XMARGIN + (BOXSIZE + GAP) * x
    top = YMARGIN + (BOXSIZE + GAP) * y
    return left, top


def draw_buttons():
    """
    Draw buttons that reset input and submit input for pathfinding. Return their collision boxes to check for mouse clicks.
    """
    widths = [30, WINDOWWIDTH - 130]
    phrases = ["Reset", "Find Path"]
    buttons = []

    for i in range(2):
        button = pygame.Rect(widths[i], WINDOWHEIGHT - 70, 100, 40)
        text = BUTTONFONT.render(phrases[i], True, BLACK)
        rect = text.get_rect()
        rect.center = button.center
        pygame.draw.rect(DISPLAY, LIGHTGREY, button)
        DISPLAY.blit(text, rect)
        buttons.append(button)

    return buttons


def draw_text(error):
    """
    Draw all text in window, including error message if parameter != 0.
    """
    phrases = [     # Text phrases for different parts of the screen
        "Click boxes to create walls! The algorithm will then find the",
        "shortest path around the walls from your start to your end!",
        "Input your endpoints in this format: (x, y)",
        "start: ",
        "end: ",
        "1",
        "1",
        "50",
        "50",
        "Input endpoints in valid format" if error == 1 else "Endpoints are the same or in a wall"      # Different error message if error is 1 or 2
        ]

    centers = [     # Centers of text rects
        (WINDOWWIDTH / 2, 13),
        (WINDOWWIDTH / 2, 28),
        (WINDOWWIDTH / 2, WINDOWHEIGHT - 70),
        (195, WINDOWHEIGHT - 38),
        (400, WINDOWHEIGHT - 38),
        (17, 46),
        (30, 32),
        (WINDOWWIDTH - 17, WINDOWHEIGHT - 92),
        (WINDOWWIDTH - 33, WINDOWHEIGHT - 79),
        (WINDOWWIDTH / 2, WINDOWHEIGHT - 13)
        ]

    for i in range(10) if error else range(9):      # Only draw error if parameter != 0
        newText = SMALLFONT.render(phrases[i], True, LIGHTGREY if i < 9 else RED)       # Error message in red, all else in grey
        newRect = newText.get_rect()
        newRect.center = centers[i]
        DISPLAY.blit(newText, newRect)


def draw_inputs():
    """
    Draw input boxes, return the classes for the boxes.
    """
    input1 = Input(220, WINDOWHEIGHT - 50, 100, 25)
    input2 = Input(420, WINDOWHEIGHT - 50, 100, 25)
    return [input1, input2]


def find_clicked_box(mouse):
    """
    Check if a box has been clicked based on whether its collision rect intersects with mouse coordinates.
    """
    for box_x in range(FIELDSIZE):
        for box_y in range(FIELDSIZE):
            left, top = get_box_placement(box_x, box_y)
            boxSpace = pygame.Rect(left, top, BOXSIZE + GAP, BOXSIZE + GAP)     # Add gap into collision box for some cushion
            if boxSpace.collidepoint(mouse):
                return (box_x, box_y)
    return (None, None)


def pg_events(clickedBoxes, endpoints, error, inputs, buttons, path):
    """
    Handle any pygame events that occur. Return values that could be influenced by events.

    clickedBoxes -- Set of boxes that have been clicked (walls)
    endpoints -- List of 2 tuples, one startpoint and one endpoint
    error -- 0, 1 or 2 depending on input from user
    inputs -- List of input boxes
    buttons -- List of button collision boxes
    path -- Path that algorithm found from start to finish (empty if no path yet)
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Reset button clicked
            if buttons[0].collidepoint(event.pos):
                error = 0
                endpoints = []
                path = []
                clickedBoxes = set()
                inputs = draw_inputs()

            # Find path button clicked
            if buttons[1].collidepoint(event.pos):
                error = 0
                endpoints = handle_input((inputs[0].text, inputs[1].text))

                if len(endpoints) == 2:
                    # Condition to handle if endpoints are same or in a wall
                    if endpoints[0] == endpoints[1] or endpoints[0] in clickedBoxes or endpoints[1] in clickedBoxes:
                        error = 2
                        endpoints = []
                        continue
                    # Find path if endpoints are valid
                    path = shortest_path(clickedBoxes, *endpoints)
                
                # If invalid input for endpoints
                else:
                    endpoints = []
                    error = 1

        # Handle keystrokes or clicking for input boxes
        for inp in inputs:
            inp.handle_event(event)

    return clickedBoxes, endpoints, error, inputs, path



def main():
    """
    Main function that controls GUI.
    """
    clickedBoxes = set()
    endpoints = []
    path = []
    error = 0
    pygame.display.set_caption("Shortest path")
    inputs = draw_inputs()

    while True:
        # Draw window
        DISPLAY.fill(BLACK)
        pygame.draw.rect(DISPLAY, BLACK, (XMARGIN, YMARGIN, (BOXSIZE + GAP) * FIELDSIZE, (BOXSIZE + GAP) * FIELDSIZE))

        # Draw components
        draw_text(error)
        buttons = draw_buttons()
        draw_field(clickedBoxes, endpoints, path)

        # Handle events
        clickedBoxes, endpoints, error, inputs, path = pg_events(clickedBoxes, endpoints, error, inputs, buttons, path)

        for inp in inputs:
            inp.draw(DISPLAY)

        # Handle grid boxes being clicked (Different from pg_events because mouse can be held down with get_pressed)
        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            clickedBox = find_clicked_box(mouse)
            if clickedBox[0] is not None:
                clickedBoxes.add(clickedBox)

        pygame.display.update()


if __name__ == "__main__":
    main()