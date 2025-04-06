import pygame
import ai, time
from screens.screen import Screen

class AIGame(Screen):
    def __init__(self, state):
        super().__init__()
        self.gajo = ai.AIAgent(state)
        self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))
        self.display_calculation()
        self.stats = self.run_game(state) 

    def run_game(self, state):
        if state.player == "Depth-First Search AI":
            solution = self.gajo.depth_first_search()
        elif state.player == "Breadth-First Search AI":
            solution = self.gajo.bfs_search()
        elif state.player == "Iterative Deepening AI":
            solution = self.gajo.iterative_deepening()
        elif state.player == "A* Maximize Empty AI":
            solution = self.gajo.a_star_search(self.gajo.heuristic_non_empty_jellies)
        elif state.player == "A* Minimize Goal AI":
            solution = self.gajo.a_star_search(self.gajo.heuristic_goal_vals)
        elif state.player == "A* Maximize Collapse AI":
            solution = self.gajo.a_star_search(self.gajo.heuristic_collapse_count)
        elif state.player == "Greedy Maximize Empty AI":
            solution = self.gajo.greedy_search(self.gajo.heuristic_non_empty_jellies)
        elif state.player == "Greedy Minimize Goal AI":
            solution = self.gajo.greedy_search(self.gajo.heuristic_goal_vals)
        elif state.player == "Greedy Maximize Collapse AI":
            solution = self.gajo.greedy_search(self.gajo.heuristic_collapse_count)

        if solution:
            score, steps, solution_time = self.gajo.get_solution_stats(solution)
        else:
            score, steps, solution_time = 0, 0, 0

        return {'time': solution_time, 'level': state.stats['level'], 'player': state.player, 'score': score, 'steps': steps}

    def save_game(self, stats):
        with open('leaderboard.csv', 'a') as file:
            file.write(f"{stats['player']},{stats['time']},{stats['score']},{stats['steps']},{stats['level']}\n")
   
    def display_calculation(self):
        self.surface.blit(self.bg, (0, 0))
        self.draw_text("Calculating...", "large_bold", (self.width // 2, self.height // 2))
        pygame.display.flip()
    def display(self, state):
        self.surface.blit(self.bg, (0, 0))
        self.draw_text("Game Stats", "large_bold", (self.width // 2, 50))
        self.draw_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))

        self.draw_text(f"Level: {self.stats['level']}", "medium", (self.width // 2, 200))
        self.draw_text(f"Time: {self.stats['time']:.2f} seconds", "medium", (self.width // 2, 300))
        self.draw_text(f"Moves: {self.stats['steps']}", "medium", (self.width // 2, 400))
        self.draw_text(f"Score: {self.stats['score']:.2f}", "large", (self.width // 2, 500))
        

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Return To Main Menu":
                            if (self.stats['steps'] > 0):
                                self.save_game(self.stats)
                            return "main_menu", state

        return "ai_game", state