import json
import operator
import os
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)


def load_database(database):
    global conn
    conn = sqlite3.connect(":memory:")
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

    json_data = json.load(open(database))
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


@app.route('/frida')
def frida_results():

    season_results = {}
    season_pallplatser = {}
    season_pallplatser_grouped = {}

    for season in fseasons:
        dbconn.execute("select a.name, a.tour, b.teqnique, b.distance, b.time, b.result, b.competitionpart, "
                       "b.tourresult from competition a, results b, season c, skier d where "
                       "a.id=b.compid and b.seasonid=c.id and b.skierid=d.id and d.name='Frida Bergqvist' and "
                       "c.name='" + season + "' order by b.compid, b.competitionpart")

        res = dbconn.fetchall()

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 1 and c.id=a.seasonid and c.name='" +
            season + "' group by a.tourresult")
        vinster = dbconn.fetchall()
        if len(vinster) == 0:
            fvinster = 0
        else:
            fvinster = vinster[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 2 and c.id=a.seasonid and c.name='"
            + season + "' group by a.tourresult")
        andra = dbconn.fetchall()
        if len(andra) == 0:
            fandra = 0
        else:
            fandra = andra[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 3 and c.id=a.seasonid and c.name='" +
            season + "' group by a.tourresult")
        tredje = dbconn.fetchall()
        if len(tredje) == 0:
            ftredje = 0
        else:
            ftredje = tredje[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and c.id=a.seasonid and c.name='" + season + "'")
        stot = dbconn.fetchall()
        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Frida Bergqvist' and "
            "c.name='" + season + "' and a.competitionpart in (0, 1) and c.id=a.seasonid and a.skierid=b.id "
                                  "and a.tourresult < 4 and a.tourresult > 0")
        scountpallplatser = dbconn.fetchall()
        results = [x for x in res]

        results.sort(key=operator.itemgetter(0, 6))
        print(results)
        season_results[season] = results
        season_pallplatser[season] = [scountpallplatser[0], stot[0]]
        season_pallplatser_grouped[season] = [fvinster, fandra, ftredje]

    return render_template('frida.html', seasons=fseasons, season_results=season_results,
                           season_pallplatser=season_pallplatser, season_pallplatser_grouped=season_pallplatser_grouped)


