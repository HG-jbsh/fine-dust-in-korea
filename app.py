import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. API 설정
SERVICE_KEY = '8a4edeedbcb75d75a704e7153881a3e5540070c2cff8f9ed23084f2303f224eb' # 발급받은 Decoding 인증키 입력
URL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'

def get_air_quality(sido_name):
    params = {
        'serviceKey': SERVICE_KEY,
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': sido_name,
        'ver': '1.0',
    }
    
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()
        items = data['response']['body']['items']
        return pd.DataFrame(items)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 2. Streamlit 대시보드 구성
st.set_page_config(page_title="실시간 미세먼지 대시보드", layout="wide")
st.title("🌡️ 실시간 대기오염 정보 대시보드")

sido = st.sidebar.selectbox("지역(시도) 선택", ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종'])

if st.sidebar.button("데이터 업데이트"):
    df = get_air_quality(sido)
    
    if not df.empty:
        # 데이터 전처리 (숫자형 변환)
        df['pm10Value'] = pd.to_numeric(df['pm10Value'], errors='coerce')
        df['pm25Value'] = pd.to_numeric(df['pm25Value'], errors='coerce')
        df = df.dropna(subset=['pm10Value', 'pm25Value'])

        # 메트릭 표시 (상단)
        avg_pm10 = round(df['pm10Value'].mean(), 2)
        avg_pm25 = round(df['pm25Value'].mean(), 2)
        
        col1, col2 = st.columns(2)
        col1.metric("평균 미세먼지 (PM10)", f"{avg_pm10} ㎍/㎥")
        col2.metric("평균 초미세먼지 (PM2.5)", f"{avg_pm25} ㎍/㎥")

        # 시각화 (Plotly 차트)
        st.subheader(f"{sido} 지역 측정소별 미세먼지 현황")
        fig = px.bar(df, x='stationName', y='pm10Value', 
                     title="측정소별 PM10 농도",
                     labels={'stationName': '측정소', 'pm10Value': '농도(㎍/㎥)'},
                     color='pm10Value', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

        # 상세 데이터 표
        st.subheader("상세 데이터")
        st.dataframe(df[['stationName', 'dataTime', 'pm10Value', 'pm25Value', 'khaiValue']])
    else:
        st.warning("데이터를 불러올 수 없습니다. API 키를 확인해주세요.")
