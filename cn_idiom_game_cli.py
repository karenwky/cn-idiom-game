#!/usr/bin/env python3
"""
Chinese 4-Character Idiom CLI Game.
A game where players fill in the blanks of Chinese idioms.
Supports multiple languages (EN/JP/KR).
"""

import json
import random
import os
import sys
import time
from typing import Dict, Any, List

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    HIGHLIGHT = '\033[7m'  # Inverted colors for highlighting

# Key codes for arrow keys and enter
UP_ARROW = '\x1b[A'
DOWN_ARROW = '\x1b[B'
ENTER = '\r'
ENTER_ALT = '\n'

# Language settings
LANGUAGES = ["en", "ja", "ko"]
LANGUAGE_DISPLAY = {"en": "English", "ko": "한국어", "ja": "日本語"}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_idioms() -> Dict[str, Any]:
    """Load idioms from the JSON file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        idioms_path = os.path.join(script_dir, 'idioms.json')
        with open(idioms_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"{Colors.RED}Error loading idioms: {e}{Colors.ENDC}")
        sys.exit(1)

def load_translations() -> Dict[str, Dict[str, str]]:
    """Load translations from the JSON file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        translations_path = os.path.join(script_dir, 'translations.json')
        with open(translations_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"{Colors.RED}Error loading translations: {e}{Colors.ENDC}")
        sys.exit(1)

def get_key():
    """Get a single keypress from the user."""
    import termios
    import fcntl
    import sys
    import os
    
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    
    try:
        while True:
            try:
                c = sys.stdin.read(1)
                if c:  # If we actually got a character
                    if c == '\x1b':  # Escape sequence
                        # Try to read the next two characters
                        c2 = sys.stdin.read(1)
                        c3 = sys.stdin.read(1)
                        if c2 and c3:  # If we got both characters
                            return '\x1b' + c2 + c3
                        else:
                            return c  # Just return escape if we didn't get the full sequence
                    else:
                        return c
            except IOError:
                pass
            time.sleep(0.01)  # Small delay to prevent CPU hogging
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def select_language(translations: Dict[str, Dict[str, str]]) -> str:
    """Let the user select a language using arrow keys."""
    clear_screen()
    selected = 0
    
    while True:
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}Select Language / 언어 선택 / 言語選択{Colors.ENDC}\n")
        
        for i, lang in enumerate(LANGUAGES):
            if i == selected:
                print(f"{Colors.HIGHLIGHT} > {LANGUAGE_DISPLAY[lang]} {Colors.ENDC}")
            else:
                print(f"   {LANGUAGE_DISPLAY[lang]}")
        
        print("\n(Use arrow keys to navigate, Enter to select)")
        
        key = get_key()
        
        if key == UP_ARROW and selected > 0:
            selected -= 1
        elif key == DOWN_ARROW and selected < len(LANGUAGES) - 1:
            selected += 1
        elif key == ENTER or key == ENTER_ALT:  # Accept both Enter key representations
            selected_lang = LANGUAGES[selected]
            print(f"\nSelected language: {LANGUAGE_DISPLAY[selected_lang]}")
            time.sleep(0.5)  # Give user feedback before continuing
            return selected_lang
        
        # Small delay to prevent too rapid key processing
        time.sleep(0.1)

def get_text(key: str, translations: Dict[str, Dict[str, str]], language: str, *args) -> str:
    """Get translated text for the current language."""
    if key in translations[language]:
        text = translations[language][key]
        if args:
            text = text.format(*args)
        return text
    return key

def select_idiom(idioms_data: Dict[str, Any]) -> Dict[str, Any]:
    """Randomly select an idiom from the data."""
    return random.choice(idioms_data['idioms'])

