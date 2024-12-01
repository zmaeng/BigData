import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.preprocessing import MinMaxScaler
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, WheelZoomTool, ResetTool
from datetime import timedelta

# Bokeh 출력 설정
output_notebook()

# 데이터 로드 및 날짜로 인덱스 설정
data_path = 'processed_weather_data/processed_all_years.csv'
df = pd.read_csv(data_path, parse_dates=['날짜'], index_col='날짜')
df.sort_index(inplace=True)

# 분석 기간 설정
train_df = df['1954':'2020']  # 학습 데이터
validate_df = df['2021':'2023']  # 검증 데이터

# 데이터 정규화
scaler = MinMaxScaler()
train_scaled = scaler.fit_transform(train_df['평균기온'].values.reshape(-1, 1))

# 데이터셋 생성 함수
def create_dataset(data, look_back=30):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        y.append(data[i + look_back, 0])
    return np.array(X), np.array(y)

# 학습 데이터셋 생성
look_back = 60
X_train, y_train = create_dataset(train_scaled, look_back)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

# LSTM 모델 구성
model = Sequential([
    Input(shape=(look_back, 1)),
    LSTM(50),
    Dense(1)
])
model.compile(loss='mean_squared_error', optimizer='adam')

# 모델 학습
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# 검증 데이터 준비
validate_scaled = scaler.transform(validate_df['평균기온'].values.reshape(-1, 1))
X_validate, _ = create_dataset(validate_scaled, look_back)
X_validate = X_validate.reshape(X_validate.shape[0], X_validate.shape[1], 1)
validate_predictions = model.predict(X_validate, verbose=0)
validate_predictions = scaler.inverse_transform(validate_predictions)

# 검증 데이터 시각화 준비
validate_dates = validate_df.index[look_back:]
validate_source = ColumnDataSource(data={
    'date': validate_dates,
    'actual_temp': validate_df['평균기온'][look_back:],
    'predicted_temp': validate_predictions.flatten()
})

# 검증 데이터 시각화
p = figure(title="2021-2023년 기온 예측", x_axis_type="datetime", tools=[BoxZoomTool(), WheelZoomTool(), ResetTool()], width=900, height=400)
p.line('date', 'actual_temp', source=validate_source, color='blue', legend_label="실제 기온")
p.line('date', 'predicted_temp', source=validate_source, color='red', legend_label="예측 기온")

# 마우스 오버 효과 추가
hover = HoverTool(tooltips=[
    ("날짜", "@date{%F}"),
    ("실제 기온", "@actual_temp{0.2f}°C"),
    ("예측 기온", "@predicted_temp{0.2f}°C")
], formatters={'@date': 'datetime'}, mode='vline')
p.add_tools(hover)

# 그래프 설정
p.legend.location = 'top_left'
p.xaxis.axis_label = '날짜'
p.yaxis.axis_label = '기온 (°C)'

# 그래프 출력
show(p)

# 미래 데이터 예측 함수
def predict_future(data, model, steps, look_back):
    future_preds = data[-look_back:].reshape(1, look_back, 1)
    predictions = []

    for _ in range(steps):
        pred = model.predict(future_preds, verbose=0)
        predictions.append(pred[0, 0])
        future_preds = np.concatenate((future_preds[:, 1:, :], pred.reshape(1, 1, 1)), axis=1)

    return np.array(predictions)

# 미래 5년간 데이터 예측
future_steps = 1825  # 5년
last_scaled_data = scaler.transform(df['평균기온'].values[-look_back:].reshape(-1, 1))
future_predictions_scaled = predict_future(last_scaled_data, model, future_steps, look_back)
future_predictions = scaler.inverse_transform(future_predictions_scaled.reshape(-1, 1))

# 미래 날짜 생성
future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=future_steps)

# 미래 데이터 시각화 준비
future_source = ColumnDataSource(data={
    'date': future_dates,
    'predicted_temp': future_predictions.flatten()
})

# 미래 데이터 시각화
p_future = figure(title="2024-2028년 기온 예측", x_axis_type="datetime", width=900, height=400)
p_future.line('date', 'predicted_temp', source=future_source, color='red', legend_label="예측 기온")

# 마우스 오버 효과 추가
hover_future = HoverTool(tooltips=[
    ("날짜", "@date{%F}"),
    ("예측 기온", "@predicted_temp{0.2f}°C")
], formatters={'@date': 'datetime'}, mode='vline')
p_future.add_tools(hover_future, BoxZoomTool(), WheelZoomTool(), ResetTool())

# 그래프 설정
p_future.legend.location = 'top_left'
p_future.xaxis.axis_label = '날짜'
p_future.yaxis.axis_label = '기온 (°C)'

# 그래프 출력
show(p_future)
