import pygame
import copy


# *************************************  'drawable' class definition *************************************
class Drawable:
    """A "Drawable" is basically anything that can be drawn to the screen in the game
    such as characters, backgrounds, or text"""
    image_path = "assets/not_found.jpg"  # by default, a drawable has the "not found" image displayed
    image = pygame.image.load("assets/not_found.jpg")
    text = ""
    textSurface = None
    isText = False  # if this drawable is a text, this value becomes true
    fontSize = 30
    pos_x = 0
    pos_y = 0
    size_x = 0
    size_y = 0

    # the init function which is called when we create a new drawable
    def __init__(self, image_path, pos_x, pos_y, size_x, size_y, isText, text="No Text", fontSize=30):
        self.image_path = image_path
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.isText = isText
        self.text = text
        self.fontSize = fontSize

    # method called to make the 'drawable' draw itself on the window
    def draw_self(self, window):
        if self.isText:  # if this drawable was a text
            # Try assigning text
            try:
                myFont = pygame.font.SysFont('Comic Sans MS', self.fontSize)
                self.textSurface = myFont.render(self.text, False, (0, 0, 0))
            except:
                myFont = pygame.font.SysFont('Comic Sans MS', 30)
                self.textSurface = myFont.render("No Text", False, (0, 0, 0))
            # draw the text
            window.blit(self.textSurface, (self.pos_x, self.pos_y))

        else:  # else if it wasn't a text, then its an image
            # Try assigning image path
            try:
                self.image = pygame.image.load(self.image_path)
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            except:
                self.image = pygame.image.load("assets/not_found.jpg")
                scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

            window.blit(scaled_image, (self.pos_x, self.pos_y))


# ************************************* end of class 'drawable' definition **************************************

# defining window size 1200 x 600
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

# creating the window with the dimensions above, setting its title and background color
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("StallionGames")
window.fill((255, 255, 255))
pygame.display.update()

# pygame mixer is used to play audio
pygame.mixer.init()
redGreenLightSound = pygame.mixer.Sound("assets/red_green_sound_short.wav")

# pygame font is used to display text
pygame.font.init()

# Frames per second
FPS = 100
clock = pygame.time.Clock()

# state is used to see which level the game is in,
# innerState is used to see which part of the current level we are in
state = 0  # 0- Intro screen | 1- Character selection Screen | 2- Level 1 | 3- Level 2 | 4- Level 3 | 5- Winner screen
innerState = 0

# a list of all drawables to draw on screen, empty for now
all_drawables = []


def generate_multi_line_text(s, pos_x, pos_y, font_size):
    """Method used to generate a list of text drawables out of a multiline string input"""
    generated_text_list = []
    current_y = pos_y
    stream = ""
    for char in s:
        if char != '\n':
            stream += char
        else:
            generated_text_list.append(Drawable("", pos_x, current_y, 0, 0, True, stream, font_size))
            stream = ""
            current_y += font_size
    return generated_text_list


# defining drawables that will be added to our list at different times of the game
# we are creating them using the class 'drawable', and its __init__ method
logo_drawable = Drawable("assets/logo.png", 400, 50, 300, 300, False)
intro_background_drawable = Drawable("assets/intro_bg.png", 0, 0, 1200, 600, False)
intro_text_drawable = Drawable("", 400, 500, 0, 0, True, "Press Space to Start!", 30)
character_doll_drawable = Drawable("assets/char_doll.png", 0, 0, 100, 300, False)
character_saif_drawable = Drawable("assets/char_saif.png", 0, 0, 100, 180, False)
character_nadeen_drawable = Drawable("assets/char_nadeen.png", 0, 0, 100, 180, False)
character_hashem_drawable = Drawable("assets/char_hashem.png", 0, 0, 100, 180, False)
character_triangle_drawable = Drawable("assets/char_triangle.png", 0, 0, 100, 180, False)
character_circle_drawable = Drawable("assets/char_circle.png", 0, 0, 100, 180, False)
select_char_text_list_drawable = generate_multi_line_text("Select your characters\n"
                                                          "with A and D for player 1\n"
                                                          "and Arrows for player 2\n"
                                                          "Press Enter to continue", 450, 50, 30)

