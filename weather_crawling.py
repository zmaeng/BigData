import os
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import logging
import time

# 로깅 설정: 로그 파일을 설정하고 로그 레벨을 INFO로 설정합니다.
logging.basicConfig(filename="seoul_weather_data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API 설정: API 키와 기본 URL을 설정합니다.
SERVICE_KEY = "VjDldzOF1i8S1REbDaCSRc8cYehpbiIW/oad3OLSyC9btr2p1n7OsaHMb9/L/jzcYgQYE3ePEf5dTsZm1E/2Gw=="
BASE_URL = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
OUTPUT_DIR = "seoul_weather_data"

# 데이터 저장 디렉토리 생성: 데이터를 저장할 디렉토리가 없으면 생성합니다.
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_seoul_weather_data(year, retries=5):
    """ API로부터 서울의 일별 날씨 데이터를 가져오는 함수입니다.
        연도별로 데이터를 요청하며, 요청 실패 시 최대 retries 회수만큼 재시도합니다. """
    params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": "366",
        "pageNo": "1",
        "dataCd": "ASOS",
        "dateCd": "DAY",
        "stnIds": "108",  # 서울 지점 코드
        "dataType": "JSON",
        "startDt": f"{year}0101",
        "endDt": f"{year}1231" if year != datetime.now().year else datetime.now().strftime('%Y%m%d')
    }
    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            if 'body' in data['response']:
                return data['response']['body']['items']['item']
            else:
                logging.error(f"Error retrieving data for year {year}: {data['response']['header']['resultMsg']}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}, retrying... ({attempt + 1}/{retries})")
            time.sleep(5)
    return None

def process_data(year, items):
    """ 수집된 데이터를 CSV 파일로 저장하는 함수입니다. """
    if items:
        df = pd.DataFrame(items)
        filename = os.path.join(OUTPUT_DIR, f"seoul_weather_{year}.csv")
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logging.info(f"{year}년 데이터 저장 완료.")

if __name__ == "__main__":
    # 1954년부터 현재 연도까지의 데이터를 수집합니다.
    for year in tqdm(range(1954, datetime.now().year + 1), desc="데이터 수집"):
        items = fetch_seoul_weather_data(year)
        if items:
            process_data(year, items)
