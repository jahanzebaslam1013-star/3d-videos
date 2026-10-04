"""Geolayers-ready GeoJSON for the "Why did Paris become so massive?" short. WGS84 lon/lat.
Sources: Paris open data arrondissements (via github.com/fxjollois/cours-2017-2018), France/IDF boundaries
(github.com/gregoiredavid/france-geojson, from IGN/INSEE), Natural Earth 10m (rivers, urban areas, roads),
SNCF Reseau open data (rail lines, stations). Ile de la Cite / Ile Saint-Louis outlines are hand-drawn approximations."""
import json, os
import shapely
from shapely.geometry import shape, mapping, Polygon, LineString, MultiLineString, Point, box
from shapely.ops import unary_union, linemerge, substring

SRC = "/home/user/src"
RAIL = "/tmp/claude-0/-home-user-3d-videos/570c65c2-574e-5a7c-a66a-c655fdf9cb1f/scratchpad"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geojson")
load = lambda p: json.load(open(p))["features"]
ml = lambda g: g if g.geom_type == "LineString" else linemerge(g)
r4 = lambda g: json.loads(json.dumps(mapping(g)), parse_float=lambda x: round(float(x), 5))


def write(name, items):
    fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": p, "geometry": r4(g)} for p, g in items]}
    json.dump(fc, open(os.path.join(OUT, name), "w"), separators=(",", ":"))
    n = sum(shapely.get_num_coordinates(g) for _, g in items)
    print(f"{name:52s} {len(items):3d} features  ~{n} vertices  {os.path.getsize(os.path.join(OUT, name)) // 1024} KB")


# 01 - "a city built around a small island on the Seine"
cite = Polygon([(2.3396, 48.8577), (2.3420, 48.8581), (2.3455, 48.8574), (2.3482, 48.8566), (2.3510, 48.8557),
                (2.3526, 48.8542), (2.3535, 48.8526), (2.3521, 48.8519), (2.3495, 48.8524), (2.3470, 48.8530),
                (2.3445, 48.8541), (2.3424, 48.8553), (2.3405, 48.8567)])
st_louis = Polygon([(2.3543, 48.8526), (2.3570, 48.8531), (2.3596, 48.8522), (2.3613, 48.8508), (2.3601, 48.8500),
                    (2.3576, 48.8505), (2.3551, 48.8515)])
write("01_Ile_de_la_Cite_and_Ile_Saint-Louis.geojson",
      [({"name": "Ile de la Cite (approx.)"}, cite), ({"name": "Ile Saint-Louis (approx.)"}, st_louis)])

# 02 - The Seine: detailed through Paris (shared border of left/right-bank arrondissements) + regional course
arr = {f["properties"]["c_ar"]: shape(f["geometry"]) for f in load(f"{SRC}/fxj/analyse-donnees-massives/paris-arrondissements.geojson")}
right, left = unary_union([arr[i] for i in (1, 4, 8, 12, 16)]), unary_union([arr[i] for i in (5, 6, 7, 13, 15)])
seine_paris = right.boundary.intersection(left.buffer(1e-6))
if seine_paris.geom_type != "LineString":
    seine_paris = linemerge(seine_paris)
if seine_paris.geom_type == "MultiLineString":  # keep the long river course, drop slivers
    parts = sorted(seine_paris.geoms, key=lambda g: -g.length)
    seine_paris = linemerge(MultiLineString([p for p in parts if p.length > 0.002]))
seine_paris = seine_paris.simplify(0.00005)
if seine_paris.geom_type == "LineString" and seine_paris.coords[0][0] < seine_paris.coords[-1][0]:
    seine_paris = LineString(list(seine_paris.coords)[::-1])  # flow direction: east -> west
write("02a_Seine_through_Paris_detailed.geojson", [({"name": "La Seine (Paris)"}, seine_paris)])
rivers = load(f"{SRC}/natural-earth-vector/geojson/ne_10m_rivers_lake_centerlines.geojson")
seine = [shape(f["geometry"]) for f in rivers if f["properties"]["name"] == "Seine"][0]
marne = [shape(f["geometry"]) for f in rivers if f["properties"]["name"] == "Marne"][0]
write("02b_Seine_regional_Troyes-Paris-Le_Havre.geojson",
      [({"name": "La Seine"}, ml(seine).simplify(0.002)), ({"name": "La Marne"}, ml(marne).simplify(0.002))])

# 03 - "trade between several regions in northern France" + "the whole of France"
regions = {f["properties"]["nom"]: shape(f["geometry"]) for f in load(f"{SRC}/france-geojson/regions.geojson")}
north = ["Île-de-France", "Hauts-de-France", "Normandie", "Grand Est", "Centre-Val de Loire", "Bourgogne-Franche-Comté"]
write("03a_northern_France_regions.geojson", [({"name": n}, regions[n].simplify(0.005)) for n in north])
write("03b_France_outline.geojson", [({"name": "France"}, shape(json.load(open(f"{SRC}/france-geojson/metropole.geojson"))["geometry"]).simplify(0.01))])

# 04 - "railways organised around the capital" / "massive train stations"
termini = {"Paris-Nord": "Gare du Nord", "Paris-Est": "Gare de l'Est", "Paris-Gare-de-Lyon": "Gare de Lyon",
           "Paris-Austerlitz": "Gare d'Austerlitz", "Paris-Montparnasse": "Gare Montparnasse", "Paris-St-Lazare": "Gare Saint-Lazare"}
gares = [({"name": termini[f["properties"]["libelle"]]}, shape(f["geometry"]))
         for f in load(f"{RAIL}/localites.geojson") if f["properties"]["libelle"] in termini]
