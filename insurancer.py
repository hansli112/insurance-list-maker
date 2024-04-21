import json
import pandas as pd
from argparse import ArgumentParser
from datetime import date
from pathlib import Path

from utils.id_checker import IDChecker

class Insurancer():
    def __init__(self, database: str = "data.json"):
        with open(database) as f:
            self.data = json.load(f)
        self.columns = ["姓名", "身分證字號", "生日", "保額", "國籍", "性別"]
        self.id_checker = IDChecker()
        self.activity = None
        self.date = None

    def load_input(self, input_path: str):
        with open(input_path) as f:
            self.names = f.read().split()
        self.activity = input("請輸入活動名稱：")
        self.date = input("請輸入活動日期(e.g. 2024.01.01)：")

    def make(self):
        # collect information
        out = []
        for name in self.names:
            if name not in self.data.keys():
                info = self.make_info(name)
                self.data[name] = info
            out.append([name, *self.data[name]])

        # update the dataset
        with open(args.database, 'w', encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

        # output to csv file
        out_df = pd.DataFrame(data=out, columns=self.columns)
        out_df = out_df.sort_values(by="生日", key=lambda infos: [date(*[int(n) for n in info.split('/')]) for info in infos])
        out_df.to_csv(f"{self.date} {self.activity}.csv", index=False)

    def make_info(self, name: str):
        # ID number
        while True:
            print(f"新人員：{name}")
            id_number = input("請輸入身分證字號：").upper()
            is_id = self.id_checker.check(id_number)
            if is_id:
                res = input("身分證字號檢查未通過，是否確認資料無誤 (y/n)：")
                if res == 'n':
                    continue
            break

        while True:
            birthday = input("請輸入生日 (西元年/月/日)：")
            if birthday:
                break
            print("生日不得為空白，請重新輸入")

        # country
        while True:
            country = "A+B+C" if not is_id else input("非本國籍，請輸入國籍：")
            if country:
                break
            print("國籍不得為空白，請重新輸入")

        # gender
        while True:
            gender = self._to_gender(id_number) if not is_id else input("非本國籍，請輸入性別 M / F：").upper()
            if gender in ["M", "F"]:
                break
            print("性別錯誤，請重新輸入")

        info = (id_number, birthday, str(100), country, gender)
        return info
    
    def _to_gender(self, id_number: str) -> str:
        if id_number[1] == '1':
            return 'M'
        elif id_number[1] == '2':
            return 'F'
        else:
            return None


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--database", type=Path, default="data.json")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    insurancer = Insurancer(database=args.database)
    insurancer.load_input(input_path=args.input_path)
    insurancer.make()
