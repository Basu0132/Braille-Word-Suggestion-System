import time
import json
import os
import argparse
from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.upper():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word.upper():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def _collect_words(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(prefix)
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)

    def get_suggestions(self, prefix):
        node = self.root
        for char in prefix.upper():
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._collect_words(node, prefix.upper(), results)
        return results



def levenshtein_distance(a, b):
    a = a.upper()
    b = b.upper()
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0: dp[i][j] = j
            elif j == 0: dp[i][j] = i
            elif a[i - 1] == b[j - 1]: dp[i][j] = dp[i - 1][j - 1]
            else: dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]

def get_closest_match(word, dictionary, max_distance=2):
    best_match = word
    min_distance = float('inf')
    for dict_word in dictionary:
        distance = levenshtein_distance(word, dict_word)
        if distance < min_distance and distance <= max_distance:
            min_distance = distance
            best_match = dict_word
    return best_match



braille_contractions = {
    '⠮': 'THE', '⠯': 'AND', '⠷': 'ING',
    '⠾': 'ED', '⠄': 'CH', '⠡': 'SH', '⠣': 'WH'
}

qwerty_braille_map = {
    'a': '1', 's': '2', 'd': '3', 'f': '4', 'j': '5', 'k': '6'
}

braille_to_char = {
    '100000': 'A', '101000': 'B', '110000': 'C', '110100': 'D',
    '100100': 'E', '111000': 'F', '111100': 'G', '101100': 'H',
    '011000': 'I', '011100': 'J',
    # Add more as needed
}

def qwerty_to_braille_char(qwerty_input):
    dots = ['0'] * 6
    for key in qwerty_input:
        if key in qwerty_braille_map:
            dots[int(qwerty_braille_map[key]) - 1] = '1'
    braille_code = ''.join(dots)
    return braille_to_char.get(braille_code, '?')

def apply_braille_contractions(input_text):
    for contraction, word in braille_contractions.items():
        input_text = input_text.replace(contraction, word)
    return input_text


FREQ_FILE = 'frequency.json'

if os.path.exists(FREQ_FILE):
    with open(FREQ_FILE, 'r') as f:
        selection_frequency = defaultdict(int, json.load(f))
else:
    selection_frequency = defaultdict(int)

def save_frequency():
    with open(FREQ_FILE, 'w') as f:
        json.dump(selection_frequency, f)

def rank_suggestions(suggestions):
    return sorted(suggestions, key=lambda word: selection_frequency[word.upper()], reverse=True)



def load_dictionary(filepath):
    with open(filepath, 'r') as f:
        return [line.strip().upper() for line in f.readlines() if line.strip()]



def main():
    parser = argparse.ArgumentParser(description="Braille Word Suggestion System")
    parser.add_argument('--lang', default='EN', help='Language code like EN or HI')
    parser.add_argument('--dict', default='words.txt', help='Path to dictionary file')
    args = parser.parse_args()

    lang = args.lang.upper()
    dictionary = load_dictionary(args.dict)
    trie = Trie()
    for word in dictionary:
        trie.insert(word)

    raw_input_text = input("Enter Braille input (contractions or QWERTY like 'asdf'): ").strip()
    if all(c in 'asdfjkl;' for c in raw_input_text.lower()):
        typed_word = qwerty_to_braille_char(raw_input_text)
    else:
        typed_word = apply_braille_contractions(raw_input_text)

    typed_word = typed_word.upper()

    print("\n🔎 Real-time typed word suggestions:")
    for i in range(1, len(typed_word) + 1):
        prefix = typed_word[:i]
        suggestions = trie.get_suggestions(prefix)
        ranked = rank_suggestions(suggestions)
        print(f"{prefix} → {ranked}")
        time.sleep(0.2)

    corrected_word = get_closest_match(typed_word, dictionary)
    print("\n✅ Suggested Correction:", corrected_word)

    selection_frequency[corrected_word.upper()] += 1
    save_frequency()
    print("✅ Frequency updated and saved.")

    prefix = corrected_word[:2].upper()
    suggestions = trie.get_suggestions(prefix)
    ranked = rank_suggestions(suggestions)
    print(f"\n📈 Updated ranked suggestions for '{prefix}': {ranked}")

if __name__ == "__main__":
    main()
