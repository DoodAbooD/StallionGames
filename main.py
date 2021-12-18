import pygame
import copy


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


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("StallionGames")
window.fill((255, 255, 255))
pygame.display.update()

pygame.mixer.init()
redGreenLightSound = pygame.mixer.Sound("assets/red_green_sound_short.wav")


pygame.font.init()

FPS = 100
clock = pygame.time.Clock()

state = 0
innerState = 0

# empty list of things to draw on screen
things = list()

# things that can be added
thing_intro_background = Thing("assets/intro_bg.png", 0, 0, 1200, 600, False)
thing_intro_text = Thing("", 400, 500, 0, 0, True, "Press Space to Start!", 30)
thing_character_doll = Thing("assets/char_doll.png", 0, 0, 100, 300, False)
thing_character_saif = Thing("assets/char_saif.png", 0, 0, 100, 180, False)
thing_character_nadeen = Thing("assets/char_nadeen.png", 0, 0, 100, 180, False)
thing_character_hashem = Thing("assets/char_hashem.png", 0, 0, 100, 180, False)
thing_character_triangle = Thing("assets/char_triangle.png", 0, 0, 100, 180, False)
thing_character_circle = Thing("assets/char_circle.png", 0, 0, 100, 180, False)
thing_selectChar_text = Thing("", 450, 50, 0, 0, True, "Select your characters", 30)
thing_logo = Thing("assets/logo.png",400,50,300,300,False)

# TODO add remaining things

player1_character = None
player2_character = None
player1_selection = 0
player2_selection = 1

key_counter = 0
countdown = 180  # 1000 frames

while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()

    # get all keys pressed
    keys = pygame.key.get_pressed()

    # Main States tree
    if state == 0:  # Intro screen
        # empty all things to draw
        things.clear()

        # add background and text to things to draw
        things.append(thing_intro_background)
        things.append(thing_logo)
        # TODO add logo
        things.append(thing_intro_text)

        # Check for space is entered
        if keys[pygame.K_SPACE]:
            innerState = 0  # reset inner state
            state = 1  # go to state 1 (Player selection screen)

    elif state == 1:  # Character Selection
        # empty all things to draw
        things.clear()

        # add background and text
        things.append(thing_intro_background)
        things.append(thing_selectChar_text)

        available_characters = [thing_character_saif, thing_character_nadeen, thing_character_hashem, thing_character_triangle, thing_character_circle]
        # by default, both characters are set to 0


        # player1 switches character by using A,D keys
        # player2 switches character by using left,right keys

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1_selection = player1_selection - 1
                    if player1_selection < 0:
                        player1_selection = len(available_characters) - 1

                if event.key == pygame.K_d:
                    player1_selection = player1_selection + 1
                    if player1_selection > (len(available_characters) - 1):
                        player1_selection = 0

                # TODO (HASHEM) do the same for player 2 (Using keys right and left)
                # hint: same code as above, but change player1 to 2, and they keys to arrows


        player1_character = copy.deepcopy(available_characters[player1_selection])
        player2_character = copy.deepcopy(available_characters[player2_selection])

        # Set the positions of the 2 characters , and add them to the list of "things"
        player1_character.pos_x = 200
        player1_character.pos_y = 300

        player2_character.pos_x = 900
        player2_character.pos_y = 300
        things.append(player1_character)
        things.append(player2_character)

        # TODO add key listener to confirm selection and move to next state (SAIF)
        # hint: check how we handled key presses above (line 138) TODO change this


    elif state == 2:  # Level 1  (Red light, Green Light)


        if innerState == 0:  # GET READY SCREEN
            things.clear()

            # TODO handle this state as following: (FARHAN)
            # empty list of things
            # Add the level background to list of things
            # Add a text "GET READY" to list of things , in the middle of screen
            # Add the 2 selected characters to list of things, positioned at the left of screen
            # Add the "Doll" character to list of things, positioned at the right of screen
            # hint: see the beginning of state 1


            # decrease countdown by one, if it reaches zero switch to next innerState
            # (Acts like a timer)
            countdown -= 1
            if (countdown == 0):
                innerState = 1
                countdown = 320

        elif innerState == 1:  # GAME STILL ON GREEN LIGHT
            if countdown == 320:
                redGreenLightSound.play()
            countdown -= 1
            if (countdown == 0):
                innerState = 2
                countdown = 320
            pass
        elif innerState == 2:  # GAME STILL ON RED LIGHT
            countdown -= 1
            if (countdown == 0):
                innerState = 1
                countdown = 320
            pass
        elif innerState == 3:  # PLAYER 1 WON
            pass
        elif innerState == 4:  # PLAYER 2 WON
            pass

    elif state == 3:  # level 2 (Candy Carving)
        # TODO: Find assets for this level

        pass

    elif state == 4:  # level 3 (Tug of War)
        # TODO (MAEEN)
        # 1- Add background to the level
        # 2- Add the 2 characters at opposite sides of the screen

        pass

    elif state == 5:  # Level Winner screen
        pass

    elif state == 6:  # Final winner screen
        pass

    # black out the screen
    window.fill((0, 0, 0))

    # draw everything in the list "things"
    for thing in things:
        thing.draw_self(window)

    # update the display
    pygame.display.update()
