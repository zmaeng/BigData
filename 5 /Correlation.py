import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
from matplotlib import font_manager, rc


# 상관관계를 분석할 컬럼 선택
columns_of_interest = ['평균기온', '최저기온', '최고기온', '일강수량', '평균기압', '최저기압', '최고기압', '평균습도', '최저습도']

# 상관관계 계산
correlation_matrix = processed_data[columns_of_interest].corr()

# 상관관계 시각화
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title('기상 데이터의 상관관계')
plt.show()
