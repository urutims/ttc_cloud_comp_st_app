import streamlit as st
from huggingface_hub import InferenceClient
from huggingface_hub.utils import RepositoryNotFoundError, HfHubHTTPError

MODEL = "google/gemma-2-2b-it"
API_TOKEN = st.secrets["hugging_face_token"]
client = InferenceClient(model=MODEL, token=API_TOKEN)

system_message_init = """あなたは雷で怖がっている保育園にいる子供、田中ゆずき5歳です。会話の相手は保育
士です。"""
system_message_eval = """ここまでで会話は終了です。上記の会話の評価結果を表示してください。あなたは保育士の言葉に対して以下の3つの観点で評価してください。各観点について、0-10点の範囲で点数を付け、理由を簡潔に説明してください。合計点は100点満点とし、各観点の点数を3倍して33.3点満点に換算します。

* 安心度 (0-33点): 保育士の言葉が子供の不安をどれだけ和らげ、安心感を与えたか。子供の感情に寄り添い、共感を示す言葉遣いや内容が評価対象。
* 機転 (0-33点): 保育士の対応の機転の良さ。状況に応じた適切な言葉選びや、子供の反応に対する柔軟な対応が評価対象。
* 雷の克服度 (0-33点): 保育士の言葉が雷の恐怖を克服する手助けになったか。科学的な説明やポジティブな視点の提供などが評価対象。

評価結果の表示形式:
- 安心度: [点数]/33点 (理由: [簡潔な説明])
- 機転: [点数]/33点 (理由: [簡潔な説明])
- 雷の克服度: [点数]/33点 (理由: [簡潔な説明])
- 総合評価: [合計点]/100点

また、上記の評価の他に、その後のあなたのストーリーを書き加えてください。ストーリーは15年後のゆずきの視点で、ユーザーからの回答で言及されたことを交えて、点数に応じてよい思い出か悪い思い出かが変わる。ストーリーは200-300文字程度とし、子供時代の体験が大人になってどのように影響を与えたかを描写してください。"""

initial_conversation = [
    {"role": "user", "content": "（保育士）おはよう、ゆずきちゃん！今日はちょっと雷が鳴ってるけど、大丈夫かな？"},
    {"role": "assistant", "content": "（ゆずき）うぅ…こわいよ〜💦"},
    {"role": "user", "content": "（保育士）どうして怖いのかな？教えてくれる？"},
    {"role": "assistant", "content": "（ゆずき）だって、ゴロゴロ言ってて怒ってるみたいなんだもん！"},
]

st.title("ジェネリックおしゃべりキング")

st.markdown("雷で怖がっているゆずきちゃんに安心できる言葉をかけてあげよう。")

if "log" not in st.session_state:
    st.session_state["log"] = [
        {"role": "system", "content": system_message_init}] + initial_conversation

for post in st.session_state["log"]:
    if post["role"] != "system":
        with st.chat_message(post["role"]):
            st.write(post["content"])

message = st.chat_input("あなたの言葉で、ゆずきちゃんを安心させてあげよう。")

if message:
    st.session_state["log"].append({"role": "user", "content": message})
    st.session_state["log"].append(
        {"role": "system", "content": system_message_eval})
    with st.chat_message("user"):
        st.write(message)
    try:
        completion = client.chat.completions.create(
            messages=st.session_state["log"],
            max_tokens=500,

        )
        reply = completion.choices[0].message["content"]
        st.session_state["log"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

    except HfHubHTTPError:
        st.warning("モデルのロードに失敗しました。しばらくしてからもう一度お試しください。")
