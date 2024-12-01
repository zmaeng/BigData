# 서울 지역 기상 데이터 수집 및 분석 프로젝트

## 프로젝트 개요
이 프로젝트는 1954년부터 현재까지 서울 지역의 일별 기상 데이터를 수집하고 분석하는 것을 목표로 합니다. 수집된 데이터를 기반으로 기온 변화 추세를 분석하고, 미래 기온을 예측하는 머신 러닝 모델을 개발합니다.

## 데이터 수집
- **데이터 출처**: 한국 기상청 ASOS (Automated Surface Observing System)
- **수집 방법**: Python을 사용하여 공공 API로부터 데이터 수집
- **주요 수집 데이터**: 일별 평균기온, 최저기온, 최고기온, 강수량 등

## 데이터 처리
- **데이터 전처리**: 결측치 처리, 날짜 변환, 필요한 컬럼 선택 및 이름 변경
- **저장 형식**: 각 연도별 CSV 파일로 저장 후 전체 데이터를 하나의 파일로 통합

## 데이터 분석 및 시각화
- **라이브러리 사용**: Pandas, Bokeh, Matplotlib
- **주요 분석 내용**:
  - 연도별 평균기온 변화 추세
  - 기온과 다른 기상 요소와의 상관관계 분석
  - 5년 이동 평균 기온 변화

## 머신 러닝 모델
- **모델 유형**: LSTM (Long Short-Term Memory) 네트워크
- **목표**: 미래 5년간의 일별 평균기온 예측
- **훈련 데이터**: 최근 60일의 기온 데이터를 사용하여 다음 날의 기온을 예측

## 사용법
1. API 키 설정
2. 필요한 라이브러리 설치: `pip install -r requirements.txt`
3. 데이터 수집 스크립트 실행
4. 데이터 전처리 스크립트 실행
5. 데이터 분석 및 시각화 스크립트 실행
6. LSTM 모델 훈련 및 예측 스크립트 실행

## 라이선스
[MIT License](LICENSE)


