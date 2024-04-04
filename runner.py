import pygame
import pygame.mixer
import time
import cv2
import tictactoe as ttt

pygame.init()
size = width, height = 1920, 1080

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

# Loads the video for title screen
snow = "assets/titlescreen.mp4"
cap = cv2.VideoCapture(snow)

# Initializes the sound
pygame.mixer.init()

# Created game loop
clock = pygame.time.Clock()

# All fonts
moveFont = pygame.font.Font("assets/OpenSans-Regular.ttf", 120)
pixelfont = pygame.font.Font("assets/ThaleahFat.ttf", 120)

# Initializes the buttons
exit_button_img = pygame.image.load('assets/Exit.png')
exit_button_rect = exit_button_img.get_rect()
exit_button_rect.topleft = (width - exit_button_rect.width + 90, 20)
exit_button_img = pygame.transform.scale(exit_button_img, (exit_button_img.get_width() // 2, exit_button_img.get_height() // 2))

playX_img = pygame.image.load('assets/playx.png')
playO_img = pygame.image.load('assets/playo.png')

playX_img = pygame.transform.scale(playX_img, (playX_img.get_width() // 2, playX_img.get_height() // 2))
playO_img = pygame.transform.scale(playO_img, (playO_img.get_width() // 2, playO_img.get_height() // 2))

replay = pygame.image.load('assets/replay.png')
replay = pygame.transform.scale(replay, (replay.get_width() // 2, replay.get_height() // 2))

user = None
board = ttt.initial_state()
ai_turn = False
playing_game_music = False

def play_title_music():
    """
    Plays the title music
    """
    global playing_game_music
    pygame.mixer.music.load('assets/titlemusic.mp3')
    pygame.mixer.music.play(-1)
    playing_game_music = False

def play_game_music():
    """
    Playes the game music
    """
    global playing_game_music
    if not playing_game_music:
        pygame.mixer.music.load('assets/gamemusic.mp3')
        pygame.mixer.music.play(-1)
        playing_game_music = True

def play_sound(filepath):
    """
    Plays given sound effect
    """
    sound = pygame.mixer.Sound(filepath)
    sound.play()

def draw_exit_button():
    """
    Draws exit button
    """
    screen.blit(exit_button_img, exit_button_rect)

def draw_board():
    """
    Draws the tic tac toe board
    """
    tile_size = 160
    tile_origin = (width / 2 - (1.5 * tile_size),
                   height / 2 - (1.5 * tile_size))
    tiles = []
    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 3)

            if board[i][j] != ttt.EMPTY:
                move = moveFont.render(board[i][j], True, white)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)
            row.append(rect)
        tiles.append(row)
    return tiles

play_title_music()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    running = False

    ret, frame = cap.read()

    if ret:
        # Convert the OpenCV frame to a Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pygame = pygame.image.frombuffer(frame_rgb.flatten(), frame.shape[:2][::-1], 'RGB')

        screen.fill((0, 0, 0))
        screen.blit(frame_pygame, (0, 0))

        clock.tick(30)
    else:
        # Rewind the video to the beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    draw_exit_button()

    # Let user choose a player.
    if user is None:

        playXButton = playX_img.get_rect(center=(width // 3, height // 1.8))
        playOButton = playO_img.get_rect(center=(2.7 * width // 4, height // 1.8))
        screen.blit(playX_img, playXButton)
        screen.blit(playO_img, playOButton)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                play_sound('assets/gamestart.mp3')
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                play_sound('assets/gamestart.mp3')
                time.sleep(0.2)
                user = ttt.O

    else:

        play_game_music()

        player = ttt.player(board)

        if player == "X":
            background_img_x = pygame.image.load('assets/xturngame.png')
            background_img_x = pygame.transform.scale(background_img_x, (width, height))
            screen.blit(background_img_x, (0, 0))
            draw_exit_button()
        else:
            background_img_o = pygame.image.load('assets/oturngame.png')
            background_img_o = pygame.transform.scale(background_img_o, (width, height))
            screen.blit(background_img_o, (0, 0))
            draw_exit_button()

        # Draw game board
        tiles = draw_board()

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            background_img_o = pygame.image.load('assets/regbackgroundgame.png')
            # Scale the background image to match the screen size
            background_img_o = pygame.transform.scale(background_img_o, (width, height))
            screen.blit(background_img_o, (0, 0))
            draw_exit_button()
            if winner is None:
                title = f"Game Over: Tie."
                draw_board()
            else:
                title = f"Game Over: {winner} wins."
                draw_board()
        elif user == player:
            title = f"Your turn!"
        else:
            title = f"Computer thinking..."
        title = pixelfont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 200)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))
                        play_sound('assets/placesound.mp3')

        if game_over:
            replay_button = playO_img.get_rect(center=(width // 2, 900))
            screen.blit(replay, replay_button)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse):
                    play_sound('assets/gamestart.mp3')
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    play_title_music()

    pygame.display.flip()
