import streamlit as st
from insurancer import Insurancer

def main():
    st.title("保險名單")

    insurancer = Insurancer()
    insurancer.activity = st.text_input("請輸入活動名稱")
    insurancer.date = st.text_input("請輸入活動日期 (e.g. 2024.01.01)")

    attendants = []
    with st.container(height=400):
        for name in insurancer.data.keys():
            if st.checkbox(name):
                attendants.append(name)

    insure_list = ""
    for name in attendants:
        insure_list += ','.join([name, *insurancer.data[name]]) + '\n'

    filename = f"{insurancer.date} {insurancer.activity}.csv"
    st.download_button("下載名單", data=insure_list, file_name=filename)

if __name__ == "__main__":
    main()
