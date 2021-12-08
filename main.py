import pygame


class Thing:
    image_path = "assets/not_found.jpg"
    image = pygame.image.load("assets/not_found.jpg")
    text = ""
    textSurface = None
    isText = False
    fontSize = 30
    pos_x = None
    pos_y = 0
    size_x = 0
    size_y = 0

    def __init__(self, image_path, pos_x, pos_y, size_x, size_y, isText, text="No Text", fontSize=30):
        self.image_path = image_path
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.isText = isText
        self.text = text
        self.fontSize = fontSize

    def draw_self(self, w):
        if self.isText:
            # Try assigning text
            try:
                myFont = pygame.font.SysFont('Comic Sans MS', self.fontSize)
                self.textSurface = myFont.render(self.text, False, (0, 0, 0))
            except:
                myFont = pygame.font.SysFont('Comic Sans MS', 30)
                self.textSurface = myFont.render("No Text", False, (0, 0, 0))

            w.blit(self.textSurface, (self.pos_x, self.pos_y))

        else:
            # Try assigning image path
            try:
                self.image = pygame.image.load(self.image_path)
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            except:
                self.image = pygame.image.load("assets/not_found.jpg")
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

            w.blit(scaled_image, (self.pos_x, self.pos_y))


window = pygame.display.set_mode((1200,600))
pygame.display.set_caption("StallionGames")
window.fill((255,255,255))
pygame.display.update()

pygame.font.init()

FPS = 100
clock = pygame.time.Clock()

state = 0
innerState = 0

# empty list of things to draw on screen
things = list()

# things that can be added
thing_intro_background = Thing("assets/intro_bg.jpg",0,0,1200,600,False)
thing_intro_text = Thing("",100,100,0,0,True,"Press Space to Start!",30)
thing_character_doll = Thing()
# TODO add remaining things

while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()

    # Main States tree
    if state == 0: # Intro screen
        # empty all things to draw
        things.clear()

        # add background and text to things to draw
        things.append(thing_intro_background)
        # TODO add logo
        things.append(thing_intro_text)

        # Check for space is entered
        if keys[pygame.K_SPACE]:
            innerState = 0 # reset inner state
            state = 1 # go to state 1 (Player selection screen)

    elif state == 1: # Character Selection
        # empty all things to draw
        things.clear()
        pass

    elif state == 2: # Level 1  (Red light, Green Light)
        get_ready_countdown = 3000 # 3000 frames

        if innerState == 0: # GET READY SCREEN
            # TODO handle this state as following:
            # Add the level background to things
            # Add a text "GET READY" to things , in the middle of screen
            # Add the 2 selected characters to things, positioned at the left of screen
            # Add the "Doll" character to things, at the right of screen

            # decrease countdown by one, if it reaches zero switch to next innerState
            # (Acts like a timer)
            get_ready_countdown -= 1
            if (get_ready_countdown == 0):
                innerState = 1

        elif innerState == 1: # GAME STILL ON GREEN LIGHT
            pass
        elif innerState == 2: # GAME STILL ON RED LIGHT
            pass
        elif innerState == 3: # PLAYER 1 WON
            pass
        elif innerState == 4: # PLAYER 2 WON
            pass

    elif state == 3: # level 2 (Candy Carving)
        pass

    elif state == 4: # level 3 (Tug of War)
        pass

    elif state == 5: # Level Winner screen
        pass

    elif state == 6: # Final winner screen
        pass

    # black out the screen
    window.fill((0,0,0))

    # draw everything in the list "things"
    for thing in things:
        thing.draw_self(window)

    # update the display
    pygame.display.update()


