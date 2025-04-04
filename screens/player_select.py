import pygame, time
from screens.screen import Screen

class PlayerSelect(Screen):
    def __init__(self):
        super().__init__()
        self.add_text_button("Main Menu", "medium_bold", (50, 50), alignment="left")
        self.add_text_button("Human", "medium_bold", (100, 300) ,alignment="left")
        self.add_text_button("Depth-First Search AI", "medium_bold", (100, 400), alignment="left")
        self.add_text_button("Breadth-First Search AI", "medium_bold", (100, 500), alignment="left")
        self.add_text_button("Greedy Maximize Empty AI", "medium_bold", (100, 600), alignment="left")
        self.add_text_button("Iterative Deepening AI", "medium_bold", (self.width - 100, 300), alignment="right")
        self.add_text_button("A* Maximize Empty AI", "medium_bold", (self.width - 100, 400), alignment="right")
        self.add_text_button("A* Minimize Goal AI", "medium_bold", (self.width - 100, 500), alignment="right")
        self.add_text_button("Greedy Minimize Goal AI", "medium_bold", (self.width - 100, 600), alignment="right")

    def display(self, state):
        self.surface.blit(self.bg, (0, 0))
        self.draw_text("Select Player", "large_bold", (self.width // 2, 100))
        self.draw_button("Main Menu", "medium_bold", (50, 50), alignment="left")
        self.draw_button("Human", "medium_bold", (100, 300) ,alignment="left")
        self.draw_button("Depth-First Search AI", "medium_bold", (100, 400), alignment="left")
        self.draw_button("Breadth-First Search AI", "medium_bold", (100, 500), alignment="left")
        self.draw_button("Greedy Maximize Empty AI", "medium_bold", (100, 600), alignment="left")
        self.draw_button("Iterative Deepening AI", "medium_bold", (self.width - 100, 300), alignment="right")
        self.draw_button("A* Maximize Empty AI", "medium_bold", (self.width - 100, 400), alignment="right")
        self.draw_button("A* Minimize Goal AI", "medium_bold", (self.width - 100, 500), alignment="right")
        self.draw_button("Greedy Minimize Goal AI", "medium_bold", (self.width - 100, 600), alignment="right")

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            return "main_menu", state
                        if button_text == "Human":
                            state.player = "Human"
                            state.stats['time'] = time.time()
                            return "game_screen", state
                        elif button_text == "Depth-First Search AI":
                            state.player = "Depth-First Search AI"
                            return "ai_game", state
                        elif button_text == "Breadth-First Search AI":
                            state.player = "Breadth-First Search AI"
                            return "ai_game", state
                        elif button_text == "Iterative Deepening AI":
                            state.player = "Iterative Deepening AI"
                            return "ai_game", state
                        elif button_text == "A* Maximize Empty AI":
                            state.player = "A* Maximize Empty AI"
                            return "ai_game", state
                        elif button_text == "A* Minimize Goal AI":
                            state.player = "A* Minimize Goal AI"
                            return "ai_game", state
                        elif button_text == "Greedy Maximize Empty AI":
                            state.player = "Greedy Maximize Empty AI"
                            return "ai_game", state
                        elif button_text == "Greedy Minimize Goal AI":
                            state.player = "Greedy Minimize Goal AI"
                            return "ai_game", state

        return "player_select", state
