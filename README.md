# 서울 지역 기상 데이터 수집 및 분석 프로젝트

## 프로젝트 개요
이 프로젝트는 1954년부터 2023년까지 서울 지역의 일별 기상 데이터를 수집 및 분석하여 기온 변화 추세를 파악하고, 미래 기온을 예측합니다. 이러한 분석을 통해 기후 변화에 대한 깊은 이해를 목표로 하며, 장기적인 기상 변화에 대비하는 통찰을 제공합니다.

## 데이터 수집
  ### Weather_Crawling.py 코드 실행
- **데이터 출처**: 한국 기상청의 자동 기상 관측 시스템(ASOS) API
- **수집 데이터**:
  - 일별 평균기온, 최저기온, 최고기온
  - 일강수량, 평균 기압, 평균 습도 등
- **수집 방법**: Python `requests` 라이브러리를 사용하여 API에서 JSON 형식의 데이터를 수집합니다.

## 데이터 처리
  ### Data_Processing.py 코드 실행
- **전처리 작업**:
  - 필요한 데이터 추출 및 컬럼이름 재부여합니다.
  - 결측치는 해당 변수의 평균값으로 대체합니다. 단 강수량은 0으로 대체합니다.
  - 날짜 포맷은 ISO 표준인 `YYYY-MM-DD` 형식으로 통일합니다.
  - 분석에 필요한 주요 컬럼만을 선택하여 저장합니다.
- **데이터 저장**:
  - 연도별로 분리하여 각 연도별로 CSV 파일을 생성합니다.
  - 모든 연도의 데이터를 하나의 파일(`processed_all_years.csv`)로 통합하여 저장합니다.

## 데이터 분석 및 시각화
  ### Correlation.py, Temperature_Analysis.py 코드 실행
- **사용된 도구**: Pandas, Bokeh, Matplotlib, Seaborn
- **분석 내용**:
  - 연도별 평균기온 변화 추세 분석
  - 기온과 다른 기상 요소(습도, 기압, 강수량)와의 상관관계 시각화
  - 5년 이동 평균을 사용한 장기 추세 분석
- **시각화 결과**: 인터랙티브 차트를 생성하여 데이터의 트렌드와 패턴을 시각화합니다.

### 시각화 결과 예시
![연도별 평균기온 변화 및 추세](https://github.com/user-attachments/assets/8f2a4529-9068-4857-a637-c6d095fa2ef3)
![5년간 이동 평균기온 변화 및 추세](https://github.com/user-attachments/assets/555a7bf3-b4ba-4114-8467-e3227ce61c69)
![날씨 요소별 상관관계](https://github.com/user-attachments/assets/6764a80b-1ffc-42e7-b5e5-8641c76432a0)

## 머신 러닝 모델
  ###Weather_Predict.py 코드 실행
- **모델 유형**: LSTM (Long Short-Term Memory)을 사용한 시계열 예측
- **목적**: 향후 5년간의 일별 평균기온 예측
- **데이터 처리**: 최근 60일의 데이터를 기반으로 다음 날의 기온을 예측합니다.
- **성능 평가**: Mean Squared Error (MSE)를 사용하여 테스트 데이터셋에 대한 모델의 예측 정확도를 평가합니다.

### 예측 결과 예시
![기온 예측 2021 ~ 2023](https://github.com/user-attachments/assets/06616575-b3a8-49b6-b631-71048dacdc79)
![기온 예측 2024 ~ 2028](https://github.com/user-attachments/assets/2348d616-258c-4385-bdfa-e76cc14af383)


## 사용 방법

1. **패키지 설치**:
    ### 한글 꺠짐
   ```bash
      # 한글 폰트 설치
      sudo apt-get install -y fonts-nanum

      # 폰트 캐시 재구성
      sudo fc-cache -fv

      # Matplotlib 설정
      import matplotlib.pyplot as plt
      plt.rcParams['font.family'] = 'NanumGothic'
      plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 오류 방지

