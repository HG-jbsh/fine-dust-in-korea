import requests
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta

def run_monitor():
    # 설정 정보
    API_KEY = "431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c"
    URL = "https://apis.data.go.kr/1480523/MetalMeasuringResultService/MetalService"
    ADMIN_NAME = "1416현겸"
    
    STATIONS = {"1":"수도권","2":"백령도","3":"호남권","4":"중부권","5":"제주권","6":"영남권","7":"경기권","8":"충청권","9":"전북권","10":"강원권","11":"충북권"}
    ITEMS = {"90303":"납(Pb)","90304":"니켈(Ni)","90305":"망간(Mn)","90314":"아연(Zn)","90319":"칼슘(Ca)","90318":"칼륨(K)","90325":"황(S)"}

    print(f"\n{'='*50}")
    print(f"{' [ ' + ADMIN_NAME + ' 미세먼지 모니터링 시스템 ] ':^48}")
    print(f"{'='*50}")

    # 날짜 입력 (기본값 어제)
    default_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    target_date = input(f"▶ 조회 날짜 입력 (예: {default_date}, 미입력시 어제): ").strip()
    if not target_date: target_date = default_date

    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '100',
        'resultType': 'JSON',
        'date': target_date,
        'timecode': 'RH02'
    }

    try:
        print(f"\n[상태] {ADMIN_NAME} 관리자 계정으로 API 데이터 요청 중...")
        response = requests.get(URL, params=params, verify=True, timeout=10)
        data = response.json()

        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])

        if not items:
            print(f"⚠️ {target_date} 데이터가 아직 없습니다. 날짜를 확인해 주세요.")
            return

        # 데이터 가공
        records = []
        for item in items:
            records.append({
                "지역": STATIONS.get(str(item['stationcode']), item['stationcode']),
                "항목": ITEMS.get(str(item['itemcode']), item['itemcode']),
                "농도": f"{item['value']} ng/m³",
                "측정시간": item['sdate']
            })

        df = pd.DataFrame(records)
        # 피벗 테이블로 변환
        pivot_df = df.pivot(index='지역', columns='항목', values='농도')

        print(f"\n✅ {target_date} 조회 결과 리포트")
        print(tabulate(pivot_df, headers='keys', tablefmt='fancy_grid'))
        print(f"\n[시스템 운영자: {ADMIN_NAME}]")

    except Exception as e:
        print(f"❌ 오류 발생: {e}\n(API 키가 유효하지 않거나 서버 연결에 실패했습니다.)")

if __name__ == "__main__":
    run_monitor()
