# France rail short — Geolayers 3 data

Lines for the "Why do all French trains go through Paris?" short. Script: see `TRANSCRIPTS.md`.
Preview of every file: `preview_map.png`.

All files are GeoJSON, WGS84 (EPSG:4326). Each line is ONE continuous `LineString`, oriented so the path
**starts at Paris** (or at the obvious origin), so Trim Paths "End 0 → 100%" draws it outward.

| File | Script moment | What it is |
|---|---|---|
| `00_full_French_rail_network_simplified.geojson` | "Take a look at this map of the French rail network" | Entire national network (~100 m simplification) — background layer |
| `10_classic_19th-century_star_lines.geojson` | "19th century… star-like shape around Paris" | 8 historic main lines from Paris: Lyon–Marseille (PLM), Bordeaux, Lille, Strasbourg, Mulhouse, Le Havre, Brest, Orléans–Toulouse (POLT) |
| `01_LGV_Sud-Est_Paris-Lyon_1981.geojson` | "In 1981, the first high-speed line connected Paris to Lyon" | LGV Sud-Est + Lyon-St-Clair link into Lyon |
| `02_LGV_Nord_Paris-Lille.geojson` | "…Lille" | LGV Nord (1993) |
| `03_LGV_Atlantique+SEA_Paris-Tours-Bordeaux.geojson` | "…Bordeaux" | LGV Atlantique (1989) + LGV SEA Tours–Bordeaux (2017) |
| `04_LGV_Est_Paris-Strasbourg.geojson` | "…Strasbourg" | LGV Est européenne (2007/2016) |
| `05_LGV_Rhone-Alpes+Mediterranee_Lyon-Marseille.geojson` | "…Marseille" | LGV Rhône-Alpes + LGV Méditerranée (continues from line 01) |
| `ALL_high-speed_lines_from_script.geojson` | "The high-speed lines radiate out from the capital" | All high-speed lines in one file |
| `06_LGV_Interconnexion_Est_Paris_bypass.geojson` | "Lines already allow you to bypass Paris" | Interconnexion Est (CDG – Marne-la-Vallée), lets TGVs skip central Paris |
| `07_LGV_Rhin-Rhone_cross-country.geojson` | "…improve connections between regions" | LGV Rhin-Rhône (Dijon – Mulhouse), a province-to-province line |
| `08_LGV_Bretagne-Pays-de-Loire_Le-Mans-Rennes.geojson` | optional | LGV BPL extension towards Rennes |
| `09_LGV_Nimes-Montpellier_bypass.geojson` | optional | Contournement Nîmes–Montpellier |
| `11_city_points.geojson` | labels/pins | Main stations: Paris, Lyon, Lille, Bordeaux, Strasbourg, Marseille, Nantes, Toulouse, Rennes, … |

## In After Effects / Geolayers 3
1. Create a map comp centred on France (Geolayers panel → new map).
2. Drag a `.geojson` into the Geolayers **Data** / **Features** import (or Project panel), select the map comp, then use
   **Draw Features** → it builds shape layers locked to the map.
3. On each line's shape layer add Trim Paths and keyframe End 0 → 100% to animate the route.
4. Tip: "Paris → Lyon → Marseille" = file 01 then 05 back-to-back; "Bordeaux → Paris → Lyon" (the detour joke) = 03 reversed + 01.

Note: high-speed lines physically start in the Paris suburbs (e.g. LGV Sud-Est at Combs-la-Ville), not at the stations —
that is accurate; use the classic-line file if you want the line to reach the station in central Paris.

## Source & licence
SNCF Réseau open data (lignes / vitesses, gares), ODbL — via
https://github.com/nicolaswurtz/extras-opendata-sncf-reseau. Credit on screen if required: "Données © SNCF Réseau, ODbL".
Rebuild: `python3 build_geojson.py <folder with lignes-vitesses.geojson and localites.geojson>` (needs `shapely`).
