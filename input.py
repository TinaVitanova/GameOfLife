import pygame as pg
from constants import botsValues

COLOR_INACTIVE = (0, 0, 255)
COLOR_ACTIVE = (0, 255, 0)
COLOR_ERROR = (255, 0, 0)

FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text='', variable='', n_type='FLOAT', validation='greater_than_zero'):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.variable = variable
        self.n_type = n_type
        self.validation = validation

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.color = COLOR_ACTIVE
            else:
                self.active = False
                number = None
                if self.n_type == 'FLOAT':
                    number = float(self.text)
                else:
                    number = int(float(self.text))
                if self.validation == 'greater_than_zero' and number > 0:
                    self.color = COLOR_INACTIVE
                elif self.validation == 'zero_and_above' and number >= 0:
                    self.color = COLOR_INACTIVE
                else:
                    self.color = COLOR_ERROR
            self.txt_surface = FONT.render(self.text, True, self.color)
        #   Catch all keydown events and decide what to do with the text
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ""
                elif event.key == pg.K_BACKSPACE:
                    if self.text != '-':
                        self.text = self.text[:-1]
                elif event.unicode.isdecimal() or (self.n_type == 'FLOAT' and event.key == pg.K_PERIOD):
                    self.text += event.unicode
                    # self.text = self.text.lstrip('0')
                if self.variable and self.text:
                    botsValues.set_attr(self.variable, self.text)
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def get_text(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
