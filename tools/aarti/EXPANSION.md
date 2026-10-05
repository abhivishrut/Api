# Aarti expansion and popularity order — 2026-10-05

The requested expansion retains all 85 previously reviewed items and adds exactly 20 distinct items (IDs 97–116). The API now contains **105 items**, version **1.5**. All existing IDs and existing item payloads are preserved; only their array positions change.

The full `Aarti` array is ordered by an **editorial estimate of general familiarity and worship use**, from more familiar to more specialised. This is not a measured national popularity chart: no streaming counts, survey, or app usage analytics were available. The estimate favours the audience of this predominantly Hindi devotional collection while also placing widely used Marathi and Sanskrit works appropriately. Regional audiences can reasonably prefer a different order.

The opening items are Hanuman Chalisa, Om Jai Jagdish Hare, Gayatri Mantra, Maha Mrityunjaya Mantra, Om Namah Shivaya, Ganesh Aarti, Jai Ambe Gauri, Shiv Aarti, Lakshmi Aarti, and Hare Krishna Mahamantra.

## The 20 additions

| ID | Item | Text reference |
|---|---|---|
| 97 | Om Namah Shivaya | [Text reference](https://www.drikpanchang.com/vedic-mantra/gods/lord-shiva/yantra/diagram/shiva-panchakshari-yantra.html?lang=hi) |
| 98 | Om Namo Bhagavate Vasudevaya | [Text reference](https://www.swaminarayan.faith/media/3912/purvardh-dasham-skandha-bhumanand-chopai-resize.pdf) |
| 99 | Om Gam Ganapataye Namah | [Text reference](https://www.drikpanchang.com/puja-vidhi/homa/ganapati-homa/ganapati-homa-vidhi.html) |
| 100 | Sukhkarta Dukhharta | [Text reference](https://www.drikpanchang.com/marathi/lyrics/aarti/gods/shri-ganesha/ganapati-sukhakarta-dukhaharta-aarti.html?ck=1&lang=mr) |
| 101 | Shendur Lal Chadhayo | [Text reference](https://dharmkosh.in/aarti/ganesh/shendur-lal-chadhayo) |
| 102 | Bajrang Baan | [Text reference](https://www.bhaktibharat.com/bhajan/bajrang-baan-paath) |
| 103 | Damodar Ashtakam | [Text reference](https://www.srimadbhagavatam.org/music/text/damodarastaka.html) |
| 104 | Durga Saptashloki | [Text reference](https://www.drikpanchang.com/lyrics/durga-saptashati/saptashloki-durga/shri-saptashloki-durga.html) |
| 105 | Shri Ram Ashtakam | [Text reference](https://sanskritdocuments.org/doc_raama/raamaashhTaka3.html) |
| 106 | Saha Navavatu | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 107 | Shri Krishna Chalisa | [Text reference](https://www.drikpanchang.com/lyrics/chalisa/lord-krishna/shree-krishna-chalisa.html?ck=1&lang=hi) |
| 108 | Asato Ma Sadgamaya | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 109 | Sarve Bhavantu Sukhinah | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 110 | Purnamadah Purnamidam | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 111 | Shanti Path (Om Dyauh Shantih) | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 112 | Brahmarpanam (Bhojan Mantra) | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 113 | Karagre Vasate Lakshmi | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 114 | Samudra Vasane Devi | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |
| 115 | Gajananam Bhuta Ganadi Sevitam | [Text reference](https://www.ganeshchalisa.com/ganesh-vandana-hindi/) |
| 116 | Shantakaram Bhujagashayanam | [Text reference](https://sanskritdocuments.org/doc_z_misc_general/DAILY_PRAYERS04.pdf) |

## Text scope and checks

- The additions include short, established daily prayers as complete named items, not invented extended verses. Brahmarpanam is Bhagavad Gita 4.24; Shantakaram is the independent Vishnu dhyana prayer (also part of the existing Sahasranamam invocation). These are intentional separately named prayers, not duplicate complete catalog entries.
- Sukhkarta Dukhharta contains all three stanzas and repeated refrain, with language Marathi. Its Devanagari text uses the existing API key `hindi` for compatibility.
- Bajrang Baan uses a commonly recited 35-couplet version plus opening and closing dohas. Traditional editions differ in wording; the source's obvious `ह्नीं` transcription is normalised to `ह्रीं`, and a missing closing double danda is repaired.
- Krishna Chalisa includes 40 chaupai couplets and its dohas. Damodar Ashtakam contains all eight verses, Durga Saptashloki all seven plus its invocation, and Ram Ashtakam eight plus phalashruti.
- Krishna Chalisa's opening dohas are cross-checked against [Kavita Kosh](https://kavitakosh.org/kk/श्री_कृष्ण_चालीसा_/_चालीसा) and [Adiveda](https://adiveda.in/reading/chalisa/krishna-chalisa/): the Drik page has omitted lines and an unrelated “रवि तनय” line. The restored opening uses “नयन कमल अभिराम” and “पूर्ण इन्दु अरविन्द मुख”; “मसूर धार” is corrected to the attested “मूसर धार”.
- Damodar Ashtakam uses the traditional “नमामीश्वरं” version; comparison of the Devanagari and Roman sources corrects transcription defects in “बिम्बरक्ताधरं”, “वरेशादपीह” and “स्वकां”.
- Every new entry includes matching IAST Roman lyrics in `english`. No English translations or modern explanatory prose were imported.
- New recording URLs and durations remain empty because no recording has been supplied. Deity images are reused where a matching existing image exists; Bhumi Devi has no invented or mismatched image.
- Validation checks the exact 105-item ID set, unique IDs/names/complete texts, API fields, metadata count, bilingual parity, verse completeness anchors, the new chalisa/couplet counts, and source debris.
