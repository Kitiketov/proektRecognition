import Levenshtein
from fuzzywuzzy import process


class Postprocessing():
    def __init__(self) -> None:
        self.key_list = {}
        self.word_len = set()
        with open("recognition/common_words.txt") as f:
            s = f.readlines()
        for word in s:
            word = word[:-1]
            self.word_len.add(len(word))
            if len(word) not in self.key_list:
                self.key_list[len(word)] = set()
            self.key_list[len(word)].add(word)
        self.word_len = sorted(self.word_len,reverse=True)

    def fuzzy_comparison(self,text):
        for lenght in self.word_len:

            if len(text)<lenght:continue

            for i in range(len(text)-lenght):
                window = text[i:i+lenght]
                if "1" in window:
                    edit_window = window.replace("1","l")

                    word,percent = process.extractOne(window,self.key_list[lenght])
                    word2,edit_percent = process.extractOne(edit_window,self.key_list[lenght])

                    if edit_percent>percent>65 and word == word2:
                        text = text[:i]+edit_window+text[i+lenght:]

        return text



if __name__ == "__main__":
    pp = Postprocessing()
    print(pp.fuzzy_comparison("1231og7890"))