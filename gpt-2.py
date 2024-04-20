import streamlit as st  # フロントエンドを扱うstreamlitの機能をインポート
import openai  # openAIのchatGPTのAIを活用するための機能をインポート
import os  # OSが持つ環境変数OPENAI_API_KEYにAPIを入力するためにosにアクセスするためのライブラリをインポート
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 上記の行でAPIキーを設定した後、APIキーをopenai.api_keyに直接設定する必要があります。
openai.api_key = os.getenv("OPENAI_API_KEY")

age_kind_of = [
    " ",
    "10代",
    "20代",
    "30代",
    "40代",
    "50代",
    "60代以上",
]

sex_kind_of = [
    " ",
    "男性",
    "女性",
]

# chatGPTにリクエストするためのメソッドを設定。引数には書いてほしい内容と文章のテイストと最大文字数を指定
def run_gpt(age_to_gpt, sex_to_gpt, feel_to_gpt, payment_to_gpt):
    # リクエスト内容を決める
    request_to_gpt = f"年代は{age_to_gpt}、性別は{sex_to_gpt}、{feel_to_gpt}の人にお菓子のカテゴリや具体的名称を合計{payment_to_gpt}円分でおすすめしてください。年代、性別、気分、金額によってお薦めするお菓子の内容を変えてください。{name_to_gpt}をつかったあだ名をつけて、そのあだ名で呼びかけながら話してください。なぜそのお菓子カテゴリや商品をお勧めしたかの理由もしっかり書いてください。"
    
    # 決めた内容を元にclient.ChatCompletion.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_to_gpt},
        ],
    )

    # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    output_content = response.choices[0].message["content"].strip()  # response.choices[0].message.content.strip() から修正
    return output_content  # 返って来たレスポンスの内容を返す

st.title('頂いたお金の使い道決定アプリ')  # タイトル
st.subheader("あなたに適したカテゴリのお菓子持ってきます")

# 名前入れる
name_to_gpt = st.text_input("名前を教えてください")

# 入れてくれたお金を聞く
payment_to_gpt = st.number_input("入れていただいた金額はいくらですか（10円単位で最大1万円）", min_value=0, max_value=10000, step=10, format='%d')

# 年齢を入れる
age_to_gpt = st.selectbox("年代を入力してください", options=age_kind_of)

# 性別を入れる
sex_to_gpt = st.selectbox("性別を入力してください", options=sex_kind_of)

# 気分を入れる
feel_to_gpt = st.text_input("気分を詳しく教えてください（〇〇な気分）")


if age_to_gpt and sex_to_gpt and feel_to_gpt and payment_to_gpt > 0:
    output_content_text = run_gpt(age_to_gpt, sex_to_gpt, feel_to_gpt, payment_to_gpt)
    st.write(output_content_text)
else:
    st.write("すべての項目を入力してください。")
