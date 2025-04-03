import pygame
from screens.screen import Screen

class PlayerSelect(Screen):
    def __init__(self):
        super().__init__()
        self.add_text_button("Main Menu", "large_bold", (150, 50))
        self.add_text_button("Human", "medium_bold", (100, 200))
        self.add_text_button("Depth-First Search AI", "medium_bold", (150, 300))

    def display(self, state):
        self.surface.fill((0, 0, 0))
        self.draw_text("Select Player", "large_bold", (self.width // 2, 100))
        self.draw_text("Main Menu", "large_bold", (150, 50))
        self.draw_text("Human", "medium_bold", (100, 200))
        self.draw_text("Depth-First Search AI", "medium_bold", (150, 300))

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            return "main_menu", state
                        if button_text == "Human":
                            state.player = "human"
                            return "game_screen", state
                        elif button_text == "Depth-First Search AI":
                            state.player = "Depth-First Search AI"
                            return "ai_game", state

        return "player_select", state
