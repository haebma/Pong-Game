import pygame
import random

'''TODO:    - draw ball as a circle (optional)
            - add custom ballsize- settings (easy, normal, hard) and with that different score_boards
            - prettier game_speed-growth function (slower in the end, little too fast)
            - create scoreboard logic (name and 10 best scores) 
            - add multiplayer -> stir racket with w/s and up/down
'''
class game_ball(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.radius = 30
        self.image = pygame.Surface((50, 50)) #pygame.image.load('graphics/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screenwidth/2, screenheight/2))
        # doesn't work
        self.image.fill(color, self.rect)
        # set initial moving y-direction randomly, move towards player first
        y = screenheight/2
        while screenheight/2 - 5 <= y <= screenheight/2 + 5:
            y = random.randint(0, screenheight)
        self.target = pygame.math.Vector2(screenwidth, y)
        self.v = pygame.math.Vector2(self.target.x - self.rect.centerx, self.target.y - self.rect.centery).normalize() # compute vector that represents the route between ball and target

    
    def get_pos(self):
        return self.rect.center
    
    def move(self):
        self.rect.centerx += 5 * self.v.x
        self.rect.centery += 5 * self.v.y # the greater the factor, the more fluent is the game!
        
    # does not yet work as supposed to, draws no circle, do in the end
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.radius)
    
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
        if position == 'left':
            self.rect = self.image.get_rect(midleft = (10, screenheight/2)) # create left racket
        else:
            self.rect = self.image.get_rect(midright = (screenwidth - 10, screenheight/2)) # create right racket

    def update(self, y_new):
        self.rect.centery = y_new


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # compute relative time (time that's passed since clicking mouse)
    score_surf = font.render(f'Score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center = (screenwidth/2, screenheight/5))
    screen.blit(score_surf, score_rect)
    return current_time


# Initialization
pygame.init()

# Global Variables

# adjustable :) -----------
ball_size = -1
initial_game_speed = 100
#--------------------------

score = 0
start_time = 0
game_speed = initial_game_speed

screenwidth = 1400
screenheight = 900
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Pong Game')
font = pygame.font.SysFont('Quantum Sans Serif Font', 100)
clock = pygame.time.Clock()
game_active = False

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
ball.add(game_ball((200, 200, 200)))


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
        screen.fill('#aa899a')
        score = display_score()

        # com racket constantly adapts to ball-position
        com_racket.update(ball.sprite.get_pos()[1])
        com_racket.draw(screen) # on screen

        player_racket.update(pygame.mouse.get_pos()[1])
        player_racket.draw(screen)

        ball.update()
        ball.draw(screen)

    else:
        screen.fill((94, 129, 162))

        if score == 0:
            # blit custom intro screen
            screen.blit(game_name, game_name_rect)
            screen.blit(intro_msg, intro_msg_rect)
        else:
            # print custom game over screen
            screen.blit(game_over_msg, game_over_rect)
            score_msg = font.render(f'Your Score: {score}', False, (255, 255, 255))
            score_rect = score_msg.get_rect(center = (screenwidth/2, screenheight*3/5))
            screen.blit(score_msg, score_rect)
            screen.blit(restart_msg, restart_rect)

            # reset variables
            game_speed = initial_game_speed
            ball.sprite.rect.center = (screenwidth/2, screenheight/2)
            y = screenheight/2
            while screenheight/2 - 5 <= y <= screenheight/2 + 5:
                y = random.randint(0, screenheight)
            ball.sprite.target = pygame.math.Vector2(screenwidth, y)
            ball.sprite.v = pygame.math.Vector2(ball.sprite.target.x - ball.sprite.rect.centerx, ball.sprite.target.y - ball.sprite.rect.centery).normalize()


    pygame.display.update()
    clock.tick(game_speed)