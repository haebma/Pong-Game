import pygame
import random

'''TODO:    - fix move-function in game_ball
            - draw ball as a circle
            - create scoreboard logic (name and 10 best scores) 
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
        self.target = pygame.math.Vector2(screenwidth, random.randint(0, screenheight))
        self.v = pygame.math.Vector2(self.target.x - self.rect.centerx, self.target.y - self.rect.centery) # compute vector that represents the route between ball and target

    def get_pos(self):
        return self.rect.center
    
    def move(self):
        #v = v.move_towards(self.target, ball_speed_factor) # returns a vector moved toward the target by a given distance.
        print(f'target: {self.target}, {self.v.x}, {self.v.y}')
        #(x, y) = self.rect.center
        self.rect.centerx += ball_speed * self.v.x
        self.rect.centery += ball_speed * self.v.y

    # does not yet work as supposed to, draws no circle, do in the end
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.radius)
    
    def update(self):
        global game_active

        if self.rect.collidepoint(self.target.x, self.target.y):
            game_active = False
        elif self.rect.colliderect(player_racket.sprite.rect):
            pass
        elif self.rect.colliderect(com_racket.sprite.rect):
            pass
        
        
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
        (x,_) = self.rect.midright
        self.rect.midright = (x, y_new)

def normalize(x, y):
    res = 1/(x+y)

# Initialization
pygame.init()

screenwidth = 1400
screenheight = 900
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Pong Game')
font = pygame.font.SysFont('Quantum Sans Serif Font', 100)

clock = pygame.time.Clock()
game_active = False
game_name = font.render('Pong Game', False, (255,255,255))
game_name_rect = game_name.get_rect(center = (screenwidth/2, screenheight/3))
intro_msg = font.render('Press mouse to start', False, (255,255,255))
intro_msg_rect = intro_msg.get_rect(center = (screenwidth/2, screenheight*2/3))
ball_speed = 0.001 # must lay between 0 and 1


# Objects/Groups
com_racket = pygame.sprite.GroupSingle()
com_racket.add(racket('left'))

player_racket = pygame.sprite.GroupSingle()
player_racket.add(racket('right'))

ball = pygame.sprite.GroupSingle()
ball.add(game_ball((200, 200, 200)))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # quit game on close or esc
                pygame.quit()
                exit()

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                (x,y) = pygame.mouse.get_pos()
                player_racket.update(y)        

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
    # end of event loop
            

    if game_active:
        screen.fill('#aa899a')
        (_, y_new) = ball.sprite.get_pos()
        com_racket.update(y_new)
        com_racket.draw(screen) # on screen
        player_racket.draw(screen)
        ball.update()
        ball.draw(screen)

    else:
        # blit custom intro screen
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(intro_msg, intro_msg_rect)
    
    pygame.display.update()