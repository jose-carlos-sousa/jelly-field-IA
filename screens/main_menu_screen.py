import pygame
from screens.screen import Screen

class MainMenuScreen(Screen):
    def __init__(self):
        super().__init__()
        self.button_texts = ["Play", "Leaderboard", "Quit"]
        self.start_y = int(self.height / 2)

        for index, button_text in enumerate(self.button_texts):
            self.add_text_button(button_text, "large_bold", (self.width // 2, self.start_y + index * 80))


    def display(self, state):
        self.surface.fill((0, 0, 0))
        self.draw_text("Jelly Field Puzzle", "large_bold", (self.width // 2, 100))
        
        for index, text in enumerate(self.button_texts):
            position = (self.width // 2, self.start_y + index * 80)
            self.draw_text(text, "large_bold", position)
    
        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Play":
                            return "level_select", state
                        elif button_text == "Leaderboard":
                            return "leaderboard", state
                        elif button_text == "Quit":
                            pygame.quit()
                            exit()
        return "main_menu", state