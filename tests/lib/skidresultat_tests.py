import sys
sys.path.append("/Users/micke/PycharmProjects/skidresultat")
from lib import functions as funs


def test_ok_get_locations():

    locactionlist = funs.get_locations("/Users/micke/PycharmProjects/skidresultat/static/skid_db.json")
    assert isinstance(list(), type(locactionlist))
    assert 'Hudikrännet' in [x['name'] for x in locactionlist]