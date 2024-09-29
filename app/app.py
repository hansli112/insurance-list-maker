import streamlit as st
import pandas as pd
from insurancer import Insurancer

def main():
    st.title("保險名單")

    # input prompt
    insurancer = Insurancer("database.csv")
    insurancer.activity = st.text_input("請輸入活動名稱")
    insurancer.date = st.text_input("請輸入活動日期 (e.g. 2024.01.01)")

    # select attendants
    attendants = []
    with st.container(height=400):
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

if __name__ == "__main__":
    main()
