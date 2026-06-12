import pandas as pd
import json
import io
import re

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', None)


def extract_csv_from_output(output: str) -> str:
    """outputバリューからCSV部分のテキストを取り出す。

    outputの先頭には【テーマ】などのメタ情報行が含まれ、
    その後に `id,参照,...` で始まるCSVヘッダ行以降が続く。
    まずコードブロック(```)があればその中身を、無ければ
    CSVヘッダ行を起点に末尾までを抽出する。
    """
    # ```で囲まれたコードブロックがある場合はその中身を優先
    if "\n```\n" in output:
        return output.split("\n```\n")[1]

    # CSVヘッダ行(id, から始まる行)を探して、そこから末尾までを返す
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^\s*id\s*,", line):
            return "\n".join(lines[i:])

    # 見つからなければそのまま返す
    return output


def load_dataframe(filename: str) -> pd.DataFrame:
    """JSONファイルのoutputキーからCSVを抽出してDataFrameを返す。"""
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    # データはリストの先頭要素に格納されている
    record = data[0]
    csv_text = extract_csv_from_output(record["output"])
    df = pd.read_csv(io.StringIO(csv_text))
    return df


if __name__ == "__main__":
    # 抽出したDataFrameを変数dfに保存
    filename = "100_________.json"  # 対象のJSONファイル名に合わせて変更
    df = load_dataframe(filename)
    print(df)
    print(df.shape)
