from pygame.locals import *
import pygame
import sys

lvl1=["*","*","*","*","*","*","*"]
lvl2=["*","*","*","*","*","*","*"]
lvl3=["*","*","*","*","*","*","*"]
lvl4=["*","*","*","*","*","*","*"]
lvl5=["*","*","*","*","*","*","*"]
lvl6=["*","*","*","*","*","*","*"]
    
pygame.init()

yellow_time=0
red_time=0
last_turn_time=0
yellow_minute=0
yellow_seconds=0
red_minutes=0
red_seconds=0
total_minutes=0
total_seconds=0
timewithcorrectformat=0
undo_stack = []
redo_stack = []
undo_button=None
redo_button=None
quit_button=None

yellow_colour=(255,255,0)
red_colour=(255,0,0)
black_colour = (0, 0, 0) 
white_colour = (255, 255, 255)
good_colour=(0, 51, 204)
board_colour=(96,119,49)
grey_colour=(192,192,192)
screen = pygame.display.set_mode((1550,780))  
pygame.display.set_caption('Python Connect 4')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
turn=0
player1=""
player2=""
leaderboard_data=[]

o1=t2=t3=f4=f5=s6=s7=1 

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def insert_score(player1, player2,total_time, winner):
    leaderboard_data.append((player1,player2,total_time,winner))

def print_mouse_click(event):
    print(f"Mouse clicked at coordinates: ({event.pos[0]}, {event.pos[1]})")

def reset_game(check=False):
    global o1, t2, t3, f4, f5, s6, s7
    global yellow_time, red_time, last_turn_time, yellow_minute, yellow_seconds, red_minutes, red_seconds, total_minutes, total_seconds, timewithcorrectformat
    global lvl1, lvl2, lvl3, lvl4, lvl5, lvl6
    global turn
    turn = 0
    o1 = t2 = t3 = f4 = f5 = s6 = s7 = 1
    yellow_time = red_time = last_turn_time = 0
    last_turn_time = pygame.time.get_ticks()
    lvl1 =["*","*","*","*","*","*","*"] 
    lvl2 =["*","*","*","*","*","*","*"]
    lvl3 =["*","*","*","*","*","*","*"]
    lvl4 =["*","*","*","*","*","*","*"]
    lvl5 =["*","*","*","*","*","*","*"]
    lvl6 =["*","*","*","*","*","*","*"]

