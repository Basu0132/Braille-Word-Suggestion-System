# Braille-Word-Suggestion-System
This Braille Word Suggestion System enables users to input Braille characters using a standard QWERTY keyboard (six-key entry) and provides real-time word suggestions and autocorrections. It leverages:

Trie data structure for fast prefix-based lookup

Levenshtein distance for typo correction

Persistent learning to improve suggestions based on user selection frequency

Basic Braille contractions and QWERTY-to-Braille mappings

Multilingual support via command-line options

**Features**

Real-time suggestions: As the user types, the system displays possible completions.

Autocorrect: Suggests the closest match when the input is not an exact prefix.

Persistence: Remembers user-selected words across sessions by saving frequencies to frequency.json.

Braille contractions: Supports Grade 2 contractions (e.g., ⠮ → THE).

QWERTY mappings: Maps keys a,s,d,f,j,k to Braille dots 1–6.

Multilingual: Switch between languages (e.g., EN, HI) via --lang.

Large dictionary: Load a dictionary file (words.txt) with 10,000+ words.

**Installation**

Clone the repository or copy the script.

Ensure you have Python 3.6+ installed.

Install dependencies if any (standard library only).

**Usage**

python braille_suggester.py --lang EN --dict words.txt

--lang : Language code (default: EN)

--dict : Path to dictionary file (each word on separate line)

Example Session

$ python braille_suggester.py --lang EN --dict words.txt
Enter Braille input (contractions or QWERTY like 'asdf'): asdf

 Real-time typed word suggestions:
1 → ['A', ...]
12 → ['AB', ...]
...

 Suggested Correction: ABLE
 Frequency updated and saved.

 Updated ranked suggestions for 'AB': ['ABLE', 'ABOUT', ...]


**Learning Mechanism:**

Improves accuracy over time by promoting frequently selected words.

Frequency data persisted in frequency.json.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Braille Keyboard Layout
Place your fingers on the keyboard as shown to input Braille patterns via QWERTY six-key entry.

 <img width="1010" height="636" alt="image" src="https://github.com/user-attachments/assets/76a84450-1b6f-430f-a592-313da2968034" />

This diagram illustrates how to position your left hand (keys Q, W, D) and right hand (keys K, O, P) to represent the six dots of a Braille cell. Each key corresponds to a dot number:
Key	Dot	Finger
Q	3	Ring
W	2	Middle
D	1	Index
K	4	Index
O	5	Middle
P	6	Ring
Tip: Press multiple keys simultaneously to form a single Braille character.
**Braille Character Mapping**
Each letter of the alphabet is encoded by raising specific dots in the 2×3 Braille cell shown below.
The chart above shows all 26 letters (A–Z) with their corresponding dot patterns. Dots are numbered:
1 4
2 5
3 6


<img width="1872" height="546" alt="image" src="https://github.com/user-attachments/assets/9bf91afa-a6f4-4caf-b176-8db100725d90" />

•	A: dot 1
•	B: dots 1,2
•	C: dots 1,4
•	D: dots 1,4,5
•	... up to Z: dots 1,3,5,6
Use this mapping to verify which keys to press for each letter when typing via QWERTY.
Each letter of the alphabet corresponds to a unique combination of raised dots. Below is the standard six-dot mapping for A–Z:
•	Dots are numbered: 1 4 2 5 3 6
•	For example, C is dots 1 + 4, H is dots 1 + 2 + 5, W is dots 2 + 4 + 5 + 6.



