import pygame
import sys
import time
import os
from tkinter import Tk, filedialog

def create_blank_window(width, height):
    pygame.init()
    pygame.display.set_mode((1, 1))  # Initialize pygame display (required for tkinter)

    window_size = (width, height)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Blank Window")

    # Button properties
    button_width = 200
    button_height = 50
    button_color = (0, 128, 255)
    button_text_color = (0, 0, 0)  # Black color for the text
    button_font = pygame.font.Font(None, 30)

    # Game state dictionary
    game_state = {
        "Score": 0,
        "Score per click": 1,
        "SPS": 0
    }

    # Last update time for score per second
    last_update_time = time.time()

    def draw_button(text, x, y):
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(screen, button_color, button_rect)

        button_text = button_font.render(text, True, button_text_color)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        return button_rect

    # Function to save the game state as a .sgf file
    def save_game_state(filename):
        with open(filename, "w") as file:
            for key, value in game_state.items():
                file.write(f"{key} = {value}\n")

    # Function to load the game state from a .sgf file
    def load_game_state():
        try:
            Tk().withdraw()  # Hide the main tkinter window
            file_path = filedialog.askopenfilename(initialdir="C:/Users/donal/Saved Games", title="Select a saved game file", filetypes=[("Saved Game Files", "*.txt")])
            if file_path:
                with open(file_path, "r") as file:
                    data = file.read().splitlines()
                    for line in data:
                        key_value = line.split(" = ")
                        if len(key_value) == 2:
                            key = key_value[0].strip()  # Remove any leading/trailing spaces for the key
                            value = key_value[1].strip()  # Remove any leading/trailing spaces for the value
                            try:
                                value = int(value)
                            except ValueError:
                                print(f"Invalid value for key {key}: {value}. Skipping.")
                                continue
                            if key == "Score":
                                game_state["Score"] = value
                            elif key == "Score per click":
                                    game_state["Score per click"] = value
                            elif key == "SPS":
                                game_state["SPS"] = value
                            else:
                                print(f"Invalid key found: {key}. Skipping.")
                        else:
                            print(f"Invalid data in line: {line}. Skipping.")
        except FileNotFoundError:
            print("Saved game not found. Starting a new game.")

    # Helper function to handle score per click
    def handle_score_per_click(click_count):
        nonlocal game_state  # Mark 'game_state' as nonlocal since we are modifying it
        # The cost per score per click upgrade
        cost_per_click_upgrade = 5

        # Calculate the total cost based on the click count
        total_cost = click_count * cost_per_click_upgrade

        # Check if there are enough points to upgrade the score per click
        if game_state['Score'] >= total_cost:
            game_state['Score per click'] += click_count
            game_state['Score'] -= total_cost

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shift_click = pygame.key.get_mods() & pygame.KMOD_SHIFT

                if add_button_rect.collidepoint(event.pos):
                    game_state['Score'] += game_state["Score per click"]
                elif score_per_click_button_rect.collidepoint(event.pos):
                    if shift_click:
                        # Shift-clicking, buy 100 score per click upgrades at once
                        handle_score_per_click(100)
                    else:
                        # Regular clicking, buy 1 score per click upgrade
                        handle_score_per_click(game_state['Score per click'])  # Fix here
                elif save_button_rect.collidepoint(event.pos):
                    save_game_state(r"C:\users\donal\Saved Games\saved_game.txt")
                elif load_button_rect.collidepoint(event.pos):
                    load_game_state()
                elif score_per_second_button_rect.collidepoint(event.pos):
                    game_state['SPS'] += 1
                    game_state['Score'] -= 10

        # Calculate the time difference since the last update
        current_time = time.time()
        time_difference = current_time - last_update_time

        if time_difference >= 1.0:
            # Update the score per second
            game_state['Score'] += game_state['SPS']
            last_update_time = current_time

        # Clear the screen with a white background
        screen.fill((255, 255, 255))

        # Draw the buttons and get their rects for collision detection
        add_button_rect = draw_button("Add", 200, 200)
        score_per_click_button_rect = draw_button("Score Per Click", 200, 300)
        save_button_rect = draw_button("Save Game", 200, 400)
        load_button_rect = draw_button("Load Game", 200, 500)
        score_per_second_button_rect = draw_button(f"SPS: {game_state['SPS']}: -10", 450, 200)

        # Display the score and score per click at the top-left corner
        score_text = button_font.render(f"Score: {game_state['Score']}", True, (0, 0, 0))  # Black color
        score_per_click_text = button_font.render(f"Score Per Click: {game_state['Score per click']}", True, (0, 0, 0))  # Black color
        screen.blit(score_text, (10, 10))
        screen.blit(score_per_click_text, (10, 40))

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    window_width = 800
    window_height = 600
    create_blank_window(window_width, window_height)
