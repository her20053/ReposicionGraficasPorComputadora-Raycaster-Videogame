import math
import pygame

from pygame import mixer

BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)

SKY = (135,206,235)
GROUND = (55,62,76)

TRASNPARENT = (152,0,136,255)

colors = [
    (0,20,10),
    (4,40,63),
    (0,91,82),
    (219,242,38),
    (21,42,138)
]

wall1 = pygame.image.load("./assets/textures/wool_colored_yellow.png")
wall2 = pygame.image.load("./assets/textures/stone_andesite_smooth.png")
wall3 = pygame.image.load("./assets/textures/wool_colored_silver.png")
wall4 = pygame.image.load("./assets/textures/planks_birch.png")
wall5 = pygame.image.load("./assets/textures/wool_colored_gray.png")

sprite1 = pygame.image.load("./assets/sprite1.png")
sprite2 = pygame.image.load("./assets/sprite2.png")

walls = {
    "1": wall1,
    "2": wall2,
    "3": wall3,
    "4": wall4,
    "5": wall5,
}

enemies = [
    {
        "x":90,
        "y":90,
        "sprite": sprite1,
    },
    {
        "x":300,
        "y":300,
        "sprite": sprite2,
    }
]

mapa_seleccionado = './assets/map.txt'

class RaycasterClass(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.worldmap = []
        self.player = {
            "x": int(self.blocksize + self.blocksize /  2),
            "y": int(self.blocksize + self.blocksize /  2),
            "fov": int(math.pi / 3),
            "a":int(math.pi / 3),
        }
    
    def point(self, x,y,c = WHITE):
        self.screen.set_at((x,y), c)

    def block(self,x,y, wall):
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i-x) * 128 / self.blocksize)
                ty = int((j-y) * 128 / self.blocksize)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)
    
    def load_map(self, path):
        with open(path, 'r') as file:
            for line in file.readlines():
                self.worldmap.append(list(line))

    def cast_ray(self, angle):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]
        while True:
            x = int(ox + d * math.cos(angle))
            y = int(oy + d * math.sin(angle))
            if self.worldmap[y//self.blocksize][x//self.blocksize] != ' ':
                hitx = x - x//self.blocksize * self.blocksize
                hity = y - y//self.blocksize * self.blocksize
                
                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)

                return d, self.worldmap[y//self.blocksize][x//self.blocksize], tx


            self.point(x,y,WHITE)



            d += 1

    def draw_strake(self, x,h,c,tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for i in range(int(start_y), int(end_y)):
            ty = int((i-start_y) * 128 / height)
            color = walls[c].get_at((tx,ty))
            self.point(x,i,color)

    def draw_map(self):
        for x in range(0,500,self.blocksize):
            for y in range(0,500,self.blocksize):
                i = int(x//self.blocksize)
                j = int(y//self.blocksize)
                if self.worldmap[j][i] != ' ':


                    self.block(x,y, walls[self.worldmap[j][i]])
                    pass



    def draw_player(self):
        self.point(self.player["x"], self.player["y"], WHITE)

    def draw_sprite(self, sprite):

        sprite_a = math.atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        

        d = math.sqrt((sprite["x"] - self.player["x"])**2 + (sprite["y"] - self.player["y"])**2)
        sprite_size = int(500/d * 50)

        sprite_x = int(500 + (sprite_a - self.player["a"]) * 500 / self.player["fov"] + sprite_size/2)
        sprite_y = int(500/2 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x-sprite_x) * 128 / sprite_size)
                ty = int((y-sprite_y) * 128 / sprite_size)
                c = sprite["sprite"].get_at((tx,ty))
                if c != TRASNPARENT:
                    if x > 500:
                        self.point(x,y,c)


    def render(self):
        self.draw_player()
        self.draw_map()

        density = 50
        # Minimapa
        for i in range(0,density):
            a = self.player["a"] - (self.player["fov"] / 2) + (i * self.player["fov"] / density)
            d, c, _ = self.cast_ray(a)


        for i in range(0,500):
            self.point(499,i)
            self.point(500,i)
            self.point(501,i)

        # Jugador
        for i in range(0,int(self.width/2)):
            a = self.player["a"] - (self.player["fov"] / 2) + (i * self.player["fov"] / (self.width/2))
            d, c ,tx= self.cast_ray(a)

            x = int(self.width/2) + i
            h = self.height/(d * math.cos(a - self.player["a"])) * self.height/10

            self.draw_strake(x,h, c, tx)

        for enemy in enemies:
            self.draw_sprite(enemy)

class Proyecto3Raycaster():

    def iniciar(self):

        pygame.init()

        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial" , 40 , bold = True)

        screen = pygame.display.set_mode((1000,500))
        canvas = RaycasterClass(screen)
        canvas.load_map(mapa_seleccionado)
 
        def fps_counter():
            fps = str(int(clock.get_fps()))
            fps_text = font.render(fps, 1, pygame.Color("coral"))
            # screen.blit(fps_text, (10, 10))
            pygame.display.set_caption("Cantidad de FPS: " + fps)

        # mixer.init()
        # mixer.music.load('./assets/sounds/bgmusic.mp3')
        # mixer.music.set_volume(0.7)
        # mixer.music.play()

        mixer.music.load("./assets/sounds/bgmusic.mp3")
        mixer.music.play(-1)


        # efectopisada = pygame.mixer.music.load("./assets/sounds/footsteps.mp3")

        prev_mouse_pos = 750

        running = True
        while running:

            # print(clock.get_fps())

            mouse_position = pygame.mouse.get_pos()

            # print(mouse_position[0])

            clock.tick()
            fps_counter()

            screen.fill(BLACK, (0,0, canvas.width/2, canvas.height))

            screen.fill(SKY, (canvas.width/2,0,canvas.width,canvas.height/2))
            screen.fill(GROUND, (canvas.width/2,canvas.height/2,canvas.width,canvas.height/2))
            
            # screen.fill(GROUND)

            canvas.render()
            pygame.display.flip()

            # print(canvas.player["x"], canvas.player["y"])
            # print(screen.get_at((canvas.player["x"], canvas.player["y"])))
            


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if mouse_position[0] > 500 and mouse_position[0] < 1000:
                    if mouse_position[0] > prev_mouse_pos:
                        canvas.player["a"] += math.pi/10
                    elif mouse_position[0] < prev_mouse_pos:
                        canvas.player["a"] -= math.pi/10
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:

                        if screen.get_at((canvas.player["x"] + 5, canvas.player["y"])) == (0, 0, 0, 255) or screen.get_at((canvas.player["x"] + 5, canvas.player["y"])) == (255, 255, 255, 255):
                            canvas.player["x"] += 5
                        
                        fstsound = mixer.Sound("./assets/sounds/footsteps.mp3")
                        fstsound.play()

                    if event.key == pygame.K_LEFT:

                        # print(screen.get_at((canvas.player["x"] - 5, canvas.player["y"])))
                        if screen.get_at((canvas.player["x"] - 5, canvas.player["y"])) == (0, 0, 0, 255) or screen.get_at((canvas.player["x"] - 5, canvas.player["y"])) == (255, 255, 255, 255):
                            canvas.player["x"] -= 5

                        # canvas.player["x"] -= 5

                        fstsound = mixer.Sound("./assets/sounds/footsteps.mp3")
                        fstsound.play()

                    if event.key == pygame.K_UP:

                        if screen.get_at((canvas.player["x"], canvas.player["y"] - 5)) == (0, 0, 0, 255) or screen.get_at((canvas.player["x"], canvas.player["y"] - 5)) == (255, 255, 255, 255):
                            canvas.player["y"] -= 5

                        fstsound = mixer.Sound("./assets/sounds/footsteps.mp3")
                        fstsound.play()

                    if event.key == pygame.K_DOWN:

                        if screen.get_at((canvas.player["x"], canvas.player["y"] + 5)) == (0, 0, 0, 255) or screen.get_at((canvas.player["x"], canvas.player["y"] + 5)) == (255, 255, 255, 255):
                            canvas.player["y"] += 5

                        fstsound = mixer.Sound("./assets/sounds/footsteps.mp3")
                        fstsound.play()


                    if event.key == pygame.K_a:
                        canvas.player["a"] -= math.pi/10
                    if event.key == pygame.K_d:
                        canvas.player["a"] += math.pi/10

if "__main__" == __name__:

    def main_menu():

        pygame.init()
        screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Menu Principal")
        font = pygame.font.SysFont("arialblack" , 40 , bold = True)
        opcionesFont = pygame.font.SysFont("arialblack" , 30 , bold = False)
        TXT_COLOR = (255,255,255)
        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        run = True
        screen.fill((52,78,91))
        draw_text('Proyecto 3 Raycaster', font, TXT_COLOR, 150, 200)
        draw_text('Presionar 1 para cargar primer mapa', opcionesFont, TXT_COLOR, 70, 300)
        draw_text('Presionar 2 para cargar segundo mapa', opcionesFont, TXT_COLOR, 60, 350)
        while run:
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        # print("1")
                        proyecto = Proyecto3Raycaster()
                        proyecto.iniciar()
                        pass
                    if event.key == pygame.K_2:
                        # print("2")
                        global mapa_seleccionado
                        mapa_seleccionado = './assets/map2.txt'
                        proyecto = Proyecto3Raycaster()
                        proyecto.iniciar()
                        pass
        
        
            
    main_menu()
    