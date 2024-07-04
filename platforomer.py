import pygame,os,time,random,math,pickle,sys

pygame.init()
pygame.mixer.init()
screen_width = 1500
screen_heigth = 900      
fps = 60

screen = pygame.display.set_mode((screen_width,screen_heigth))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mario = pygame.image.load("1691046555_grizly-club-p-kartinki-mario-pikselnii-bez-fona-15_pixian_ai — копия.png").convert_alpha()
background = pygame.image.load("i.webp").convert()
block_image = pygame.image.load("png-transparent-bricks-block-cub.png").convert_alpha()
question_object_image = pygame.image.load("dc935zl-26497f72-5a96-4677-a9fc-827d190a106b.png").convert_alpha()
enemy_image = pygame.image.load("gratis-png-mario-bros-nuevo-super-mario-bros-mario-kart-7-papel-mario-mario-thumbnail.png").convert_alpha()
grib_image = pygame.image.load("th (1).png")
black_hole_image = pygame.image.load("png-transparent-ultra-high-definition-television-desktop-4k-resolution-display-resolution-others-miscellaneous-desktop-wallpaper-theme-thumbnail.png")
green_obj = pygame.image.load("i16.png")

my_font = pygame.font.SysFont("Times New Roman",20)
 
score = 0
life = 0
 
 
block_group = pygame.sprite.Group()
question_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
blackholes_group = pygame.sprite.Group()
green_object_group = pygame.sprite.Group()

player_speed = 3
jump_strength = -17
gravity = 0.9

#*Super Jump
super_jump = -25
gravity = 0.7


#* scrolling bk
scrolling = 0


jumping = -5
graviti_fols = 0.5

pygame.mixer.music.load("super-mario-saundtrek.mp3")
pygame.mixer.music.play(1)

collision = False
collision_time = pygame.time.get_ticks()

mario_images = [
    pygame.image.load("1691046555_grizly-club-p-kartinki-mario-pikselnii-bez-fona-15_pixian_ai — копия.png"),pygame.image.load("1691046555_grizly-club-p-kartinki-mario-pikselnii-bez-fona-14_pixian_ai.png"),
    pygame.image.load("1691046555_grizly-club-p-kartinki-mario-pikselnii-bez-fona-15_pixian_ai.png"),pygame.image.load("1691046555_grizly-club-p-kartinki-mario-pikselnii-bez-fona-16_pixian_ai.png")
]

#* Анимация
mario_image_number = 0

delay = 0

class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (30,screen_heigth - 135)
        self.is_jump = False
        self.speedy = 0
        self.cooldown = 500



    def update(self):
        self.speedx = 0
        global mario_image_number
        keys = pygame.key.get_pressed()
        global delay
        #* Delay
        delay += pygame.time.get_ticks()
        if delay > 5000:
            delay = 0
        if keys[pygame.K_RIGHT] and delay == 0:
            self.speedx += player_speed
            #TODO scrolling bk if player used right keyboard
            global scrolling
            scrolling -= 5
                    #* Анимация
            mario_image_number += 1
            if mario_image_number >= 4:
                mario_image_number = 0


        
        if keys[pygame.K_LEFT]:
            self.speedx -= player_speed
        #TODO Прыжок
        if keys[pygame.K_UP] and not self.is_jump:
            self.speedy = jump_strength
            self.is_jump = True
            pygame.mixer.music.load("maro-jump-sound-effect_1.mp3")
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.1)

        if keys[pygame.K_SPACE] and not self.is_jump:
            self.speedy = super_jump
            self.is_jump = True
            pygame.mixer.music.load("maro-jump-sound-effect_1.mp3")
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.1)
        


        #TODO Прыжок
        self.speedy += gravity
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right >= screen_width / 2:
            self.rect.right = screen_width / 2
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0:
            self.rect.top = 0
       
       #TODO Прыжок
        if self.rect.bottom >= screen_heigth - 115 :
            self.rect.bottom = screen_heigth - 115
            self.speedy = 0
            self.is_jump = False
    

 


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = random.randint(800,2000)
        self.image = block_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.direction ,555)
        self.is_jump = False
        self.speedy = 0
 


    def update(self):
        #* Чтобы объект двигался вместе с фоном(в self.rect.x добавляем значение столько сколько в scrolling)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5

        if pygame.sprite.collide_rect(player,enemy) and not self.is_jump:
            self.speedy = jumping
            self.is_jump = True

        
        self.speedy += graviti_fols
        self.rect.y += self.speedy
    

        
        if self.rect.bottom >= 555:
            self.rect.bottom = 555
            self.speedy = 0
            self.is_jump = False
        
        if self.rect.left <= 0:
            self.kill()

class Question_Objects(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = random.randint(700,3000)
        self.image = question_object_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.direction,555)
        self.is_jump = False
        self.speedy = 0


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5
        
        if pygame.sprite.collide_rect(player,question_object) and not self.is_jump:
            self.speedy = jumping
            self.is_jump = True
            global score
            score += 10
            if score == 100 or score == 200 or  score  == 400: 
                global life
                life += 1
            
         
        self.speedy += graviti_fols
        self.rect.y += self.speedy

        if self.rect.bottom >= 555:
            self.rect.bottom = 555
            self.speedy = 0
            self.is_jump = False
        
        if self.rect.left <= 0:
            self.kill()

