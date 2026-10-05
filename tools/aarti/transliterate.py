"""Deterministic Devanagari-to-IAST spelling, not an English translation.

Preserves Sanskrit vowels and Hindi/Awadhi orthography (no guessed schwa deletion).
The API's historical `english` key contains Roman lyrics.
"""
import unicodedata

CONSONANTS = dict(zip('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ',
    ['k','kh','g','gh','ṅ','c','ch','j','jh','ñ','ṭ','ṭh','ḍ','ḍh','ṇ',
     't','th','d','dh','n','p','ph','b','bh','m','y','r','l','v','ś','ṣ','s','h','ḷ']))
VOWELS = dict(zip('अआइईउऊऋॠऌॡएऐओऔ',
    ['a','ā','i','ī','u','ū','ṛ','ṝ','ḷ','ḹ','e','ai','o','au']))
SIGNS = dict(zip('ािीुूृॄॢॣेैोौ',
    ['ā','i','ī','u','ū','ṛ','ṝ','ḷ','ḹ','e','ai','o','au']))
OTHER = {'ं':'ṃ','ँ':'m̐','ः':'ḥ','ऽ':"'",'ॐ':'oṃ','।':'.','॥':'||',
    **dict(zip('०१२३४५६७८९','0123456789'))}
NUKTA = {'क':'q','ख':'kh','ग':'ġ','ज':'z','ड':'ṛ','ढ':'ṛh','फ':'f','य':'y'}

def romanize(text):
    text = unicodedata.normalize('NFD', text)
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch in CONSONANTS:
            value = CONSONANTS[ch]
            i += 1
            if i < len(text) and text[i] == '़':
                value = NUKTA.get(ch, value)
                i += 1
            if i < len(text) and text[i] == '्':
                i += 1
            elif i < len(text) and text[i] in SIGNS:
                value += SIGNS[text[i]]
                i += 1
            else:
                value += 'a'
            out.append(value)
            continue
        out.append(VOWELS.get(ch, OTHER.get(ch, '' if ch in '़्\u200c\u200d' else ch)))
        i += 1
    return unicodedata.normalize('NFC', ''.join(out))