def create_challenge(idiom_data: Dict[str, Any], extra_words: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
    """Create a challenge by selecting two positions to blank out and generating options."""
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
    random_extra = random.sample(extra_words, 3)
    options.extend(random_extra)
    
    # Shuffle options
    random.shuffle(options)
    
    return {
        'idiom_data': idiom_data,
        'blank_positions': blank_positions,
        'display_idiom': ''.join(display_idiom),
        'options': options,
        'correct_answers': correct_answers,
        'language': language
    }

def display_challenge(challenge: Dict[str, Any], translations: Dict[str, Dict[str, str]], language: str):
    """Display the challenge to the player."""
    idiom_data = challenge['idiom_data']
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{get_text('game_title', translations, language)}{Colors.ENDC}")
    print(f"\n{Colors.YELLOW}{get_text('idiom_with_blanks', translations, language)}{Colors.ENDC} {challenge['display_idiom']}")
    print(f"{Colors.YELLOW}{get_text('pinyin', translations, language)}{Colors.ENDC} {idiom_data['pinyin']}")
    print(f"{Colors.YELLOW}{get_text('meaning', translations, language)}{Colors.ENDC} {idiom_data['meaning'][language]}")
    
    # Show the non-blank characters with their meanings
    print(f"\n{Colors.BLUE}{get_text('given_characters', translations, language)}{Colors.ENDC}")
    for i, char in enumerate(idiom_data['idiom']):
        if i not in challenge['blank_positions']:
            word_data = idiom_data['words'][i]
            print(f"  {word_data['word']} - {word_data['meaning'][language]}")
    
    # Show options
    print(f"\n{Colors.GREEN}{get_text('options_for_blanks', translations, language)}{Colors.ENDC}")
    for i, option in enumerate(challenge['options']):
        print(f"  {i+1}. {option['word']} - {option['meaning'][language]}")

def get_player_choices(num_blanks: int, num_options: int, translations: Dict[str, Dict[str, str]], language: str) -> List[int]:
    """Get the player's choices for filling in the blanks."""
    choices = []
    
    print(f"\n{Colors.BLUE}{get_text('fill_blanks_prompt', translations, language)}{Colors.ENDC}")
    
    for i in range(num_blanks):
        while True:
            try:
                choice = input(f"{get_text('blank_prompt', translations, language)}{i+1}: ")
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < num_options:
                    choices.append(choice_idx)
                    break
                else:
                    print(f"{Colors.RED}{get_text('invalid_choice', translations, language)} {num_options}.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.RED}{get_text('enter_valid_number', translations, language)}{Colors.ENDC}")
    
    return choices

def check_answer(challenge: Dict[str, Any], player_choices: List[int]) -> bool:
    """Check if the player's answer is correct."""
    selected_options = [challenge['options'][idx] for idx in player_choices]
    correct_answers = challenge['correct_answers']
    
    # Check if the selected options match the correct answers (in any order)
    return sorted(selected_options, key=lambda x: x['word']) == sorted(correct_answers, key=lambda x: x['word'])

def display_result(challenge: Dict[str, Any], is_correct: bool, translations: Dict[str, Dict[str, str]], language: str):
    """Display the result of the player's answer."""
    idiom_data = challenge['idiom_data']
    
    if is_correct:
        print(f"\n{Colors.GREEN}{get_text('correct', translations, language)}{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}{get_text('incorrect', translations, language)}{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}{get_text('idiom', translations, language)}{Colors.ENDC} {idiom_data['idiom']}")
    print(f"{Colors.YELLOW}{get_text('pinyin', translations, language)}{Colors.ENDC} {idiom_data['pinyin']}")
    print(f"{Colors.YELLOW}{get_text('meaning', translations, language)}{Colors.ENDC} {idiom_data['meaning'][language]}")
    
    # Show all characters with their meanings
    print(f"\n{Colors.BLUE}{get_text('character_meanings', translations, language)}{Colors.ENDC}")
    for word_data in idiom_data['words']:
        print(f"  {word_data['word']} - {word_data['meaning'][language]}")

def play_game():
    """Main game function."""
    # Load translations and idioms
    translations = load_translations()
    idioms_data = load_idioms()
    
    try:
        # Let the user select a language
        language = select_language(translations)
        
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}{get_text('welcome', translations, language)}{Colors.ENDC}")
        print(get_text('instructions', translations, language))
        
        lives = 3
        score = 0
        used_idioms = set()
        
        while lives > 0:
            # Display lives and score
            print(f"\n{Colors.YELLOW}{get_text('lives', translations, language)} {'❤️ ' * lives}{Colors.ENDC}")
            print(f"{Colors.GREEN}{get_text('score', translations, language)} {score}{Colors.ENDC}")
            
            # Select an idiom that hasn't been used yet
            available_idioms = [idiom for idiom in idioms_data['idioms'] 
                               if idiom['idiom'] not in used_idioms]
            
            if not available_idioms:
                print(f"\n{Colors.GREEN}{get_text('completed_all', translations, language)}{Colors.ENDC}")
                break
            
            idiom_data = random.choice(available_idioms)
            used_idioms.add(idiom_data['idiom'])
            
            # Create and display challenge
            challenge = create_challenge(idiom_data, idioms_data['extra_words'], language)
            display_challenge(challenge, translations, language)
            
            # Get player's choices
            player_choices = get_player_choices(len(challenge['blank_positions']), 
                                               len(challenge['options']),
                                               translations, language)
            
            # Check answer
            is_correct = check_answer(challenge, player_choices)
            display_result(challenge, is_correct, translations, language)
            
            if is_correct:
                score += 1
            else:
                lives -= 1
                if lives == 0:
                    print(f"\n{Colors.RED}{get_text('game_over', translations, language)}{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}{get_text('lives_remaining', translations, language, lives)}{Colors.ENDC}")
            
            # Continue prompt
            input(f"\n{get_text('press_continue', translations, language)}")
            clear_screen()
        
        # Final score
        print(f"\n{Colors.BOLD}{get_text('final_score', translations, language)} {score}{Colors.ENDC}")
        print(f"\n{get_text('thanks_for_playing', translations, language)}")
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting...")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    play_game()
