import pandas as pd
import json
import io
import csv
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


def csv_text_to_dataframe(csv_text: str) -> pd.DataFrame:
    """CSVテキストをDataFrameに変換する（列数の揺れに頑健）。

    LLMが生成したCSVは行ごとにフィールド数が一致しないことがある
    （例: 戦略フラグ列が余分に付く）。そのままpd.read_csvに渡すと
    「Expected N fields, saw M」のParserErrorになるため、
    ヘッダーの列数に合わせて各行を切り詰め／不足分はパディングする。
    """
    rows = list(csv.reader(io.StringIO(csv_text)))
    if not rows:
        return pd.DataFrame()

    header = rows[0]
    ncol = len(header)

    fixed_rows = []
    for r in rows[1:]:
        # 50件ごとに挿入される重複ヘッダー行をスキップする
        if r[:len(header)] == header or r[0] == header[0]:
            continue
        if len(r) > ncol:
            r = r[:ncol]          # 余分な末尾フィールドを捨てる
        elif len(r) < ncol:
            r = r + [None] * (ncol - len(r))  # 不足分を埋める
        fixed_rows.append(r)

    df = pd.DataFrame(fixed_rows, columns=header)

    # 数値列を可能な範囲で数値型に変換する（変換できない列はそのまま）
    for col in df.columns:
        if col in ("発言者", "発言"):
            continue
        converted = pd.to_numeric(df[col], errors="coerce")
        # 元が非欠損なのに変換でNaNになった値がなければ数値列として採用
        if not (converted.isna() & df[col].notna()).any():
            df[col] = converted
    return df


def load_dataframe(filename: str) -> pd.DataFrame:
    """JSONファイルのoutputキーからCSVを抽出してDataFrameを返す。"""
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    # データはリストの先頭要素に格納されている
    record = data[0]
    csv_text = extract_csv_from_output(record["output"])
    df = csv_text_to_dataframe(csv_text)
    return df


if __name__ == "__main__":
    # 抽出したDataFrameを変数dfに保存
    import glob

    file_list = glob.glob("*.json")
    df_list = []
    for filename in file_list:
        # デバッグ用: 読み込み中のファイル名を表示
        print(f"読み込み中: {filename}")
        try:
            df = load_dataframe(filename)
        except Exception as e:
            # エラーが起きたファイルを特定できるようファイル名と一緒に表示
            print(f"  -> エラー発生: {filename}")
            print(f"     {type(e).__name__}: {e}")
            continue
        print(f"  -> OK: {df.shape}")
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    print(combined_df.head())
