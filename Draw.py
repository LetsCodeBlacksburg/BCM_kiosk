import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))

while True:

    # End the game when player closes the window.
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()

    # Start with a blank screen, before drawing anything else.
    screen.fill(pygame.Color("black"))

    ##################################################
    # Draw stuff
    # Remeber to indent four spaces, so you start typing at the same level
    # as this line.
    

    
    ##################################################
    # Show the screen. This must come last.
    pygame.display.flip()

