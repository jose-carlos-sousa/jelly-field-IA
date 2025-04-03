import pygame, time
from screens.screen import Screen

class GameScreen(Screen):
    def __init__(self, state):
        super().__init__()
        self.offset_x = 0
        self.offset_y = 0
        self.cell_size = 50
        self.dragging = False
        self.selected_jelly = None
        self.add_text_button("Main Menu", "medium_bold", (150, 50))

        self.jelly_positions = {}
        for i in range(len(state.next_jellies)):
            self.jelly_positions[i] = pygame.Rect(((self.width - 2 * self.cell_size - 50) // 2) + i * (self.cell_size + 50), 
                                        (self.height - self.cell_size - 100), 
                                        self.cell_size, self.cell_size)

    def draw_board(self, state):
        board = state.board
        rows, cols = len(board), len(board[0])
        board_x = (self.width - cols * self.cell_size) // 2
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
                        pygame.draw.rect(self.surface, cell_color, cell_rect)
                        pygame.draw.rect(self.surface, (255, 255, 255), cell_rect, 2)

    def draw_goals(self, state):
        goals = len(state.goal)
        goals_x = (self.width - goals * (self.cell_size) - (goals - 1) * 10) // 2
        goals_y = 30
        for i, (color, goal) in enumerate(state.goal.items()):
            cell_color = state.colors[color]
            cell_rect = pygame.Rect(goals_x + i * (self.cell_size + 10), goals_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.surface, cell_color, cell_rect)
            self.draw_text(str(goal), "medium_large", cell_rect.center, (0, 0, 0))
    
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
                    pygame.draw.rect(self.surface, cell_color, cell_rect)
                    pygame.draw.rect(self.surface, (255, 255, 255), cell_rect, 2)

    def display(self, state):
        self.surface.fill((0, 0, 0))
        
        self.draw_text("Main Menu", "large_bold", (150, 50))

        self.draw_goals(state)
        
        #score_text = self.font.render(f"Score: {state.score}", True, (255, 255, 255))
        #score_rect = score_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        #self.screen.blit(score_text, score_rect)
        
        self.draw_board(state)

        self.draw_next_jellies(state)
                
        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            return "main_menu", state
            
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
            board_x = (self.width - len(state.board[0]) * self.cell_size) // 2
            board_y = 150
            
            col = (mouse_x - board_x) // self.cell_size
            row = (mouse_y - board_y) // self.cell_size

            for i in range(len(state.next_jellies)):
                self.jelly_positions[i] = pygame.Rect(((self.width - 2 * self.cell_size - 50) // 2) + i * (self.cell_size + 50), 
                                            (self.height - self.cell_size - 100), 
                                            self.cell_size, self.cell_size)
            
            if 0 <= row < len(state.board) and 0 <= col < len(state.board[0]):
                state.stats['steps'] += 1
                state.move(selected_jelly, col, row)
                state.collapse()
                if state.isGoal():
                    state.stats['time'] = time.time() - state.stats['time']
                    board_size = len(state.board) * len(state.board[0])
                    state.stats['score'] = round((1000 * board_size) / (state.stats['steps'] + state.stats['time']), 2)
                    return "victory", state
                elif state.isBoardFull():
                    return "defeat", state
                else:
                    return "game_screen", state
            
        return "game_screen", state