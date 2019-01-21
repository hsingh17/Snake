import pygame
import random
import time


class Snake:
    def __init__(self):
        self.body = [(250,250), (240,250), (230,250)]
        self.head = self.body[0]
        self.tail = self.body[len(self.body) - 1]

    def move(self, x_velocity, y_velocity):
        new_body = []
        self.body.pop()
        x,y = self.head
        x += x_velocity
        y += y_velocity
        new_body.append((x,y))
        new_body.extend(self.body)
        self.body = new_body
        self.head = self.body[0]
        self.tail = self.body[len(self.body) - 1]
        
    def grow(self, x_velocity, y_velocity):
        x,y = self.tail
        x += x_velocity
        y += y_velocity
        self.body.append((x,y))
        self.tail = self.body[len(self.body) - 1]

    def check_collision(self):
        for segment in self.body[1:]:
            if self.head == segment:
                return True
    
    def check_outofbounds(self):
        for segment in self.body:
            x,y = segment
            if x >= 500 or x <= 0:
                return True
            elif y >= 500 or y <= 0:
                return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(window, (255,0,0), (*segment, 10, 10))

    def get_head_cords(self):
        return self.head


class Apple:
    def __init__(self):
       self.cords = (random.randrange(0,500,10), random.randrange(0,500,10)) 

    def spawn(self):
       self.cords = (random.randrange(0,500,10), random.randrange(0,500,10)) 

    def draw(self):
        pygame.draw.rect(window, (0,255,0), (*self.cords,10,10))

    def get_cords(self):
        return self.cords
    

def game_over():    
    game_over_msg = large_font.render('Game Over!', True, (0,0,0))
    instructions = small_font.render('Press Q to exit or R to restart!', True, (0,0,0))
    window.blit(instructions, (100, 240))
    window.blit(game_over_msg, (80, 160))

def display_score(score):
    score_msg = small_font.render(f'Score: {score}', True, (0,0,0))
    window.blit(score_msg, (30,30))


def game_loop():
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()
    current_direction = 1
    direction_velocity_pairs = [(0,-10), (10,0), (0,10), (-10,0)]
    x_velocity, y_velocity = direction_velocity_pairs[1]
    score = 0
    run = True
    lose = False

    while run:
        while lose:
            game_over()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                    elif event.key == pygame.K_q:
                        run = False
                        lose = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_velocity != 10:
                    current_direction = 3
                elif event.key == pygame.K_RIGHT and x_velocity != -10:
                    current_direction = 1
                elif event.key == pygame.K_UP and y_velocity != 10:
                    current_direction = 0
                elif event.key == pygame.K_DOWN and y_velocity != -10:
                    current_direction = 2

        x_velocity, y_velocity = direction_velocity_pairs[current_direction]    
        snake.move(x_velocity, y_velocity)
        
        if apple.get_cords() == snake.get_head_cords():
            score += 1
            apple.spawn()
            snake.grow(x_velocity, y_velocity)
        
        if snake.check_collision() or snake.check_outofbounds():
            lose = True

        window.fill((255,255,255))
        snake.draw()
        apple.draw()
        display_score(score)
        clock.tick(30)
        pygame.display.update()
        
    pygame.quit()

pygame.init()
pygame.font.init()

small_font = pygame.font.SysFont('Arial', 25, bold = 1)
large_font = pygame.font.SysFont('Arial', 75, bold = 1)
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake")

game_loop()
