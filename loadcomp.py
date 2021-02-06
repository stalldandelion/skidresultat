#!/usr/bin/env python
import yaml

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

technique = input('Vilken teknik (skate/klassisk: ')
distance = input('Vilken distans (km): ')
