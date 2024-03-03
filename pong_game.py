import pygame
import random

'''TODO:    - add easy, normal, hard mode with custom ballsize- and racket-settings and maybe bg_colors and different score_boards
            - prettier game_speed-growth function (slower in the end, little too fast)
            - create scoreboard logic (name and 10 best scores) -> new file for storage
            - add multiplayer -> stir racket with w/s and up/down

'''
class game_ball(pygame.sprite.Sprite):
    def __init__(self, color, diameter):
        super().__init__()
        self.image = pygame.Surface((diameter, diameter)) #pygame.image.load('graphics/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screenwidth/2, screenheight/2))
        self.image.fill(color)
        self.radius = diameter/2
        self.color = color
        # set initial moving y-direction randomly, move towards player first
        y = screenheight/2
        while screenheight/2 - 10 <= y <= screenheight/2 + 10:
            y = random.randint(0, screenheight)
        self.target = pygame.math.Vector2(screenwidth, y) # sets point where ball is initially headed to
        self.v = pygame.math.Vector2(self.target.x - self.rect.centerx, self.target.y - self.rect.centery).normalize() # compute vector that represents the route between ball and target
    
    def get_pos(self):
        return self.rect.center
    
    def move(self):
        # the greater the factor, the more fluent is the game! Moves 'factor' pixels per frame
        self.rect.centerx += 5 * self.v.x
        self.rect.centery += 5 * self.v.y
        
    # ball is a circle not a square
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
    
    def update(self):
        global game_active, game_speed

        # game over
        if self.rect.midright[0] > screenwidth:
            game_active = False

        # reflect ball of rackets
        elif self.rect.colliderect(player_racket.sprite.rect): 
            surface_normal = pygame.math.Vector2(1, 0)
            self.v.reflect_ip(surface_normal)
            game_speed *= 1.1
        elif self.rect.colliderect(com_racket.sprite.rect):
            print(f'game_speed: {game_speed}')
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

    def update(self, y_new):
        self.rect.centery = y_new


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # compute relative time (time that's passed since clicking mouse)
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
bg_color = ('#aa899a') # game active, other ones: '#aa899a'
intro_color = (94, 129, 162) # intro and game-over
#--------------------------

score = 0
start_time = 0
game_speed = initial_game_speed

screenwidth = 1400
screenheight = 900
screen = pygame.display.set_mode((screenwidth, screenheight))
font = pygame.font.SysFont('Quantum Sans Serif Font', 100)
clock = pygame.time.Clock()
game_active = False
pygame.display.set_caption('Pong Game')

# Intro Screen
game_name = font.render('Pong Game', False, (255,255,255))
game_name_rect = game_name.get_rect(center = (screenwidth/2, screenheight/3))
intro_msg = font.render('Press mouse to start', False, (255,255,255))
intro_msg_rect = intro_msg.get_rect(center = (screenwidth/2, screenheight*2/3))

# Game Over Screen
game_over_msg = font.render('Game Over', False, (255, 255, 255))
game_over_rect = game_over_msg.get_rect(center = (screenwidth/2, screenheight/5))
restart_msg = font.render('Press mouse to restart', False, (255, 255, 255))
restart_rect = restart_msg.get_rect(center = (screenwidth/2, screenheight*4/5))

# Objects/Groups
com_racket = pygame.sprite.GroupSingle()
com_racket.add(racket('left'))

player_racket = pygame.sprite.GroupSingle()
player_racket.add(racket('right'))

ball = pygame.sprite.GroupSingle()
ball.add(game_ball(ball_color, ball_diameter))


while True:
    for event in pygame.event.get():
        # quit game on close or esc
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()       

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
            

    if game_active:
        screen.fill(bg_color)
        score = display_score()

        # update ball and racket positions and draw them
        com_racket.update(ball.sprite.get_pos()[1]) # com racket constantly adapts to ball-position
        com_racket.draw(screen)

        player_racket.update(pygame.mouse.get_pos()[1])
        player_racket.draw(screen)

        ball.update()
        ball.sprite.draw(screen) # opt: remove 'sprite' to make ball squared

    else:
        screen.fill(intro_color)

        if score == 0:
            # show custom intro screen
            screen.blit(game_name, game_name_rect)
            screen.blit(intro_msg, intro_msg_rect)
        else:
            # show custom game over screen
            screen.blit(game_over_msg, game_over_rect)
            score_msg = font.render(f'Your Score: {score}', False, (255, 255, 255))
            score_rect = score_msg.get_rect(center = (screenwidth/2, screenheight*3/5))
            screen.blit(score_msg, score_rect)
            screen.blit(restart_msg, restart_rect)

            # reset variables
            game_speed = initial_game_speed
            ball.sprite.rect.center = (screenwidth/2, screenheight/2)
            y = screenheight/2
            while screenheight/2 - 10 <= y <= screenheight/2 + 10:
                y = random.randint(0, screenheight)
            ball.sprite.target = pygame.math.Vector2(screenwidth, y)
            ball.sprite.v = pygame.math.Vector2(ball.sprite.target.x - ball.sprite.rect.centerx, ball.sprite.target.y - ball.sprite.rect.centery).normalize()


    pygame.display.update()
    clock.tick(game_speed)