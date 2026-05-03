import os
import random
import sys

import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
WORDS_FILE = os.path.join(BASE_DIR, "words", "words.txt")
CRAB_WORDS_FILE = os.path.join(BASE_DIR, "words", "crab_words.txt")

WIDTH = 900
HEIGHT = 560
FPS = 60
BG_COLOR = (18, 33, 58)
TEXT_COLOR = (240, 240, 240)
ACCENT_COLOR = (52, 214, 219)
ERROR_COLOR = (234, 94, 94)
TREASURE_COLOR = (212, 175, 55)

NINJA_START_X = 100
PIRATE_START_X = 100
TARGET_X = 760

NINJA_STEP = 45
PIRATE_STEP = 20


def load_words(path, min_length=3):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
        words = [word for word in words if len(word) >= 3]
        if words:
            return words

    return ["cat", "dog", "sun", "map", "hat", "fox", "pig", "run", "sky", "box"]


def load_sprite(filename, size, color):
    path = os.path.join(IMAGES_DIR, filename)
    try:
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.scale(sprite, size)
        return sprite
    except pygame.error:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=12)
        return surface


def draw_text(surface, text, x, y, size=32, color=TEXT_COLOR, center=False):
    font = pygame.font.SysFont("arial", size, bold=True)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)


def reset_game(state, words):
    state["current_word"] = random.choice(words)
    state["typed"] = ""
    state["ninja_x"] = NINJA_START_X
    state["pirate_x"] = PIRATE_START_X
    state["score"] = 0
    state["message"] = "Type the letters to move the ninja!"
    state["game_over"] = False
    state["winner"] = None
    state["crab_mode"] = False
    state["crab_done"] = False
    state["normal_words_finished"] = 0


def main():
    pygame.init()
    pygame.display.set_caption("Ninja vs Pirate Typing Game")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    words = load_words(WORDS_FILE, min_length=3)
    crab_words = load_words(CRAB_WORDS_FILE, min_length=4)
    state = {}
    reset_game(state, words)

    ninja_sprite = load_sprite("ninja.png", (120, 120), (49, 121, 217))
    pirate_sprite = load_sprite("pirate.png", (120, 120), (210, 81, 81))
    treasure_sprite = load_sprite("treasure.png", (100, 100), TREASURE_COLOR)
    crab_sprite = load_sprite("crab.png", (100, 80), (224, 98, 18))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state["game_over"]:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        reset_game(state, words)
                    continue

                if event.key == pygame.K_BACKSPACE:
                    state["typed"] = state["typed"][:-1]
                elif event.unicode.isalpha() and len(state["typed"]) < len(state["current_word"]):
                    typed_char = event.unicode.lower()
                    next_char = state["current_word"][len(state["typed"])].lower()
                    if typed_char == next_char:
                        state["typed"] += typed_char
                        state["ninja_x"] += NINJA_STEP
                        state["message"] = "Nice! Keep going..."
                    else:
                        state["message"] = f"Oops! Expected '{next_char.upper()}'. Try again."

                if state["typed"] == state["current_word"]:
                    state["score"] += 1
                    state["typed"] = ""
                    state["pirate_x"] += PIRATE_STEP

                    if state["crab_mode"]:
                        state["crab_mode"] = False
                        state["current_word"] = random.choice(words)
                        state["message"] = "Crab defeated! Back to regular words."
                    else:
                        state["normal_words_finished"] += 1
                        if not state["crab_done"] and state["normal_words_finished"] >= 2 and random.random() < 0.35:
                            state["crab_mode"] = True
                            state["crab_done"] = True
                            state["current_word"] = random.choice(crab_words)
                            state["message"] = "🦀 Crab Attack! Type the mini-boss word!"
                        else:
                            state["current_word"] = random.choice(words)
                            state["message"] = "Word complete! New challenge ahead."

        if not state["game_over"]:
            if state["ninja_x"] >= TARGET_X - 70:
                state["game_over"] = True
                state["winner"] = "Ninja"
                state["message"] = "You found the treasure! Press Enter to play again."
            elif state["pirate_x"] >= TARGET_X - 70:
                state["game_over"] = True
                state["winner"] = "Pirate"
                state["message"] = "Pirate reached the treasure! Press Enter to try again."

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, (35, 41, 68), (0, 0, WIDTH, 110))
        pygame.draw.rect(screen, (40, 60, 90), (50, 420, WIDTH - 100, 100), border_radius=12)


        if state["crab_mode"]:
            draw_text(screen, "CRAB ATTACK!", WIDTH // 2, 20, size=36, color=ERROR_COLOR, center=True)
        else:
            draw_text(screen, "Ninja vs Pirate — Type the word to reach the treasure!", WIDTH // 2, 20, size=30, center=True)

        draw_text(screen, f"Score: {state['score']}", 50, 20, size=28)
        draw_text(screen, state["message"], 50, 60, size=24, color=ACCENT_COLOR)

        # Draw treasure
        treasure_rect = treasure_sprite.get_rect(center=(TARGET_X + 50, HEIGHT // 2 + 40))
        screen.blit(treasure_sprite, treasure_rect)
        draw_text(screen, "TREASURE", treasure_rect.centerx, treasure_rect.bottom + 8, size=18, center=True)

        # Draw ninja and pirate
        ninja_pos = (state["ninja_x"], 250)
        pirate_pos = (state["pirate_x"], 380)
        screen.blit(ninja_sprite, ninja_pos)
        screen.blit(pirate_sprite, pirate_pos)

        if state["crab_mode"]:
            crab_pos = (state["ninja_x"] + 130, 260)
            screen.blit(crab_sprite, crab_pos)

        # Word display
        draw_text(screen, "Current word:", 50, 140, size=26)

        # Animated reveal: each letter drawn separately, centered horizontally
        word = state["current_word"]
        letter_spacing = 25
        font = pygame.font.SysFont("arial", 48, bold=True)
        char_widths = [font.render(char.upper(), True, TEXT_COLOR).get_width() for char in word]
        total_width = sum(char_widths) + letter_spacing * (len(word) - 1) if len(word) > 0 else 0
        start_x = WIDTH // 2 - total_width // 2
        x = start_x
        for i, char in enumerate(word):
            color = ACCENT_COLOR if i < len(state["typed"]) else TEXT_COLOR
            draw_text(screen, char.upper(), x, 180, size=48, color=color)
            x += char_widths[i] + letter_spacing


        draw_text(screen, f"Typed: {state['typed'].upper()}", 50, 240, size=28)

        # Progress bars
        pygame.draw.line(screen, (80, 88, 126), (50, 520), (TARGET_X + 50, 520), 8)
        pygame.draw.circle(screen, (69, 138, 252), (int(state["ninja_x"] + 60), 520), 14)
        pygame.draw.circle(screen, (210, 81, 81), (int(state["pirate_x"] + 60), 520), 14)
        pygame.draw.circle(screen, TREASURE_COLOR, (TARGET_X + 50, 520), 18)

        if state["game_over"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "Game Over", WIDTH // 2, HEIGHT // 2 - 80, size=56, center=True)
            winner_text = "You win!" if state["winner"] == "Ninja" else "Pirate wins!"
            draw_text(screen, winner_text, WIDTH // 2, HEIGHT // 2 - 20, size=42, color=ACCENT_COLOR, center=True)
            draw_text(screen, "Press Enter to play again.", WIDTH // 2, HEIGHT // 2 + 40, size=28, center=True)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
