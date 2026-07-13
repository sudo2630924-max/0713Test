import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌆 서울과 양평의 기온 비교")
st.write("서울과 양평의 시간별 기온 데이터를 비교하여 도시 열섬현상을 살펴봅니다.")

# 데이터 읽기
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yang = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜 형식 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yang["일시"] = pd.to_datetime(yang["일시"])

# 필요한 열만 선택
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울"})
yang = yang[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평"})

# 데이터 합치기
df = pd.merge(seoul, yang, on="일시")

# 기온 차(서울 - 양평)
df["기온차"] = df["서울"] - df["양평"]

# 시간, 월 정보 추가
df["시간"] = df["일시"].dt.hour
df["월"] = df["일시"].dt.month

# -------------------------------
st.header("① 1년간 두 지역의 기온 변화")

line_df = df.set_index("일시")[["서울", "양평"]]
st.line_chart(line_df)

# -------------------------------
st.header("② 시각(0~23시)별 평균 기온차 (서울 - 양평)")

hour_avg = df.groupby("시간")["기온차"].mean()
st.bar_chart(hour_avg)

# -------------------------------
st.header("③ 월(1~12월)별 평균 기온차 (서울 - 양평)")

month_avg = df.groupby("월")["기온차"].mean()
st.bar_chart(month_avg)

# -------------------------------
st.header("기본 통계")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("서울 평균 기온", f"{df['서울'].mean():.2f} ℃")

with col2:
    st.metric("양평 평균 기온", f"{df['양평'].mean():.2f} ℃")

with col3:
    st.metric("평균 기온차", f"{df['기온차'].mean():.2f} ℃")

st.write("---")
st.write("※ 기온차가 **양수(+)**일수록 서울이 양평보다 더 따뜻하며, 이는 도시 열섬현상을 확인하는 데 활용할 수 있습니다.")
