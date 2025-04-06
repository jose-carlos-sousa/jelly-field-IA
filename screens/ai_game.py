import pygame
import ai, time
from screens.screen import Screen

class AIGame(Screen):
    def __init__(self, state):
        super().__init__()
        self.gajo = ai.AIAgent(state)
        self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))
        self.stats = None 
        self.weight = 1
        self.depth = 10

    def run_game(self, state):
        if state.player == "Depth-First Search AI":
            solution = self.gajo.depth_first_search()
        elif state.player == "Breadth-First Search AI":
            solution = self.gajo.bfs_search()
        elif state.player == "Iterative Deepening AI":
            state.player = f"Iterative Deepening AI ({self.depth})"
            solution = self.gajo.iterative_deepening(self.depth)
        elif state.player == "A* Maximize Empty AI":
            state.player = f"A* Maximize Empty AI ({self.weight})"
            solution = self.gajo.a_star_search(self.gajo.heuristic_non_empty_jellies, self.weight)
        elif state.player == "A* Minimize Goal AI":
            state.player = f"A* Minimize Goal AI ({self.weight})"
            solution = self.gajo.a_star_search(self.gajo.heuristic_goal_vals, self.weight)
        elif state.player == "A* Maximize Collapse AI":
            state.player = f"A* Maximize Collapse AI ({self.weight})"
            solution = self.gajo.a_star_search(self.gajo.heuristic_collapse_count, self.weight)
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

    def draw_weight_choices(self):
        self.buttons = {}
        self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))

        rect = ((self.width - 600) // 2, (self.height - 500) // 2 - 50, 600, 500)
        pygame.draw.rect(self.surface, (148, 51, 44), rect, border_radius=10)
        
        self.draw_text("Heuristic Weight", "medium_bold", (self.width // 2, self.height - 615))

        weights = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        rect_x, rect_y, rect_w, rect_h = rect

        cols = 2
        rows = 5
        button_width = 200
        button_height = 40
        h_spacing = rect_w // cols
        v_spacing = rect_h // (rows + 1)

        for index, weight in enumerate(weights):
            col = index % cols
            row = index // cols
            x = rect_x + h_spacing * col + h_spacing // 2
            y = rect_y + v_spacing * (row + 1) + 25
            self.add_text_button(str(weight), "medium_bold", (x, y))
            self.draw_button(str(weight), "medium_bold", (x, y))

    def draw_depth_choices(self):
        self.buttons = {}
        self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))

        rect = ((self.width - 600) // 2, (self.height - 500) // 2 - 50, 600, 500)
        pygame.draw.rect(self.surface, (148, 51, 44), rect, border_radius=10)
        
        self.draw_text("Maximum Depth", "medium_bold", (self.width // 2, self.height - 615))

        weights = [2, 3, 5, 8, 10, 15]

        rect_x, rect_y, rect_w, rect_h = rect

        cols = 2
        rows = 3
        button_width = 200
        button_height = 40
        h_spacing = rect_w // cols
        v_spacing = rect_h // (rows + 1)

        for index, weight in enumerate(weights):
            col = index % cols
            row = index // cols
            x = rect_x + h_spacing * col + h_spacing // 2
            y = rect_y + v_spacing * (row + 1) + 25
            self.add_text_button(str(weight), "medium_bold", (x, y))
            self.draw_button(str(weight), "medium_bold", (x, y))

    def display(self, state):
        self.surface.blit(self.bg, (0, 0))
        self.draw_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))

        if self.stats:
            self.draw_text("Game Stats", "large_bold", (self.width // 2, 50))

            self.draw_text(f"Level: {self.stats['level']}", "medium", (self.width // 2, 200))
            if self.stats['time'] == 0:
                self.draw_text("NO SOLUTION FOUND!", "large", (self.width // 2, 400))
            else:
                self.draw_text(f"Time: {self.stats['time']:.2f} seconds", "medium", (self.width // 2, 300))
                self.draw_text(f"Moves: {self.stats['steps']}", "medium", (self.width // 2, 400))
                self.draw_text(f"Score: {self.stats['score']:.2f}", "large", (self.width // 2, 500))
        else:
            if state.player.startswith("A*"):
                self.draw_weight_choices()
            elif state.player.startswith("Iterative"):
                self.draw_depth_choices()


        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Return To Main Menu":
                            if self.stats and self.stats['steps'] > 0:
                                self.save_game(self.stats)
                            return "main_menu", state
                        elif state.player.startswith("A*"):
                            self.weight = float(button_text)
                            self.buttons = {}
                            self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))
                            self.stats = self.run_game(state)
                        elif state.player.startswith("Iterative"):
                            self.depth = int(button_text)
                            self.buttons = {}
                            self.add_text_button("Return To Main Menu", "large_bold", (self.width // 2, self.height - 100))
                            self.stats = self.run_game(state)

        return "ai_game", state