import pygame, random
from gamemaps import *

#Use 2D vectors
vector = pygame.math.Vector2

#Initialize pygame
pygame.init()

#Set display surface (tile size is 32x32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Faster and Faster")


spawn_points = {
    0: (120, 650), 
    1: (50, 300),  
    2: (640, 74),   
    3: (122, 110),
    4: (120, 120),
    5: (50, 746),
}
#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()
mapnum = 0

class HUD():

    def __init__(self):
        self.score = 0
        self.levels_completed = 0
        self.juice_collected = 0
        self.remaining_time = 10000
        self.remaining_default = 10000

        self.score_font = pygame.font.Font("fonts/font2.otf", 32)
        self.juice_font = pygame.font.Font("fonts/font2.otf", 16)
        self.hud_font = pygame.font.Font("fonts/font4.otf", 16)

        pygame.mixer.music.load("sounds/soundtrack.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 1.5)

        self.juice_drink_sound = pygame.mixer.Sound("sounds/juicedrink.mp3")
        self.next_level_sound = pygame.mixer.Sound("sounds/nextlevel.mp3")
        self.jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
        self.ghost_sound = pygame.mixer.Sound("sounds/ghostlaugh.ogg")
        self.ghost_sound.set_volume(0.2)
        self.lava_sound = pygame.mixer.Sound("sounds/lava.mp3")
        self.lava_sound.set_volume(0.5)


    def draw(self):

        WHITE = (255,255,255)
        GREEN = (25,200,25)
        BLACK = (0, 0, 0)

        title_text = self.hud_font.render("Faster and Faster", True, WHITE)
        title_text_rect = title_text.get_rect()
        title_text_rect.topleft = (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 800)

        score_text = self.score_font.render("Score: " +str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 380, WINDOW_HEIGHT - 780)

        juice_text = self.juice_font.render("Juice collected: " +str(self.juice_collected), True, WHITE)
        juice_rect = juice_text.get_rect()
        juice_rect.topleft = (WINDOW_WIDTH - 180, WINDOW_HEIGHT - 780)

        level_text = self.juice_font.render("Levels completed: " +str(self.levels_completed), True, WHITE)
        level_rect = level_text.get_rect()
        level_rect.topleft = (WINDOW_WIDTH - 180, WINDOW_HEIGHT - 760)

        display_surface.blit(title_text, title_text_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(juice_text, juice_rect)
        display_surface.blit(level_text, level_rect)
        self.remaining_time -= 10
        if self.remaining_time <= 0:
            self.remaining_time = 0

#Define classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        #Load in the correct image and add it to the correct sub groups
        if image_int == 1:
            self.image = pygame.image.load("tileset/images/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("tileset/images/grass.png")
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("tileset/images/water.png")
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.image.load("tileset/images/lava.png")
            sub_group.add(self)
        elif image_int == 5:
            self.trophy_source = pygame.image.load("tileset/images/trophy.png")
            self.image = pygame.transform.scale_by(self.trophy_source, 0.10)
            sub_group.add(self)
        elif image_int == 6:
            self.juice_source = pygame.image.load("tileset/images/juice.png")
            self.image = pygame.transform.scale_by(self.juice_source, 0.25)
            sub_group.add(self)
        
        #Add every tile to the main tile group
        main_group.add(self)

        #Get the rect of the image and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Player(pygame.sprite.Sprite):
    """A player class the user can control"""

    def __init__(self, x, y, grass_tiles, lava_tiles, trophy_tiles, juice_tiles):
        super().__init__()

        #Animation Frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []

        #Moving
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (1).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (2).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (3).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (4).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (5).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (6).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (7).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (8).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (9).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (10).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (11).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (12).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (13).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (14).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (15).png"), (64,64)))
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #Idling
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (1).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (8).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (9).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (10).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (11).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (12).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (13).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (14).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (15).png"), (64,64)))
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Jumping
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (6).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (7).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (8).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (9).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (10).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (11).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (12).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (13).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (14).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Jump (15).png"), (64,64)))
        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))
            
        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.animate_jump = False

        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.lava_tiles = lava_tiles
        self.trophy_tiles = trophy_tiles
        self.juice_tiles = juice_tiles
        
        #Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        #Kinematic constants
        self.HORIZONTAL_ACCELERATION = 0.8
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = .5 #Gravity
        self.VERTICAL_JUMP_SPEED = 12 #Detemerines how high we can jump
       


    def update(self): 
        #Create a mask
        self.mask = pygame.mask.from_surface(self.image)

        self.move()
        self.check_collisions()


    def move(self):
        #Set the accleration vector to (0, 0) so there is initially no acceleration
        #If there is no force (no key presses) acting on the player then accerlation should be 0
        #Vertical accelration (gravity) is present always regardless of key-presses
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        #If the user is presseing a key, set the x-component of the accleration vector to a non zero value.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .2)
            else:
                self.animate(self.idle_left_sprites, .2)

         #Check if player is jumping
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, .05)
            else:
                self.animate(self.jump_left_sprites, .05)


        #Calculate new kinematics values (2, 5) + (1, 6) = (3, 11)
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update new rect based on kinematic calculations
        if self.position.x < -10:
            self.position.x += self.HORIZONTAL_ACCELERATION * 10
        elif self.position.x > WINDOW_WIDTH - 50:
            self.position.x -= self.HORIZONTAL_ACCELERATION * 10
        #Stop the player from running out of bounds
        if self.position.y >= 820:
            self.position.y = WINDOW_HEIGHT - 200

        self.rect.bottomleft = self.position

    def check_collisions(self):
        #Check for collisions with the grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if collided_platforms:
            #Only move to the platform if the player is falling down
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top + 10
                self.velocity.y = 0
                if self.animate_jump:
                    self.animate_jump = False

        # Check for collisions with the juice tiles
        collided_juice = pygame.sprite.spritecollide(self, self.juice_tiles, False)
        if collided_juice:
            self.HORIZONTAL_ACCELERATION += 0.2
            gamehud.juice_drink_sound.play()
            gamehud.juice_collected += 1
            gamehud.score += 500
            for juice in collided_juice:
                juice.kill()

        # Check for collisions with Monsters
        collided_monsters = pygame.sprite.spritecollide(self, monster_group, False, pygame.sprite.collide_mask)
        if collided_monsters:
            gamehud.ghost_sound.play()
            self.position = vector(self.starting_x, self.starting_y)
            self.rect.bottomleft = self.position
            gamehud.score -= 200
               
        # Check for collisions with the trophy tiles
        if pygame.sprite.spritecollide(self, self.trophy_tiles, False):
            gamehud.next_level_sound.play()
            gamehud.levels_completed += 1
            gamehud.score += gamehud.remaining_time
            gamehud.remaining_time = gamehud.remaining_default

            monster_group.empty()

            global mapnum
            mapnum += 1
            if mapnum >= len(all_maps):
                print(f"Invalid mapnum: {mapnum}")
                mapnum = random.randint(0, len(all_maps) - 1)
            print(f"Map changed to: {mapnum}")
            update_map(mapnum)

            # Move player to the new spawn point based on the current map
            if mapnum in spawn_points:
                new_spawn_x, new_spawn_y = spawn_points[mapnum]
                self.position = vector(new_spawn_x, new_spawn_y)
                self.rect.bottomleft = self.position  # Update the rect as well
                self.starting_x = new_spawn_x
                self.starting_y = new_spawn_y
                

        #Check for collisions with the lava tiles
        if pygame.sprite.spritecollide(self, self.lava_tiles, False):
            gamehud.lava_sound.play()
            self.position = vector(self.starting_x, self.starting_y)
            self.rect.bottomleft = self.position 
            gamehud.score -= 5000
  
    def jump(self):
        #Only jump if on a grass tile
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def animate(self, sprite_list, speed):
        #Loop through the sprite list changing the current sprite
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed 
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rawimg = pygame.image.load("tileset/images/monster.png")
        self.image = pygame.transform.scale_by(self.rawimg, 0.25)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = random.choice([-1, 1])  # 1 for moving right, -1 for left
        self.speed = random.randint(2,4)  # The speed of the monster

        self.mask = pygame.mask.from_surface(self.image)
        

    def update(self):
        # Make the monster move horizontally
        self.rect.x += self.speed * self.direction

        # If the monster hits the edges of the screen, reverse direction
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.direction *= -1  

    def check_collision(self, player):
        return pygame.sprite.collide_mask(player, self.mask)

#Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
lava_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
lava_tile_group = pygame.sprite.Group()
trophy_group = pygame.sprite.Group()
juice_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()

#Initialize player
my_player = Player(120, 650, grass_tile_group, lava_tile_group, trophy_group, juice_group)
my_player_group.add(my_player)

gamehud = HUD()

#Create individual Tile objects from the tile map
#Loop through the 20 lists in tile_map (i moves us down the map)
current_map = all_maps[mapnum]
for i in range(len(current_map)):
    #Loop through the 30 elements in a given list (j moves us across the map)
    for j in range(len(current_map[i])):
        if current_map[i][j] == 1: # Dirt
            Tile(j*32, i*32, 1, main_tile_group)
        elif current_map[i][j] == 2: # Ground
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif current_map[i][j] == 5: # Lava
            Tile(j*32, i*32, 4, main_tile_group, lava_tile_group)
        elif current_map[i][j] == 6: # Trophy
            Tile(j*32, i*32, 5, main_tile_group, trophy_group)
        elif current_map[i][j] == 7: # Juice
            Tile(j*32, i*32, 6, main_tile_group, juice_group)
        elif current_map[i][j] == 8: # Monster
            monster = Monster(j*32, i*32)
            monster_group.add(monster)

def update_map(mapnum):
    for tile in main_tile_group:
        tile.kill()
        
    current_map = all_maps[mapnum]
    
     # Add new tiles to the groups based on the selected map
    for i in range(len(current_map)):
        for j in range(len(current_map[i])):
            tile_type = current_map[i][j]
            if tile_type == 0:
                continue  
            x = j * 32  
            y = i * 32  
            if tile_type == 1:  # Dirt
                Tile(x, y, 1, main_tile_group)
            elif tile_type == 2:  # Ground
                Tile(x, y, 2, main_tile_group, grass_tile_group)
            elif tile_type == 5:  # Lava
                Tile(x, y, 4, main_tile_group, lava_tile_group)
            elif tile_type == 6:  # Trophy
                Tile(x, y, 5, main_tile_group, trophy_group)
            elif tile_type == 7:  # Juice
                Tile(x, y, 6, main_tile_group, juice_group)
            elif tile_type == 8:  #Monster
                monster = Monster(j*32, i*32)
                monster_group.add(monster)
                


#Load in a background image
background_image = pygame.image.load(f"backgrounds/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

#The main game loop
running = True
while running:
    #print(my_player.position)
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Player wants to jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()
                gamehud.jump_sound.play()
            if event.key == pygame.K_RETURN:
                mapnum += 1
                update_map(mapnum)

                

    #Blit the background
    display_surface.blit(background_image, background_rect)

    #Draw tiles
    main_tile_group.draw(display_surface)
    main_tile_group.update()

    #Update and draw sprites
    my_player_group.update()
    monster_group.update()
    my_player_group.draw(display_surface)
    monster_group.draw(display_surface)  

    gamehud.draw()
    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()