import fortnite_api
from fortnite_api import MatchMethod

fn = fortnite_api.FortniteAPI('api_key')


if __name__ == '__main__':
    print([e.name for e in fn.cosmetics.search_all(name='ome', match_method=MatchMethod.STARTS)])
