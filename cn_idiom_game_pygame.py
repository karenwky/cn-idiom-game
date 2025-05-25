#!/usr/bin/env python3
"""
Chinese 4-Character Idiom Game with Pygame UI.
A game where players fill in the blanks of Chinese idioms with a retro 8-bit style UI.
"""

import json
import random
import os
import sys
import pygame
from typing import Dict, Tuple, Any

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)

# Game states
STATE_MENU = 0
STATE_GAME = 1
STATE_RESULT = 2
STATE_GAME_OVER = 3
STATE_COMPLETE = 4

# Language settings
LANGUAGES = ["en", "ja", "ko"]
LANGUAGE_DISPLAY = {"en": "EN", "ko": "KR", "ja": "JP"}

class IdiomGame:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chinese 4-Character Idiom Game")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.load_fonts()
        
        # Load game data
        self.idioms_data = self.load_idioms()
        self.translations = self.load_translations()
        
        # Load sounds
        self.load_sounds()
        
        # Game state
        self.state = STATE_MENU
        self.language = "en"
        self.lives = 3
        self.score = 0
        self.used_idioms = set()
        self.current_challenge = None
        self.result_correct = False
        
        # Load pixel art assets
        self.heart_img = self.create_pixel_heart()
        
        # Create retro-style background
        self.background = self.create_retro_background()
    
    def load_fonts(self):
        """Load fonts for different languages."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, 'assets')
        font_dir = os.path.join(assets_dir, 'font')
        
        # Default fonts
        self.font_small = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Load custom fonts if available
        try:
            # Chinese font
            cn_font_path = os.path.join(font_dir, 'NotoSansSC-Bold.ttf')
            if os.path.exists(cn_font_path):
                # Make Chinese font slightly smaller to fit in boxes
                self.cn_font_small = pygame.font.Font(cn_font_path, 22)  # Smaller size
                self.cn_font_medium = pygame.font.Font(cn_font_path, 28)  # Smaller size
                self.cn_font_large = pygame.font.Font(cn_font_path, 40)  # Smaller size
            else:
                self.cn_font_small = self.font_small
                self.cn_font_medium = self.font_medium
                self.cn_font_large = self.font_large
            
            # Korean font (15% smaller)
            kr_font_path = os.path.join(font_dir, 'NotoSansKR-Bold.ttf')
            if os.path.exists(kr_font_path):
                self.kr_font_small = pygame.font.Font(kr_font_path, 24)  # 15% smaller
                self.kr_font_medium = pygame.font.Font(kr_font_path, 30)  # 15% smaller
                self.kr_font_large = pygame.font.Font(kr_font_path, 40)  # 15% smaller
            else:
                self.kr_font_small = self.font_small
                self.kr_font_medium = self.font_medium
                self.kr_font_large = self.font_large
            
            # Japanese font (15% smaller)
            jp_font_path = os.path.join(font_dir, 'NotoSansJP-Bold.ttf')
            if os.path.exists(jp_font_path):
                self.jp_font_small = pygame.font.Font(jp_font_path, 24)  # 15% smaller
                self.jp_font_medium = pygame.font.Font(jp_font_path, 30)  # 15% smaller
                self.jp_font_large = pygame.font.Font(jp_font_path, 40)  # 15% smaller
            else:
                self.jp_font_small = self.font_small
                self.jp_font_medium = self.font_medium
                self.jp_font_large = self.font_large
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Fallback to default fonts
            self.cn_font_small = self.font_small
            self.cn_font_medium = self.font_medium
            self.cn_font_large = self.font_large
            self.kr_font_small = self.font_small
            self.kr_font_medium = self.font_medium
            self.kr_font_large = self.font_large
            self.jp_font_small = self.font_small
            self.jp_font_medium = self.font_medium
            self.jp_font_large = self.font_large
    
    def load_sounds(self):
        """Load sound effects."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.join(script_dir, 'assets', 'sounds')
        
        # Initialize sound placeholders
        self.sound_correct = None
        self.sound_wrong = None
        self.sound_game_over = None
        self.sound_end_game = None
        
        # Try to load sounds if they exist
        try:
            # Define sound file paths
            sound_files = {
                'correct': os.path.join(sounds_dir, 'correct.wav'),
                'wrong': os.path.join(sounds_dir, 'wrong.wav'),
                'game_over': os.path.join(sounds_dir, 'game_over.wav'),
                'end_game': os.path.join(sounds_dir, 'end_game.wav')
            }
            
            # Load sounds if files exist
            for sound_name, sound_path in sound_files.items():
                if os.path.exists(sound_path):
                    setattr(self, f"sound_{sound_name}", pygame.mixer.Sound(sound_path))
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound if it exists."""
        sound = getattr(self, f"sound_{sound_name}", None)
        if sound:
            sound.play()
    
    def get_font(self, size="medium", text_type=None):
        """
        Get the appropriate font based on language, size, and text type.
        text_type can be 'chinese' to force Chinese font for idioms and characters.
        """
        if text_type == 'chinese':
            return getattr(self, f"cn_font_{size}")
        elif self.language == "ko":
            return getattr(self, f"kr_font_{size}")
        elif self.language == "ja":
            return getattr(self, f"jp_font_{size}")
        else:  # default to English
            return getattr(self, f"font_{size}")
    
    def load_idioms(self) -> Dict[str, Any]:
        """Load idioms from the JSON file."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            idioms_path = os.path.join(script_dir, 'idioms.json')
            with open(idioms_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading idioms: {e}")
            sys.exit(1)
    
    def load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translations from the JSON file."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            translations_path = os.path.join(script_dir, 'translations.json')
            with open(translations_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading translations: {e}")
            sys.exit(1)
    
    def create_pixel_heart(self) -> pygame.Surface:
        """Create a pixel art heart."""
        heart = pygame.Surface((20, 20), pygame.SRCALPHA)
        
        # Define heart shape in a 2D grid (1 = filled, 0 = transparent)
        heart_shape = [
            [0, 1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0]
        ]
        
        # Draw the heart pixel by pixel
        for y, row in enumerate(heart_shape):
            for x, pixel in enumerate(row):
                if pixel:
                    pygame.draw.rect(heart, RED, (x*2+1, y*2+1, 2, 2))
        
        return heart
    
    def create_retro_background(self) -> pygame.Surface:
        """Create a retro-style background with grid pattern."""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill(DARK_GRAY)
        
        # Draw grid lines
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(bg, (60, 60, 60), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(bg, (60, 60, 60), (0, y), (SCREEN_WIDTH, y), 1)
        
        return bg
    
    def get_text(self, key: str, *args) -> str:
        """Get translated text for the current language."""
        if key in self.translations[self.language]:
            text = self.translations[self.language][key]
            if args:
                text = text.format(*args)
            return text
        return key
    
    def draw_text(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int], 
                 x: int, y: int, align: str = "left") -> pygame.Rect:
        """Draw text on the screen with specified alignment."""
        # Handle newlines in text
        if "\n" in text:
            lines = text.split("\n")
            max_width = 0
            total_height = 0
            line_surfaces = []
            
            for line in lines:
                line_surface = font.render(line, True, color)
                line_surfaces.append(line_surface)
                max_width = max(max_width, line_surface.get_width())
                total_height += line_surface.get_height()
            
            # Create a surface to hold all lines
            text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
            
            # Blit each line onto the surface
            current_y = 0
            for line_surface in line_surfaces:
                line_rect = line_surface.get_rect()
                if align == "center":
                    line_rect.centerx = max_width // 2
                elif align == "right":
                    line_rect.right = max_width
                line_rect.top = current_y
                text_surface.blit(line_surface, line_rect)
                current_y += line_surface.get_height()
            
            # Position the combined surface
            text_rect = text_surface.get_rect()
            if align == "center":
                text_rect.center = (x, y)
            elif align == "right":
                text_rect.right = x
                text_rect.top = y
            else:  # left
                text_rect.left = x
                text_rect.top = y
            
            self.screen.blit(text_surface, text_rect)
            return text_rect
        else:
            # Original code for single line text
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            
            if align == "center":
                text_rect.center = (x, y)
            elif align == "right":
                text_rect.right = x
                text_rect.top = y
            else:  # left
                text_rect.left = x
                text_rect.top = y
            
            self.screen.blit(text_surface, text_rect)
            return text_rect
        
    def draw_mixed_text(self, text: str, chinese_chars: str, font: pygame.font.Font, 
                      chinese_font: pygame.font.Font, color: Tuple[int, int, int],
                      x: int, y: int, align: str = "left") -> pygame.Rect:
        """
        Draw text with mixed fonts - Chinese characters with Chinese font, rest with regular font.
        Returns the total rect that encompasses all text.
        """
        # Split the text by Chinese characters to render them separately
        parts = []
        current_part = ""
        
        for char in text:
            if char in chinese_chars:
                if current_part:
                    parts.append((current_part, font))
                    current_part = ""
                parts.append((char, chinese_font))
            else:
                current_part += char
        
        if current_part:
            parts.append((current_part, font))
        
        # Calculate total width for positioning
        total_width = sum(part_font.render(part_text, True, color).get_width() 
                          for part_text, part_font in parts)
        
        # Calculate starting position based on alignment
        if align == "center":
            start_x = x - total_width // 2
        elif align == "right":
            start_x = x - total_width
        else:  # left
            start_x = x
        
        # Draw each part with its appropriate font
        current_x = start_x
        max_height = 0
        for part_text, part_font in parts:
            text_surface = part_font.render(part_text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.left = current_x
            text_rect.top = y - text_rect.height // 2 if align == "center" else y
            
            self.screen.blit(text_surface, text_rect)
            current_x += text_rect.width
            max_height = max(max_height, text_rect.height)
        
        # Return a rect that encompasses all the text
        return pygame.Rect(start_x, y, total_width, max_height)
    
    def draw_button(self, text: str, x: int, y: int, width: int, height: int, 
                   color: Tuple[int, int, int], hover_color: Tuple[int, int, int]) -> Tuple[pygame.Rect, bool]:
        """Draw a button and return its rect and hover state."""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        hover = button_rect.collidepoint(mouse_pos)
        
        # Draw button
        pygame.draw.rect(self.screen, hover_color if hover else color, button_rect)
        pygame.draw.rect(self.screen, WHITE, button_rect, 2)  # Border
        
        # Draw text
        self.draw_text(text, self.get_font("medium"), WHITE, 
                      button_rect.centerx, button_rect.centery, "center")
        
        return button_rect, hover
    
    def select_idiom(self) -> Dict[str, Any]:
        """Randomly select an idiom from the data."""
        available_idioms = [idiom for idiom in self.idioms_data['idioms'] 
                           if idiom['idiom'] not in self.used_idioms]
        
        if not available_idioms:
            # All idioms have been used
            return None
        
        idiom_data = random.choice(available_idioms)
        self.used_idioms.add(idiom_data['idiom'])
        return idiom_data
    
    def create_challenge(self, idiom_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a challenge by selecting two positions to blank out and generating options."""
        if idiom_data is None:
            return None
            
        idiom = idiom_data['idiom']
        words = idiom_data['words']
        
        # Select two positions to blank out (0-3)
        blank_positions = sorted(random.sample(range(4), 2))
        
        # Get the correct answers
        correct_answers = [words[pos] for pos in blank_positions]
        
        # Create a display version with blanks
        display_idiom = list(idiom)
        for pos in blank_positions:
            display_idiom[pos] = '_'
        
        # Generate options (including the correct answers)
        options = correct_answers.copy()
        
        # Add 3 random words from extra_words
        random_extra = random.sample(self.idioms_data['extra_words'], 3)
        options.extend(random_extra)
        
        # Shuffle options
        random.shuffle(options)
        
        return {
            'idiom_data': idiom_data,
            'blank_positions': blank_positions,
            'display_idiom': ''.join(display_idiom),
            'options': options,
            'correct_answers': correct_answers,
            'filled_blanks': [None, None]  # To track which option is placed in which blank
        }
    
    def check_answer(self, challenge: Dict[str, Any]) -> bool:
        """Check if the player's answer is correct."""
        if None in challenge['filled_blanks']:
            return False
            
        selected_words = [challenge['options'][idx]['word'] for idx in challenge['filled_blanks']]
        correct_words = [word['word'] for word in challenge['correct_answers']]
        
        # Check if the selected words match the correct words in the correct positions
        blank_positions = challenge['blank_positions']
        idiom_chars = list(challenge['idiom_data']['idiom'])
        
        for i, blank_pos in enumerate(blank_positions):
            idiom_chars[blank_pos] = selected_words[i]
        
        reconstructed_idiom = ''.join(idiom_chars)
        return reconstructed_idiom == challenge['idiom_data']['idiom']
    
    def draw_menu(self):
        """Draw the main menu screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title = self.get_text("game_title")
        self.draw_text(title, self.get_font("large"), YELLOW, SCREEN_WIDTH//2, 100, "center")
        
        # Draw buttons
        play_button, play_hover = self.draw_button(
            self.get_text("play_button"), 
            SCREEN_WIDTH//2 - 100, 250, 200, 60, BLUE, (100, 100, 255)
        )
        
        quit_button, quit_hover = self.draw_button(
            self.get_text("quit_button"), 
            SCREEN_WIDTH//2 - 100, 350, 200, 60, RED, (255, 100, 100)
        )
        
        # Language buttons (smaller, just showing language code)
        # Use the same font size for all language buttons
        lang_font = self.font_small  # Use the same small font for all language buttons
        
        # EN button
        en_text = "EN"
        en_surface = lang_font.render(en_text, True, WHITE)
        en_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 40, 40)
        pygame.draw.rect(self.screen, GREEN if self.language == "en" else DARK_GRAY, en_rect)
        pygame.draw.rect(self.screen, WHITE, en_rect, 2)  # Border
        en_text_rect = en_surface.get_rect(center=en_rect.center)
        self.screen.blit(en_surface, en_text_rect)
        
        # JP button
        jp_text = "JP"
        jp_surface = lang_font.render(jp_text, True, WHITE)
        jp_rect = pygame.Rect(SCREEN_WIDTH - 100, 20, 40, 40)
        pygame.draw.rect(self.screen, GREEN if self.language == "ja" else DARK_GRAY, jp_rect)
        pygame.draw.rect(self.screen, WHITE, jp_rect, 2)  # Border
        jp_text_rect = jp_surface.get_rect(center=jp_rect.center)
        self.screen.blit(jp_surface, jp_text_rect)
        
        # KR button
        kr_text = "KR"
        kr_surface = lang_font.render(kr_text, True, WHITE)
        kr_rect = pygame.Rect(SCREEN_WIDTH - 50, 20, 40, 40)
        pygame.draw.rect(self.screen, GREEN if self.language == "ko" else DARK_GRAY, kr_rect)
        pygame.draw.rect(self.screen, WHITE, kr_rect, 2)  # Border
        kr_text_rect = kr_surface.get_rect(center=kr_rect.center)
        self.screen.blit(kr_surface, kr_text_rect)
        
        # Handle button clicks
        if pygame.mouse.get_pressed()[0]:
            if play_hover:
                self.state = STATE_GAME
                self.lives = 3
                self.score = 0
                self.used_idioms = set()
                self.current_challenge = self.create_challenge(self.select_idiom())
                pygame.time.delay(200)  # Prevent double-click
            
            elif quit_hover:
                pygame.time.delay(300)  # Give time for sound to play
                pygame.quit()
                sys.exit()
            
            # Handle language button clicks
            mouse_pos = pygame.mouse.get_pos()
            if en_rect.collidepoint(mouse_pos):
                self.language = "en"
                pygame.time.delay(200)  # Prevent double-click
            elif jp_rect.collidepoint(mouse_pos):
                self.language = "ja"
                pygame.time.delay(200)  # Prevent double-click
            elif kr_rect.collidepoint(mouse_pos):
                self.language = "ko"
                pygame.time.delay(200)  # Prevent double-click
    
    def draw_idiom_with_filled_blanks(self, challenge, x, y):
        """Draw the idiom with any selected words filled in the blanks."""
        idiom = challenge['idiom_data']['idiom']
        blank_positions = challenge['blank_positions']
        filled_blanks = challenge['filled_blanks']
        
        # Create a display version with blanks or filled words
        display_chars = list(idiom)
        for i, pos in enumerate(blank_positions):
            if filled_blanks[i] is not None:
                display_chars[pos] = challenge['options'][filled_blanks[i]]['word']
            else:
                display_chars[pos] = '_'
        
        # Calculate total width to center the idiom
        total_width = len(display_chars) * 40
        start_x = x - total_width // 2 + 20  # Add 20px offset to move slightly rightward
        
        # Draw each character with spacing
        for i, char in enumerate(display_chars):
            color = YELLOW
            if i in blank_positions:
                blank_index = blank_positions.index(i)
                if filled_blanks[blank_index] is not None:
                    color = GREEN
            
            # Always use Chinese font for idiom characters
            self.draw_text(char, self.get_font("medium", 'chinese'), color, 
                          start_x + i * 40, y, "center")
    
    def draw_game(self):
        """Draw the game screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Check if all idioms have been used
        if self.current_challenge is None:
            self.state = STATE_COMPLETE
            self.play_sound("end_game")
            return
        
        # Draw lives and score
        for i in range(self.lives):
            self.screen.blit(self.heart_img, (20 + i * 30, 20))
        
        score_text = f"{self.get_text('score')} {self.score}"
        self.draw_text(score_text, self.get_font("medium"), GREEN, SCREEN_WIDTH - 20, 20, "right")
        
        # Draw idiom challenge
        challenge = self.current_challenge
        idiom_data = challenge['idiom_data']
        
        # Draw idiom with blanks or filled selections (centered)
        self.draw_idiom_with_filled_blanks(challenge, SCREEN_WIDTH//2, 80)
        
        # Draw pinyin and meaning
        pinyin_label = f"{self.get_text('pinyin')} "
        pinyin_value = idiom_data['pinyin']
        label_width = self.get_font("small").size(pinyin_label)[0]
        self.draw_text(pinyin_label, self.get_font("small"), WHITE, 50, 120, "left")
        self.draw_text(pinyin_value, self.get_font("small", 'chinese'), WHITE, 50 + label_width, 120, "left")
        
        meaning_text = f"{self.get_text('meaning')} {idiom_data['meaning'][self.language]}"
        self.draw_text(meaning_text, self.get_font("small"), WHITE, 50, 150, "left")
        
        # Draw given characters - No boxes, just text
        self.draw_text(self.get_text('given_characters'), self.get_font("medium"), BLUE, 50, 200, "left")
        
        # First column
        y_pos = 230
        col_width = SCREEN_WIDTH // 2 - 70  # Width for each column
        
        for i, char in enumerate(idiom_data['idiom']):
            if i not in challenge['blank_positions']:
                word_data = idiom_data['words'][i]
                
                # Use Chinese font for the character
                char_text = f"  {word_data['word']} - "
                self.draw_text(char_text, self.get_font("small", 'chinese'), WHITE, 50, y_pos, "left")
                
                # Draw meaning with the same font as the label for consistency
                meaning_text = f"{word_data['meaning'][self.language]}"
                char_width = self.get_font("small", 'chinese').size(char_text)[0]
                self.draw_text(meaning_text, self.get_font("small"), WHITE, 
                              50 + char_width, y_pos, "left")
                
                y_pos += 30  # Add spacing between items
        
        # Draw options - With boxes, aligned with given_characters
        self.draw_text(self.get_text('options_for_blanks'), self.get_font("medium"), GREEN, 50, 300, "left")
        
        option_buttons = []
        y_pos = 330
        
        for i, option in enumerate(challenge['options']):
            # Check if this option is already selected
            is_selected = i in challenge['filled_blanks']
            
            # Create button rect - wider and with more height
            box_height = 45  # Increased height for better text containment
            box_width = col_width
            button_rect = pygame.Rect(50, y_pos, box_width, box_height)
            
            # Draw button background
            pygame.draw.rect(self.screen, 
                            BLUE if is_selected else DARK_GRAY, 
                            button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)  # Border
            
            # Draw option text with Chinese font for character - positioned higher in the box
            option_text = f"{i+1}. {option['word']} - "
            self.draw_text(option_text, self.get_font("small", 'chinese'), WHITE, 
                          button_rect.left + 10, button_rect.centery - 5, "left")
            
            # Draw meaning with the same font as the label for consistency
            meaning_text = f"{option['meaning'][self.language]}"
            char_width = self.get_font("small", 'chinese').size(option_text)[0]
            self.draw_text(meaning_text, self.get_font("small"), WHITE, 
                          button_rect.left + 10 + char_width, button_rect.centery - 5, "left")
            
            # Check if mouse is hovering over button
            hover = button_rect.collidepoint(pygame.mouse.get_pos())
            if hover and not is_selected:
                pygame.draw.rect(self.screen, (100, 100, 255), button_rect, 2)  # Highlight border
            
            option_buttons.append((button_rect, i))
            y_pos += box_height + 5  # Add spacing between boxes
        
        # Draw submit button if 2 options are selected
        if None not in challenge['filled_blanks']:
            # Original button size with 15% reduction
            button_width = int(200 * 0.85)  # 15% smaller than original 200
            submit_button, submit_hover = self.draw_button(
                self.get_text("submit_button"), 
                SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT - 70, 
                button_width, 50, 
                GREEN, (100, 255, 100)
            )
            
            if pygame.mouse.get_pressed()[0] and submit_hover:
                self.result_correct = self.check_answer(challenge)
                if self.result_correct:
                    self.score += 1
                    self.play_sound("correct")
                else:
                    self.lives -= 1
                    self.play_sound("wrong")
                
                self.state = STATE_RESULT
                pygame.time.delay(200)  # Prevent double-click
        
        # Handle option selection
        if pygame.mouse.get_pressed()[0]:
            for button_rect, option_idx in option_buttons:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    # If already selected, deselect it
                    if option_idx in challenge['filled_blanks']:
                        blank_idx = challenge['filled_blanks'].index(option_idx)
                        challenge['filled_blanks'][blank_idx] = None
                    else:
                        # Find the first empty blank
                        for i, val in enumerate(challenge['filled_blanks']):
                            if val is None:
                                challenge['filled_blanks'][i] = option_idx
                                break
                    
                    pygame.time.delay(200)  # Prevent double-click
                    break
    
    def draw_result(self):
        """Draw the result screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw result
        if self.result_correct:
            self.draw_text(self.get_text('correct'), self.get_font("large"), GREEN, SCREEN_WIDTH//2, 80, "center")
        else:
            self.draw_text(self.get_text('incorrect'), self.get_font("large"), RED, SCREEN_WIDTH//2, 80, "center")
        
        # Draw correct idiom
        idiom_data = self.current_challenge['idiom_data']
        self.draw_text(idiom_data['idiom'], self.get_font("large", 'chinese'), YELLOW, SCREEN_WIDTH//2, 140, "center")
        
        # Draw pinyin and meaning - Left aligned, not centered
        pinyin_label = f"{self.get_text('pinyin')} "
        pinyin_value = idiom_data['pinyin']
        label_width = self.get_font("small").size(pinyin_label)[0]
        
        # Left align pinyin
        self.draw_text(pinyin_label, self.get_font("small"), WHITE, 50, 180, "left")
        self.draw_text(pinyin_value, self.get_font("small", 'chinese'), WHITE, 50 + label_width, 180, "left")
        
        # Left align meaning
        meaning_text = f"{self.get_text('meaning')} {idiom_data['meaning'][self.language]}"
        self.draw_text(meaning_text, self.get_font("small"), WHITE, 50, 210, "left")
        
        # Draw all character meanings - No boxes
        self.draw_text(self.get_text('character_meanings'), self.get_font("medium"), BLUE, 50, 260, "left")
        y_pos = 300
        
        for word_data in idiom_data['words']:
            # Use Chinese font for the character
            char_text = f"  {word_data['word']} - "
            self.draw_text(char_text, self.get_font("small", 'chinese'), WHITE, 50, y_pos, "left")
            
            # Draw meaning with the same font as the label for consistency
            meaning_text = f"{word_data['meaning'][self.language]}"
            char_width = self.get_font("small", 'chinese').size(char_text)[0]
            self.draw_text(meaning_text, self.get_font("small"), WHITE, 
                          50 + char_width, y_pos, "left")
            
            y_pos += 30  # Add spacing between items
        
        # Draw continue button
        continue_button, continue_hover = self.draw_button(
            self.get_text('continue_button'), 
            SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 70, 150, 50, 
            BLUE, (100, 100, 255)
        )
        
        if pygame.mouse.get_pressed()[0] and continue_hover:
            if self.lives <= 0:
                self.state = STATE_GAME_OVER
                self.play_sound("game_over")
            else:
                # Get next idiom
                next_idiom = self.select_idiom()
                if next_idiom:
                    self.state = STATE_GAME
                    self.current_challenge = self.create_challenge(next_idiom)
                else:
                    self.state = STATE_COMPLETE
                    self.play_sound("end_game")
            pygame.time.delay(200)  # Prevent double-click
    
    def draw_game_over(self):
        """Draw the game over screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw game over message
        self.draw_text(self.get_text('game_over'), self.get_font("large"), RED, SCREEN_WIDTH//2, 150, "center")
        
        # Draw final score
        score_text = f"{self.get_text('final_score')} {self.score}"
        self.draw_text(score_text, self.get_font("large"), GREEN, SCREEN_WIDTH//2, 250, "center")
        
        # Draw thanks message
        self.draw_text(self.get_text('thanks_for_playing'), self.get_font("medium"), YELLOW, SCREEN_WIDTH//2, 350, "center")
        
        # Draw back to menu button
        menu_button, menu_hover = self.draw_button(
            self.get_text('play_again_button'), 
            SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 70, 150, 50, 
            BLUE, (100, 100, 255)
        )
        
        if pygame.mouse.get_pressed()[0] and menu_hover:
            self.state = STATE_MENU
            pygame.time.delay(200)  # Prevent double-click
    
    def draw_complete(self):
        """Draw the completion screen when all idioms are answered."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw completion message
        self.draw_text(self.get_text('completed_all'), self.get_font("large"), GREEN, SCREEN_WIDTH//2, 150, "center")
        
        # Draw final score
        score_text = f"{self.get_text('final_score')} {self.score}"
        self.draw_text(score_text, self.get_font("large"), YELLOW, SCREEN_WIDTH//2, 250, "center")
        
        # Draw thanks message
        self.draw_text(self.get_text('thanks_for_playing'), self.get_font("medium"), WHITE, SCREEN_WIDTH//2, 350, "center")
        
        # Draw back to menu button
        menu_button, menu_hover = self.draw_button(
            self.get_text('play_again_button'), 
            SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 70, 150, 50, 
            BLUE, (100, 100, 255)
        )
        
        if pygame.mouse.get_pressed()[0] and menu_hover:
            self.state = STATE_MENU
            pygame.time.delay(200)  # Prevent double-click
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in [STATE_GAME, STATE_RESULT, STATE_GAME_OVER, STATE_COMPLETE]:
                            self.state = STATE_MENU
                        else:
                            running = False
            
            # Draw current state
            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_GAME:
                self.draw_game()
            elif self.state == STATE_RESULT:
                self.draw_result()
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over()
            elif self.state == STATE_COMPLETE:
                self.draw_complete()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = IdiomGame()
    game.run()
