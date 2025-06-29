from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# =============================
# データベースから質問・選択肢・全質問を取得
# =============================
def get_question(q_id):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # 現在の質問を取得
    cursor.execute("SELECT id, text FROM questions WHERE id=?", (q_id,))
    question = cursor.fetchone()

    if not question:
        conn.close()
        return None, [], []

    # 選択肢を取得
    cursor.execute("SELECT label, next_id FROM options WHERE question_id=?", (q_id,))
    options_raw = cursor.fetchall()
    options = []
    for o in options_raw:
        next_id = o[1]
        if not next_id or str(next_id).lower() in ['none', 'result', 'end']:
            next_id = 'end'
        options.append((o[0], next_id))

    # 全質問を取得（スライドUI用）
    cursor.execute("SELECT id, text FROM questions")
    all_questions_raw = cursor.fetchall()
    all_questions = []
    for q in all_questions_raw:
        cursor.execute("SELECT label, next_id FROM options WHERE question_id=?", (q[0],))
        opts = cursor.fetchall()
        opt_list = []
        for o in opts:
            next_id = o[1]
            if not next_id or str(next_id).lower() in ['none', 'result', 'end']:
                next_id = 'end'
            opt_list.append({'text': o[0], 'next_id': next_id})
        all_questions.append({'id': q[0], 'question': q[1], 'options': opt_list})

    # 表示済みの質問を除外（現在の質問以外を表示）
    all_questions = [q for q in all_questions if q['id'] != question[0]]

    conn.close()
    return question, options, all_questions

# =============================
# ルーティング
# =============================
@app.route('/')
def index():
    return redirect(url_for('question', q_id='q01'))

@app.route('/question/start')
def question_start():
    return redirect(url_for('question', q_id='q01'))

@app.route('/question/<q_id>')
def question(q_id):
    question_data, options, all_questions = get_question(q_id)
    if not question_data:
        return redirect(url_for('end'))
    return render_template('question.html',
                           question=question_data,
                           options=options,
                           all_questions=all_questions)

@app.route('/end')
def end():
    return render_template('end.html')

# =============================
# アプリ起動
# =============================
if __name__ == '__main__':
    app.run(debug=True)
