"""Build Geolayers-ready GeoJSON for the "Why do French trains go through Paris?" short.

Source: SNCF Reseau open data (ODbL) via github.com/nicolaswurtz/extras-opendata-sncf-reseau
(lignes-vitesses.geojson + localites.geojson). Coordinates are WGS84 lon/lat (EPSG:4326).
Usage: python3 build_geojson.py <dir with lignes-vitesses.geojson & localites.geojson>
"""
import json, os, sys
from collections import defaultdict
from shapely.geometry import mapping, LineString, MultiLineString, Point
from shapely.ops import substring

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geojson")
os.makedirs(OUT, exist_ok=True)

feats = json.load(open(os.path.join(SRC, "lignes-vitesses.geojson")))["features"]
by_code = defaultdict(list)
for f in feats:
    by_code[f["properties"]["code_ligne"]].append(f)


def merged(codes):
    """Chain the speed segments of the given line codes, in kilometre-post order, into ONE
    continuous LineString (a single path animates cleanly with Trim Paths in Geolayers)."""
    chain, n = [], 0
    for c in codes:
        for f in sorted(by_code[c], key=lambda f: f["properties"]["pkd"]):
            pts = [tuple(xy[:2]) for xy in f["geometry"]["coordinates"]]
            if len(pts) < 2 or LineString(pts).length < 1e-6:
                continue
            if chain:
                d = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
                # the first segment may be stored backwards: flip it if that joins better
                if n == 1 and min(d(chain[0], pts[0]), d(chain[0], pts[-1])) < \
                        min(d(chain[-1], pts[0]), d(chain[-1], pts[-1])):
                    chain.reverse()
                if d(chain[-1], pts[-1]) < d(chain[-1], pts[0]):
                    pts = pts[::-1]
                if pts[0] == chain[-1]:
                    pts = pts[1:]
            chain.extend(pts)
            n += 1
    return LineString(chain)


def orient_from(g, lon, lat):
    """Make a single LineString start at the end nearest (lon, lat) so trim-path animates outward."""
    if isinstance(g, LineString):
        a, b = g.coords[0], g.coords[-1]
        if (a[0] - lon) ** 2 + (a[1] - lat) ** 2 > (b[0] - lon) ** 2 + (b[1] - lat) ** 2:
            g = LineString(list(g.coords)[::-1])
    return g


def write(name, items):
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": props, "geometry": mapping(geom)} for props, geom in items]}
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        json.dump(fc, fh, separators=(",", ":"))
    for props, geom in items:
        print(f"{name:45s} {geom.geom_type:16s} {geom.length * 111:7.0f} km(approx)  {props['name']}")


PARIS = (2.35, 48.85)

# Line 752000 runs Paris -> Lyon -> Marseille as one code. Split it geometrically at the Montanay
# junction north of Lyon, where the Lyon-St-Clair link (752330) leaves for Lyon itself.
sud_full = merged(["752000"])
montanay = sud_full.project(Point(4.877, 45.894))
sud_est = LineString(list(substring(sud_full, 0, montanay).coords) + list(merged(["752330"]).coords))
rhone_med = substring(sud_full, montanay, sud_full.length)

