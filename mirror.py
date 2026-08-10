from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}mirror <teks>", "Balik teks jadi upside-down (unicode flip)", "Fun")

FLIP_MAP = {
    "a": "ɐ", "b": "q", "c": "ɔ", "d": "p", "e": "ǝ", "f": "ɟ", "g": "ƃ",
    "h": "ɥ", "i": "ᴉ", "j": "ɾ", "k": "ʞ", "l": "l", "m": "ɯ", "n": "u",
    "o": "o", "p": "d", "q": "b", "r": "ɹ", "s": "s", "t": "ʇ", "u": "n",
    "v": "ʌ", "w": "ʍ", "x": "x", "y": "ʎ", "z": "z",
    "A": "∀", "B": "𐐒", "C": "Ɔ", "D": "◖", "E": "Ǝ", "F": "Ⅎ", "G": "⅁",
    "H": "H", "I": "I", "J": "ſ", "K": "Ʞ", "L": "⅂", "M": "W", "N": "N",
    "O": "O", "P": "Ԁ", "Q": "Ό", "R": "ᴚ", "S": "S", "T": "⊥", "U": "∩",
    "V": "Λ", "W": "M", "X": "X", "Y": "⅄", "Z": "Z",
    "0": "0", "1": "Ɩ", "2": "ᄅ", "3": "Ɛ", "4": "ㄣ", "5": "ϛ", "6": "9",
    "7": "ㄥ", "8": "8", "9": "6",
    ".": "˙", ",": "'", "'": ",", '"': ",,", "?": "¿", "!": "¡",
    "(": ")", ")": "(", "[": "]", "]": "[", "<": ">", ">": "<",
}


def _mirror(text):
    return "".join(FLIP_MAP.get(ch, ch) for ch in text)[::-1]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}mirror (.+)$"))
async def mirror_handler(event):
    text = event.pattern_match.group(1)
    result = _mirror(text)
    await event.edit(f"🙃 {result}")
