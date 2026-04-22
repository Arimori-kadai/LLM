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
    
def gpt_generate(input_text):
	res = gpt.chat.completions.create(
	    model="gpt-4o-mini",
	    messages=[
	        {"role": "system", "content": "あなたはチャットボットです．"},
	        {"role": "user", "content": input_text}
	    ],
	    # --- 生成の振る舞いを調整するオプション ---
    
    # 0.0〜2.0 の範囲。高いほどランダム性が増し、低いほど決定的（毎回同じ回答）になる。
    temperature=0.7,
    
    # 核サンプリング。上位何%の確率の単語から選ぶか（0.1なら上位10%）。
    # 通常、temperatureかtop_pのどちらか一方のみを変更するのが推奨される。
    top_p=1.0,
    
    # 出力されるトークンの最大数。
    max_tokens=500,
    
    # 同じ単語の繰り返しをどれくらい防ぐか (-2.0〜2.0)。
    presence_penalty=0.0,
    
    # すでに出現した単語をどれくらい避けるか (-2.0〜2.0)。
    frequency_penalty=0.0,
    
    # 同じ入力に対して同じ結果を返しやすくするための数値。
    seed=42,
    
    # Trueにすると、逐次的に結果を返す（ChatGPTのように文字が流れる表現が可能）。
    stream=False,
    
    # 1つのプロンプトに対して、いくつの回答候補を生成するか。
    n=1
    
	)
	response = res.choices[0].message.content
	return response
print(gpt_generate("これはテストです"))