#!/usr/bin/env python
import yaml
import json
post = {'id': '',
        'compid': '',
        'seasonid': '',
        'skierid': '',
        'competitionpart': '1',
        'result': '',
        'distance': '',
        'teqnique': '',
        'time': '',
        'tourresult': '',
        'tour': '0'}

with open('static/database/results.json') as resultstream:
    results = yaml.load(resultstream, yaml.Loader)

resultid = str(int(results['results'][-1]['id']) + 1)

with open('static/database/skiers.json') as skierstream:
    skiers = yaml.load(skierstream, yaml.Loader)
    for skier in skiers['skier']:
        print(f"{skier['id']}: {skier['name']}")

skierid = input('Vilken åkare: ')

with open('static/database/seasons.json') as seasonstream:
    seasons = yaml.load(seasonstream, yaml.Loader)
    for season in seasons['season']:
        print(f"{season['id']}: {season['name']}")

seasonid = input('Vilken säsong: ')

with open('static/database/competitions.json') as compstream:
    comps = yaml.load(compstream, yaml.Loader)
    for comp in comps['competition']:
        print(f"{comp['id']}: {comp['name']}")

compid = input('Vilken tävling: ')

choice = 0
while int(choice) != 1 and int(choice) != 2:
    print('1: Skate')
    print('2: Klassisk')
    choice = input('Vilken teknik (skate/klassisk): ')
    if int(choice) == 1:
        technique = 'skate'
    elif int(choice) == 2:
        technique = 'klassisk'
    else:
        print('Valet är inte godtagbart! Välj nåt av valen nedan....')

distance = input('Vilken distans (km): ')
time = input('Vilken tid: ')
result = input('Resultat: ')

post['id'] = resultid
post['skierid'] = skierid
post['seasonid'] = seasonid
post['compid'] = compid
post['teqnique'] = technique
post['distance'] = distance
post['result'] = result
post['time'] = time
post['tourresult'] = result


results['results'].append(post)
with open('static/database/results.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(results))
