import pygame
from screens.screen import Screen

class Leaderboard(Screen):
    def __init__(self, leaderboard):
        super().__init__()
        self.leaderboard = leaderboard
        self.add_text_button("Main Menu", "medium_bold", (50, 50), alignment="left")

    def display(self, state):
        self.surface.blit(self.bg, (0, 0))
        self.draw_text("Leaderboard", "large_bold", (self.width // 2, 50))
        self.draw_button("Main Menu", "medium_bold", (50, 50), alignment="left")

        self.draw_text("Player", "medium_bold", (100, 135), alignment="left")
        self.draw_text("Level", "medium_bold", (self.width - 550, 150))
        self.draw_text("Time", "medium_bold", (self.width - 400, 150))
        self.draw_text("Moves", "medium_bold", (self.width - 250, 150))
        self.draw_text("Score", "medium_bold", (self.width - 100, 150))

        y_offset = 200
        pos = 1

        for index, row in self.leaderboard.iterrows():
            self.draw_text(f"{pos}. {row['Player']}", "medium_bold", (100, y_offset - 15), alignment="left")
            self.draw_text(f"{row['Level']}", "medium", (self.width - 550, y_offset))
            self.draw_text(f"{row['Time']:.2f} s", "medium", (self.width - 400, y_offset))
            self.draw_text(f"{row['Moves']}", "medium", (self.width - 250, y_offset))
            self.draw_text(f"{row['Score']}", "medium", (self.width - 100, y_offset))

            y_offset += 50
            pos += 1

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            return "main_menu", state

        return "leaderboard", state