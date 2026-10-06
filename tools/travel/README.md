# UI update: version 2.1

The eight supplied Harinaam screens are supported through `travel/discovery.json`, index cards, and each temple's `details.ui`. See [UI-CONTRACT.md](UI-CONTRACT.md) for the full screen mapping, client behavior and missing-data rules. Existing IDs and version 2 data fields remain available.

# Hindu temple travel API, version 2

`travel.json` is a static JSON catalogue. This update replaces the former mixed,
unreviewed feed with a curated India and international catalogue. It is **not an
exhaustive census of all famous or local Hindu temples** and is not a live Google
Places service. See `report.json` for generated coverage counts.

## Read the API

All paths below are relative to the repository/hosting root, not to the current
JSON file. Keep the existing static hosting base URL; no backend or API key is
required to read these files.

| File | Purpose |
| --- | --- |
| `travel.json` | Full catalogue; India in `states[].temples`, overseas records in `international_temples` |
| `travel.schema.json` | JSON Schema Draft 2020-12 contract; usable with standard validators |
| `travel/index.json` | Searchable summaries, country/region indexes, deity filters and collections |
| `travel/pages/001.json` | First page of 24 summaries; follow `next` until it is `null` |
| `travel/temples/{id}.json` | One full temple record in `temple` |
| `travel/assets/temple-placeholder.svg` | Generic illustration for missing/failed images; never a destination photograph |

Countries contain region names and temple IDs, so India and overseas entries are
not duplicated. `state_name` is retained for compatibility, but represents a
first-level region outside India. India-only clients can keep their existing
`states → temples → details` traversal. International clients must also consume
`international_temples`, or use the index and detail endpoints.

Filter the index by `country_code`, `state_name`, `deity_ids`, or `collection_ids`.
Search `name`, `city`, and `search_keywords`; deity aliases include Hindi and
common English spellings. These are client-side operations: adding `?deity=shiva`
to a static JSON URL does not perform server-side filtering. Pagination is a
generated snapshot, not a live cursor. Do not assume its ordering is popularity.

IDs are pinned in `ids.json`, keyed by country plus reference identity. Display
name or locality edits keep the ID. If a reference article is renamed, migrate
its registry key while retaining the value. Never reuse an ID for another place.

## Important migration changes

- Version 2 retains the old nesting and field names, including `denotes_to`, but
  does **not** promise identical field types or record counts. Make nullable
  fields safe in the app before deploying this feed.
- `opening_time`, `closing_time`, coordinates, district and facility values can
  be `null`. This means unknown/unverified, not closed, absent, false, free or
  `(0,0)`. Use nullable booleans/numbers in app models.
- Use `details.visiting.hours` for split opening sessions and local time zones.
  A single opening/closing pair cannot represent lunch closures or seasonality.
- Use `deity_ids` for filtering. `denotes_to` is a display label, not an enum.
- Places with similar names remain separate; e.g. Ayodhya/Nainital Hanuman Garhi
  or Mumbai/Siddhatek Siddhivinayak must never be deduplicated by name alone.
- The original file contained churches, Jain/Buddhist/Sikh sites, duplicate
  records, mislabelled deities, mismatched photos and locality names presented
  as states. Its 778 records are preserved byte-for-byte in
  `legacy.travel.json.gz`. `migration.json` accounts for every original entry.
  Unmatched records are a review backlog, **not a declaration that they are
  invalid or non-Hindu**. Many smaller Hindu shrines still need migration.
- Existing saved favourites based on a name or list position require a migration
  decision. Only `matched_name_and_region` mappings are supplied automatically;
  do not silently discard unmatched favourites.

## What has and has not been verified

The editorial descriptions are short, temple-specific summaries. `sources`
distinguishes primary institution search/page evidence from automated encyclopedia
retrieval. The latter supplies reference coordinates and named infobox facts;
retrieving a page is not a full fact-check. `data_quality.editorial` therefore
continues to request a complete content review. Religious narratives are described
as traditions, not established historical or medical facts.

Coordinates are approximate article reference points in WGS84, not surveyed
entrances. Some sources describe a locality or complex rather than one sanctum;
those are marked `locality_reference_only`. Missing positions remain null.
Country bounds and paired coordinates are checked automatically; this does not
replace checking the pin against an authoritative map.

Google Maps research did not load through the available research interface.
Every record instead has a documented Maps search URL and directions URL using
its name, locality, region and country. No Place IDs, Google ratings, review
counts, live opening status, travel distances or Google photos are fabricated.
The user should confirm the result before navigating. Site access, operating
hours, prices, festivals, reservations and eligibility can change; do not label
an entry open-now using this catalogue.

Festival and architecture text marked `reference_extracted` comes from a saved
reference infobox. Festival dates are not projected into the Gregorian calendar.
The eight pilgrimage collections have exact membership/count checks. Regional
Jyotirlinga identifications and differing Shakti Peetha lists are not treated as
one universally settled list. The Devi filter is deliberately broader than a
claim to enumerate all Shakti Peethas or all forms of Mata.

## Photos and presentation

Do not reuse the original gallery without review. Lead photos are associated
with an identified reference article and have an explicit Commons author and
CC BY/CC BY-SA licence. A license parser is not a visual identity check, and the
media object states that limitation. Render the supplied attribution and licence
link with the image. Respect ShareAlike when distributing an adapted image.
Missing or unsupported licences cause omission, not an assumed reuse right.
Images from broader locality articles are withheld to avoid misleading cards.

`thumbnail` and `gallery` are legacy convenience fields. New clients should use
`media.items` for the photo, author, source page, licence, alt text and changes.
Use the bundled generic illustration if the remote image is absent or fails.
The API does not download or republish the original photographs.

## Maintain and validate

From the repository root:

```text
python tools/travel/build.py
python tools/travel/validate.py
```

The build is offline and uses `catalogue.tsv`, `references.json`,
`primary_sources.json` and the ID registry. It rebuilds the full JSON, search
index, pages, per-temple details, migration map and counts. Rebuilding must not
change the archive. Source refresh is a separate network operation:

```text
python tools/travel/research.py
python tools/travel/check_images.py
```

The refresh caches successfully retrieved records. For an intentional refresh,
remove only the desired cached reference entries, then rerun it. Failed fetches
are explicitly retained as unavailable. Add an independently checked primary
source for a temple with no encyclopedia article. A URL in `primary_sources.json`
means selected facts were inspected, not that every operational detail was checked.

Before publishing, run validation and review the generated diff. The validation
checks IDs, primary relationships, source presence, coordinates, map URL encoding,
licence requirements, complete circuits, page coverage, detail-file consistency,
and archive integrity. It does not verify every remote link or current visitor
arrangement. No Android client build, device check or remote deployment is included.

To restore the exact original without overwriting the new feed, decompress
`legacy.travel.json.gz` to a separate file and verify its SHA-256 against
`migration.json`. Do not serve that archive as reviewed travel advice.