# TODO add more drawables we might need

# we have 2 players, making an empty "drawable" class for each of them
# selection index (0 and 1) used to loop between available characters at character selection screen
player1_character = None  # nothing selected for now
player2_character = None  # nothing selected for now
player1_selection = 0  # for a start, player 1 selection is set to character # 0
player2_selection = 1  # for a start, player 2 selection is set to character # 1


# ************************************* Main game loop starts here **************************************

while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    # get all keys pressed and store them in dictionary "keys"
    keys = pygame.key.get_pressed()

    # black out the screen
    window.fill((0, 0, 0))

    # draw everything in the list "all_drawables" to the screen
    for drawable in all_drawables:
        drawable.draw_self(window)

    # update the display
    pygame.display.update()

    # ************************ STATE 0 INTRO SCREEN ************************
    if state == 0:  # Intro screen
        # empty list of all things to draw (all_drawables)
        all_drawables.clear()

        # add intro background, logo, and intro text to list of things to draw (all_drawables)
        all_drawables.append(intro_background_drawable)
        all_drawables.append(logo_drawable)
        all_drawables.append(intro_text_drawable)

        # Check if space is pressed
        if keys[pygame.K_SPACE]:
            innerState = 0  # reset inner state
            state = 1  # go to state 1 (Player selection screen)

    # ************** STATE 1 CHARACTER SELECTION SCREEN ********************

    elif state == 1:  # Character Selection
        # empty all things to draw
        all_drawables.clear()
        print("At state 1")

        # add background and text
        all_drawables.append(intro_background_drawable)
        for thing in select_char_text_list_drawable:
            all_drawables.append(thing)
        print(len(all_drawables))

        available_characters = [character_saif_drawable, character_nadeen_drawable, character_hashem_drawable,
                                character_triangle_drawable, character_circle_drawable]
        # by default, both characters are set to 0

        # player1 switches character by using A,D keys
        # player2 switches character by using left,right keys

        for event in events:
            if event.type == pygame.KEYDOWN:  # if a key is pressed

                if event.key == pygame.K_d:  # if the pressed key is (d)
                    player1_selection = player1_selection + 1  # increment player 1 selection by 1
                    if player1_selection > (len(
                            available_characters) - 1):  # if player 1 selection reaches above the number of available characters
                        player1_selection = 0  # cycle back to first character (number 0)

                if event.key == pygame.K_a:  # and the pressed key is (a)
                    player1_selection = player1_selection - 1  # decrement player 1 selection by 1
                    if player1_selection < 0:  # if player 1 selection reaches number 0
                        player1_selection = len(available_characters) - 1  # cycle back to last character

                # TODO (SAIF) the same for player 2 (Using keys right and left)
                # hint: same code as above, but change player1 to 2, and they keys to arrows

        # after selections were made, assign each player a copy of the character they selected
        player1_character = copy.deepcopy(available_characters[player1_selection])
        player2_character = copy.deepcopy(available_characters[player2_selection])

        # Set the positions of the 2 characters , and add them to the list of "things"
        player1_character.pos_x = 200
        player1_character.pos_y = 300
        player2_character.pos_x = 900
        player2_character.pos_y = 300
        all_drawables.append(player1_character)
        all_drawables.append(player2_character)

        # Check if space is pressed
        if keys[pygame.K_RETURN]:
            innerState = 0  # reset inner state
            state = 2  # go to state 2 (level 1)

    # **************************** STATE 2: LEVEL 1 (RED LIGHT GREEN LIGHT)  ****************************

    elif state == 2:  # Level 1  (Red light, Green Light)
        print("at state 2")
        # countdown value to wait between events
        countdown = 180  # 180 frames
        if innerState == 0:  # GET READY SCREEN
            all_drawables.clear()

            # TODO (MAEEN) the following:
            # empty list of all drawables
            # Add the level 1 background to list of drawables
            # Add the 2 selected characters to list of drawables, positioned at the left of screen
            # hint: see the beginning of state 1 to check how we add drawables

            # TODO (SAIF) the following:
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
    elif state == 5:  # Winner screen
        pass


