from typing import Counter
from flask import Flask, request, redirect, url_for, render_template, abort, jsonify
from model import db, save_db

app = Flask(__name__)


@app.route('/')
def welcome():
    cards = db
    return render_template('welcome.html', cards=cards)


@app.route('/card/<int:index>')
def card_view(index):
    try:
        card = db[index]
        return render_template('card.html', card=card, index=index, max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route('/cards/add', methods=['GET', 'POST'])
def card_add():
    if request.method == 'GET':
        return render_template('card_add.html')
    else:
        body = request.form
        if body is None:
            abort(422)
        else:
            question = body.get('question', None)
            answer = body.get('answer', None)
            if question is None or answer is None:
                abort(400)
            else:
                item = {"question": question, "answer": answer}
                db.append(item)
                save_db()
                return redirect(url_for('card_view', index=len(db)-1))


@app.route('/api')
def welcome_api():
    return jsonify(db)


@app.route('/api/<int:index>')
def card_view_api(index):
    return jsonify(db[index])
