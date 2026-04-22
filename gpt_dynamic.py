#APIキーは環境変数を利用(ベタ打ちすると，gitで公開 or 生成AIに質問するタイミングで情報漏洩の恐れあり)
import os
from openai import OpenAI

try:
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        print("警告: OPENAI_API_KEY が設定されていません。")
    
    # クライアント作成（API_KEYがNoneでも初期化自体は可能ですが、実行時にエラーになります）
    gpt = OpenAI(api_key=API_KEY)
 
except Exception as e:
    print(f"OpenAIの初期化に失敗: {e}")
    gpt = None
    
prompt=[{"role": "system", "content": "あなたはチャットボットです．"}]
print("初期化完了")

# この形式だと見づらいから，html+cssでUIを作った方がいい
# 終了時はCtrl+Cで抜ける
while(True):
    input_text = input("User : ")
    prompt.append({"role": "user", "content": input_text})
    res = gpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt
    )
    
    response = res.choices[0].message.content
    prompt.append({"role": "assistant", "content": response})    
    print(f"Assistant : {response} \n")
