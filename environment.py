from assets import *

WIN_ON = True

with open("model.pickle", "rb") as f:
    net = pickle.load(f)

keys_pressed = pygame.key.get_pressed()

ball = Ball(50, 50, (255, 255, 255))
paddle = Paddle(400, 390, (255, 0, 0))
def draw_window(screen, obstacles): 
    screen.fill((0,0,0))

    ball.draw(screen)
    paddle.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

def main():
    global WIN_ON
    score = 0

    clock = pygame.time.Clock()

    obstacle_count = 10 
    obstacles = []
    boundaries = [(0, 40, 90, 200),(0, 40, 90, 200), (100, 40, 190, 200), (200, 40, 290, 200),  (300, 40, 390, 200), (300, 40, 390, 200),  (400, 40, 490, 200), (500, 40, 590, 200), (500, 40, 590, 200), (600, 40, 660, 200)]
    cnt = 0
    for _ in range(obstacle_count):
        obstacle = Obstacle(50, 6, (255, 255, 255))
        obstacle.movement(boundaries[cnt])
        obstacles.append(obstacle)
        cnt += 1
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from menu import main_menu
                    main_menu()
        if ball.collide(paddle): 
            ball.change_vel_y()
            score += 1
        if ball.get_y() + ball.rect.height >= HEIGHT:
            score = 0

        output = net.activate((paddle.get_x(), abs(paddle.get_y() - ball.rect.y), ball.rect.x))
        if output[0] > output[1]:
            if output[0] > 0.5:
                paddle.move_left()
            else:
                paddle.move_stop()
        elif output[1] > 0.5:
            paddle.move_right()
        else:
            paddle.move_stop()

        if WIN_ON:
            ball.move()
            paddle.move()
            draw_window(screen, obstacles) 

        for cnt, obstacle in enumerate(obstacles):
            if ball.collide(obstacle):
                obstacle.movement(boundaries[cnt])
                ball.change_vel_y()
                ball.vel[0] *= random_sign()
            
        if WIN_ON: 
            clock.tick(60) 
       
        score_text = font.render(f"Score: {str(score)}", False, (255, 255, 255))
        screen.blit(score_text, (800-10-score_text.get_width(), 10))          
        pygame.display.update()
