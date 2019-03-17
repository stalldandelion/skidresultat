import json


def get_locations(jsondb):
    locations = list()

    with open(jsondb) as json_file:
        data = json.load(json_file)

    for i in data['competition']:
        locations.append(i)

    return locations


def get_highest_location_id():

    return max(
        [int(x.get('id')) for x in get_locations("/Users/micke/PycharmProjects/skidresultat/static/skid_db.json")]
    )


def get_seasons(c, skier):

    c.execute("select distinct(a.name) from season a, results b, skier c where c.name='" + skier + "' and "
              "b.skierid=c.id and a.id in (select distinct(seasonid) from results)")

    return [x[0] for x in c.fetchall()][::-1]


def get_biathlon_results(c, skier, season):

    c.execute("select a.name, b.shooting, b.distance, b.time, b.result, b.competitionpart, b.shooting "
              "from competition a, biathlon_results b, season c, skier d where "
              "a.id=b.compid and b.seasonid=c.id and b.skierid=d.id and d.name='" + skier + "' and "
              "c.name='" + season + "'")

    res = c.fetchall()

    c.execute(
        "select count(a.result) from biathlon_results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.result == 1 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
    vinster = c.fetchall()
    if len(vinster) == 0:
        vinster = 0
    else:
        vinster = vinster[0][0]

    c.execute(
        "select count(a.result) from biathlon_results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.result == 2 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
    andra = c.fetchall()
    if len(andra) == 0:
        andra = 0
    else:
        andra = andra[0][0]

    c.execute(
        "select count(a.result) from biathlon_results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.result == 3 and c.id=a.seasonid and c.name='" + season + "' group by a.result")
    tredje = c.fetchall()
    if len(tredje) == 0:
        tredje = 0
    else:
        tredje = tredje[0][0]

    c.execute(
        "select count(a.result) from biathlon_results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and c.id=a.seasonid and c.name='" + season + "'")
    tot = c.fetchall()
    c.execute(
        "select count(a.result) from biathlon_results a, skier b, season c where b.name='" + skier + "' and "
        "c.name='" + season + "' and c.id=a.seasonid and a.skierid=b.id and a.result < 4 and a.result > 0")
    scountpallplatser = c.fetchall()

    results = [x for x in res]

    return results, vinster, andra, tredje, tot, scountpallplatser


def get_results(c, skier, season):

    c.execute("select a.name, a.tour, b.teqnique, b.distance, b.time, b.result, b.competitionpart, "
              "b.tourresult from competition a, results b, season c, skier d where "
              "a.id=b.compid and b.seasonid=c.id and b.skierid=d.id and d.name='" + skier + "' and "
              "c.name='" + season + "' order by b.compid, b.competitionpart")

    res = c.fetchall()

    c.execute(
        "select count(a.tourresult) from results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 1 and c.id=a.seasonid and c.name='" +
        season + "' group by a.tourresult")
    vinster = c.fetchall()
    if len(vinster) == 0:
        vinster = 0
    else:
        vinster = vinster[0][0]

    c.execute(
        "select count(a.tourresult) from results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 2 and c.id=a.seasonid and c.name='"
        + season + "' group by a.tourresult")
    andra = c.fetchall()
    if len(andra) == 0:
        andra = 0
    else:
        andra = andra[0][0]

    c.execute(
        "select count(a.tourresult) from results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.competitionpart in (0, 1) and a.tourresult == 3 and c.id=a.seasonid and c.name='" +
        season + "' group by a.tourresult")
    tredje = c.fetchall()
    if len(tredje) == 0:
        tredje = 0
    else:
        tredje = tredje[0][0]

    c.execute(
        "select count(a.tourresult) from results a, skier b, season c where b.name='" + skier + "' and "
        "a.skierid=b.id and a.competitionpart in (0, 1) and c.id=a.seasonid and c.name='" + season + "'")
    tot = c.fetchall()

    c.execute(
        "select count(a.tourresult) from results a, skier b, season c where b.name='" + skier + "' and "
        "c.name='" + season + "' and a.competitionpart in (0, 1) and c.id=a.seasonid and a.skierid=b.id "
                              "and a.tourresult < 4 and a.tourresult > 0")
    scountpallplatser = c.fetchall()

    results = [x for x in res]

    return results, vinster, andra, tredje, tot, scountpallplatser


def get_pallplatser_index(c, skier):

    c.execute(
        "select count(a.tourresult) from results a, skier b where b.name='" + skier + "' and a.skierid=b.id and "
        "a.tourresult < 4 and a.tourresult > 0  and a.competitionpart in (0, 1) group by a.tourresult")
    pallplatser = c.fetchall()

    c.execute(
        "select count(a.tourresult) from results a, skier b where b.name='" + skier + "' and a.skierid=b.id")
    tot = c.fetchall()

    c.execute(
        "select count(a.tourresult) from results a, skier b where b.name='" + skier + "' and a.skierid=b.id "
        "and a.competitionpart in (0, 1)")
    totcomp = c.fetchall()

    c.execute(
        "select count(a.tourresult) from results a, skier b where b.name='" + skier + "' and a.skierid=b.id and "
        "a.tourresult < 4 and a.tourresult > 0 and a.competitionpart in (0, 1)")
    countpallplatser = c.fetchall()

    return pallplatser, tot, totcomp, countpallplatser


def get_pallplatser_biathlon_index(c, skier):

    c.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='" + skier + "' and a.skierid=b.id and "
        "a.result < 4 and a.result > 0 group by a.result")
    pallplatser = c.fetchall()

    c.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='" + skier + "' and a.skierid=b.id")
    tot = c.fetchall()

    c.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='" + skier + "' and a.skierid=b.id "
        "and a.competitionpart in (0, 1)")
    totcomp = c.fetchall()

    c.execute(
        "select count(a.result) from biathlon_results a, skier b where b.name='" + skier + "' and a.skierid=b.id and "
        "a.result < 4 and a.result > 0")
    countpallplatser = c.fetchall()

    return pallplatser, tot, totcomp, countpallplatser
