import pygame

class pygameGUI:
    def __init__(self, state):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.offset_x = 0
        self.offset_y = 0
        self.current_screen = "main_menu"
        self.font = pygame.font.Font(None, 48)
        self.cell_size = 50
        self.buttons = {}
        self.clock = pygame.time.Clock()
        self.dragging = False
        self.selected_jelly = None
        self.jelly_positions = {}
        for i in range(len(state.next_jellies)):
            self.jelly_positions[i] = pygame.Rect(((self.screen.get_width() - 2 * self.cell_size - 50) // 2) + i * (self.cell_size + 50), 
                                        (self.screen.get_height() - self.cell_size - 100), 
                                        self.cell_size, self.cell_size)


    def display(self, state):
        if self.current_screen == "main_menu":
            self.display_main_menu()
        elif self.current_screen == "defeat_screen":
            self.display_defeat_screen()
        elif self.current_screen == "victory_screen":
            self.display_victory_screen()
        elif self.current_screen == "leaderboard_screen":
            self.display_leaderboard_screen()
        elif self.current_screen == "game_screen":
            self.display_game(state)

    def display_main_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Jelly Field Puzzle", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)

        button_texts = ["Play", "Leaderboard", "Quit"]
        self.buttons = {}
        start_y = 200

        for index, text in enumerate(button_texts):
            button = self.font.render(text, True, (255, 255, 255))
            button_rect = button.get_rect(center=(self.screen.get_width() // 2, start_y + index * 80))
            self.screen.blit(button, button_rect)
            self.buttons[text] = button_rect

        pygame.display.flip()

    def handle_main_menu_click(self, pos):
        for button_text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_text == "Play":
                    self.current_screen = "game_screen"
                elif button_text == "Leaderboard":
                    self.current_screen = "leaderboard_screen"
                elif button_text == "Quit":
                    self.quit()
    
    def handle_game_click(self, pos):
        for button_text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_text == "Main Menu":
                    self.current_screen = "main_menu"

    def display_defeat_screen(self):
        pass

    def display_victory_screen(self):
        pass
    
    def display_leaderboard_screen(self):
        pass

    def display_game(self, state):
        self.screen.fill((0, 0, 0))
        
        menu_button = self.font.render("Main Menu", True, (255, 255, 255))
        menu_button_rect = menu_button.get_rect(topleft=(10, 10))
        self.screen.blit(menu_button, menu_button_rect)
        self.buttons["Main Menu"] = menu_button_rect

        self.draw_goals(state)
        
        score_text = self.font.render(f"Score: {state.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(score_text, score_rect)
        
        self.draw_board(state)

        self.draw_next_jellies(state)
                
        pygame.display.flip()


    def handle_events(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.current_screen == "main_menu":
                        self.handle_main_menu_click(event.pos)
                    elif self.current_screen == "game_screen":
                        self.handle_game_click(event.pos)
                mouse_x, mouse_y = event.pos
                
                for i in range(min(2, len(state.next_jellies))):
                    square = state.next_jellies[i].array
                    srows, scols = len(square), len(square[0])
                    jelly_rect = self.jelly_positions[i]
                    if jelly_rect.collidepoint(mouse_x, mouse_y):
                        self.dragging = True
                        self.selected_jelly = i
                        self.offset_x = jelly_rect.x - event.pos[0]
                        self.offset_y = jelly_rect.y - event.pos[1]
                        break

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.jelly_positions[self.selected_jelly].x = event.pos[0] + self.offset_x
                self.jelly_positions[self.selected_jelly].y = event.pos[1] + self.offset_y


            elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
                selected_jelly = self.selected_jelly
                self.dragging = False
                self.selected_jelly = None
                mouse_x, mouse_y = event.pos
                board_x = (self.screen.get_width() - len(state.board[0]) * self.cell_size) // 2
                board_y = 150
                
                col = (mouse_x - board_x) // self.cell_size
                row = (mouse_y - board_y) // self.cell_size
                
                if 0 <= row < len(state.board) and 0 <= col < len(state.board[0]):
                    for i in range(len(state.next_jellies)):
                        self.jelly_positions[i] = pygame.Rect(((self.screen.get_width() - 2 * self.cell_size - 50) // 2) + i * (self.cell_size + 50), 
                                                    (self.screen.get_height() - self.cell_size - 100), 
                                                    self.cell_size, self.cell_size)
                    return True, selected_jelly, col, row
            
        return False, None, None, None 

    def draw_board(self, state):
        board = state.board
        rows, cols = len(board), len(board[0])
        board_x = (self.screen.get_width() - cols * self.cell_size) // 2
        board_y = 150
        
        for row in range(rows):
            for col in range(cols):
                square = board[row][col].array
                srows, scols = len(square), len(square[0])
                for square_row in range(srows):
                    for square_column in range(scols):
                        cell_color = state.colors[square[square_row][square_column]]
                        square_width, square_height = self.cell_size / scols, self.cell_size / srows
                        cell_rect = pygame.Rect(board_x + col * self.cell_size + square_column * square_width,
                        board_y + row * self.cell_size + square_height * square_row, square_width, square_height)
                        pygame.draw.rect(self.screen, cell_color, cell_rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, 2)

    def draw_goals(self, state):
        goals = len(state.goal)
        goals_x = (self.screen.get_width() - goals * (self.cell_size) - (goals - 1) * 10) // 2
        goals_y = 30
        for i, (color, goal) in enumerate(state.goal.items()):
            cell_color = state.colors[color]
            cell_rect = pygame.Rect(goals_x + i * (self.cell_size + 10), goals_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, cell_color, cell_rect)
            text_surface = self.font.render(str(goal), True, (0, 0, 0))  
            text_rect = text_surface.get_rect(center=cell_rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_next_jellies(self, state):
        for i in range(min(2, len(state.next_jellies))):
            square = state.next_jellies[i].array
            srows, scols = len(square), len(square[0])
            for square_row in range(srows):
                for square_column in range(scols):
                    cell_color = state.colors[square[square_row][square_column]]
                    square_width, square_height = self.cell_size / scols, self.cell_size / srows
                    jelly_rect = self.jelly_positions[i]
                    cell_rect = pygame.Rect(jelly_rect.x + square_column * square_width,
                    jelly_rect.y + square_height * square_row, square_width, square_height)
                    pygame.draw.rect(self.screen, cell_color, cell_rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, 2)


    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
        exit()
