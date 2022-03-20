from assets import *
from environment import *

WIN_ON = True

with open("model.pickle", "rb") as f:
    net = pickle.load(f)

keys_pressed = pygame.key.get_pressed()

ball = Ball(50, 50, (255, 255, 255))
paddle = Paddle(390, 5, (0, 255, 0))
ai_paddle = Paddle(400, 390, (255, 0, 0))
def draw_window(screen): 
    screen.fill((0,0,0))
    ball.draw(screen)
    paddle.draw(screen)
    ai_paddle.draw(screen)

def play():
    global WIN_ON
    score = 0
    ai_score = 0

    clock = pygame.time.Clock()
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.move_left()
                elif event.key == pygame.K_RIGHT:
                    paddle.move_right()
                elif event.key == pygame.K_SPACE:
                    from menu import main_menu
                    main_menu()
            elif event.type == pygame.KEYUP:
                paddle.move_stop()
            
        if ball.collide(paddle): 
            ball.change_vel_y()
            ai_score +=1
        if ball.collide(ai_paddle): 
            ball.change_vel_y()
            score += 1
        if ball.get_y() + ball.rect.height >= HEIGHT:
            score = 0
        if ball.get_y() <= 0:
            ai_score = 0 
            

        output = net.activate((ai_paddle.get_x(), abs(ai_paddle.get_y() - ball.rect.y), ball.rect.x))
        if output[0] > output[1]:
            if output[0] > 0.5:
                ai_paddle.move_left()
            else:
                ai_paddle.move_stop()
        elif output[1] > 0.5:
            ai_paddle.move_right()
        else:
            ai_paddle.move_stop()

        if WIN_ON:
            ball.move()
            paddle.move()
            ai_paddle.move()
            draw_window(screen) 

        if WIN_ON: 
            clock.tick(60) 
        
        font = pygame.font.SysFont(None, 25) 
        score_text = font.render(f"AI Score: {str(score)}", False, (255, 255, 255))
        ai_score_text = font.render(f"Player Score: {str(ai_score)}", False, (255, 255, 255))
        screen.blit(score_text, (800-10-score_text.get_width(), 10))   
        screen.blit(ai_score_text, (800-10-ai_score_text.get_width(), 40))          
        pygame.display.update()
