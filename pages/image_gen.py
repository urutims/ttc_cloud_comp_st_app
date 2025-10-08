import io
import requests
import streamlit as st


def render_error_response(resp):
    """補助: レスポンスの内容を表示する"""
    content_type = resp.headers.get("content-type", "")
    if "application/json" in content_type or resp.text.strip().startswith("{"):
        try:
            st.json(resp.json())
        except Exception:
            st.code(resp.text)
    else:
        st.code(resp.text)


def try_display_image_from_bytes(bts):
    try:
        from PIL import Image

        buf = io.BytesIO(bts)
        Image.open(buf).verify()
        buf.seek(0)
        st.image(buf, use_column_width=True)
        return True
    except Exception:
        return False


def main():
    token = st.secrets.get("hugging_face_token")
    model = "black-forest-labs/FLUX.1-dev"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    st.title("Image generation (Hugging Face)")
    prompt = st.text_input("Enter your prompt here:")

    if st.button("Generate Image"):
        if not prompt:
            st.warning("プロンプトを入力してください。")
            return
        if not token:
            st.error("Hugging Face のトークンが設定されていません。secrets に `hugging_face_token` を追加してください。")
            import io
            import base64
            import requests
            import streamlit as st


            def render_error_response(resp):
                """補助: レスポンスの内容を表示する"""
                content_type = resp.headers.get("content-type", "")
                if "application/json" in content_type or resp.text.strip().startswith("{"):
                    try:
                        st.json(resp.json())
                    except Exception:
                        st.code(resp.text)
                else:
                    st.code(resp.text)


            def try_display_image_from_bytes(bts):
                """Pillowで検証して表示する。成功すればTrueを返す。"""
                try:
                    from PIL import Image

                    buf = io.BytesIO(bts)
                    Image.open(buf).verify()
                    buf.seek(0)
                    st.image(buf, use_column_width=True)
                    return True
                except Exception:
                    return False


            def extract_base64_bytes(obj):
                """再帰的にpayloadから base64 エンコードされた画像を見つけてbytesで返す（見つからなければNone）。"""
                if isinstance(obj, str):
                    s = obj.strip()
                    if s.startswith("data:image/") and "," in s:
                        _prefix, b64 = s.split(",", 1)
                        try:
                            return base64.b64decode(b64)
                        except Exception:
                            return None
                    # 直接base64文字列だけが返るケースの簡易判定（長さ閾値）
                    if len(s) > 100 and all(c.isalnum() or c in "+/=\n\r" for c in s):
                        try:
                            return base64.b64decode(s)
                        except Exception:
                            return None
                    return None
                if isinstance(obj, list):
                    for v in obj:
                        b = extract_base64_bytes(v)
                        if b:
                            return b
                if isinstance(obj, dict):
                    for v in obj.values():
                        b = extract_base64_bytes(v)
                        if b:
                            return b
                return None


            def main():
                token = st.secrets.get("hugging_face_token")
                model = "black-forest-labs/FLUX.1-dev"
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {token}"} if token else {}

                st.title("Image generation (Hugging Face)")
                prompt = st.text_input("Enter your prompt here:")

                if st.button("Generate Image"):
                    if not prompt:
                        st.warning("プロンプトを入力してください。")
                        return
                    if not token:
                        st.error("Hugging Face のトークンが設定されていません。secrets に `hugging_face_token` を追加してください。")
                        return

                    try:
                        resp = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
                    except requests.RequestException as e:
                        st.error(f"APIリクエストでエラーが発生しました: {e}")
                        return

                    content_type = resp.headers.get("content-type", "")

                    # 1) 直接画像バイナリが返る
                    if content_type.startswith("image/"):
                        ok = try_display_image_from_bytes(resp.content)
                        if not ok:
                            st.error("返ってきたデータが画像として認識できませんでした。APIのレスポンスを確認してください。")
                            render_error_response(resp)
                        return

                    # 2) JSON が返る場合 — payloadの中にbase64画像がある可能性を探す
                    if "application/json" in content_type or resp.text.strip().startswith("{"):
                        try:
                            payload = resp.json()
                        except Exception:
                            st.error("JSONレスポンスの解析に失敗しました。")
                            st.code(resp.text)
                            return

                        # エラーとして返っている場合
                        if isinstance(payload, dict) and ("error" in payload or "error_message" in payload):
                            msg = payload.get("error") or payload.get("error_message")
                            st.error(f"API エラー: {msg}")
                            return

                        # payload内にbase64画像が含まれているか探す
                        bts = extract_base64_bytes(payload)
                        if bts:
                            ok = try_display_image_from_bytes(bts)
                            if not ok:
                                st.error("payload内のbase64データが画像として認識できませんでした。")
                                st.json(payload)
                            return

                        # 画像なしのJSON（メタ情報や失敗メッセージなど）
                        st.info("APIからJSONレスポンスが返されました（画像は含まれていない可能性があります）。")
                        st.json(payload)
                        return

                    # 3) その他（テキスト/HTML/エラーメッセージ）
                    st.error("APIレスポンスが画像ではありませんでした。下記レスポンスを確認してください。")
                    render_error_response(resp)


            if __name__ == "__main__":
                main()

def main():
    token = st.secrets.get("hugging_face_token")
    model = "black-forest-labs/FLUX.1-dev"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    st.title("Image generation (Hugging Face)")
    prompt = st.text_input("Enter your prompt here:")

    if st.button("Generate Image"):
        if not prompt:
            st.warning("プロンプトを入力してください。")
            return
        if not token:
            st.error("Hugging Face のトークンが設定されていません。secrets に `hugging_face_token` を追加してください。")
            return

        try:
            resp = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
        except requests.RequestException as e:
            st.error(f"APIリクエストでエラーが発生しました: {e}")
            return

        content_type = resp.headers.get("content-type", "")

        if content_type.startswith("image/"):
            ok = try_display_image_from_bytes(resp.content)
            if not ok:
                st.error("返ってきたデータが画像として認識できませんでした。APIのレスポンスを確認してください。")
                render_error_response(resp)
            return

        # JSON or text
        if "application/json" in content_type or resp.text.strip().startswith("{"):
            try:
                payload = resp.json()
            except Exception:
                st.error("JSONレスポンスの解析に失敗しました。")
                st.code(resp.text)
                return

            if isinstance(payload, dict) and ("error" in payload or "error_message" in payload):
                msg = payload.get("error") or payload.get("error_message")
                st.error(f"API エラー: {msg}")
            else:
                st.info("APIからJSONレスポンスが返されました（画像は含まれていない可能性があります）。")
                st.json(payload)
            return

        # それ以外
        st.error("APIレスポンスが画像ではありませんでした。下記レスポンスを確認してください。")
        render_error_response(resp)


if __name__ == "__main__":
    main()
        try:
