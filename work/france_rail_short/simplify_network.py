"""Cut vertices of the full-network GeoJSON ~80% while keeping the Paris area detailed.
Inside ~R_IN km of Paris: light simplification. Further out: tolerance grows with distance,
and tiny stubs (sidings, short links) far from Paris are dropped."""
import json, sys
from shapely.geometry import shape, LineString, MultiLineString, Point, mapping
from shapely.ops import linemerge
from shapely import affinity

src, dst, far_tol, STUB = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
PARIS = Point(2.35, 48.85)
# ellipse in lon/lat so the zone is ~round on the ground (1 deg lon ~ 73 km here, 1 deg lat ~ 111 km)
zone_in = affinity.scale(PARIS.buffer(1), 70 / 73, 70 / 111)    # ~70 km: keep detail
zone_mid = affinity.scale(PARIS.buffer(1), 180 / 73, 180 / 111)  # ~180 km: medium

g = shape(json.load(open(src))["features"][0]["geometry"])
lines = list(g.geoms) if g.geom_type == "MultiLineString" else [g]
n0 = sum(len(l.coords) for l in lines)
m = linemerge(MultiLineString(lines))
m = list(m.geoms) if m.geom_type == "MultiLineString" else [m]

def parts(geom):
    if geom.is_empty: return []
    if geom.geom_type == "LineString": return [geom]
    return [p for p in getattr(geom, "geoms", []) if p.geom_type == "LineString"]

out = []
for l in m:
    for p in parts(l.intersection(zone_in)):
        out.append(p.simplify(0.0003))
    for p in parts(l.intersection(zone_mid).difference(zone_in)):
        out.append(p.simplify(far_tol / 2))
    for p in parts(l.difference(zone_mid)):
        if p.length < STUB:  # short stub far from Paris
            continue
        out.append(p.simplify(far_tol))
out = linemerge(MultiLineString([o for o in out if len(o.coords) > 1]))
out = list(out.geoms) if out.geom_type == "MultiLineString" else [out]
n1 = sum(len(l.coords) for l in out)
print(f"vertices {n0} -> {n1} ({n1 / n0 * 100:.1f}% kept), lines {len(lines)} -> {len(out)}")
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature",
           "properties": {"name": "Reseau ferre national (light, detailed around Paris)"},
           "geometry": mapping(MultiLineString(out))}]},
          open(dst, "w"), separators=(",", ":"))