lines = [
    ("01_LGV_Sud-Est_Paris-Lyon_1981.geojson",
     {"name": "LGV Sud-Est (Paris - Lyon)", "opened": "1981 (Paris-Lyon full 1983)", "codes": "752000 + 752330 (Lyon-St-Clair)"},
     orient_from(sud_est, *PARIS)),
    ("02_LGV_Nord_Paris-Lille.geojson",
     {"name": "LGV Nord (Paris - Lille)", "opened": "1993", "codes": "226000"},
     orient_from(merged(["226000"]), *PARIS)),
    ("03_LGV_Atlantique+SEA_Paris-Tours-Bordeaux.geojson",
     {"name": "LGV Atlantique + LGV SEA (Paris - Tours - Bordeaux)", "opened": "1989-90 / 2017", "codes": "431000 + 566000"},
     orient_from(merged(["431000", "566000"]), *PARIS)),
    ("04_LGV_Est_Paris-Strasbourg.geojson",
     {"name": "LGV Est europeenne (Paris - Strasbourg)", "opened": "2007 / 2016", "codes": "005000"},
     orient_from(merged(["005000"]), *PARIS)),
    ("05_LGV_Rhone-Alpes+Mediterranee_Lyon-Marseille.geojson",
     {"name": "LGV Rhone-Alpes + LGV Mediterranee (Lyon - Valence - Marseille)", "opened": "1992-94 / 2001", "codes": "752000 south of Montanay junction"},
     orient_from(rhone_med, 4.9, 45.9)),
    ("06_LGV_Interconnexion_Est_Paris_bypass.geojson",
     {"name": "LGV Interconnexion Est (bypasses Paris: CDG - Marne-la-Vallee)", "opened": "1994", "codes": "226310"},
     orient_from(merged(["226310"]), 2.6, 49.06)),
    ("07_LGV_Rhin-Rhone_cross-country.geojson",
     {"name": "LGV Rhin-Rhone (Dijon - Mulhouse, province-to-province)", "opened": "2011", "codes": "014000"},
     orient_from(merged(["014000"]), 5.0, 47.3)),
    ("08_LGV_Bretagne-Pays-de-Loire_Le-Mans-Rennes.geojson",
     {"name": "LGV Bretagne-Pays de la Loire (Le Mans - Rennes)", "opened": "2017", "codes": "429000 + 408000"},
     orient_from(merged(["429000", "408000"]), 0.8, 48.0)),
    ("09_LGV_Nimes-Montpellier_bypass.geojson",
     {"name": "Contournement Nimes - Montpellier", "opened": "2018", "codes": "834000"},
     orient_from(merged(["834000"]), 4.4, 43.9)),
]
for fname, props, geom in lines:
    write(fname, [(props, geom)])
write("ALL_high-speed_lines_from_script.geojson", [(p, g) for _, p, g in lines])

# 19th-century classic radial lines (the "star" around Paris)
classic = [
    ("830000", "Paris-Lyon - Marseille (PLM)"), ("570000", "Paris-Austerlitz - Bordeaux"),
    ("272000", "Paris-Nord - Lille"), ("070000", "Noisy-le-Sec (Paris-Est) - Strasbourg"),
    ("001000", "Paris-Est - Mulhouse"), ("340000", "Paris-St-Lazare - Le Havre"),
    ("420000", "Paris-Montparnasse - Brest"), ("590000", "Les Aubrais (Orleans) - Montauban (POLT, Paris-Toulouse)"),
]
write("10_classic_19th-century_star_lines.geojson",
      [({"name": n, "codes": c}, orient_from(merged([c]), *PARIS).simplify(0.0005)) for c, n in classic])

# Whole French network, simplified (~100 m) for the opening "look at this map" shot
everything = MultiLineString([f["geometry"]["coordinates"] for f in feats
                               if len(f["geometry"]["coordinates"]) > 1]).simplify(0.001)
write("00_full_French_rail_network_simplified.geojson", [({"name": "Reseau ferre national (all lines)"}, everything)])

# City / station points
cities = {"Paris-Gare-de-Lyon": "Paris", "Lyon-Part-Dieu": "Lyon", "Lille-Flandres": "Lille",
          "Bordeaux-St-Jean": "Bordeaux", "Strasbourg-Ville": "Strasbourg", "Marseille-St-Charles": "Marseille",
          "Nantes": "Nantes", "Toulouse-Matabiau": "Toulouse", "Rennes": "Rennes", "Montpellier-St-Roch": "Montpellier",
          "Nice-Ville": "Nice", "Dijon-Ville": "Dijon", "Mulhouse-Ville": "Mulhouse", "Tours": "Tours",
          "Valence-TGV": "Valence TGV", "Roissy-Aéroport-CDG 2-TGV": "Paris-CDG (TGV)", "Marne-la-Vallée-Chessy": "Marne-la-Vallee (TGV)"}
loc = json.load(open(os.path.join(SRC, "localites.geojson")))["features"]
pts = []
for f in loc:
    lib = f["properties"]["libelle"]
    if lib in cities and f["geometry"]:
        pts.append({"type": "Feature", "properties": {"name": cities.pop(lib), "station": lib}, "geometry": f["geometry"]})
json.dump({"type": "FeatureCollection", "features": pts}, open(os.path.join(OUT, "11_city_points.geojson"), "w"))
print("points:", [p["properties"]["name"] for p in pts], "missing:", list(cities))
