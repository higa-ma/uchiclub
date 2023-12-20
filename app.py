#flaskモジュールからFlaskクラスをインポート
from flask import Flask,render_template,request,redirect,session
#Flaskクラスでインスタンス化してapp変数に代入
#sqlite3をインポート
import sqlite3
app = Flask(__name__)
#secret_keyでセッション情報を暗号化
app.secret_key = "SUNABACO2023"

@app.route("/")
def top():
    template = "top"
    if "ploblem_No" in session:
        session.pop("ploblem_No", None)
    session["correct"] = 0
    session["ploblem_No"] = 1
    ploblem_No = session["ploblem_No"]
    return render_template("top.html",template = template, ploblem_No = ploblem_No)

@app.route("/answer/<int:number>", methods=["POST"])
def answer(number):
    template = "answer"
    a_answer = request.form.get("A")
    b_answer = request.form.get("B")
    print("--------------------------")
    print(a_answer)
    print(b_answer)
    ploblem_No = session["ploblem_No"]
    conn = sqlite3.connect("works.db")
    #3,DBを操作するための準備 Cは変数名なんでもいい
    c = conn.cursor()
    #4,SQLを実行してDBにデータを送る
    c.execute("SELECT id FROM problems where numbers = ? AND answers = ? AND answers2 = ? ",(ploblem_No, a_answer, b_answer))
    #5,DBを保存（変更を書き込む）
    answer = c.fetchone()
    if answer is None:
        judge = "不正解"
    else:
        judge = "正解"
    
    if judge == "正解":
        correct=session["correct"]
        session["correct"]=correct+1
        
    c.execute("select explanA,explanB from Explan where numbers = ?",(number,))
    explan = c.fetchone()
    
    # 問題の制御 ploblem_Noで現在の問題番号に+1
    session["ploblem_No"] = number+1
    ploblem_No = session["ploblem_No"]
    # 登録されている現在の問題数を取得
    c.execute("SELECT count(*) FROM problems ")
    all_ploblem = c.fetchone()[0]
    c.close()
    # 現在の問題番号がDBに登録されている問題数より多い場合result.htmlを表示
    # if ploblem_No > all_ploblem :
    #     correct = session["correct"]
    #     template = "result"
    #     return render_template("result.html",correct = correct,all_ploblem = all_ploblem,template = template)
    
    return render_template("answer.html",template = template,judge = judge,explan=explan,ploblem_No=ploblem_No, all_ploblem = all_ploblem ,number = number)

@app.route("/result")
def result():
    conn = sqlite3.connect("works.db")
    #3,DBを操作するための準備 Cは変数名なんでもいい
    c = conn.cursor()
    c.execute("SELECT count(*) FROM problems ")
    all_ploblem = c.fetchone()[0]
    c.close()
    correct = session["correct"]
    template = "result"
    return render_template("result.html",correct = correct,all_ploblem = all_ploblem,template = template)


@app.route("/question/<int:number>")
def question(number):
    template = "demo"
    conn = sqlite3.connect("works.db")
    #3,DBを操作するための準備 Cは変数名なんでもいい
    c = conn.cursor()
    #4,SQLを実行してDBにデータを送る
    c.execute("SELECT * FROM problems where numbers = ?",(number,))
    #5,DBを保存（変更を書き込む）
    problems = c.fetchone()
    if problems is None:
        return redirect("/")
    c.execute("SELECT * FROM choices where numbers =? and adapt = 'A' ",(number,))
    choicesA = c.fetchall()
    c.execute("SELECT * FROM choices where numbers =? and adapt = 'B' ",(number,))
    choicesB = c.fetchall()

    conn.close()

    return render_template("demo.html",template = template,choicesA = choicesA ,choicesB = choicesB,problems=problems,number = number )




#スクリプトが直接実行された場合
if __name__ == "__main__":
    #FlaskのWEBアプリケーションを起動（デバックデートで）
    app.run(debug=True)
        
