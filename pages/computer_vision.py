import json
import streamlit as st
from google.cloud import vision


@st.cache_data
def get_response(content):
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


st.markdown("# 画像認識アプリ")

file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
content = None

if file is not None:
    content = file.getvalue()
    st.image(content)

    if st.button('解析をする'):
        if content is not None:
            response = get_response(content)
            if response is not None:
                labels = response.label_annotations
                st.write('Labels:')

                if response.error.message:
                    st.error(f'{response.error.message}\nfor more info on error messages, check: '
                             'https://cloud.google.com/apis/design/errors')
                else:
                    for label in labels:
                        st.write(f"{label.description}: {label.score:.2%}")
        else:
            st.warning("画像をアップロードしてから解析ボタンを押してください。")
else:
    st.info("画像をアップロードしてください。")
