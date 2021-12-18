# CREDIT TO skrx ON STACKOVERFLOW
# https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame


import pygame
from pygame.locals import *
pygame.init()

INPUTCOLOR = (150, 150, 150)
LIGHTGREY = (225, 225, 225)
SMALLFONT =pygame.font.SysFont("courier", 13)

class Input:
    """
    Class for implementing input boxes and handling events corresponding to those boxes.
    """

    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = INPUTCOLOR
        self.text = text
        self.text_surface = SMALLFONT.render(text, True, LIGHTGREY)
        self.active = False

    def handle_event(self, event):
        """
        Handles events for an input box.
        """
        # Change border color if box is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = LIGHTGREY if self.active else INPUTCOLOR

        # Change text string if key is pressed while box is selected
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 8:
                        self.text += event.unicode
                self.text_surface = SMALLFONT.render(self.text, True, self.color)

    def draw(self, screen):
        """
        Draws new text into box.
        """
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)