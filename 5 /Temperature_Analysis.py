from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, Span, Label
from bokeh.layouts import column
import pandas as pd
import numpy as np

# Jupyter 노트북 내에서 그래프를 직접 보여주기 위해 호출
output_notebook()

# 가공된 데이터 사용
# 여기서 processed_data는 필요한 모든 처리를 완료한 상태의 DataFrame을 가정합니다.
processed_data = processed_data[processed_data['연도'] <= 2023]
avg_temp_by_year = processed_data.groupby('연도')['평균기온'].mean().reset_index()
overall_avg_temp = avg_temp_by_year['평균기온'].mean()

# 5년 이동 평균과 추세선 계산
avg_temp_by_year['5년 이동 평균'] = avg_temp_by_year['평균기온'].rolling(window=5, center=True).mean()
avg_temp_by_year['차이'] = avg_temp_by_year['평균기온'] - overall_avg_temp
avg_temp_by_year['시작 연도'] = (avg_temp_by_year['연도'] - 2).astype(int)
avg_temp_by_year['끝 연도'] = (avg_temp_by_year['연도'] + 2).astype(int)
coefs = np.polyfit(avg_temp_by_year['연도'], avg_temp_by_year['평균기온'], 1)
avg_temp_by_year['추세선'] = np.polyval(coefs, avg_temp_by_year['연도'])
avg_temp_by_year['5년 이동 평균과 전체 평균의 차이'] = avg_temp_by_year['5년 이동 평균'] - overall_avg_temp

# 데이터 소스 준비
source = ColumnDataSource(avg_temp_by_year)

# 첫 번째 그래프: 연도별 평균 기온 및 추세선
p1 = figure(title='1954년부터 2023년까지의 연도별 평균 기온 및 추세선', x_axis_label='연도', y_axis_label='기온 (°C)',
            tools="pan,wheel_zoom,box_zoom,reset", width=800, height=400)
p1.line('연도', '평균기온', source=source, line_width=2, color='blue', legend_label='연도별 평균 기온')
p1.line('연도', '추세선', source=source, line_color='red', line_width=1.5, legend_label='추세선')

# 평균 기온선 (초록색 점선)
average_span = Span(location=overall_avg_temp, dimension='width', line_color='green', line_dash='dashed', line_width=2)
p1.add_layout(average_span)
average_label = Label(x=1955, y=overall_avg_temp, text=f'전체 평균 기온: {overall_avg_temp:.2f}°C', text_font_size='10pt', text_color='green')
p1.add_layout(average_label)

# 두 번째 그래프: 5년 이동 평균 및 추세선
p2 = figure(title='1954년부터 2023년까지의 5년 이동 평균 기온 및 추세선', x_axis_label='연도', y_axis_label='기온 (°C)',
            tools="pan,wheel_zoom,box_zoom,reset", width=800, height=400)
p2.line('연도', '5년 이동 평균', source=source, line_color='orange', line_width=2, legend_label='5년 이동 평균')
p2.line('연도', '추세선', source=source, line_color='red', line_width=1.5, legend_label='추세선')
p2.add_layout(average_span)
p2.add_layout(Label(x=1955, y=overall_avg_temp, text=f'전체 평균 기온: {overall_avg_temp:.2f}°C', text_font_size='10pt', text_color='green'))

# 툴팁 설정
hover1 = HoverTool()
hover1.tooltips = [
    ("연도", "@연도"),
    ("평균 기온", "@평균기온{0.2f}°C"),
    ("평균과의 차이", "@차이{0.2f}°C")
]
p1.add_tools(hover1)

hover2 = HoverTool()
hover2.tooltips = [
    ("5년 이동 평균", "@{5년 이동 평균}{0.2f}°C"),
    ("기간", "@{시작 연도}년 - @{끝 연도}년"),
    ("5년 이동 평균과 전체 평균의 차이", "@{5년 이동 평균과 전체 평균의 차이}{0.2f}°C")
]
p2.add_tools(hover2)


p1.legend.location = 'top_left'
p2.legend.location = 'top_left'

# 두 그래프를 세로로 배열하여 출력
show(column(p1, p2))