def display_instructions():
    global screen
    while True:
        fill_gradient(screen, (58, 62, 88), (119, 127, 148))
        font = pygame.font.Font(None, 36)
        instructions = [
            "Instructions:",
            "1. Player 1 is Yellow, Player 2 is Red.",
            "2. Click or press a key (1-7) to drop your piece.",
            "3. Connect four pieces in a row to win!",
            "Press any key to return to the menu."
        ]
        
        for i, line in enumerate(instructions):
            text = font.render(line, True,white_colour)  # White text
            screen.blit(text, (screen.get_width()//2-250, 250 + i * 40))  # Display each line
        
        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
                return  # Return to menu when any key is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def name_entry_screen(screen):
    # Initialize variables
    input_active = True
    player1_name = ""
    player2_name = ""
    font = pygame.font.Font(None, 36)  # Use a default font
    current_player = 1  # Start with player 1

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (192, 192, 192)
    blue = (0, 51, 204)

    # Calculate the center position for the entry box
    box_width = 500
    box_height = 300
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2

    # Create input box for the name
    input_box1 = pygame.Rect(box_x + 50, box_y + 100, box_width - 100, 40) 
    input_box2 = pygame.Rect(box_x + 50, box_y + 200, box_width - 100, 40) 

    while input_active:
        fill_gradient(screen, (58, 62, 88), (119, 127, 148))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type== pygame.MOUSEBUTTONDOWN:
                print_mouse_click(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    if current_player == 1 and player1_name:
                        current_player = 2
                    elif current_player == 2 and player2_name:
                        input_active = False 
                elif event.key == pygame.K_BACKSPACE:
                    if current_player == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                elif event.unicode and len(event.unicode) == 1:  # Only accept single characters
                    if current_player == 1:
                        player1_name += event.unicode 
                    else:
                        player2_name += event.unicode 

        # Fill the screen with a gradient background
        screen.fill((58, 62, 88))

        # Render the name input
        pygame.draw.rect(screen, grey, (box_x, box_y, box_width, box_height), 0, 10)  
        pygame.draw.rect(screen, black, (box_x, box_y, box_width, box_height), 3, 10) 

        # Title
        title_surface = font.render("Enter Player Names", True, black)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, box_y + 40))
        screen.blit(title_surface, title_rect)

        # Player 1 name
        player1name_surface = font.render("Player 1(Yellow):", True, black)
        player1name_rect = player1name_surface.get_rect(center=(screen.get_width() // 2 - 100, box_y + 80))

        # Player 2 name
        player2name_surface = font.render("Player 2(Red):", True, black)
        player2name_rect = player2name_surface.get_rect(center=(screen.get_width() // 2 - 100, box_y + 180))

        # Player 1 input box
        pygame.draw.rect(screen, white, input_box1, 0, 5)  
        pygame.draw.rect(screen, black, input_box1, 2, 5) 
        if current_player == 1:
            pygame.draw.rect(screen, blue, input_box1, 2, 5)  

        current_name_surface1 = font.render(player1_name, True, black)
        current_name_rect1 = current_name_surface1.get_rect(topleft=(input_box1.x + 5, input_box1.y + 5))
        screen.blit(current_name_surface1, current_name_rect1)

        # Player 2 input box
        pygame.draw.rect(screen, white, input_box2, 0, 5) 
        pygame.draw.rect(screen, black, input_box2, 2, 5) 
        if current_player == 2:
            pygame.draw.rect(screen, blue, input_box2, 2, 5)  

        current_name_surface2 = font.render(player2_name, True, black)
        current_name_rect2 = current_name_surface2.get_rect(topleft=(input_box2.x + 5, input_box2.y + 5))
        screen.blit(current_name_surface2, current_name_rect2)

        # Main Menu Button
        mainmenu_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 280, 200, 40)
        pygame.draw.rect(screen, black, mainmenu_button, 2, 5)
        mainmenu_text = font.render("Main Menu", True, black)
        mainmenu_text_rect = mainmenu_text.get_rect(center=mainmenu_button.center)

        #Saving
        screen.blit(mainmenu_text, mainmenu_text_rect)
        screen.blit(player1name_surface, player1name_rect)
        screen.blit(player2name_surface, player2name_rect)

        # Check for mouse click on main menu button
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if mainmenu_button.collidepoint(pygame.mouse.get_pos()):
                return menuscreen()

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Limit to 60 FPS

    return player1_name, player2_name

def menuscreen():
    global player1, player2
    global font
    while True:
        fill_gradient(screen, (58, 62, 88), (119, 127, 148))

        # Title
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("Connect 4", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_text, title_rect)

        # Play Button
        play_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 100, 200, 100), 2, 5)
        play_text = font.render("Play", True, black_colour)
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)

        # Quit Button
        quit_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 190, 200, 50), 2, 5)
        quit_text = font.render("Quit", True, black_colour)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_text_rect)

        # Leaderboard Button
        leaderboard_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 200, 50), 2, 5)
        leaderboard_text = font.render("Leaderboard", True, black_colour)
        leaderboard_text_rect = leaderboard_text.get_rect(center=leaderboard_button.center)
        screen.blit(leaderboard_text, leaderboard_text_rect)

        instruction_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 120, 200, 50), 2, 5)
        instruction_text = font.render("Instructions", True, (0,0,0))
        instruction_text_rect = instruction_text.get_rect(center=instruction_button.center)
        screen.blit(instruction_text,instruction_text_rect) # Center text
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    player1, player2 = name_entry_screen(screen)
                    main()
                if instruction_button.collidepoint(event.pos):
                    display_instructions()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif leaderboard_button.collidepoint(event.pos):
                    leaderboard_screen(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def leaderboard_screen(screen):
    font = pygame.font.Font(None, 36)
    
    while True:
        screen.fill((58, 62, 88))  # Background color

        title_surface = font.render("Leaderboard", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_surface, title_rect)

        # Define column widths and positions
        num_columns = 4
        col_width = screen.get_width() // num_columns
        col1_x = col_width // 2  # Rank
        col2_x = col1_x + col_width  # Players
        col3_x = col2_x + col_width  # Time
        col4_x = col3_x + col_width  # Winner

        # Column headers
        headers = ["Rank", "Players", "Time", "Winner"]
        for i, header in enumerate(headers):
            header_surface = font.render(header, True, (255, 255, 255))
            header_rect = header_surface.get_rect(center=(col1_x + i * col_width, 100))
            screen.blit(header_surface, header_rect)

        # Display the leaderboard entries
        for index, (player1, player2, total_time, winner) in enumerate(leaderboard_data):
            y_pos = 150 + index * 40

            # Rank
            rank_surface = font.render(f"{index + 1}", True, (255, 255, 255))
            rank_rect = rank_surface.get_rect(center=(col1_x, y_pos))
            screen.blit(rank_surface, rank_rect)

            # Players
            players_surface = font.render(f"{player1} vs {player2}", True, (255, 255, 255))
            players_rect = players_surface.get_rect(center=(col2_x, y_pos))
            screen.blit(players_surface, players_rect)

            # Time
            time_surface = font.render(total_time, True, (255, 255, 255))
            time_rect = time_surface.get_rect(center=(col3_x, y_pos))
            screen.blit(time_surface, time_rect)

            # Winner
            winner_surface = font.render(winner, True, (255, 255, 255))
            winner_rect = winner_surface.get_rect(center=(col4_x, y_pos))
            screen.blit(winner_surface, winner_rect)

        # Back to menu button
        back_button = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() - 200, 200, 50), 2, 5)
        back_text = font.render("Back to Menu", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_button.center)

        reset_leaderboard_button = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 + 330, 300, 40)
        pygame.draw.rect(screen,(0,0,0), reset_leaderboard_button, 2, 5)
        reset_leaderboard_text = font.render("Reset Leaderboard", True, (0,0,0))
        reset_leaderboard_text_rect = reset_leaderboard_text.get_rect(center=reset_leaderboard_button.center)

        #Refreshing
        screen.blit(reset_leaderboard_text,reset_leaderboard_text_rect)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if  reset_leaderboard_button.collidepoint(event.pos):
                    leaderboard_data=[]
                    pass
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def handle_mouse_click_column(pos):
    global turn
    global last_turn_time
    column = (pos[0] - 250) // 150 + 1
    if column < 0 or column > 7:
        return
    return column

