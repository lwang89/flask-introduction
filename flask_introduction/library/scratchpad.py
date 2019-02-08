from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from . import config
import os
import random
import json


app = Flask(__name__)


USERID = ''
AGE = ''
GENDER = ''
VIDEOLIST = []
ACTUAL_RESULTS = {}
COUNTER = 0
REST_NUMBER = 20
REST_TIME = 45
TOTAL_VIDEO_NUMBER = 60

# TODO: need to add new global variables for ScratchPad.
# TODO: USERID, AGE, GENDER, TPOIC, SUBTOPICS, and so on.

def connect_db():
    return sqlite3.connect(config.DATABASE_NAME)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        # load_video_list()

        return render_template('inheritance/index.html')

    elif request.method == 'POST':

        USERID = request.form['userid']
        print(USERID)
        AGE = request.form['age']
        print(AGE)
        GENDER = request.form.getlist('gridRadios')
        print(GENDER)
        if USERID != '' and AGE != '' and GENDER != '':
            initial_data()
            return redirect(url_for('start'))
        else:
            return render_template('inheritance/index.html')
        # return render_template('inheritance/video_play.html')

@app.route('/start', methods=['POST', 'GET'])
def start():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        return render_template('inheritance/start.html')


@app.route('/task1_intro', methods=['POST', 'GET'])
def task1_intro():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        return render_template('inheritance/task1_intro.html')

## We won't use the functions and related pages below

@app.route('/video_play', methods=['POST', 'GET'])
def video_play():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':

        base_path = '/static/video/'
        temp_video_name = VIDEOLIST[COUNTER]

        if 'spontaneous' in temp_video_name:
            video_path = base_path + 'spontaneous/' + temp_video_name
        else:
            video_path = base_path + 'deliberate/' + temp_video_name
        # test_filename = '/static/video/deliberate/002_deliberate_smile_1.mp4'
        print(video_path)

        return render_template('inheritance/video_play.html', file_path = video_path)

    # elif request.method == 'POST':
    #
    #     print(request.form)
    #     # return redirect('inheritance/video_play.html')
    #     return render_template('inheritance/video_play.html')


@app.route('/results_submit', methods=['POST', 'GET'])
def submit():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':

        return render_template('inheritance/results_submit.html')

    elif request.method == 'POST':

        # Save results to the dict

        video_name = VIDEOLIST[COUNTER]
        video_result = request.form.getlist('gridRadios')
        print(video_result)
        ACTUAL_RESULTS[video_name] = video_result[0]
        print (len(ACTUAL_RESULTS))
        COUNTER += 1

        return redirect(url_for('rest'))

@app.route('/rest', methods=['POST', 'GET'])
def rest():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        if COUNTER % REST_NUMBER == 0:
            rest_time = REST_TIME
        else:
            rest_time = 1
        if COUNTER == TOTAL_VIDEO_NUMBER:
            return redirect(url_for('finish'))
        else:
            return render_template('inheritance/rest.html', Rest_time = rest_time, count_number = COUNTER )



@app.route('/quit', methods=['POST', 'GET'])
def quit():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        reset_data()
        return render_template('inheritance/quit.html')

@app.route('/finish', methods=['POST', 'GET'])
def finish():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    if request.method == 'GET':
        save_to_json()
        reset_data()
        return render_template('inheritance/finish.html')

def initial_data():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER

    ACTUAL_RESULTS = {}
    COUNTER = 0
    load_video_list()


def save_to_json():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER
    # 1. userid
    # 2. ACTUAL_RESULTS
    # 3. accuracy
    # 4. age
    # 5. gender
    right_answers = 0
    print(ACTUAL_RESULTS)
    for key, value in ACTUAL_RESULTS.items():
        if value in key:
            right_answers += 1
    accuracy = right_answers / len(ACTUAL_RESULTS)

    data = {}
    data[USERID] = []
    data[USERID].append(ACTUAL_RESULTS)
    data[USERID].append({'accuracy' : accuracy})
    data[USERID].append({'Age': AGE})
    data[USERID].append({'Gender': GENDER})
    accuracy_json = {}
    accuracy_json[USERID] = accuracy

    with open('smile_results.txt', 'a') as outfile:
        json.dump(data, outfile)
    with open('smile_accuracy.txt', 'a') as accuracy_file:
        json.dump(accuracy_json, accuracy_file)

    print("save to local json file")

# reset the global variables when we quit or finishing the test
def reset_data():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER

    USERID = ''
    AGE = ''
    GENDER = ''
    VIDEOLIST = []
    ACTUAL_RESULTS = {}
    COUNTER = 0

def load_video_list():
    global VIDEOLIST, USERID, ACTUAL_RESULTS, COUNTER, REST_NUMBER, TOTAL_VIDEO_NUMBER, REST_TIME, AGE, GENDER

    # we need absolute path here
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    spon_list_path = BASE_DIR + '/static/video/spontaneous/'
    deli_list_path = BASE_DIR + '/static/video/deliberate/'
    spon_all_files = os.listdir(spon_list_path)
    deli_all_files = os.listdir(deli_list_path)
    total_all_files = spon_all_files + deli_all_files
    spon_counter = 0
    deli_counter = 0

    random_spon_video_list = []
    random_deli_video_list = []

    while (spon_counter < (TOTAL_VIDEO_NUMBER/2)):
        new_spon_video = random.choice(spon_all_files)

        if len(random_spon_video_list) == 0:
            random_spon_video_list.append(new_spon_video)
            spon_counter += 1
        else:
            if any (new_spon_video[:3] in spon_video for spon_video in random_spon_video_list):
                continue
            else:
                random_spon_video_list.append(new_spon_video)
                spon_counter += 1

    while (deli_counter < (TOTAL_VIDEO_NUMBER/2)):
        new_deli_video = random.choice(deli_all_files)

        if len(random_deli_video_list) == 0:
            random_deli_video_list.append(new_deli_video)
            deli_counter += 1
        else:
            if any (new_deli_video[:3] in deli_video for deli_video in random_deli_video_list):
                continue
            else:
                random_deli_video_list.append(new_deli_video)
                deli_counter += 1

    random_all_video_list = random_deli_video_list + random_spon_video_list
    random.shuffle(random_all_video_list)
    VIDEOLIST = random_all_video_list
    # print(VIDEOLIST)
    # print(len(VIDEOLIST))
