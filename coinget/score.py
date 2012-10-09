"""
score.py

tracks the current score and the highscore
"""

import os

HISCORE_PATH = os.path.join("~", ".coinget")

class Score(object):
    def __init__(self):
        self.score = 0
        self.hiscore = 0

        self.path = os.path.expanduser(HISCORE_PATH)

        if os.path.isfile(self.path):
            f = open(self.path)
            self.hiscore = int(f.read())
            f.close()

    def update(self, score):
        self.score = score
        if self.score > self.hiscore:
            self.hiscore = self.score
            f = open(self.path, "w")
            f.write(str(self.hiscore))
            f.close()

    def reset(self):
        self.score = 0