def display_whose_turn(screen, font, turn):
    if turn%2==0:
        turn_text = "Yellow's Turn"
    else:
        turn_text ="Red's Turn"
    turn_surface = font.render(turn_text, True, (255, 255, 255))  # White text
    turn_rect = turn_surface.get_rect(topleft=(30, 50))  # Top-left corner
    screen.blit(turn_surface, turn_rect)

def display_time(screen, font, yellow_time, red_time):
    yellow_minutes = int(yellow_time // 60)
    yellow_seconds = int(yellow_time % 60)
    red_minutes = int(red_time // 60)
    red_seconds = int(red_time % 60)
    total_time = yellow_time + red_time
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)
    
    time_text = f"Yellow Time: {yellow_minutes:02d}:{yellow_seconds:02d} | Red Time: {red_minutes:02d}:{red_seconds:02d} | Total time: {total_minutes:02d}:{total_seconds:02d}"
    time_surface = font.render(time_text, True, (255, 255, 255))  # White text
    time_rect = time_surface.get_rect(topleft=(30, 10))  # Top-left corner
    screen.blit(time_surface, time_rect)

def winscreen(screen, font, clock, winner):
    global timewithcorrectformat
    total_time = yellow_time + red_time  # Total time for the game
    if winner == "Yellow":
        insert_score(player1, player2, format_time(total_time), player1)
        fill_gradient(screen, (255, 212, 0), (255, 255, 183))
        move_time_text = font.render(f"Your move time: {format_time(yellow_time)}", True, (0, 0, 0))
    elif winner == "Red":
        insert_score(player1, player2, format_time(total_time), player2)
        fill_gradient(screen, (223, 27, 27), (255, 71, 76))
        move_time_text = font.render(f"Your move time: {format_time(red_time)}", True, (0, 0, 0))

    # Display total game time
    total_time_text = font.render(f"Total time of game: {format_time(total_time)}", True, (0, 0, 0))

    # Display winner
    winner_text = font.render(f"Congratulations, {winner} wins!", True, (0, 0, 0))

    # Create buttons for Play Again and Main Menu
    play_again_button = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 20, 200, 40), 2, 5)
    play_again_text = font.render("Play Again", True, black_colour)
    play_again_text_rect = play_again_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    mainmenu_button = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 80, 200, 40), 2, 5)
    mainmenu_text = font.render("Main Menu", True, black_colour)
    mainmenu_text_rect = mainmenu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    # Update the screen
    screen.blit(winner_text, winner_text.get_rect(center=(screen.get_width() // 2, 40)))
    screen.blit(move_time_text, move_time_text.get_rect(center=(screen.get_width() // 2, 70)))
    screen.blit(total_time_text, total_time_text.get_rect(center=(screen.get_width() // 2, 100)))
    screen.blit(play_again_text, play_again_text_rect)
    screen.blit(mainmenu_text, mainmenu_text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    reset_game(True)
                    return
                if mainmenu_button.collidepoint(event.pos):
                    reset_game()
                    menuscreen()
                    return

        clock.tick(60)
                

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    if rect is None:
        rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical:
        h = y2-y1
    else:
        h = x2-x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (float(b[0]-a[0])/h,float(b[1]-a[1])/h,float(b[2]-a[2])/h)
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

def draw():
    global undo_button,redo_button,quit_button
    global font
    global yellow_time, red_time, last_turn_time
    current_time = pygame.time.get_ticks()
    if turn % 2 == 0:
        yellow_time += (current_time - last_turn_time) / 1000
    else:
        red_time += (current_time - last_turn_time) / 1000
    last_turn_time = current_time
    x1=50
    y1=90
    x2=90
    y2=90
    fill_gradient(screen,(58, 62, 88),(119, 127, 148))
    #TO DISPLAY TURN
    pygame.draw.rect(screen,(black_colour),(x1-5,y1-5,x2+10,y2+10))
    if turn%2==0:
        pygame.draw.rect(screen,(yellow_colour),(x1,y1,x2,y2)) 
    elif turn%2!=0:
        pygame.draw.rect(screen,(red_colour),(x1,y1,x2,y2)) 
    #Draw Undo Button
    undo_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width()- 250, screen.get_height()-250, 200, 50), 2, 5)
    undo_text = font.render("Undo", True, black_colour)
    undo_text_rect = undo_text.get_rect(center=undo_button.center)
    screen.blit(undo_text, undo_text_rect)
    
    #Draw Redo Button
    redo_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width()- 250, screen.get_height()-175, 200, 50), 2, 5)
    redo_text = font.render("Redo", True, black_colour)
    redo_text_rect = redo_text.get_rect(center=redo_button.center)
    screen.blit(redo_text, redo_text_rect)
    
    #Draw Quit Button
    quit_button = pygame.draw.rect(screen, black_colour, pygame.Rect(screen.get_width()- 250, screen.get_height()-100, 200, 50), 2, 5)
    quit_text = font.render("Quit", True, black_colour)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)
    #TO PRINT THE CIRCLES
    for j, k in enumerate([lvl6, lvl5, lvl4, lvl3, lvl2, lvl1]):
        i = 0
        for card in k:
            pygame.draw.circle(screen, black_colour, (300 + 150 * i, 700 - 100 * j), 47)
            if card == "r":
                pygame.draw.circle(screen, red_colour, (300 + 150 * i, 700 - 100 * j), 43)
            elif card == "y":
                pygame.draw.circle(screen, yellow_colour, (300 + 150 * i, 700 - 100 * j), 43)
            else:
                pygame.draw.circle(screen, grey_colour, (300 + 150 * i, 700 - 100 * j), 43)
            pygame.draw.rect(screen,(black_colour),(245+150*i,95,110,50))
            pygame.draw.rect(screen,(grey_colour),(250+150*i,100,100,40))
            font = pygame.font.Font(None, 36)
            text = font.render(str(i+1), True, black_colour)
            text_rect = text.get_rect(center=(300 + 150 * i, 120))
            screen.blit(text, text_rect)
            i += 1
    display_whose_turn(screen,font,turn)
    display_time(screen, font, yellow_time, red_time)
    pygame.display.flip()

def undo(): 
    global undo_stack, redo_stack, turn 
    global lvl1, lvl2, lvl3, lvl4, lvl5, lvl6 
    global o1, t2, t3, f4, f5, s6, s7  # Include the variables to be updated

    if undo_stack: 
        current_state = (list(lvl1), list(lvl2), list(lvl3), list(lvl4), list(lvl5), list(lvl6), turn, o1, t2, t3, f4, f5, s6, s7) 
        redo_stack.append(current_state) 
        last_state = undo_stack.pop() 
        lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, turn, o1, t2, t3, f4, f5, s6, s7 = last_state 

def redo(): 
    global undo_stack, redo_stack, turn 
    global lvl1, lvl2, lvl3, lvl4, lvl5, lvl6 
    global o1, t2, t3, f4, f5, s6, s7  # Include the variables to be updated

    if redo_stack: 
        current_state = (list(lvl1), list(lvl2), list(lvl3), list(lvl4), list(lvl5), list(lvl6), turn, o1, t2, t3, f4, f5, s6, s7) 
        undo_stack.append(current_state) 
        last_state = redo_stack.pop() 
        lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, turn, o1, t2, t3, f4, f5, s6, s7 = last_state 

def updategame(playerturn,colour):
    global o1, t2, t3, f4, f5, s6, s7
    global undo_stack
    
    current_state = (list(lvl1), list(lvl2), list(lvl3), list(lvl4), list(lvl5), list(lvl6), turn, o1, t2, t3, f4, f5, s6, s7)
    undo_stack.append(current_state)
    redo_stack.clear()
    
    if playerturn==1:
        if o1==1:
            lvl6[0]=colour        
        elif o1==2:
            lvl5[0]=colour
        elif o1==3:
            lvl4[0]=colour
        elif o1==4:
            lvl3[0]=colour
        elif o1==5:
            lvl2[0]=colour
        elif o1==6:
            lvl1[0]=colour
        o1+=1
    elif playerturn==2:
        if t2==1:
            lvl6[1]=colour
        elif t2==2:
            lvl5[1]=colour
        elif t2==3:
            lvl4[1]=colour
        elif t2==4:
            lvl3[1]=colour
        elif t2==5:
            lvl2[1]=colour
        elif t2==6:
            lvl1[1]=colour
        t2+=1
        
    elif playerturn==3:
        if t3==1:
            lvl6[2]=colour
        elif t3==2:
            lvl5[2]=colour
        elif t3==3:
            lvl4[2]=colour
        elif t3==4:
            lvl3[2]=colour
        elif t3==5:
            lvl2[2]=colour
        elif t3==6:
            lvl1[2]=colour
        t3+=1
        
    elif playerturn==4:
        if f4==1:
            lvl6[3]=colour
        elif f4==2:
            lvl5[3]=colour
        elif f4==3:
            lvl4[3]=colour
        elif f4==4:
            lvl3[3]=colour
        elif f4==5:
            lvl2[3]=colour
        elif f4==6:
            lvl1[3]=colour
        f4+=1
        
    elif playerturn==5:
        if f5==1:
            lvl6[4]=colour
        elif f5==2:
            lvl5[4]=colour
        elif f5==3:
            lvl4[4]=colour
        elif f5==4:
            lvl3[4]=colour
        elif f5==5:
            lvl2[4]=colour
        elif f5==6:
            lvl1[4]=colour
        f5+=1
        
    elif playerturn==6:
        if s6==1:
            lvl6[5]=colour
        elif s6==2:
            lvl5[5]=colour
        elif s6==3:
            lvl4[5]=colour
        elif s6==4:
            lvl3[5]=colour
        elif s6==5:
            lvl2[5]=colour
        elif s6==6:
            lvl1[5]=colour
        s6+=1
        
    elif playerturn==7:
        if s7==1:
            lvl6[6]=colour
        elif s7==2:
            lvl5[6]=colour
        elif s7==3:
            lvl4[6]=colour
        elif s7==4:
            lvl3[6]=colour
        elif s7==5:
            lvl2[6]=colour
        elif s7==6:
            lvl1[6]=colour
        s7+=1

def checkwin():
    #For Horizontal
    for i in range(0,7):
        if lvl6[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")
        elif lvl5[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")
        elif lvl4[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")
        elif lvl3[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")
        elif lvl2[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")
        elif lvl1[i:i+4]==["y","y","y","y"]:
            winscreen(screen,font,clock,"Yellow")

    for i in range(0,7):
        if lvl6[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")
        elif lvl5[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")
        elif lvl4[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")
        elif lvl3[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")
        elif lvl2[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")
        elif lvl1[i:i+4]==["r","r","r","r"]:
            winscreen(screen,font,clock,"Red")

    #FOR VERTICAL
    for i in range(0,7):
        if lvl6[i]=="y" and lvl5[i]=="y" and lvl4[i]=="y" and lvl3[i]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl5[i]=="y" and lvl4[i]=="y" and lvl3[i]=="y" and lvl2[i]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl4[i]=="y" and lvl3[i]=="y" and lvl2[i]=="y" and lvl1[i]=="y":
            winscreen(screen,font,clock,"Yellow")
    for i in range(0,7):
        if lvl6[i]=="r" and lvl5[i]=="r" and lvl4[i]=="r" and lvl3[i]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl5[i]=="r" and lvl4[i]=="r" and lvl3[i]=="r" and lvl2[i]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl4[i]=="r" and lvl3[i]=="r" and lvl2[i]=="r" and lvl1[i]=="r":
            winscreen(screen,font,clock,"Red")

    #FOR DIAGONAL
    for i in range(0,4):
        if lvl6[i]=="y" and lvl5[i+1]=="y" and lvl4[i+2]=="y" and lvl3[i+3]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl5[i]=="y" and lvl4[i+1]=="y" and lvl3[i+2]=="y" and lvl2[i+3]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl4[i]=="y" and lvl3[i+1]=="y" and lvl2[i+2]=="y" and lvl1[i+3]=="y":
            winscreen(screen,font,clock,"Yellow")
    for i in range(0,4):
        if lvl6[i]=="r" and lvl5[i+1]=="r" and lvl4[i+2]=="r" and lvl3[i+3]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl5[i]=="r" and lvl4[i+1]=="r" and lvl3[i+2]=="r" and lvl2[i+3]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl4[i]=="r" and lvl3[i+1]=="r" and lvl2[i+2]=="r" and lvl1[i+3]=="r":
            winscreen(screen,font,clock,"Red")
    for i in range(-1,-5,-1):
        if lvl6[i]=="r" and lvl5[i-1]=="r" and lvl4[i-2]=="r" and lvl3[i-3]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl5[i]=="r" and lvl4[i-1]=="r" and lvl3[i-2]=="r" and lvl2[i-3]=="r":
            winscreen(screen,font,clock,"Red")
        elif lvl4[i]=="r" and lvl3[i-1]=="r" and lvl2[i-2]=="r" and lvl1[i-3]=="r":
            winscreen(screen,font,clock,"Red")
    for i in range(-1,-5,-1):
        if lvl6[i]=="y" and lvl5[i-1]=="y" and lvl4[i-2]=="y" and lvl3[i-3]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl5[i]=="y" and lvl4[i-1]=="y" and lvl3[i-2]=="y" and lvl2[i-3]=="y":
            winscreen(screen,font,clock,"Yellow")
        elif lvl4[i]=="y" and lvl3[i-1]=="y" and lvl2[i-2]=="y" and lvl1[i-3]=="y":
            winscreen(screen,font,clock,"Yellow")

def main():
    global o1, t2, t3, f4, f5, s6, s7
    global yellow_time, red_time, last_turn_time, yellow_minute, yellow_seconds, red_minutes, red_seconds, total_minutes, total_seconds, timewithcorrectformat
    global lvl1, lvl2, lvl3, lvl4, lvl5, lvl6
    global turn
    while True:
        current_time = pygame.time.get_ticks()
        if turn % 2 == 0:
            yellow_time += (current_time - last_turn_time) / 1000
        else:
            red_time += (current_time - last_turn_time) / 1000
        last_turn_time = current_time
        draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #MOUSE INPUTS
            if event.type == pygame.MOUSEBUTTONDOWN and event.button != 4 and event.button != 5:
                print_mouse_click(event)
                if event.button == 1:
                    if undo_button.collidepoint(event.pos):
                        undo()
                    elif redo_button.collidepoint(event.pos):
                        redo()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if handle_mouse_click_column(event.pos)==1:
                    if turn % 2 == 0:
                        if o1<7:
                            updategame(1,"y")
                            turn+=1
                    else:
                        if o1<7:
                            updategame(1,"r")
                            turn+=1
                        
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==2:
                    if turn % 2 == 0:
                        if t2<7:
                            updategame(2,"y")
                            turn+=1
                    else:
                        if t2<7:
                            updategame(2,"r")
                            turn+=1
                        
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==3:
                    if turn % 2 == 0:
                        if t3<7:
                            updategame(3,"y")
                            turn+=1
                    else:
                        if t3<7:
                            updategame(3,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==4:
                    if turn % 2 == 0:
                        if f4<7:
                            updategame(4,"y")
                            turn+=1
                    else:
                        if f4<7:
                            updategame(4,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==5:
                    if turn % 2 == 0:
                        if f5<7:
                            updategame(5,"y")
                            turn+=1
                    else:
                        if f5<7:
                            updategame(5,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==6:
                    if turn % 2 == 0:
                        if s6<7:
                            updategame(6,"y")
                            turn+=1
                    else:
                        if s6<7:
                            updategame(6,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif handle_mouse_click_column(event.pos)==7:
                    if turn % 2 == 0:
                        if s7<7:
                            updategame(7,"y")
                            turn+=1
                    else:
                        if s7<7:
                            updategame(7,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()

            #KEYPAD INPUTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if turn % 2 == 0:
                        if o1<7:
                            updategame(1,"y")
                            turn+=1
                    else:
                        if o1<7:
                            updategame(1,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_2:
                    if turn % 2 == 0:
                        if t2<7:
                            updategame(2,"y")
                            turn+=1
                    else:
                        if t2<7:
                            updategame(2,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_3:
                    if turn % 2 == 0:
                        if t3<7:
                            updategame(3,"y")
                            turn+=1
                    else:
                        if t3<7:
                            updategame(3,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_4:
                    if turn % 2 == 0:
                        if f4<7:
                            updategame(4,"y")
                            turn+=1
                    else:
                        if f4<7:
                            updategame(4,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_5:
                    if turn % 2 == 0:
                        if f5<7:
                            updategame(5,"y")
                            turn+=1
                    else:
                        if f5<7:
                            updategame(5,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_6:
                    if turn % 2 == 0:
                        if s6<7:
                            updategame(6,"y")
                            turn+=1
                    else:
                        if s6<7:
                            updategame(6,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                elif event.key == pygame.K_7:
                    if turn % 2 == 0:
                        if s7<7:
                            updategame(7,"y")
                            turn+=1
                    else:
                        if s7<7:
                            updategame(7,"r")
                            turn+=1
                    
                    last_turn_time = pygame.time.get_ticks()
                if event.key == pygame.K_z:  # Press 'Z' to undo
                    undo()
                elif event.key == pygame.K_x:  # Press 'X' to redo
                    redo()
                elif event.key == pygame.K_r:
                    reset_game(True)
                #CHEAT CODES
                elif event.key == pygame.K_END:
                    winscreen(screen,font,clock,winner="Yellow")
                elif event.key == pygame.K_PAGEDOWN:
                    winscreen(screen,font,clock,winner="Red")
        timewithcorrectformat=format_time(last_turn_time)
        checkwin()
menuscreen()