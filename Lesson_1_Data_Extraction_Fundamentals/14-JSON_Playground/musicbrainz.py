# -*- coding: iso-8859-1 -*-

import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    # 1º) ¿Cuantos grupos musicales se llaman "FIRST AID KIT"?
    # http://musicbrainz.org/ws/2/artist/?query=artist:FIRST+AID+KIT&fmt=json
    results = query_by_name(ARTIST_URL, query_type["simple"], "FIRST AID KIT")
    print "1º)", len(results["artists"])

    # 2º) ¿Cuál es el nombre de la "begin-area" del grupo "Queen"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    print "2º)", results["artists"][0]["begin-area"]["name"]

    # 3º) ¿Cuál es el alias en español del grupo "Beatles"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    print "3º)", results["artists"][0]["aliases"][5]["name"]

    # 4º) ¿Cuál es la desambiguación para el grupo "Nirvana"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    print "4º)", results["artists"][0]["disambiguation"]

    # 5º) ¿Qué año se creó el grupo "One direction"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    print "5º)", results["artists"][0]["life-span"]["begin"][:4]

    # http://musicbrainz.org/ws/2/artist/?query=artist:Nirvana&fmt=json
    # results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    # pretty_print(results)

    # Existen varios artistas correspondientes al nombre "Nirvana". Tomamos el identificador ("id")
    # del artista que aparece en la segunda posición ([1]) del array results["artists"]
    # artist_id = results["artists"][1]["id"]
    # print "\nARTIST:", artist_id
    # pretty_print(results["artists"][1])

    # http://musicbrainz.org/ws/2/artist/9282c8b4-ca0b-4c6b-b7e3-4f7762dfc4d6?fmt=json&inc=releases
    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]
    # print "\nONE RELEASE:"
    # pretty_print(releases[0], indent=2)
    # release_titles = [r["title"] for r in releases]

    # print "\nALL TITLES:"
    # for t in release_titles:
    #    print t


if __name__ == '__main__':
    main()
