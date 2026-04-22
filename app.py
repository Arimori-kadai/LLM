import os
import time
import markdown
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI  # OpenAIライブラリをインポート

# OpenAIクライアントの初期化
try:
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        print("警告: OPENAI_API_KEY が設定されていません。")
    
    # クライアント作成（API_KEYがNoneでも初期化自体は可能ですが、実行時にエラーになります）
    client = OpenAI(api_key=API_KEY)
 
except Exception as e:
    print(f"OpenAIの初期化に失敗: {e}")
    client = None

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # templates/index.html を探して表示する
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'メッセージがありません。'}), 400

    if client and API_KEY:
        try:
            # OpenAI APIにリクエストを送信 (Chat Completion API)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # または "gpt-3.5-turbo"
                messages=[
                    {"role":"system", "content": "あなたは大阪弁で話すチャットボットです．"},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1024,
                temperature=1.0,
                top_p=0.95,
                frequency_penalty=0.0
            )
            
            # レスポンスのテキストを取得
            llm_response = response.choices[0].message.content
                        
            return jsonify({'response': llm_response})

        except Exception as e:
            print(f"OpenAI APIエラー: {e}")
            return jsonify({'error': f'LLM APIエラー: {e}'}), 500
    else:
        # APIキーがない場合のダミー応答
        time.sleep(1)
        llm_response = f"APIキー未設定です。「{user_message}」 を受け取りました。（ダミー応答）"
        return jsonify({'response': llm_response})
   
if __name__ == '__main__':
    app.run(port=5000,debug=True)
