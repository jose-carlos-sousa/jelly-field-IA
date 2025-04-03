import pygame
import ai, time
from screens.screen import Screen

class AIGame(Screen):
    def __init__(self, state):
        super().__init__()
        self.gajo = ai.AIAgent(state)
        self.add_text_button("Main Menu", "large_bold", (150, 50))
        self.stats = self.run_game(state) 

    def run_game(self, state):
        if state.player == "Depth-First Search AI":
            start = time.time()
            solution = self.gajo.depth_first_search()
            solution_time = time.time() - start

        return {'time': solution_time, 'level': state.stats['level'], 'player': state.player, 'score': 0, 'steps': 0}

    def save_game(self, stats):
        with open('leaderboard.csv', 'a') as file:
            file.write(f"{stats['player']},{stats['time']},{stats['score']},{stats['steps']},{stats['level']}\n")

    def display(self, state):
        self.surface.fill((0, 0, 0))
        self.draw_text("Game Stats", "large_bold", (self.width // 2, 50))
        self.draw_text("Main Menu", "large_bold", (150, 50))

        self.draw_text(f"Time: {self.stats['time']:.2f} seconds", "medium", (self.width // 2, 200))

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            self.save_game(self.stats)
                            return "main_menu", state

        return "ai_game", state