class Enemy_Object(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.direction = random.randint(800,3000)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.direction,screen_heigth - 145)

    def update(self):
        if self.rect.left <= 0:
            self.kill()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5
        else:
            self.rect.x -= 5
        
        
        global life
        if pygame.sprite.groupcollide(all_sprites,enemy_group,False,False):
            if life >= 1 :
                life -= 1
                player.kill()
            else:
                global running
                if life <= 0:
                    running = False



        
class Black_Hole(pygame.sprite.Sprite):
    def __init__(self,image):
        self.direction = random.randint(1600,4000)
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.direction,screen_heigth - 135)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x  -= 5


        if pygame.sprite.groupcollide(all_sprites,green_object_group,False,False) and pygame.sprite.groupcollide(all_sprites,enemy_group,False,False):
            global running
            print("Hello")
            running = True
        elif pygame.sprite.groupcollide(all_sprites,blackholes_group,True,True):
                running = False


        if self.rect.left <= 0:
            self.kill()

             
class Green_Object(pygame.sprite.Sprite):
    def __init__(self,image):
        self.direction = random.randint(1500,4000)
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.direction,screen_heigth - 220)



    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5

        if self.rect.left <= 0:
            self.kill()
        
        if pygame.sprite.groupcollide(all_sprites,green_object_group,False,False):
            player.rect.right = green_object.rect.right



player = Player(mario_images[mario_image_number])
all_sprites.add(player)


#* Получаем ширину для бесконечного фона
background_width = background.get_width()
background_height = background.get_height()

jump_block = -15
gravity_block = 0.9

is_jump = False
speed_y = 0
running = True
randomNumber = random.randint(1,1500)


button_surface = pygame.Surface((150,50))
button_text = my_font.render("Start the game",True,(0,0,0))
button_text_rect = button_text.get_rect(center = (button_surface.get_width() / 2,button_surface.get_height() /2 ))
button_rect = pygame.Rect(300,200,400,900)


quit_surface = pygame.Surface((150,50))
quit_text = my_font.render("Quit game",True,(0,0,0))
quit_text_rect = quit_text.get_rect(center = (quit_surface.get_width() / 2, quit_surface.get_height() / 2))
quit_rect = pygame.Rect(900,200,500,900)

main_menu = False
while (main_menu == False):
    screen.fill((192,192,192))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = True
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                main_menu = True
    


    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_surface,(127,127,212),(1,1,148,48))
    else:
        pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 148, 48))
        pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
        pygame.draw.rect(button_surface, (0, 100, 0), (1, 48, 148, 10), 2)

    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if quit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()



    if quit_rect.collidepoint(pygame.mouse.get_pos()):
       pygame.draw.rect(quit_surface,(192,192,192),(1,1,148,48))
    else:
        pygame.draw.rect(quit_surface, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(quit_surface, (255, 255, 255), (1, 1, 148, 48))
        pygame.draw.rect(quit_surface, (0, 0, 0), (1, 1, 148, 1), 2)
        pygame.draw.rect(quit_surface, (0, 100, 0), (1, 48, 148, 10), 2)



    button_surface.blit(button_text,button_text_rect)
    screen.blit(button_surface,(button_rect.x,button_rect.y))

    quit_surface.blit(quit_text,quit_text_rect)
    screen.blit(quit_surface,(quit_rect.x,quit_rect.y))
    pygame.display.flip()



paused = False
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    if not paused:


        if len(all_sprites) == 0:
            player = Player(mario_images[mario_image_number])
            all_sprites.add(player)
        all_sprites.update()
    

        #* Добавление enemy(Block)
        #TODO Добавляем множество врагов от одного объекта
        if len(block_group) == 0:
            enemy = Block()
            block_group.add(enemy)
        
        block_group.update()
        #*Добавление question_Objects()
        if len(question_group) == 0:
            question_object = Question_Objects()
            question_group.add(question_object)
        
        question_group.update()

        if len(enemy_group) <= 1:
            mario_enemy = Enemy_Object(enemy_image)
            enemy_grib = Enemy_Object(grib_image)
            enemy_group.add(mario_enemy)
            enemy_group.add(enemy_grib)
        enemy_group.update()

        if len(blackholes_group) == 0:
            black_hole = Black_Hole(black_hole_image)
            blackholes_group.add(black_hole)

        blackholes_group.update()

        if len(green_object_group) == 0:
            green_object = Green_Object(green_obj)
            green_object_group.add(green_object)
        
        green_object_group.update()



        #* Endlessly scrolling background_image
        x_offset = scrolling % background.get_width() 
        screen.blit(background,(x_offset - background.get_width(),0))
        screen.blit(background,(x_offset,0))
        if x_offset < screen_width:
            screen.blit(background,(x_offset + background_width,0))



        text_surface = my_font.render(f"Score: {score}",True,(0,0,0))
        text_life = my_font.render(f"Life: {life}",True,(0,0,0))
        screen.blit(text_surface,(10,10))
        screen.blit(text_life,(10,50))
        # all_sprites.draw(screen)
        block_group.draw(screen)
        question_group.draw(screen)
        enemy_group.draw(screen)
        #* Анимация
        screen.blit(mario_images[mario_image_number],player)
        blackholes_group.draw(screen)
        green_object_group.draw(screen)

        
        pygame.display.flip() 







pygame.quit()
 
