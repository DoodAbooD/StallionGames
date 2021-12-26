import pygame
import copy


# *************************************  'thing' class definition *************************************
# A "thing" is basically anything that can be shown to the screen in the game
# such as characters, backgrounds, or text
class Thing:
    image_path = "assets/not_found.jpg" # by default, a thing has the "not found" image displayed
    image = pygame.image.load("assets/not_found.jpg")
    text = ""
    textSurface = None
    isText = False # if this thing is a text, this value becomes true
    fontSize = 30
    pos_x = 0
    pos_y = 0
    size_x = 0
    size_y = 0

    # the init function which is called when we create a new thing
    def __init__(self, image_path, pos_x, pos_y, size_x, size_y, isText, text="No Text", fontSize=30):
        self.image_path = image_path
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.isText = isText
        self.text = text
        self.fontSize = fontSize

    # method called to make the 'thing' draw itself on the window
    def draw_self(self, window):
        if self.isText: # if this thing was a text
            # Try assigning text
            try:
                myFont = pygame.font.SysFont('Comic Sans MS', self.fontSize)
                self.textSurface = myFont.render(self.text, False, (0, 0, 0))
            except:
                myFont = pygame.font.SysFont('Comic Sans MS', 30)
                self.textSurface = myFont.render("No Text", False, (0, 0, 0))
            #draw the text
            window.blit(self.textSurface, (self.pos_x, self.pos_y))

        else: # else if it wasnt a text, then its an image
            # Try assigning image path
            try:
                self.image = pygame.image.load(self.image_path)
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            except:
                self.image = pygame.image.load("assets/not_found.jpg")
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

            window.blit(scaled_image, (self.pos_x, self.pos_y))

# ************************************* end of class 'thing' definition **************************************

# defining window size 1200 x 600
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

# making the window with the dimensions above, setting its title and background color
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("StallionGames")
window.fill((255, 255, 255))
pygame.display.update()

# pygame mixer is used to play audio
pygame.mixer.init()
redGreenLightSound = pygame.mixer.Sound("assets/red_green_sound_short.wav")

# pygame font is used to display text
pygame.font.init()

#Frames per second
FPS = 100
clock = pygame.time.Clock()

# state is used to see which level the game is in,
# innerState is used to see which part of the level the game is in
state = 0 # 0- Intro screen | 1- Character selection Screen | 2- Level 1 | 3- Level 2 | 4- Level 3 | 4- Winner screen
innerState = 0

# a list of things to draw on screen, empty for now
things = list()

# things that can be added
# we are creating them using the class 'thing', and its __init__ method (see line 21)
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

# TODO add remaining things as needed

# we have 2 players, making an empty "thing" class for each of them
# selection index (0 and 1) used to loop between available characters at character selection screen
player1_character = None
player2_character = None
player1_selection = 0
player2_selection = 1

# countdown value to wait between events
countdown = 180  # 180 frames


# Main game loop starts here
while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    # get all keys pressed
    keys = pygame.key.get_pressed()

    # Main States tree

    # ************************ STATE 0 INTRO SCREEN ************************
    if state == 0:  # Intro screen
        # empty all things to draw
        things.clear()

        # add background and text to things to draw
        things.append(thing_intro_background)
        things.append(thing_logo)
        things.append(thing_intro_text)

        # Check if space is pressed
        if keys[pygame.K_SPACE]:
            innerState = 0  # reset inner state
            state = 1  # go to state 1 (Player selection screen)

    # ************** STATE 1 CHARACTER SELECTION SCREEN ********************

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
            if event.type == pygame.KEYDOWN: # if a key is pressed

                if event.key == pygame.K_d: # if the pressed key is (d)
                    player1_selection = player1_selection + 1 # increment player 1 selection by 1
                    if player1_selection > (len(available_characters) - 1): # if player 1 selection reaches above the number of available characters
                        player1_selection = 0 # cycle back to first character (number 0)

                if event.key == pygame.K_a: # and the pressed key is (a)
                    player1_selection = player1_selection - 1 # decrement player 1 selection by 1
                    if player1_selection < 0: # if player 1 selection reaches number 0
                        player1_selection = len(available_characters) - 1 # cycle back to last character



                # TODO (HASHEM) do the same for player 2 (Using keys right and left)
                # hint: same code as above, but change player1 to 2, and they keys to arrows


        # after selections were made, assign each player a copy of the character they selected
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
        # hint: check how we did this in previous state (line 135)

    # **************************** STATE 2: LEVEL 1 (RED LIGHT GREEN LIGHT)  ****************************

    elif state == 2:  # Level 1  (Red light, Green Light)

        if innerState == 0:  # GET READY SCREEN
            things.clear()

            # TODO the following: (FARHAN)
            # empty list of things
            # Add the level 1 background to list of things
            # Add the 2 selected characters to list of things, positioned at the left of screen
            # hint: see the beginning of state 1 to check how we add things

            # TODO the following: (NADEEN)
            # Add a text "GET READY" to list of things , in the middle of screen
            # Add the "Doll" character to list of things, positioned at the right of screen
            # hint: see the beginning of state 1 to check how we add things


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

    # **************************** STATE 3: LEVEL 2 (CANDY CARVING)  ****************************

    elif state == 3:  # level 2 (Candy Carving)
        # TODO: Find assets for this level

        pass

    # **************************** STATE 4: LEVEL 3 (TUG OF WAR)  ****************************
    elif state == 4:  # level 3 (Tug of War)
        # TODO (MAEEN)
        # 1- Add background to the level
        # 2- Add the 2 characters at opposite sides of the screen

        pass

    # **************************** STATE 5: WINNER SCREEN  ****************************
    elif state == 5:  #  Winner screen
        pass



    # black out the screen
    window.fill((0, 0, 0))

    # draw everything in the list "things"
    for thing in things:
        thing.draw_self(window)

    # update the display
    pygame.display.update()
