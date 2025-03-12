import pygame

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag Object with Mouse")

# Object properties
rect = pygame.Rect(300, 200, 100, 80)  # x, y, width, height
dragging = False  # Track if the object is being dragged
offset_x, offset_y = 0, 0  # Mouse offset inside the object

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Background color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):  # Check if mouse is inside the rect
                dragging = True
                offset_x = rect.x - event.pos[0]
                offset_y = rect.y - event.pos[1]

        # Mouse button up (release the object)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # Mouse motion (dragging)
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y

    # Draw the object
    pygame.draw.rect(screen, (0, 255, 0), rect)  # Green rectangle
    
    pygame.display.flip()  # Update display

pygame.quit()
