#!/usr/bin/python
import pygame

##### Constants ################################

block_color = "blue"
paddle_color = "green"
ball_color = "red"

ball_size = 25
ball_speed = 2
paddle_size = 60
paddle_speed = 4


##### Setup ####################################

pygame.init()
clock = pygame.time.Clock()
running = True
game_on = True

# This function draws a text message on the screen.
def draw_text(message, top_left):
    font = pygame.font.Font(None, 36)
    text = font.render(message, 1, (255,255,255))
    textpos = text.get_rect()
    textpos.topleft = top_left
    screen.blit(text, textpos)

#### Screen ######################################

# Setup the screen and game_board
pygame.display.set_caption("Blockout!")
screen = pygame.display.set_mode((800,600))
game_board = screen.get_rect()

#### Game Pieces ######################################

# Start the ball off-center, moving diagonally down.
ball = pygame.Rect(0, 0, ball_size, ball_size)
ball.center = game_board.center
ball.centerx -= 100
ball_dx = 1
ball_dy = ball_speed

# Put a rectangular paddle near the bottom
paddle = pygame.Rect(0, game_board.bottom-50, paddle_size, 10)
paddle.centerx = game_board.centerx
paddle_dx = 0

# Pile o' Blocks
blocks_top = game_board.height / 6
block_offset = game_board.width / 10
block_width = block_offset - 5
blocks = [ 
    pygame.Rect((column*block_offset)+2, (row*25)+blocks_top, block_width,20) 
    for row in range(5) 
    for column in range(10) ]

##### Game Play Loop ##################################

while running:

    # Run 60 frames per second
    clock.tick(60)

    ##### User Input ###################################

    # End the game when player closes the window.
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    # Move paddle left and right with arrow keys.
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            paddle_dx = -paddle_speed
        elif event.key == pygame.K_RIGHT:
            paddle_dx = paddle_speed
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            paddle_dx = 0
        if event.key == pygame.K_ESCAPE:
            running = False

    ##### Game Rules ###################################

    # If that was the last block, you win!
    if not blocks:
        game_on = False
        end_message = "You Win!"
    
    # Bounce ball off the paddle.
    if paddle.colliderect(ball):
        ball_dy = -ball_dy

    # Bounce off the right edge
    if ball_dx > 0 and ball.right > game_board.right:
        ball_dx = -ball_dx

    # Bounce off the left edge
    elif ball_dx < 0 and ball.left < game_board.left:
        ball_dx = -ball_dx

    # Bounce off the top edge
    if ball_dy < 0 and ball.top < game_board.top:
        ball_dy = -ball_dy

    # Game Over when ball hits the bottom
    elif ball_dy > 0 and ball.bottom > game_board.bottom:
        game_on = False
        end_message = "Game Over"

    # Ball hits a block
    hit = ball.collidelist(blocks)
    if hit > -1:
        # Erase the block
        block = blocks.pop(hit)
        
        # Bounce off the left edge
        if ball_dx > 0 and block.collidepoint(ball.midright):
            ball_dx = -ball_dx
        # Bounce off the right edge
        elif ball_dx < 0 and block.collidepoint(ball.midleft):
            ball_dx = -ball_dx
        # Bounce off the top and bottom edges
        else:
            ball_dy = -ball_dy

    # Move the paddle
    paddle.left += paddle_dx

    # Move the ball
    ball.centerx += ball_dx
    ball.centery += ball_dy

    ##### Draw the Screen ##############################

    # Start with a blank screen, erase everything
    # This must come first in drawing. Put all other drawing commands below.
    screen.fill((0,0,0))

    # Draw blocks, blue with white border
    for block in blocks:
        pygame.draw.rect(screen, pygame.Color(block_color), block)
        pygame.draw.rect(screen, (200,200,255), block, 2)

    if game_on:
        # Draw the paddle
        pygame.draw.rect(screen, pygame.Color(paddle_color), paddle)

        # Draw the ball
        pygame.draw.circle(screen, pygame.Color(ball_color), ball.center, ball.width//2)

    # Show ending message
    else:
        draw_text(end_message, game_board.center)
    
    # Show the screen. 
    # This must come last, put all other drawing commands above.
    pygame.display.flip()

pygame.quit()
