import numpy as np

class IDChecker():
    def __init__(self):
        self.weight = np.array([1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1])
        self.char2num = self.make_char2num()

    def make_char2num(self) -> dict[str, int]:
        char = "ABCDEFGHJKLMNPQRSTUVXYWZIO"
        num = range(10, 36)
        return dict(zip(char, num))

    def check(self, id_number: str) -> bool:
        if len(id_number) != 10:
            return False
        first = [self.char2num[id_number[0].upper()] // 10, self.char2num[id_number[0].upper()] % 10]
        res = [int(i) for i in id_number[1:]]
        id_array = np.concatenate([first + res])
        return True if (id_array * self.weight).sum() % 10 == 0 else False
