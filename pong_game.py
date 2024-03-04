import pygame
import random

'''TODO:    - add easy, normal, hard mode with custom ballsize- and racket-settings and maybe bg_colors and different score_boards
            - create scoreboard logic (name and 10 best scores) -> new file for storage
            - 2 player mode: maybe add items like ball invisible for 1 sec or faster or gets reflected by item box :-) new game mode 'special mode'
            [- prettier game_speed-growth function (slower in the end, little too fast)]

'''
class game_ball(pygame.sprite.Sprite):
    def __init__(self, color, diameter):
        super().__init__()
        self.image = pygame.Surface((diameter, diameter))
        self.rect = self.image.get_rect(center = (screenwidth/2, screenheight/2))
        self.image.fill(color)
        self.radius = diameter/2
        self.color = color
        # set initial moving y-direction randomly, move towards player first
        y = screenheight/2
        while y == screenheight/2:
            y = random.randint(0, screenheight)
        self.target = pygame.math.Vector2(screenwidth, y) # set point where ball is initially headed to
        self.v = pygame.math.Vector2(self.target.x - self.rect.centerx, self.target.y - self.rect.centery).normalize() # compute vector that represents the route from ball to target
    
    def get_pos(self):
        return self.rect.center
    
    def move(self):
        # Moves 'factor' pixels per frame; the greater the factor, the more fluent is the game at high speeds, on the contrary a high factor looks bad if ball speed is low -> function?
        self.rect.centerx += 5 * self.v.x
        self.rect.centery += 5 * self.v.y
        
    # draw round ball
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
    
    def update(self):
        global game_active, game_speed, winner

        # game over
        if self.rect.midright[0] > screenwidth:
            winner = 'left'
            game_active = False
        elif self.rect.midleft[0] < 0:
            winner = 'right'
            game_active = False

        # reflect ball of rackets
        elif self.rect.colliderect(player_racket.sprite.rect): 
            surface_normal = pygame.math.Vector2(1, 0)
            self.v.reflect_ip(surface_normal)
            game_speed *= 1.1
        elif game_mode == 1 and self.rect.colliderect(com_racket.sprite.rect):
            print(f'game_speed: {game_speed}')
            surface_normal = pygame.math.Vector2(1, 0)
            self.v.reflect_ip(surface_normal)
        elif game_mode == 2 and self.rect.colliderect(player2_racket.sprite.rect):
            surface_normal = pygame.math.Vector2(1, 0)
            self.v.reflect_ip(surface_normal)
        
        # reflect ball of top or bottom border
        elif self.rect.midtop[1] <= 0:
            surface_normal = pygame.math.Vector2(0, 1)
            self.v.reflect_ip(surface_normal)
        elif self.rect.midbottom[1] >= screenheight:
            surface_normal = pygame.math.Vector2(0, 1)
            self.v.reflect_ip(surface_normal)
        
        self.move()


