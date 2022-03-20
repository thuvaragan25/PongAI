from assets import *

font = pygame.font.SysFont(None, 100)

def main_menu():
    global click
    click = False
    while True:
 
        screen.fill((0,0,0))
        draw_text('PONG', font, (255, 255, 255), screen, 300, 50)
 
        mx, my = pygame.mouse.get_pos()

        button_1 = Button('TRAIN AI',200,50,(300,150), color= '#475F77')
        button_1.draw()
        button_2 = Button('WATCH',200,50,(300,210), color= (30, 144, 255))
        button_2.draw()
        button_3 = Button('PLAY',200,50,(300,270), color= (255, 0, 0))
        button_3.draw()

        if button_1.top_rect.collidepoint((mx, my)):
            if click:
                from training import run, config_path
                run(config_path)
        if button_2.top_rect.collidepoint((mx, my)):
            if click: 
                from environment import main 
                main()
        if button_3.top_rect.collidepoint((mx, my)):
            if click:
                from play import play
                play()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        mainClock.tick(60)

if __name__ == "__main__":
    main_menu()