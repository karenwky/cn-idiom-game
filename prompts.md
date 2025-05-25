# Prompts Archive

This archive contains prompts used with Amazon Q CLI for creating the game and README.

## v1
```txt
- work in this directory: [project-path]
- make a cli game of chinese 4-word idiom
- 2 blanks and 2 words are given, player select words to fill in the blanks
- 1-word english explanation for each of the single chinese word (the 2 words given and the 5 options given)
- a simple english explanation of the chinese 4-word idiom is given
- 3 lives for player (if wrong for 3 times then game over)
- counter for correct answers
```

## v2.0
```txt
- create a new folder "v1" for all the files you've created
- clone "v1" folder and rename as "v2" in the base folder and work here
- use pygame to build a simple UI for the game in 8-bit retro style
- add button for changing the game language (繁/简/EN)
- translate the whole game into Traditional Chinese (繁) and Simplified Chinese (简)
```

## v2.1
```txt
- no need Traditional Chinese and Simplified Chinese version, instead translate the whole game into Korean and Japanese as well, also handle translation in idioms.json
- check [assets-path], i've downloaded font files, update code for loading font files
- language button only contains the word (EN/KR/JP), no need "Language: ", adjust the button size accordingly
- adjust submit button size to 85%
- no need to show the words "idiom with blanks: " when showing answer
- show the selected word filled in the blank when selecting the word (because the ordering of selecting the word is important)
- add sound effect for correct answer, wrong answer, new question, game over, end game, new game, quit game
- check your import code, no need to import class that you don't use
```

## v2.2
```txt
- DO NOT repeat questions, end game when all questions are answered
- adjust submit button size, change it back to original size, then make it 15% smaller
- japanese and korean words are too big, make them 10% smaller, and make sure the words are shown clearly within the game screen
- for chinese words (keys "idiom" and "word" in idioms.json), use NotoSansSC-Bold.ttf
- check all the files are make sure they are correctly loaded
- check [sounds-path], only these sounds are needed, end_game means game ended when all questions completed (not because of running out of lives), update all related files
- check the file structure and make sure the code can run without error
- check import code, e.g. from typing import List, Dict, Tuple, Any, Optional, List and Optional are not used so no need to import, add step to check your code after generation
- optimize your code
```

## v2.3
```txt
- you MUST use chinese font whenever data is extract from idioms["idiom"] and idioms["words"]["word"], update data in given_characters and options_for_blanks and character_meanings sections
- edit back_button as continue_button and all related settings (e.g. translations and code)
- when the game is ended, the button name should be play again
- in japanese and korean screen, given_characters and options_for_blanks and text in answer boxes are too big, make them 15% smaller
- in japanese screen, game_over and thanks_for_playing and completed_all are too long, make them show in two lines
- the idiom displayed as questions (yellow and green words, the idioms with space and the words selected) are not center aligned, make them center align in the game screen, you can refer to the alignment with submit_button
```

## v2.4
```txt
Traceback (most recent call last):
  File "cn_idiom_game_pygame.py", line 776, in <module>
    game.run()
  File "cn_idiom_game_pygame.py", line 759, in run
    self.draw_game()
  File "cn_idiom_game_pygame.py", line 530, in draw_game
    adjusted_font = pygame.font.Font(font.get_filename(), int(font.get_height() * 0.85))
                                     ^^^^^^^^^^^^^^^^^
AttributeError: 'pygame.font.Font' object has no attribute 'get_filename'
- i can't play korean and japanese version
- the chinese characters are too big now, they are even bigger than the option box, and not align with character meaning, optimize it
```

## v2.5
```txt
- \n is not working in translations.json
- the idiom display (with blanks/selected words) still not center aligned, move it a bit rightwards
- the text inside option boxes are totally out of the box now, maybe make the whole options for the blanks section to the right? make sure all the text are inside the boxes for all language versions
- some pinyin in english versions are not shown, maybe use chinese font for the whole english version?
```

## v2.6
```txt
- korean pinyin text (병음) is not showing, maybe font issue, check if korean font is used
- the option box text is still not satifying, i want given_characters and options_for_blanks sections they are like two columns, so you can make each option height bigger, to make sure the text are inside the boxes
- in english version, the text insides given_characters and options_for_blanks and character_meanings sections are not aligned, e.g. 蛇 - snake, only 蛇 - are aligned, i can see snake is using different font, solve this issue
```

## v2.7
```
- only options_for_blanks need to draw box, cancel boxes for all other sections
- make text in given_characters and options_for_blanks and character_meanings higher, for them to be inside the box, this issue still not fixed
- pinyin and meaning after answering questions are overlapped, revert their positions, no need to align center
- bring options_for_blanks section to the right, so the section is align with given_characters section
```

## v2.8
```txt
- work in [project-path]
- edit the language order as EN/JP/KR, edit all related files for the ordering
- check [jpg-path] and follow instructions in the image
- check [jpg-path] and make the layout change accordingly
```

## CLI v2.0
```
- the new path is [project-path]
- work for "cn_idiom_game_cli.py", add language feature (EN/KR/JP), let user to use arrow and enter to select the language
- update the file to show languages properly
```

## CLI v2.1
```txt
- after selecting the language, no response after pressing Enter
- write README based on [readme-path]
- add emoji to title and subtitles to make it more vivid
- must have sections of Preview, Technologies Used, Project Structure, Acknowledgments
- you may reference this README, but NO NEED to follow exactly: https://github.com/karenwky/shakespearean-made-easy/blob/main/README.md
```