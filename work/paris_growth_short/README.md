# Paris growth short — Geolayers 3 data
Script: `TRANSCRIPTS.md`. Preview of every layer: `preview_paris_growth.png`. All GeoJSON, WGS84, light (largest file 76 KB).

| Script moment | File(s) |
|---|---|
| "a city built around a small island on the Seine" | `01_Ile_de_la_Cite_and_Ile_Saint-Louis` (hand-drawn, approximate), `02a_Seine_through_Paris_detailed`, `09_points` (Notre-Dame) |
| "a metropolis of over 10 million people" | `08_Paris_urban_area_built-up` |
| "its location… the Seine allowed transport of goods" | `02b_Seine_regional_Troyes-Paris-Le_Havre` (Seine + Marne), `09_points` (Paris, Rouen, Le Havre) |
| "trade between several regions in northern France" | `03a_northern_France_regions` (6 regions), `03b_France_outline` |
| "political heart of the kingdom… administration, universities, jobs" | `05a_Paris_city_limits_intra-muros`, `05c_Paris_20_arrondissements` (pulse/glow on centre) |
| "railways organized around the capital… massive train stations" | `04b_railway_star_from_Paris_stations_CLEAN` (7 lines, each starts at its station), `04a_Paris_great_train_stations` (6 termini) |
| "spilling over its own borders… old outlying towns grew" | `05b_old_Paris_before_1860_approx` → `05a_Paris_city_limits`, then `06d_inner_suburb_towns_communes` (123 towns) |
| "an entire suburban area developed around the capital" | `06a_inner_suburbs_petite_couronne` (92/93/94), `06b_outer_suburbs_grande_couronne` (77/78/91/95), `06c_Ile-de-France_region` |
| "new towns, highways, RER lines" | `07a_new_towns_villes_nouvelles` (5 points), `07b_highways_around_Paris`, `07c_suburban_rail_RER-Transilien_Ile-de-France` |
| "City of Paris is a tiny fraction… huge urban area" | `05a_Paris_city_limits` vs `08_Paris_urban_area_built-up` (best visual contrast) |
| "the whole of France has been organized around it" | `03b_France_outline` + `04b_railway_star…` |

Notes: "pre-1860 Paris" uses arrondissements 1–11 as a stand-in for the city before the 1860 annexation; island outlines are approximate;
highways and urban area come from Natural Earth (simplified, good at region zoom, not street-level). RER tracks are the SNCF-run network in Île-de-France.

Sources: Ville de Paris open data (arrondissements), IGN/INSEE via github.com/gregoiredavid/france-geojson, Natural Earth (public domain),
SNCF Réseau open data (ODbL). Rebuild with `python3 build_geojson.py`.
