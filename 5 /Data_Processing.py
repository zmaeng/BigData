import os
import pandas as pd
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 데이터 폴더 설정
DATA_FOLDER = "seoul_weather_data"
PROCESSED_FOLDER = "processed_weather_data"

# 데이터 저장 디렉토리 생성
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def preprocess_data():
    # 수집된 파일 목록 불러오기
    files = [os.path.join(DATA_FOLDER, file) for file in os.listdir(DATA_FOLDER) if file.endswith('.csv')]
    df_list = []

    for file in files:
        try:
            df = pd.read_csv(file)
            # 날짜 형식을 변환하고 연도 컬럼을 추가합니다.
            df['날짜'] = pd.to_datetime(df['tm'], format='%Y-%m-%d', errors='coerce')
            df['연도'] = df['날짜'].dt.year

            # 관심 있는 컬럼만 선택하고 데이터 프레임의 복사본을 만듭니다.
            columns = ['날짜', '연도', 'avgTa', 'minTa', 'maxTa', 'sumRn',  'avgPa', 'minPs', 'maxPs', 'avgRhm', 'minRhm']
            df = df[columns].copy()

            # 컬럼 이름을 변경합니다.
            df.rename(columns={
                'avgTa': '평균기온', 'minTa': '최저기온', 'maxTa': '최고기온',
                'sumRn': '일강수량', 'avgPa': '평균기압', 'minPs': '최저기압', 'maxPs': '최고기압',
                'avgRhm': '평균습도', 'minRhm': '최저습도'
            }, inplace=True)

            # 결측치 처리
            fill_values = {
                '평균기온': df['평균기온'].mean(),
                '최저기온': df['최저기온'].mean(),
                '최고기온': df['최고기온'].mean(),
                '일강수량': 0,  # 강수량이 없는 날은 0으로 처리
                '평균기압': df['평균기압'].mean(),
                '평균습도': df['평균습도'].mean(),
                '최고기압': df['최고기압'].mean(),
                '최저기압': df['최저기압'].mean(),
                '최저습도': df['최저습도'].mean()

            }
            df.fillna(fill_values, inplace=True)

            # 변환된 데이터를 저장합니다.
            output_file = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(file)}")
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            df_list.append(df)
        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")

    # 모든 데이터를 하나의 데이터프레임으로 합칩니다.
    return pd.concat(df_list, ignore_index=True)

if __name__ == "__main__":
    processed_data = preprocess_data()
    print("전처리된 데이터 확인:")
    print(processed_data.head())
    # 모든 데이터를 하나의 CSV 파일로 저장
    processed_data.to_csv(os.path.join(PROCESSED_FOLDER, 'processed_all_years.csv'), index=False, encoding='utf-8-sig')
    print("모든 데이터가 하나의 파일로 저장되었습니다.")

