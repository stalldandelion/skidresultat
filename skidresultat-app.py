import operator
import os
import sqlite3
from lib.functions import *
from flask import Flask, render_template
import glob

app = Flask(__name__)


def load_database(database):
    global conn
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    c = conn.cursor()

    try:
        c.execute('CREATE TABLE competition (id int, name text, tour int)')
        c.execute('CREATE TABLE season (id int, name text)')
        c.execute('CREATE TABLE skier (id int, name text)')
        c.execute('CREATE TABLE results (id int, compid int, seasonid int, skierid int, competitionpart int,'
                  ' result int, distance text, teqnique text, time text, tourresult int, tour int)')
        c.execute('CREATE TABLE biathlon_results (id int, compid int, seasonid int, skierid int, competitionpart int,'
                  ' result int, distance text, teqnique text, time text, shooting text, tour int)')
        c.execute('CREATE UNIQUE INDEX result_index ON results(id, compid, seasonid, skierid, competitionpart)')
        c.execute('CREATE UNIQUE INDEX biathlon_result_index ON biathlon_results(id, compid, seasonid, skierid)')
    except sqlite3.OperationalError as e:
        print(e)

    json_data = dict()
    for jsonfile in glob.glob(database + '/*.json'):
        json_data.update(json.load(open(jsonfile)))

    for sqlstatement in json_data['competition']:
        c.execute("insert into competition values (" + sqlstatement['id'] + ",'" + sqlstatement['name'] +
                  "','" + sqlstatement['tour'] + "')")

    for sqlstatement in json_data['season']:
        c.execute("insert into season values (" + sqlstatement['id'] + ",'" + sqlstatement['name'] + "')")

    for sqlstatement in json_data['skier']:
        c.execute("insert into skier values (" + sqlstatement['id'] + ",'" + sqlstatement['name'] + "')")

    for sqlstatement in json_data['results']:
        if sqlstatement['teqnique'] == 'Biathlon':
            c.execute("insert into biathlon_results values (" + sqlstatement['id'] + "," + sqlstatement['compid'] +
                      ", " + sqlstatement['seasonid'] + ", " + sqlstatement['skierid'] + ", " +
                      sqlstatement['competitionpart'] + ", " + sqlstatement['result'] + ", '" +
                      sqlstatement['distance'] + "', '" + sqlstatement['teqnique'] + "', '" + sqlstatement['time'] +
                      "', '" + sqlstatement['shooting'] + "', '" + sqlstatement['tour'] + "')")
        else:
            c.execute("insert into results values (" + sqlstatement['id'] + "," + sqlstatement['compid'] +
                      ", " + sqlstatement['seasonid'] + ", " + sqlstatement['skierid'] + ", " +
                      sqlstatement['competitionpart'] + ", " + sqlstatement['result'] + ", '" +
                      sqlstatement['distance'] + "', '" + sqlstatement['teqnique'] + "', '" + sqlstatement['time'] +
                      "', '" + sqlstatement['tourresult'] + "', '" + sqlstatement['tour'] + "')")

    conn.commit()

    return c


def skidresults(skier, template, biathlon=False):

    season_results = {}
    season_pallplatser = {}
    season_pallplatser_grouped = {}

    seasons = get_seasons(dbconn, skier)

    for season in seasons:

        if biathlon:
            results, fvinster, fandra, ftredje, stot, scountpallplatser = get_biathlon_results(dbconn, skier, season)
        else:
            results, fvinster, fandra, ftredje, stot, scountpallplatser = get_results(dbconn, skier, season)

        print('hej: ' + str(fvinster))
        results.sort(key=operator.itemgetter(0, 6))
        season_results[season] = results
        season_pallplatser[season] = [scountpallplatser[0], stot[0]]
        season_pallplatser_grouped[season] = [fvinster, fandra, ftredje]

    return render_template(template, seasons=seasons, season_results=season_results,
                           season_pallplatser=season_pallplatser, season_pallplatser_grouped=season_pallplatser_grouped,
                           namn=skier)


@app.route('/frida')
def frida_results():

    return skidresults('Frida Bergqvist', 'frida.html')


@app.route('/tilde')
def tilde_results():

    return skidresults('Tilde Bergqvist', 'tilde.html')


@app.route('/frida_biathlon')
def frida_biathlon_results():

    return skidresults('Frida Bergqvist', 'frida_biathlon.html', True)


@app.route('/')
def index():

    global dbconn

    dbconn = load_database('static/database')
    if os.path.isfile('/tmp/backup.db'):
        os.remove('/tmp/backup.db')
    with sqlite3.connect('/tmp/backup.db') as new_db:
        new_db.executescript("".join(conn.iterdump()))

    fpallplatser, ftot, ftotcomp, fcountpallplatser = get_pallplatser_index(dbconn, 'Frida Bergqvist')

    b_fpallplatser, b_ftot, b_ftotcomp, b_fcountpallplatser = get_pallplatser_biathlon_index(dbconn, 'Frida Bergqvist')

    tpallplatser, ttot, ttotcomp, tcountpallplatser = get_pallplatser_index(dbconn, 'Tilde Bergqvist')

    return render_template('index.html', fpallplatser=fpallplatser, ftot=ftot, fcountpallplatser=fcountpallplatser,
                           tpallplatser=tpallplatser, ttot=ttot, tcountpallplatser=tcountpallplatser,
                           b_fpallplatser=b_fpallplatser, b_ftot=b_ftot, b_fcountpallplatser=b_fcountpallplatser,
                           ftotcomp=ftotcomp, ttotcomp=ttotcomp)


if __name__ == '__main__':

    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
