import json
import streamlit as st
from google.cloud import vision


@st.cache_data
def get_label_response(content):
    try:
        credentials_dict = json.loads(
            st.secrets['google_credentials'], strict=False)
        client = vision.ImageAnnotatorClient.from_service_account_info(
            info=credentials_dict)
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        return response
    except KeyError:
        st.error("Google Cloud認証情報が設定されていません。Streamlit Cloudのsecretsに設定してください。")
        return None


@st.cache_data
def get_text_response(content):
    try:
        credentials_dict = json.loads(
            st.secrets['google_credentials'], strict=False)
        client = vision.ImageAnnotatorClient.from_service_account_info(
            info=credentials_dict)
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        return response
    except KeyError:
        st.error("Google Cloud認証情報が設定されていません。Streamlit Cloudのsecretsに設定してください。")
        return None


st.markdown("# 画像認識アプリ")

file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
content = None

if file is not None:
    content = file.getvalue()
    st.image(content)

    # 分析タイプ選択のためのボタンを並列に配置
    col1, col2 = st.columns(2)

    with col1:
        label_analysis = st.button('ラベル分析を実行', use_container_width=True)

    with col2:
        text_analysis = st.button('文字分析を実行', use_container_width=True)

    # ラベル分析の処理
    if label_analysis:
        if content is not None:
            with st.spinner('ラベル分析中...'):
                response = get_label_response(content)
                if response is not None:
                    labels = response.label_annotations
                    st.subheader('🏷️ ラベル分析結果')

                    if response.error.message:
                        st.error(f'{response.error.message}\nfor more info on error messages, check: '
                                 'https://cloud.google.com/apis/design/errors')
                    else:
                        if labels:
                            for label in labels:
                                st.write(
                                    f"**{label.description}**: {label.score:.2%}")
                        else:
                            st.info("ラベルが検出されませんでした。")
        else:
            st.warning("画像をアップロードしてから分析ボタンを押してください。")

    # 文字分析の処理
    if text_analysis:
        if content is not None:
            with st.spinner('文字分析中...'):
                response = get_text_response(content)
                if response is not None:
                    texts = response.text_annotations
                    st.subheader('📝 文字分析結果')

                    if response.error.message:
                        st.error(f'{response.error.message}\nfor more info on error messages, check: '
                                 'https://cloud.google.com/apis/design/errors')
                    else:
                        if texts:
                            # 最初のエントリは全体のテキスト
                            st.write("**検出されたテキスト全体:**")
                            st.text_area(
                                "", texts[0].description, height=150, disabled=True)

                            # 個別の文字/単語の詳細情報を表示
                            if len(texts) > 1:
                                st.write("**個別の文字・単語情報:**")
                                with st.expander("詳細情報を表示"):
                                    for i, text in enumerate(texts[1:], 1):
                                        confidence = text.score if hasattr(
                                            text, 'score') else "N/A"
                                        st.write(
                                            f"{i}. **'{text.description}'** (信頼度: {confidence})")
                        else:
                            st.info("テキストが検出されませんでした。")
        else:
            st.warning("画像をアップロードしてから分析ボタンを押してください。")
else:
    st.info("画像をアップロードしてください。")
