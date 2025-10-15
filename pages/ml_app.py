import streamlit as st
import pickle
import pandas as pd

MODEL_PATH = "./assets/model.pkl"


@st.cache_resource
def load_model():
    # Compatibility Unpickler: some sklearn versions use internal classes
    # (e.g. _RemainderColsList) that may not exist in the current sklearn.
    # Provide a placeholder class during unpickling so the model can be loaded.
    class CompatUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == "sklearn.compose._column_transformer" and name == "_RemainderColsList":
                # Minimal placeholder compatible with unpickling. Instances of
                # this class are not used directly by the app logic, so a
                # lightweight stub is sufficient.
                class _RemainderColsList:
                    def __init__(self, *args, **kwargs):
                        pass

                    def __repr__(self):
                        return "_RemainderColsList()"

                return _RemainderColsList
            return super().find_class(module, name)

    with open(MODEL_PATH, "rb") as f:
        try:
            model = CompatUnpickler(f).load()
        except Exception:
            # If the compat unpickler fails for any reason, fall back to
            # the normal pickle loader so the original exception is raised
            # (useful for debugging other issues).
            f.seek(0)
            model = pickle.load(f)
    return model


if "done" not in st.session_state:
    st.session_state["done"] = False


def toggle_done(value=True):
    st.session_state["done"] = value


st.markdown("# メンタルヘルススコアの見積もり")

load_state = st.markdown("モデルをロード中...")
model = load_model()
load_state.markdown("")

prep = model.named_steps["preprocessor"]
colnames = prep.feature_names_in_
cat_trans = prep.named_transformers_["cat"]
cat_colnames = cat_trans.feature_names_in_.tolist()
cat_values_dict = dict(zip(cat_colnames, cat_trans.categories_))
regressor_colmns = prep.get_feature_names_out()
regressor = model.named_steps["regressor"]
feature_importance = pd.DataFrame({
    "column": regressor_colmns,
    "importance": regressor.feature_importances_})

with st.form("入力"):
    col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
    col2_1, col2_2, col2_3 = st.columns([1, 1, 1])
    col3_1, col3_2, col3_3 = st.columns([1, 1, 1])

    with col1_1:
        age = st.number_input(
            "年齢", min_value=0, max_value=120, value=20, step=1)

    with col1_2:
        avg_hour = st.number_input(
            "1日の平均SNS使用時間（時間）", min_value=0.0, max_value=24.0, value=0.0, step=0.1)

    with col1_3:
        gender = st.radio("性別", ["Female", "Male"], index=None)

    with col2_1:
        jp_idx = cat_values_dict["Country"].tolist().index("Japan")
        country = st.selectbox("国", cat_values_dict["Country"], index=jp_idx)

    with col2_2:
        platform = st.selectbox(
            "最もよく使うSNS", cat_values_dict["Most_Used_Platform"], index=0)

    with col2_3:
        academic_level = st.selectbox(
            "現在の所属", ["High School", "Undergraduate", "Graduate"], index=0)

    with col3_1:
        sleep = st.number_input(
            "1日の平均睡眠時間（時間）", min_value=0, max_value=24, value=7)

    with col3_2:
        conflicts = st.number_input("SNSを巡るトラブルの頻度", min_value=0, value=0)

    with col3_3:
        relationship = st.radio(
            "交際状況", ["Single", "In Relationship", "Complicated"], index=None)

    st.form_submit_button("決定", on_click=toggle_done, args=[True])

if st.session_state["done"]:
    record = {"Age": age,
              "Gender": gender,
              "Academic_Level": academic_level,
              "Country": country,
              "Avg_Daily_Usage_Hours": avg_hour,
              "Most_Used_Platform": platform,
              "Sleep_Hours_Per_Night": sleep,
              "Relationship_Status": relationship,
              "Conflicts_Over_Social_Media": conflicts
              }
    features = pd.DataFrame([record], columns=colnames)
    prediction = model.predict(features)[0]
    st.success(f"推定されるメンタルヘルススコアは **{prediction:.2f}** です。")

    with st.expander("参考:入力データ", expanded=False):
        st.write(record)
    with st.expander("参考:モデルの特徴重要度", expanded=False):
        st.bar_chart(feature_importance.query("importance > 0"),
                     x="column", y="importance", horizontal=True)
