# Harinaam temple screens — API 2.1

All paths below are relative to the API hosting root. Existing IDs and data branches remain available. Load `travel/discovery.json` for screen copy and configuration, `travel/index.json` for the complete filterable catalogue, and the selected card's `detail_path` for its detail. The same discovery object is embedded in `travel.json`. Detail paths below start at `temple.details.ui` in individual endpoints.

| Supplied design | API fields |
|---|---|
| API loading state | discovery `states.loading`, `search.placeholder`, `title`; bundle these locally for the first request |
| Discovery | discovery `hero`, `categories`, `featured`, `popular`, `footer`; resolve ordered temple IDs against index `items[].card` |
| Location and category filters | discovery `locations`, `categories`, `additional_deities`, `filters` |
| Temple overview | temple `card`; UI `name_hi`, `header_title`, `overview.facts`, `overview.paragraphs`, `actions` |
| Significance and heritage | UI `significance`, `history.items`, `architecture.body`, `architecture.features`, `architecture.image` |
| Darshan and traditions | UI `darshan.hours`, `darshan.schedule`, `rituals.items`, `festivals.items`, `gallery.items` |
| Plan your visit | UI `how_to_reach.items`, `location`, `before_visit.items`, `guidelines.items`, `actions.maps` |
| Continue the journey | UI `nearby.items`, `related.items`; discovery `journey` |

## Rendering rules

Every temple has every section key. Render the section's empty message (or a general not-yet-verified label) when content is unavailable. Do not invent histories, translate names automatically as authoritative names, infer opening hours, turn unknown facilities into false, or show a fabricated image. `name_hi` is nullable. Kashi has researched history, architecture, schedules, ritual links, festivals and transport points; the rest retain existing research and honest empty states where more editorial work is needed. This is full screen-field coverage, not complete research for every temple.

Use the structured fact values and their fallback strings. Times are temple-local 24-hour values; format them for the UI. Overall hours are not continuous general darshan. Show the timing notice and source link. Never derive “open now” without holiday and special-event rules. The supplied SVG's sample aarti times, travel distances, season and festival tiles are not authoritative data. Kashi uses the official FAQ's schedule; no unverified road distance or October–March recommendation has been copied.

Render an image only with its credit, source, licence and changes. Gallery count is the actual array length; do not duplicate one photo into three fake views. The hero currently uses Kashi's attributed catalogue image, not the design's unlicensed Ganga artwork. A null map preview requires the app's map component or a clearly labelled placeholder. Coordinates are reference points, not entrance positions.

Nearby means same country, region and locality. Distance is approximate great-circle distance between reference coordinates, not a walk/drive distance. Show “Approx. straight-line” and hide the distance when null. Related results share a collection or deity, with shared collections prioritised; they are editorial suggestions, not personal recommendations. Popular and featured are curated lists, not analytics or Google ratings. Shakti Peeth currently contains a selected sourced Kamakhya entry and explicitly does not claim complete coverage.

## Filters and actions

Use OR among selected countries/regions, OR among selected deities, OR among selected circuits, and AND across these groups and search. Region keys must include country code. Empty groups do not restrict results. Use category `temple_ids` as the authoritative membership list; additional deities match index `deity_ids`. All clears deity/circuit choices; Reset clears all selections and search. Normalize search text and keywords with Unicode NFKC and case folding. Compute selected and result counts in the app. Filter the complete index before paginating results; static JSON URLs do not implement query parameters.

Back, close, keyboard, skeleton animation, selection state, gallery paging, text expansion and native sharing are app behavior. Save favorites on the device/account using the stable temple ID. Device time, signal and battery in the SVG remain operating-system UI. `journey.items[].route_key` must be mapped to existing app screens; hide unsupported routes. These are symbolic route keys, not assumed working deep links. No personal state belongs in this public catalogue.

Run `python tools/travel/build.py` then `python tools/travel/validate.py`. Edit `tools/travel/ui.py` for screen presentation and source-backed enrichments; generated files are overwritten on rebuild. Use the main schema plus semantic UI validator. No Android client implementation or device verification is included in this repository change.
