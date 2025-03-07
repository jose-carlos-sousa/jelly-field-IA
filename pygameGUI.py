import pygame

class pygameGUI:
    def __init__(self):
        """
        Initializes the pygameGUI with a given screen.
        :param screen: pygame.Surface - The current screen to render on.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.current_screen = "main_menu"
        self.font = pygame.font.Font(None, 48)
        self.buttons = {}
        self.clock = pygame.time.Clock()

    def display(self, state):
        """
        Displays the appropriate screen based on the current screen type.
        :param state: The state to be displayed (only used in game screen).
        """
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
        """Displays the main menu screen."""
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
        """Handles clicks on the main menu buttons."""
        for button_text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_text == "Play":
                    self.current_screen = "game_screen"
                elif button_text == "Leaderboard":
                    self.current_screen = "leaderboard_screen"
                elif button_text == "Quit":
                    self.quit()
    
    def handle_game_click(self, pos):
        """Handles clicks on game buttons."""
        for button_text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_text == "Main Menu":
                    self.current_screen = "main_menu"

    def display_defeat_screen(self):
        """Displays the defeat screen."""
        pass

    def display_victory_screen(self):
        """Displays the victory screen."""
        pass
    
    def display_leaderboard_screen(self):
        """Displays the leaderboard screen."""
        pass

    def display_game(self, state):
        """Displays the game screen with the given state."""
        self.screen.fill((0, 0, 0))
        
        # Draw main menu button (top left)
        menu_button = self.font.render("Main Menu", True, (255, 255, 255))
        menu_button_rect = menu_button.get_rect(topleft=(10, 10))
        self.screen.blit(menu_button, menu_button_rect)
        self.buttons["Main Menu"] = menu_button_rect
        
        # Draw score (top right)
        score_text = self.font.render(f"Score: {state.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(score_text, score_rect)
        
        # Draw board grid
        board = state.board
        rows, cols = len(board), len(board[0])
        cell_size = 50
        board_x = (self.screen.get_width() - cols * cell_size) // 2
        board_y = 100
        
        for row in range(rows):
            for col in range(cols):
                square = state.board[row][col].array
                srows, scols = len(square), len(square[0])
                for square_row in range(srows):
                    for square_column in range(scols):
                        cell_color = state.colors[square[square_row][square_column]]
                        square_width, square_height = cell_size / scols, cell_size / srows
                        cell_rect = pygame.Rect(board_x + col * cell_size + square_column * square_width,
                         board_y + row * cell_size + square_height * square_row, square_width, square_height)
                        pygame.draw.rect(self.screen, cell_color, cell_rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, 2)
                
        pygame.display.flip()

    def get_move(self):
        """
        Captures and returns the player's move.
        """
        pass

    def handle_events(self):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.current_screen == "main_menu":
                            self.handle_main_menu_click(event.pos)
                        elif self.current_screen == "game_screen":
                            self.handle_game_click(event.pos)

    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
        exit()
