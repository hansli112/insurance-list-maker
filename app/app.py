import datetime

import pandas as pd
import streamlit as st

from insurancer import Insurancer

def main():
    st.title("保險名單")
    insurancer = Insurancer("database.csv")

    # tabs
    create_list_tab, new_member_tab = st.tabs(["建立保險名單", "新增人員"])
    
    with create_list_tab:
        # input prompt
        insurancer.activity = st.text_input("請輸入活動名稱")
        insurancer.date = st.text_input("請輸入活動日期 (e.g. 2024.01.01)")
        

        # select attendants
        attendants = []
        with st.container(height=450):
            for name, note in zip(insurancer.data[insurancer.columns[0]], insurancer.data["備註"]):
                label = name if note == "" else f"{name} ({note})"
                if st.checkbox(label):
                    attendants.append(name)

        # make dataframe
        insurance_df = pd.DataFrame(columns=insurancer.data.columns)
        for name in attendants:
            info = insurancer.data[insurancer.data["姓名"] == name]
            insurance_df = pd.concat([insurance_df, info], ignore_index=True)

        # output csv file
        filename = f"{insurancer.date} {insurancer.activity}.csv"
        insurance_csv = insurance_df.to_csv(columns=insurancer.columns, index=False)
        st.download_button("下載名單", data=insurance_csv, file_name=filename)

    with new_member_tab:
        name = st.text_input("姓名")
        id_number = st.text_input("身分證字號", max_chars=10)
        if id_number != "" and not insurancer.id_checker.check(id_number.upper()):
            st.error("身分證字號檢查未通過")
        birthday = str(st.date_input("生日", min_value=datetime.date(1930, 1, 1))).replace('-', '/')
        country = st.text_input("國籍", value="中華民國")
        gender = st.selectbox("性別", ["男", "女"])
        note = st.text_input("備註")

        if st.button("新增"):
            if name and insurancer.id_checker.check(id_number.upper()) and birthday and country and gender:
                if id_number in insurancer.data["身分證字號"].values:
                    st.error("身分證字號已存在")
                if name in insurancer.data["姓名"].values and note == "":
                    st.error("姓名已存在，請輸入備註")
                else:
                    info = pd.DataFrame({
                        "姓名": [name],
                        "身分證字號": [id_number],
                        "生日": [birthday],
                        "保額": [100],
                        "國籍": ["A+B+C"] if country == "中華民國" else [country],
                        "性別": [gender],
                        "備註": [note]
                    })
                    insurancer.data = pd.concat((insurancer.data, info), ignore_index=True)
                    insurancer.data = insurancer.data.sort_values(
                            by="生日", 
                    )
                    print(insurancer.data)
                    insurancer.data.to_csv("database.csv", index=False)
                    st.success("新增成功")
            else:
                st.error("請確認資料無誤")
        

if __name__ == "__main__":
    main()
