from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from . import config
import os
import cv2


app = Flask(__name__)

# TODO: we use global varibles to do simple session management:
# 1. username or user e-mail address as primary key;
# 2. videos play-list (maybe a list);
# 3. actual result-list (maybe a dictionary);
USERID =''
VIDEOLIST = []
ACTUAL_RESULTS = {}
COUNTER = 0
REST_NUMBER = 20
REST_TIME = 60
TOTAL_VIDEO_NUMBER = 60

# TODO: we clean above global varibles when we click "quit" or jump to "successfully_finish"
def connect_db():
    return sqlite3.connect(config.DATABASE_NAME)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':

        return render_template('inheritance/index_start.html')

    elif request.method == 'POST':

        USERID = request.form['userid']
        print(USERID)
        if USERID != '':
            # TODO: initial dataL generate a video play list and clean two global variables: ACTUAL_RESULTS and COUNTER
            initial_data()
            return redirect(url_for('video_play'))
        else:
            return render_template('inheritance/index_start.html')
        # return render_template('inheritance/video_play.html')


@app.route('/video_play', methods=['POST', 'GET'])
def video_play():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':

        # TODO: load right video after we generate a play list
        test_filename = '/static/video/001_deliberate_smile_2.mp4'
        print(test_filename)
        return render_template('inheritance/video_play.html', file_path = test_filename)

    # elif request.method == 'POST':
    #
    #     print(request.form)
    #     # return redirect('inheritance/video_play.html')
    #     return render_template('inheritance/video_play.html')


@app.route('/results_submit', methods=['POST', 'GET'])
def submit():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':

        return render_template('inheritance/results_submit.html')

    elif request.method == 'POST':

        # Save results to the dict

        # video_name = VIDEOLIST[COUNTER]
        # video_result = request.form.getlist('gridRadios')
        # ACTUAL_RESULTS[video_name] = video_result
        COUNTER += 1

        return redirect(url_for('rest'))

@app.route('/rest', methods=['POST', 'GET'])
def rest():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':
        if COUNTER % REST_NUMBER == 0:
            rest_time = REST_TIME
        else:
            rest_time = 1
        if COUNTER == TOTAL_VIDEO_NUMBER:
            return render_template('inheritance/finish.html')
        else:
            return render_template('inheritance/rest.html', Rest_time = rest_time, count_number = 5 )



@app.route('/quit', methods=['POST', 'GET'])
def quit():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':
        # TODO: reset all global variables
        reset_data()
        return render_template('inheritance/quit.html')

@app.route('/finish', methods=['POST', 'GET'])
def finish():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    if request.method == 'GET':
        # TODO: save userid, video_list and results to JSON file
        save_to_json()
        reset_data()
        return render_template('inheritance/finish.html')

def initial_data():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    load_video_list()
    # to clean the data
    ACTUAL_RESULTS = {}
    COUNTER = 0

def save_to_json():
    # TODO: use the right format to save
    # 1. userid
    # 2. video play list (or maybe dict Actual results is okay?)
    # 3. accuracy

    print("save to local json file")

# reset the global variables when we quit or finishing the test
def reset_data():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME

    USERID = ''
    VIDEOLIST = []
    ACTUAL_RESULTS = {}
    COUNTER = 0

def load_video_list():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME
    # TODO: add logic to load right video list to global variable VIDEOLIST
    print("load ")