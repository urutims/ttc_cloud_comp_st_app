import streamlit as st
import requests
import json

from datetime import date
from dateutil.relativedelta import relativedelta

# 年齢計算


def calc_age(birth_day):
    today = date.today()
    age = relativedelta(today, birth_day).years
    return age


def check_known(family_name, first_name, birth_day):
    with open("assets/known_people.json", "r", encoding="utf-8") as f:
        known_people = json.load(f)

    user = {
        "family_name": family_name,
        "first_name": first_name,
        "birth_day": birth_day.strftime("%Y-%m-%d")
    }

    return user in known_people


@st.cache_data
def onomancy(family_name, first_name):
    url = f"https://enamae.net/result/{family_name}__{first_name}.webp"
    response = requests.get(url)
    return response.url


st.markdown("# 姓名判断アプリ")

family_name = st.text_input("姓を入力してください", max_chars=16)
first_name = st.text_input("名を入力してください", max_chars=16)

birth_day = st.date_input("生年月日を入力してください", value=date(
    1990, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())

if st.button("判定"):
    full_name = f"{family_name} {first_name}"

    age = calc_age(birth_day)
    if check_known(family_name, first_name, birth_day):
        st.text("あなたのことはよく知っていますよ。")
    st.text(f"こんにちは、{full_name} ({age}歳)さん。こちらがあなたの姓名判断結果です。")
    st.image(onomancy(family_name, first_name))
