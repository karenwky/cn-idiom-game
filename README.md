# 🧩 Chinese 4-Character Idiom Game (四字成语填空游戏)

A multilingual interactive game for learning Chinese 4-character idioms (四字成语 sìzìchéngyǔ) in CLI and Pygame GUI versions.

> [!NOTE]
> **Curious about the entire building process? Read my [blog post](https://www.linkedin.com/posts/wongkayankaren_amazonqcli-awscommunity-genai-activity-7335329297185873923-MFH9) for the full story! 👾**

## 🎮 Preview

The Chinese 4-Character Idiom Game offers an engaging way to learn and practice Chinese idioms through an interactive fill-in-the-blank format. Players are presented with Chinese 4-character idioms where 2 characters are hidden, and they must select the characters in correct order from a list of options.

### CLI Version

The CLI version offers a text-based interface with color-coded feedback, multiple-choice options, and language selection. Players fill in the blanks for Chinese idioms using keyboard input and receive instant validation of their answers.

<img height=700 align="center" alt="CLI Image Preview (EN)" src="https://github.com/user-attachments/assets/51277ae3-4177-4cc2-840e-c3d5ae9b7b51">

<br>
<br>

<details>
  <summary><b><big>🕹️ Video Demo</big></b></summary>
  
  https://github.com/user-attachments/assets/8ebc3f6d-b0f1-45f4-aa4f-dac0acc96d45
  
</details>

### GUI Version

The GUI version features a retro 8-bit style interface with colorful visuals, sound effects, and smooth animations. Players can select answers by clicking buttons and receive immediate feedback on their answers.

<img height=600 align="center" alt="CLI Video Preview (EN)" src="https://github.com/user-attachments/assets/0ee7268c-74e2-4a27-bbd1-b809167a12a2">

<br>
<br>

<details>
  <summary><b><big>🕹️ Video Demo (🔊Sound ON!)</big></b></summary>
  
  https://github.com/user-attachments/assets/4cd2d8f7-fa0f-4da0-90a3-9e842a4cec33

</details>

> [!TIP]
> The demo videos showcase only three sample questions for illustration purposes. [Download the game](#-how-to-play) to explore the full question set!

## 🚀 Technologies Used

- **Amazon Q CLI**: Autonomous AI agent for dynamic coding
- **Python 3.6+**: Core programming language
- **Pygame**: For the graphical user interface and game rendering
- **JSON**: For storing idioms, translations, and game data
- **Termios/Fcntl**: For terminal control in the CLI version
- **Noto Sans Fonts**: For multilingual text rendering (Chinese, Japanese, Korean)
- **WAV Audio**: For game sound effects

## 🔮 Features

- **Multilingual Support**: 
  - English (EN)
  - Japanese (JP)
  - Korean (KR)
  - Language selection via arrow key navigation in CLI version, and using click button in GUI version

- **Two Game Modes**:
  - CLI (Command Line Interface) for terminal enthusiasts
  - GUI with Pygame for a more visual experience

- **Educational Content**:
  - Learn Chinese idioms with proper context
  - Understand individual character meanings
  - Practice character recognition and pinyin (Chinese Phonetic Alphabet)

- **Game Elements**:
  - Lives system (3 hearts)
  - Score tracking
  - Randomized blank positions
  - Sound effects for actions (GUI version)
  - Retro 8-bit visual style (GUI version)

## 🎲 How to Play

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/karenwky/cn-idiom-game
   cd cn-idiom-game
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Game

**CLI Version:**
```
python cn_idiom_game_cli.py
```
- Use arrow keys to navigate the language selection menu
- Press <kbd>Enter</kbd> to select your preferred language
- Follow on-screen instructions to play

**GUI Version:**
```
python cn_idiom_game_pygame.py
```
- Click on language button to change languages
- Click on character options to fill in the blanks
- Click <kbd>Submit</kbd> when you've selected your answers

### Game Rules

1. You start with 3 lives (❤️❤️❤️)
2. Each idiom has 2 blanks that need to be filled
3. Select the characters in correct order from the options provided
4. Correct answers increase your score
5. Incorrect answers cost you a life
6. Game ends when you run out of lives or complete all idioms

## 📁 Project Structure

```
cn-idiom-game/
├── assets/
│   ├── font/
│   │   ├── NotoSansSC-Bold.ttf    # Chinese font
│   │   ├── NotoSansJP-Bold.ttf    # Japanese font
│   │   └── NotoSansKR-Bold.ttf    # Korean font
│   └── sounds/
│       ├── correct.wav            # Sound for correct answers
│       ├── wrong.wav              # Sound for wrong answers
│       ├── game_over.wav          # Sound for game over
│       └── end_game.wav           # Sound for completing all idioms
├── cn_idiom_game_cli.py           # CLI version of the game
├── cn_idiom_game_pygame.py        # GUI version with Pygame
├── idioms.json                    # Data source of Chinese idioms
├── translations.json              # Multilingual text translations
├── requirements.txt               # Project dependencies
└── prompts.md                     # Prompts archive for Amazon Q CLI
```

## ⚙️ Customization

### Adding Custom Sound Effects
Place WAV files in `assets/sounds/`:
- correct.wav
- wrong.wav
- game_over.wav
- end_game.wav

### Custom Fonts
Required fonts in `assets/font/`:
- NotoSansSC-Bold.ttf (Chinese)
- NotoSansJP-Bold.ttf (Japanese)
- NotoSansKR-Bold.ttf (Korean)

### Adding New Idioms
Edit `idioms.json` following this format:
```json
{
  "idiom": "四字成语",
  "pinyin": "sì zì chéng yǔ",
  "meaning": {
    "en": "English meaning",
    "ja": "Japanese meaning",
    "ko": "Korean meaning"
  },
  "words": [
    {
      "word": "四",
      "meaning": {
        "en": "four",        
        "ja": "四",
        "ko": "넷"
      }
    }
  ]
}
```

## 🛠️ Potential Enhancements

- **UI Optimization**: Resolve text alignment issues and prevent button overlap
- **Database Integration**: Use database instead of JSON for large datasets
- **Real-time LLM-generated Questions**: Generate more varied questions
- **Timer Limit**: Set varying time limits based on difficulty levels
- **Keyboard Control**: Use keyboard to play the game in GUI version
- **Leaderboard**: For showing score ranking
- **Additional Languages**: Support for more languages

## 🙏 Acknowledgments

**AWS Cloud Community**
- [Build Games with Amazon Q CLI and score a T shirt 🏆👕](https://community.aws/content/2xIoduO0xhkhUApQpVUIqBFGmAc/build-games-with-amazon-q-cli-and-score-a-t-shirt?lang=en)
- [Vibe Coding in Practice: Building a Classic Platform Jumping Game with Amazon Q CLI](https://community.aws/content/2vlITBGRfv8slpeU1UlTrpT4bBI/vibe-coding-in-practice-building-a-super-mario-game-with-amazon-q-developer-cli)

**AWS Blog / AWS Documentation**
- [Amazon Q Developer CLI supports image inputs in your terminal](https://aws.amazon.com/blogs/devops/amazon-q-developer-cli-supports-image-inputs-in-your-terminal/)
- [Using Amazon Q Developer on the command line - Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)

**Fonts**
- [Noto - Google Fonts](https://fonts.google.com/noto)

**Sound Effects**
- [StavSounds](https://freesound.org/people/StavSounds/)
- [deleted_user_877451](https://freesound.org/people/deleted_user_877451/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created with ❤️ for Chinese language learners everywhere
