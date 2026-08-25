# Canonical Parsha names, in Torah reading order, with common alternate
# transliterations mapped to them. Add new aliases here as they come up.

PARSHIYOT = [
    ("Bereishit", ["bereishit", "bereshit", "bereisheit", "beresheet", "bereishis", "bereisheis"]),
    ("Noach", ["noach", "noah", "noiach"]),
    ("Lech Lecha", ["lech lecha", "lech-lecha", "lekh lekha"]),
    ("Vayera", ["vayera", "vayeira"]),
    ("Chayei Sarah", ["chayei sarah", "chayei sara", "hayei sarah", "hayye sarah"]),
    ("Toldot", ["toldot", "toledot", "toldos"]),
    ("Vayetze", ["vayetze", "vayeitzei", "va'yetze", "vayetzei", "va'yetzei"]),
    ("Vayishlach", ["vayishlach", "va'yishlach"]),
    ("Vayeshev", ["vayeshev", "va'yeshev", "va'yeishev"]),
    ("Miketz", ["miketz", "mikeitz"]),
    ("Vayigash", ["vayigash", "va'yigash"]),
    ("Vayechi", ["vayechi", "va'yechi", "vayehi", "va'yehi"]),
    ("Shemot", ["shemot", "shmot"]),
    ("Vaera", ["vaera", "va'era", "vaeira"]),
    ("Bo", ["bo"]),
    ("Beshalach", ["beshalach", "b'shalach", "beshalah", "beshallach"]),
    ("Yitro", ["yitro"]),
    ("Mishpatim", ["mishpatim"]),
    ("Terumah", ["terumah", "trumah", "teruma"]),
    ("Tetzaveh", ["tetzaveh", "tetzave"]),
    ("Ki Tisa", ["ki tisa", "ki sisa"]),
    ("Vayakhel", ["vayakhel", "va'yakhel", "vayakel", "va’yakhel"]),
    ("Pekudei", ["pekudei", "pikudei", "pekude"]),
    ("Vayikra", ["vayikra", "vaykira", "vayikro"]),
    ("Tzav", ["tzav"]),
    ("Shmini", ["shmini", "shemini", "shmeni"]),
    ("Tazria", ["tazria"]),
    ("Metzora", ["metzora", "metzorah"]),
    ("Achrei Mot", ["achrei mot", "acharei mot", "aharei mot"]),
    ("Kedoshim", ["kedoshim"]),
    ("Emor", ["emor"]),
    ("Behar", ["behar"]),
    ("Bechukotai", ["bechukotai", "bechukkotai", "behukotai", "behukkotai"]),
    ("Bamidbar", ["bamidbar", "bemidbar"]),
    ("Nasso", ["nasso", "naso"]),
    ("Behaalotcha", ["behaalotcha", "beha'alotcha", "behaalotecha"]),
    ("Shlach", ["shlach", "shelach", "shlach lecha", "shelach lecha"]),
    ("Korach", ["korach", "korah"]),
    ("Chukat", ["chukat", "hukkat", "hukat", "chukkat"]),
    ("Balak", ["balak"]),
    ("Pinchas", ["pinchas", "pinhas"]),
    ("Matot", ["matot"]),
    ("Masei", ["masei", "masey"]),
    ("Devarim", ["devarim"]),
    ("Vaetchanan", ["vaetchanan", "va'etchanan", "ve'etchanan", "ve'etchnan"]),
    ("Eikev", ["eikev", "ekev"]),
    ("Re'eh", ["re'eh", "reeh", "reieh", "re'ay"]),
    ("Shoftim", ["shoftim"]),
    ("Ki Teitzei", ["ki teitzei", "ki tetzei", "ki teztei", "ki setzei"]),
    ("Ki Tavo", ["ki tavo", "ki savo"]),
    ("Nitzavim", ["nitzavim"]),
    ("Vayelech", ["vayelech", "va'yelech", "vayeilech"]),
    ("Haazinu", ["haazinu", "ha'azinu"]),
    ("V'Zot HaBerachah", ["v'zot haberachah", "vzot habracha", "v'zot habracha"]),
]

HOLIDAYS = [
    ("Rosh Hashanah", ["rosh hashanah", "rosh hashana"]),
    ("Yom Kippur", ["yom kippur"]),
    ("Sukkot", ["sukkot", "sukkos"]),
    ("Shmini Atzeret / Simchat Torah", ["shmini atzeret", "shemini atzeret", "simchat torah", "simhat torah"]),
    ("Hanukkah", ["hanukkah", "chanukah", "driedel", "dreidel"]),
    ("Purim", ["purim"]),
    ("Pesach", ["pesach", "passover", "hametz", "chametz"]),
    ("Shavuot", ["shavuot", "shavuos"]),
    ("Tisha B'Av", ["tisha b'av", "tisha bav", "9th of av"]),
]

# Manual overrides for episode titles that can't be parsed by the generic
# rules (typos, missing separators, non-standard formats, or episodes about
# a general topic rather than a specific weekly Parsha). Keyed by the exact
# Spotify episode name.
MANUAL_OVERRIDES = {
    "Yitro Retold": ["Yitro"],
    "Nitzavim/VaYelech": ["Nitzavim", "Vayelech"],
    "Vayechi: The Yosef-inci Code": ["Vayechi"],
}

# Episodes from the "Maduah Madah" science segment that tie to a specific
# Parsha or holiday by topic even though the title doesn't name it directly.
MANUAL_HOLIDAY_OVERRIDES = {
    "Scientific Meaning of Miracles": ("parsha", "Beshalach"),
    "It's Raining Hail!": ("parsha", "Vaera"),
    "This Podcast is on Fire!": ("holiday", "Hanukkah"),
    "Milking One Last Episode": ("holiday", "Shavuot"),
}

# Episodes deliberately excluded from the dashboard: no Parsha/holiday tie-in.
EXCLUDED_EPISODES = {
    "The Life of a Tree of Life",
    "The Bright Side of the Moon",
    "Oh The Humanity",
    "Maduah Madah: What 14th Century Jews of Erfurt Germany Can Teach Us Today",
}
