import numpy as np

class IDChecker():
    def __init__(self):
        self.weight = np.array([1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1])
        self.char2num = self.make_char2num()

    def make_char2num(self) -> dict:
        char = "ABCDEFGHJKLMNPQRSTUVXYWZIO"
        num = range(10, 36)
        return dict(zip(char, num))

    def check(self, id_number: str) -> bool:
        if len(id_number) != 10:
            return False
        try:
            idx = np.array([int(i) for i in self.char2num(id_number[0].upper()) + id_number[1:]])
            return True if sum(idx * weight) % 10 == 0 else False
        except:
            return False
