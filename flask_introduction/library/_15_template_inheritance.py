from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from . import config
import os
import cv2


app = Flask(__name__)


def connect_db():
    return sqlite3.connect(config.DATABASE_NAME)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':

        # return render_template('inheritance/index_start.html')
        return render_template('inheritance/index_start.html')

    elif request.method == 'POST':
        # db = connect_db()
        # sql_query = """
        #     INSERT INTO book ("title", "isbn", "author_id") VALUES (:title, :isbn, :author_id);
        # """
        # db.execute(sql_query, {
        #     'title': request.form['title'],
        #     'isbn': request.form['isbn'],
        #     'author_id': int(request.form['author']),
        # })
        # db.commit()
        # return "The new book {} was correctly saved".format(request.form['title'])
        print(request.form)
        # return redirect('inheritance/video_play.html')
        return render_template('inheritance/video_play.html')


@app.route('/video_play', methods=['POST', 'GET'])
def video_play():
    if request.method == 'GET':

        test_filename = '/static/video/001_deliberate_smile_2.mp4'
        print(APP_ROOT)
        print(test_filename)
        return render_template('inheritance/video_play.html', file_path = test_filename)

    elif request.method == 'POST':

        print(request.form)
        # return redirect('inheritance/video_play.html')
        return render_template('inheritance/video_play.html')


@app.route('/results_submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':

        return render_template('inheritance/results_submit.html')

    elif request.method == 'POST':

        print(request.form)
        # return redirect('inheritance/video_play.html')
        return render_template('inheritance/video_play.html')