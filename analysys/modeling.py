# -*- coding: utf-8


# メンタルヘルススコア予測モデル
# データセット https://www.kaggle.com/datasets/adilshamim8/social-media-addiction-vs-relationships
import pickle


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# データセットの読み込み
data = pd.read_csv("./Students Social Media Addiction.csv")
# 特徴量として使用する変数の選択
feature_cols = [
    "Age", "Gender", "Academic_Level", "Country", "Avg_Daily_Usage_Hours",
    "Most_Used_Platform", "Sleep_Hours_Per_Night", "Relationship_Status",
    "Conflicts_Over_Social_Media"
]
# 目的変数の選択
target_col = "Mental_Health_Score"
# 特徴量と目的変数の抽出
X = data[feature_cols]
y = data[target_col]
# 訓練・テストセットの分離
X_train, X_test, y_train, y_test = train_test_split(X, y)


# カテゴリ変数の指定
cat_cols = [
    "Gender", "Academic_Level", "Country", "Most_Used_Platform",
    "Relationship_Status"
]
# 数値変数の指定
num_cols = [
    "Age", "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night",
    "Conflicts_Over_Social_Media"
]
# 前処理の定義
categorical_transformer = OneHotEncoder(handle_unknown="ignore")
numeric_transformer = StandardScaler()
# ColumnTransformerで前処理をまとめる
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_transformer, cat_cols),
        ("num", numeric_transformer, num_cols)
    ]
)
# 前処理とモデルを含めたPipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])
# 学習
model.fit(X_train, y_train)
# テストデータでの評価
y_test_pred = model.predict(X_test)
r2_test = r2_score(y_test, y_test_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
print(f"r2 : {r2_test}, mae : {mae_test}, rmse : {rmse_test}")


# 学習済みモデルの保存
with open("../assets/model.pkl", "wb") as f:
    pickle.dump(model, f)
