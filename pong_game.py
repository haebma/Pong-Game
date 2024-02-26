import pygame

class game_ball(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.radius = 30
        self.image = pygame.Surface((50, 50)) #pygame.image.load('graphics/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screenwidth/2, screenheight/2))
        self.image.fill(self.color, self.rect)

    def move(self):
        pass

    # does not yet work as supposed to, draws no circle
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.radius)
    
    def update(self):
        self.move()
        
class racket(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('graphics/racket.png').convert_alpha()
        if position == 'left':
            self.rect = self.image.get_rect(midleft = (10, screenheight/2)) # create left racket
        else:
            self.rect = self.image.get_rect(midright = (screenwidth - 10, screenheight/2)) # create right racket

    def move(self, y_pos):
        self.rect.y = y_pos

    def update(self, y_pos):
        self.move(self, y_pos)

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


# Objects/Groups
left_racket = pygame.sprite.GroupSingle()
left_racket.add(racket('left'))

right_racket = pygame.sprite.GroupSingle()
right_racket.add(racket('right'))

ball = pygame.sprite.GroupSingle()
ball.add(game_ball((255, 255, 255)))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                pass        

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
    # end of event loop
            

    if game_active:
        screen.fill((94, 129, 162))
        left_racket.draw(screen) # on screen
        right_racket.draw(screen)
        ball.draw(screen)

    else:
        # blit custom intro screen
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(intro_msg, intro_msg_rect)
    
    pygame.display.update()