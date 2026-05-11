import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate

class MetalMonitor:
    def __init__(self):
        self.api_key = "431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c"
        self.url = "http://apis.data.go.kr/1480523/MetalMeasuringResultService/MetalService"
        
        # 측정소 및 항목 설정
        self.stations = {
            "1": "수도권", "2": "백령도", "3": "호남권", "4": "중부권",
            "5": "제주권", "6": "영남권", "7": "경기권", "8": "충청권",
            "9": "전북권", "10": "강원권", "11": "충북권"
        }
        self.items = {
            "90303": "납(Pb)", "90304": "니켈(Ni)", "90305": "망간(Mn)",
            "90314": "아연(Zn)", "90319": "칼슘(Ca)", "90318": "칼륨(K)", "90325": "황(S)"
        }

    def fetch_data(self, target_date=None, timecode="RH02"):
        """API 데이터를 가져와 데이터프레임으로 반환"""
        if target_date is None:
            # 어제 날짜 기본값
            target_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        else:
            target_date = target_date.replace("-", "")

        params = {
            "ServiceKey": self.api_key,
            "pageNo": "1",
            "numOfRows": "100",
            "resultType": "JSON",
            "date": target_date,
            "timecode": timecode
        }

        print(f"\n[1416현겸] {target_date} 데이터를 불러오는 중...")

        try:
            response = requests.get(self.url, params=params, timeout=10)
            data = response.json()
            
            items_list = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            
            if not items_list:
                print("⚠️ 해당 날짜에 데이터가 없습니다.")
                return None

            # 데이터 가공
            processed_data = []
            for item in items_list:
                s_code = str(item.get('stationcode'))
                i_code = str(item.get('itemcode'))
                
                processed_data.append({
                    "지역": self.stations.get(s_code, f"코드({s_code})"),
                    "성분": self.items.get(i_code, f"코드({i_code})"),
                    "농도(ng/m³)": item.get('value'),
                    "측정시간": item.get('sdate')
                })

            df = pd.DataFrame(processed_data)
            # 보기 좋게 피벗 테이블 생성
            pivot_df = df.pivot(index='지역', columns='성분', values='농도(ng/m³)')
            return pivot_df

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return None

    def display(self, df):
        """결과를 표 형태로 출력"""
        if df is not None:
            print("\n" + "="*70)
            print("         1416현겸 - 지역별 미세먼지 금속성분 모니터링 결과")
            print("="*70)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', numalign="right"))
            print(f"\n* 생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("표시할 데이터가 없습니다.")

# --- 실행부 ---
if __name__ == "__main__":
    monitor = MetalMonitor()
    
    # 1. 날짜 입력 (엔터 치면 어제 날짜로 조회)
    user_date = input("조회할 날짜(YYYYMMDD)를 입력하세요 (미입력 시 어제): ").strip()
    target = user_date if user_date else None
    
    # 2. 데이터 가져오기 및 출력
    result_df = monitor.fetch_data(target_date=target)
    monitor.display(result_df)