write("04a_Paris_great_train_stations.geojson", gares)
rail = load(f"{RAIL}/lignes-vitesses.geojson")
def line(code):
    segs = sorted([f for f in rail if f["properties"]["code_ligne"] == code], key=lambda f: f["properties"]["pkd"])
    chain = []
    for f in segs:
        pts = [tuple(c[:2]) for c in f["geometry"]["coordinates"]]
        if len(pts) < 2: continue
        if chain:
            d = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            if d(chain[-1], pts[-1]) < d(chain[-1], pts[0]): pts = pts[::-1]
        chain += pts
    return LineString(chain)
star = [("Gare du Nord", "272000", "Paris - Lille"), ("Gare de l'Est", "070000", "Paris - Strasbourg"),
        ("Gare de l'Est", "001000", "Paris - Mulhouse"), ("Gare de Lyon", "830000", "Paris - Lyon - Marseille"),
        ("Gare d'Austerlitz", "570000", "Paris - Bordeaux"), ("Gare Montparnasse", "420000", "Paris - Brest"),
        ("Gare Saint-Lazare", "340000", "Paris - Le Havre")]
gp = {p["name"]: g for p, g in gares}
items = []
for gare, code, name in star:
    l = line(code); s = gp[gare]
    if Point(l.coords[-1]).distance(s) < Point(l.coords[0]).distance(s): l = LineString(list(l.coords)[::-1])
    items.append(({"name": name, "from": gare}, LineString([(s.x, s.y)] + list(l.coords)).simplify(0.006)))
write("04b_railway_star_from_Paris_stations_CLEAN.geojson", items)

# 05 - "Paris spilling over its own borders" (+ approximate pre-1860 Paris = arrondissements 1-11)
idf_dep = {f["properties"]["code"]: (f["properties"]["nom"], shape(f["geometry"])) for f in load(f"{SRC}/france-geojson/regions/ile-de-france/departements-ile-de-france.geojson")}
paris = idf_dep["75"][1]
write("05a_Paris_city_limits_intra-muros.geojson", [({"name": "Paris intra-muros"}, paris.simplify(0.0003))])
write("05b_old_Paris_before_1860_approx.geojson",
      [({"name": "Paris before 1860 (approx. = arrondissements 1-11)"}, unary_union([arr[i] for i in range(1, 12)]).buffer(0.0002).buffer(-0.0002).simplify(0.0003))])
write("05c_Paris_20_arrondissements.geojson",
      [({"name": f"{i}e arrondissement", "num": i}, arr[i].simplify(0.0002)) for i in sorted(arr)])

# 06 - "an entire suburban area developed around the capital"
write("06a_inner_suburbs_petite_couronne.geojson", [({"name": idf_dep[c][0], "code": c}, idf_dep[c][1].simplify(0.001)) for c in ("92", "93", "94")])
write("06b_outer_suburbs_grande_couronne.geojson", [({"name": idf_dep[c][0], "code": c}, idf_dep[c][1].simplify(0.002)) for c in ("77", "78", "91", "95")])
write("06c_Ile-de-France_region.geojson", [({"name": "Ile-de-France"}, regions["Île-de-France"].simplify(0.002))])
communes = load(f"{SRC}/france-geojson/regions/ile-de-france/communes-ile-de-france.geojson")
pc = [({"name": f["properties"]["nom"], "code": f["properties"]["code"]}, shape(f["geometry"]).simplify(0.0005))
      for f in communes if f["properties"]["code"][:2] in ("92", "93", "94")]
write("06d_inner_suburb_towns_communes.geojson", pc)

# 07 - "after WWII, new towns, highways, RER lines"
centroid = {f["properties"]["nom"]: shape(f["geometry"]).centroid for f in communes}
villes = [("Cergy-Pontoise", "Cergy"), ("Evry", "Évry"), ("Marne-la-Vallee", "Noisiel"),
          ("Saint-Quentin-en-Yvelines", "Montigny-le-Bretonneux"), ("Senart", "Lieusaint")]
write("07a_new_towns_villes_nouvelles.geojson", [({"name": n}, centroid[c]) for n, c in villes if c in centroid])
roads = load(f"{SRC}/natural-earth-vector/geojson/ne_10m_roads.geojson")
idf = regions["Île-de-France"].buffer(0.05)
hw = [({"name": f["properties"].get("label") or f["properties"].get("type"), "type": f["properties"]["type"]},
       shape(f["geometry"]).intersection(idf).simplify(0.002))
      for f in roads if f["properties"]["type"] in ("Major Highway", "Secondary Highway") and shape(f["geometry"]).intersects(idf)]
write("07b_highways_around_Paris.geojson", [(p, g) for p, g in hw if not g.is_empty])
idf_rail = MultiLineString([f["geometry"]["coordinates"] for f in rail if len(f["geometry"]["coordinates"]) > 1]).intersection(regions["Île-de-France"])
write("07c_suburban_rail_RER-Transilien_Ile-de-France.geojson", [({"name": "Rail network Ile-de-France (RER/Transilien tracks)"}, ml(idf_rail).simplify(0.0008))])

# 08 - "a huge urban area home to several million people"
urban = [shape(f["geometry"]) for f in load(f"{SRC}/natural-earth-vector/geojson/ne_10m_urban_areas.geojson")
         if shape(f["geometry"]).intersects(Point(2.35, 48.86))][0]
write("08_Paris_urban_area_built-up.geojson", [({"name": "Paris urban area (built-up, ~3,100 km2)"}, urban.simplify(0.002))])

# 09 - Labels
write("09_points_Paris_Le_Havre_Rouen.geojson", [({"name": "Paris"}, Point(2.3488, 48.8534)), ({"name": "Rouen"}, Point(1.0993, 49.4431)),
      ({"name": "Le Havre"}, Point(0.1079, 49.4944)), ({"name": "Notre-Dame"}, Point(2.3499, 48.8530))])