@app.route('/frida_biathlon')
def frida_biathlon_results():

    season_results = {}
    season_pallplatser = {}
    season_pallplatser_grouped = {}

    for season in fseasons:
        dbconn.execute("select a.name, b.shooting, b.distance, b.time, b.result, b.competitionpart, b.shooting "
                       "from competition a, biathlon_results b, season c, skier d where "
                       "a.id=b.compid and b.seasonid=c.id and b.skierid=d.id and d.name='Frida Bergqvist' and "
                       "c.name='" + season + "'")

        res = dbconn.fetchall()

        dbconn.execute(
            "select count(a.result) from biathlon_results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.result == 1 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
        vinster = dbconn.fetchall()
        if len(vinster) == 0:
            fvinster = 0
        else:
            fvinster = vinster[0][0]

        dbconn.execute(
            "select count(a.result) from biathlon_results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.result == 2 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
        andra = dbconn.fetchall()
        if len(andra) == 0:
            fandra = 0
        else:
            fandra = andra[0][0]

        dbconn.execute(
            "select count(a.result) from biathlon_results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and a.result == 3 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
        tredje = dbconn.fetchall()
        if len(tredje) == 0:
            ftredje = 0
        else:
            ftredje = tredje[0][0]

        dbconn.execute(
            "select count(a.result) from biathlon_results a, skier b, season c where b.name='Frida Bergqvist' and "
            "a.skierid=b.id and c.id=a.seasonid and c.name='" + season + "'")
        stot = dbconn.fetchall()
        dbconn.execute(
            "select count(a.result) from biathlon_results a, skier b, season c where b.name='Frida Bergqvist' and "
            "c.name='" + season + "' and c.id=a.seasonid and a.skierid=b.id and a.result < 4 and a.result > 0")
        scountpallplatser = dbconn.fetchall()
        results = [x for x in res]
        results.sort(key=operator.itemgetter(0, 5))
        season_results[season] = results
        season_pallplatser[season] = [scountpallplatser[0], stot[0]]
        season_pallplatser_grouped[season] = [fvinster, fandra, ftredje]

    return render_template('frida_biathlon.html', seasons=fseasons, season_results=season_results,
                           season_pallplatser=season_pallplatser, season_pallplatser_grouped=season_pallplatser_grouped)


@app.route('/tilde')
def tilde_results():

    season_results = {}
    season_pallplatser = {}
    season_pallplatser_grouped = {}

    for season in fseasons:
        dbconn.execute("select a.name, a.tour, b.teqnique, b.distance, b.time, b.result, b.competitionpart, "
                       "b.tourresult from competition a, results b, season c, skier d where "
                       "a.id=b.compid and b.seasonid=c.id and b.skierid=d.id and d.name='Tilde Bergqvist' and "
                       "c.name='" + season + "' order by b.compid, b.competitionpart")

        res = dbconn.fetchall()

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Tilde Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 1 and c.id=a.seasonid and "
            "c.name='" + season + "' group by a.tourresult")
        vinster = dbconn.fetchall()
        if len(vinster) == 0:
            fvinster = 0
        else:
            fvinster = vinster[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Tilde Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 2 and c.id=a.seasonid and "
            "c.name='" + season + "' group by a.tourresult")
        andra = dbconn.fetchall()
        if len(andra) == 0:
            fandra = 0
        else:
            fandra = andra[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Tilde Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 3 and c.id=a.seasonid and "
            "c.name='" + season + "' group by a.result")
        tredje = dbconn.fetchall()
        if len(tredje) == 0:
            ftredje = 0
        else:
            ftredje = tredje[0][0]

        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Tilde Bergqvist' and "
            "a.skierid=b.id and a.competitionpart in (0, 1) and c.id=a.seasonid and c.name='" + season + "'")
        stot = dbconn.fetchall()
        dbconn.execute(
            "select count(a.tourresult) from results a, skier b, season c where b.name='Tilde Bergqvist' and "
            "c.name='" + season + "' and a.competitionpart in (0, 1) and c.id=a.seasonid and a.skierid=b.id and "
                                  "a.tourresult < 4 and a.tourresult > 0")
        scountpallplatser = dbconn.fetchall()
        results = [x for x in res]
        results.sort(key=operator.itemgetter(0, 6))
        print(results)
        season_results[season] = results
        season_pallplatser[season] = [scountpallplatser[0], stot[0]]
        season_pallplatser_grouped[season] = [fvinster, fandra, ftredje]

    return render_template('tilde.html', seasons=tseasons, season_results=season_results,
                           season_pallplatser=season_pallplatser, season_pallplatser_grouped=season_pallplatser_grouped)


@app.route('/')
def index():

    global fseasons
    global tseasons
    global dbconn

    dbconn = load_database('static/skid_db.json')
    if os.path.isfile('/tmp/backup.db'):
        os.remove('/tmp/backup.db')
    with sqlite3.connect('/tmp/backup.db') as new_db:
        new_db.executescript("".join(conn.iterdump()))

    dbconn.execute("select distinct(a.name) from season a, results b, skier c where c.name='Frida Bergqvist' and "
                   "b.skierid=c.id and a.id in (select distinct(seasonid) from results)")
    fseasons = [x[0] for x in dbconn.fetchall()][::-1]

    dbconn.execute("select distinct(a.name) from season a, results b, skier c where c.name='Tilde Bergqvist' and "
                   "b.skierid=c.id and a.id in (select distinct(seasonid) from results)")
    tseasons = [x[0] for x in dbconn.fetchall()][::-1]

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id and "
        "a.tourresult < 4 and a.tourresult > 0  and a.competitionpart in (0, 1) group by a.tourresult")
    fpallplatser = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id")
    ftot = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id "
        "and a.competitionpart in (0, 1)")
    ftotcomp = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id and "
        "a.tourresult < 4 and a.tourresult > 0 and a.competitionpart in (0, 1)")
    fcountpallplatser = dbconn.fetchall()

    dbconn.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id and "
        "a.result < 4 and a.result > 0 group by a.result")
    b_fpallplatser = dbconn.fetchall()

    dbconn.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id")
    b_ftot = dbconn.fetchall()

    dbconn.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='Frida Bergqvist' and a.skierid=b.id and "
        "a.result < 4 and a.result > 0")
    b_fcountpallplatser = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Tilde Bergqvist' and a.skierid=b.id and "
        "a.result < 4 and a.result > 0 and a.competitionpart in (0, 1) group by a.tourresult")
    tpallplatser = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Tilde Bergqvist' and a.skierid=b.id")
    ttot = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Tilde Bergqvist' and a.skierid=b.id "
        "and a.competitionpart in (0, 1)")
    ttotcomp = dbconn.fetchall()

    dbconn.execute(
        "select count(a.tourresult) from results a, skier b where b.name='Tilde Bergqvist' and a.skierid=b.id and "
        "a.tourresult < 4 and a.tourresult > 0 and a.competitionpart in (0, 1)")
    tcountpallplatser = dbconn.fetchall()

    return render_template('index.html', fpallplatser=fpallplatser, ftot=ftot, fcountpallplatser=fcountpallplatser,
                           tpallplatser=tpallplatser, ttot=ttot, tcountpallplatser=tcountpallplatser,
                           b_fpallplatser=b_fpallplatser, b_ftot=b_ftot, b_fcountpallplatser=b_fcountpallplatser,
                           ftotcomp=ftotcomp, ttotcomp=ttotcomp)


if __name__ == '__main__':

    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
