import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========================
# ✅ モード選択： "csv" または "sheets"
# ========================
MODE = "csv"  # ←ここを "csv" に変更

CSV_PATH = "ChatbotQuestions.csv"
SPREADSHEET_NAME = "ChatbotQuestions"
SHEET_NAME = "シート1"

# ========================
# データ読み込み
# ========================
if MODE == "csv":
    print("📄 CSVから読み込み中...")
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
elif MODE == "sheets":
    print("📡 Google Sheetsから読み込み中...")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
else:
    raise ValueError("❌ MODE は 'csv' または 'sheets' のどちらかにしてください。")

# ========================
# SQLiteデータベース初期化
# ========================
print("🛠️ SQLiteデータベースを作成中...")
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS questions")
cursor.execute("DROP TABLE IF EXISTS options")

cursor.execute("""
CREATE TABLE questions (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT,
    label TEXT,
    next_id TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
)
""")

# ========================
# データ登録（縦形式対応）
# ========================
added_questions = set()

for _, row in df.iterrows():
    qid = str(row["id"]).strip()
    qtext = str(row["question"]).strip()
    label = str(row["option"]).strip()
    next_qid = str(row["next"]).strip()

    if qid not in added_questions:
        cursor.execute("INSERT INTO questions (id, text) VALUES (?, ?)", (qid, qtext))
        added_questions.add(qid)

    if label != "" and next_qid != "":
        cursor.execute("""
            INSERT INTO options (question_id, label, next_id)
            VALUES (?, ?, ?)
        """, (qid, label, next_qid))

conn.commit()
conn.close()

print(f"✅ chatbot.db の更新が完了しました！（MODE: {MODE}）")
