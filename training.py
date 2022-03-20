from assets import *
import time 
import os

GEN = 0
WIN_ON = True

def draw_window(screen, paddles, balls, obstacles): 

    screen.fill((0,0,0))

    for ball in balls:
        ball.draw(screen)

    for paddle in paddles:
        paddle.draw(screen)
    
    for obstacle in obstacles:
        obstacle.draw(screen)

    score_label = STAT_FONT.render("Gens: " + str(GEN-1),1,(255,255,255))
    screen.blit(score_label, (800-10-score_label.get_width(), 10))
    score_label2 = STAT_FONT.render("Alive: " + str(len(paddles)),1,(255,255,255))
    screen.blit(score_label2, (800-10-score_label2.get_width(), 50))
    pygame.display.flip()


def random_sign():
    i = random.randint(0,1)
    if i == 0:
        return -1
    return 1

def eval_genomes(genomes, config):
    global GEN
    global WIN_ON
    GEN += 1
    score = 0
    paddles = []
    balls = []
    nets = [] 
    ge = [] 

    for _, g in genomes:
        tmp_color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        paddles.append(Paddle(100,390,tmp_color))
        balls.append(Ball(random.randint(100,255),random.randint(100,255),tmp_color))
        g.fitness = 0
        ge.append(g)
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
    t0 = time.time() 
    user_stop = False 
    while run and len(paddles) > 0:
        if WIN_ON: clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    user_stop = True 
                    break
        if user_stop:
            break
        for x_c, paddle in enumerate(paddles):
            paddle.move()
            outputs = nets[paddles.index(paddle)].activate((paddle.get_x(),
                                    abs(paddle.get_y() - balls[paddles.index(paddle)].rect.y),
                                    balls[paddles.index(paddle)].rect.x))
            if outputs[0] > outputs[1]:
                if outputs[0] > 0.5:
                    paddle.move_left()
                    ge[x_c].fitness += 0.5
                else:
                    ge[x_c].fitness -= 1
                    paddle.move_stop()
            elif outputs[1] > 0.5:
                paddle.move_right()
                ge[x_c].fitness += 0.5
            else:
                ge[x_c].fitness -= 1
                paddle.move_stop()

        for ball in balls:
            ball.move()
            if ball.collide(paddles[balls.index(ball)]): 
                ball.change_vel_y()
                ge[balls.index(ball)].fitness += 5
                score += 1
            if ball.get_y() + ball.rect.height >= HEIGHT:
                ge[balls.index(ball)].fitness -= 2
                nets.pop(balls.index(ball))
                ge.pop(balls.index(ball))
                paddles.pop(balls.index(ball))
                balls.pop(balls.index(ball))

            for cnt, obstacle in enumerate(obstacles):
                if ball.collide(obstacle):
                    obstacle.movement(boundaries[cnt])
                    ball.change_vel_y()
                    ball.vel[0] *= random_sign()

        elapsed = time.time() - t0
        if elapsed > 30:
            with open("model.pickle", "wb") as f:
                pickle.dump(nets[0], f)
            break
        if WIN_ON:
            draw_window(screen, paddles, balls, obstacles)
    if user_stop:
        from menu import main_menu
        GEN = 0
        main_menu()


def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')