class racket(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('graphics/racket.png').convert_alpha()
        # create and position rackets
        if position == 'left':
            self.rect = self.image.get_rect(midleft = (10, screenheight/2))
        else:
            self.rect = self.image.get_rect(midright = (screenwidth - 10, screenheight/2))

    def get_pos(self):
        return self.rect.center
    
    def update(self, y_new):
        self.rect.centery = y_new


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # compute relative time (time that's passed since clicking mouse)
    # display current score only in single player mode
    if game_mode == 1:
        score_surf = font.render(f'Score: {current_time}', True, (255, 255, 255))
        score_rect = score_surf.get_rect(center = (screenwidth/2, screenheight/5))
        screen.blit(score_surf, score_rect)
    
    return current_time


# Initialization
pygame.init()

# Global Variables

# adjustable :) -----------
initial_game_speed = 100
ball_color = (255, 255, 255)
ball_diameter = 50
bg_color = ('#aa899a') # game active
intro_color = (180, 160, 160) # intro and game-over
#--------------------------

score = 0
start_time = 0
game_speed = initial_game_speed
game_active = False
game_mode = 0 # will be set to 1 or 2 (based on #players)
winner = '' # announce winner when game's over (2 player mode)

screenwidth = 1400
screenheight = 900
screen = pygame.display.set_mode((screenwidth, screenheight))
font = pygame.font.SysFont('Arial', 100)
title_font = pygame.font.SysFont('Arial', 150)
clock = pygame.time.Clock()
pygame.display.set_caption('Pong Game')

# Intro Screen
game_name = title_font.render('Pong Game', True, (255,255,255))
game_name_rect = game_name.get_rect(center = (screenwidth/2, screenheight*2/7))
intro_msg = font.render('Choose game mode', True, (255,255,255))
intro_msg_rect = intro_msg.get_rect(center = (screenwidth/2, screenheight*3/5))

# Game Over Screen
game_over_msg = font.render('Game Over', True, (255, 255, 255))
game_over_rect = game_over_msg.get_rect(center = (screenwidth/2, screenheight/5))

# Game Modes
single_mode = font.render('One Player', True, (255, 255, 255))
single_rect = single_mode.get_rect(center = (screenwidth*1/4, screenheight*4/5))
two_player_mode = font.render('Two Players', True, (255, 255, 255))
two_player_rect = single_mode.get_rect(center = (screenwidth*3/4, screenheight*4/5))

# Objects/Groups
player_racket = pygame.sprite.GroupSingle()
com_racket = pygame.sprite.GroupSingle()
player2_racket = pygame.sprite.GroupSingle()

player_racket.add(racket('right'))

ball = pygame.sprite.GroupSingle()
ball.add(game_ball(ball_color, ball_diameter))

pygame.key.set_repeat(1) # held keys generate multiple KEYDOWN-events :)
while True:
    # buffer for pressed keys (2 player mode)
    key_p1 = 0
    key_p2 = 0

    for event in pygame.event.get():
        # quit game on close or esc
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()       

        if game_mode == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_p1 = -1
                elif event.key == pygame.K_DOWN:
                    key_p1 = +1
                elif event.key == pygame.K_w:
                    key_p2 = -1
                elif event.key == pygame.K_s:
                    key_p2 = +1

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_rect.collidepoint(pygame.mouse.get_pos()): # start single player
                    game_mode = 1
                    com_racket.add(racket('left'))
                    game_active = True
                    start_time = pygame.time.get_ticks()
                elif two_player_rect.collidepoint(pygame.mouse.get_pos()): # start two player
                    game_mode = 2
                    game_speed = game_speed * 2 // 3
                    player2_racket.add(racket('left'))
                    game_active = True
                    start_time = pygame.time.get_ticks()
                
            

    if game_active:
        screen.fill(bg_color)
        score = display_score()

        # update ball and racket positions and draw them
        if game_mode == 1:
            com_racket.update(ball.sprite.get_pos()[1]) # com racket constantly adapts to ball-position
            com_racket.draw(screen)
            player_racket.update(pygame.mouse.get_pos()[1])
            player_racket.draw(screen)
        else:
            player2_racket.update(player2_racket.sprite.get_pos()[1] + 10 * key_p2)
            player2_racket.draw(screen)
            player_racket.update(player_racket.sprite.get_pos()[1] + 10 * key_p1)
            player_racket.draw(screen)

        ball.update()
        ball.sprite.draw(screen) # opt: remove 'sprite' to make ball squared

    else:
        screen.fill(intro_color)

        if score == 0:
            # show custom intro screen
            screen.blit(game_name, game_name_rect)
            screen.blit(intro_msg, intro_msg_rect)
            screen.blit(single_mode, single_rect)
            screen.blit(two_player_mode, two_player_rect)
        else:
            # show custom game over screen
            screen.blit(game_over_msg, game_over_rect)
            score_msg = font.render(f'You lasted {score} seconds', True, (255, 255, 255))
            score_rect = score_msg.get_rect(center = (screenwidth/2, screenheight/2))
            
            if game_mode == 2:
                # display winner
                winner_msg = font.render(f'The {winner} Player won !', True, (255, 255, 255))
                winner_rect = winner_msg.get_rect(center = (screenwidth/2, screenheight*4/7))
                score_rect.centery -= 100
                screen.blit(winner_msg, winner_rect)
            
            screen.blit(score_msg, score_rect)
            screen.blit(single_mode, single_rect)
            screen.blit(two_player_mode, two_player_rect)

            # reset variables
            game_speed = initial_game_speed
            ball.sprite.rect.center = (screenwidth/2, screenheight/2)
            if game_mode == 2:
                player2_racket.sprite.rect.centery = screenheight/2
            player_racket.sprite.rect.centery = screenheight/2
            
            y = screenheight/2
            while y == screenheight/2:
                y = random.randint(0, screenheight)
            ball.sprite.target = pygame.math.Vector2(screenwidth, y)
            ball.sprite.v = pygame.math.Vector2(ball.sprite.target.x - ball.sprite.rect.centerx, ball.sprite.target.y - ball.sprite.rect.centery).normalize()


    pygame.display.update()
    clock.tick(game_speed)