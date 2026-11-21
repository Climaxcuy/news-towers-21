# stories.py — all editorial content for NEWS TOWERS (variant H), NI21.
# Sourced from the vetted edition pool (POOL21.md): 13 cards + 27 briefs = 40
# stories, every one dated Saturday 21 November 2026. Panel headlines/facts are
# faithful shortenings of the pool decks; attribution tags ride on every card.

REGION_COLORS = {
    "EUROPE":   (37, 99, 235),
    "GLOBAL":   (124, 58, 237),
    "AMERICAS": (220, 38, 38),
    "ASIA":     (5, 150, 105),
    "AFRICA":   (217, 119, 6),
    "OCEANIA":  (8, 145, 178),
    "MIDEAST":  (219, 39, 119),
}

# height_rank: taller tower = bigger story (Three.js scene reads this order)
CARDS = [
    dict(n=1, place="WARSAW", region="EUROPE",
         headline="Rutte flies to Warsaw after missiles land in Poland",
         facts=["Two missiles and a suspected jet drone came down in the south-east",
                "Rutte calls it a 'grave violation'; Tusk: a deliberate provocation"],
         data="3 WEAPONS ACROSS", tag="AP - CONFIRMED", height=34),
    dict(n=6, place="KYIV", region="EUROPE",
         headline="Russia's barrage: 400 drones, 110 missiles",
         facts=["At least eight dead across Ukraine in the overnight barrage",
                "Austrian embassy hit in Kyiv; France seeks a UN council meeting"],
         data="400 DRONES - 110 MISSILES", tag="BBC - OFFICIALS' COUNT", height=30),
    dict(n=3, place="NEW YORK", region="AMERICAS",
         headline="Wall Street enters correction as AI rout deepens",
         facts=["The S&P 500 fell about 3.7% on Friday, into correction territory",
                "The Nasdaq dropped 5.28% as chip and AI shares plunged"],
         data="NASDAQ -5.28%", tag="SIMPLELIFE - FRI CLOSE", height=28),
    dict(n=4, place="KRYVYI RIH", region="EUROPE",
         headline="Russian strike kills two, injures 42",
         facts=["An overnight strike on the city; four of the injured are children",
                "One of Russia's largest attacks of the war so far"],
         data="2 DEAD - 42 HURT", tag="CITY CHIEF SAYS", height=27),
    dict(n=2, place="ANTALYA", region="GLOBAL",
         headline="COP31 runs into overtime with no deal yet",
         facts=["Talks ran past Friday's scheduled close into Saturday",
                "Draft drops fossil-fuel text and $120bn target; new draft due this morning"],
         data="NO DEAL YET", tag="AP - ONGOING", height=26),
    dict(n=7, place="ODISHA, INDIA", region="ASIA",
         headline="After Akvan: 372,000 moved, no deaths",
         facts=["A day after landfall, no deaths are reported and relief is under way",
                "The storm weakens to a depression; schools stay shut through Saturday"],
         data="372,000 MOVED", tag="RIDHU TIMES - RELIEF REPORTS", height=24),
    dict(n=8, place="BRUSSELS", region="EUROPE",
         headline="EU adopts 1bn euro military aid for Ukraine",
         facts=["Joint buying runs via the Peace Facility",
                "Britain pledges 1,000+ drones in a 260m pound package alongside"],
         data="EUR 1BN ADOPTED", tag="REUTERS - ADOPTED", height=23),
    dict(n=5, place="COPENHAGEN", region="EUROPE",
         headline="Denmark exposes 'assassination plot'",
         facts=["Russia 'planned and initiated' a bid to kill a Ukrainian-American rapper",
                "The Russian attache is expelled"],
         data="ATTACHE EXPELLED", tag="BBC - DENMARK SAYS", height=22),
    dict(n=9, place="NEW YORK", region="AMERICAS",
         headline="JPMorgan, Visa, Mastercard hit by cyberattack",
         facts=["The banks report incidents at third-party vendors",
                "Their core payment networks are unaffected, they say"],
         data="3 NETWORKS HIT", tag="REUTERS - BANKS SAY", height=21),
    dict(n=11, place="THE HAGUE", region="GLOBAL",
         headline="Myanmar ruling rattles Israel's Gaza defence",
         facts=["The world court's genocide verdict on Myanmar raises questions in Jerusalem",
                "Experts say it bears on Israel's own case; the ruling came on Thursday"],
         data="GENOCIDE VERDICT", tag="BBC - EXPERTS SAY", height=20),
    dict(n=12, place="JOHANNESBURG", region="AFRICA",
         headline="ANC scrambles after worst result since 1994",
         facts=["The ANC wins 31% of the vote, its worst since 1994",
                "It now races for coalition deals to stay in government"],
         data="ANC 31%", tag="BBC - COUNT", height=19),
    dict(n=10, place="ULAANBAATAR", region="ASIA",
         headline="Mongolia's president resigns",
         facts=["The resignation sets the stage for a snap election",
                "It caps a week of political turmoil in the capital"],
         data="SNAP ELECTION NEXT", tag="REUTERS - CAPITAL REPORTS", height=18),
    dict(n=13, place="WELLINGTON", region="OCEANIA",
         headline="India fight back: 159/1 at stumps, day two",
         facts=["India trail New Zealand by 209 in the first Test; the hosts made 368",
                "Nicholls made 175 not out for the hosts"],
         data="159/1 - DAY TWO", tag="ICC - SCORECARD", height=17),
]

# Briefs 14-40: (n, place, text, source) — one line each, source in parens.
BRIEFS = [
    (14, "Kathmandu", "Nepal's new leader Balendra Shah faces an India test", "BBC"),
    (15, "Washington", "US releases more UFO footage filmed in the Middle East", "BBC"),
    (16, "Los Angeles", "Hyundai unveils the 2027 Elantra at the auto show", "Fast Company"),
    (17, "Cardiff", "Lauren Price beats Kotaskova to become undisputed champion", "BBC"),
    (18, "Paris", "Three police are sentenced over the beating of Michel Zecler", "BBC"),
    (19, "Oxford", "Life, 22 years minimum, for the Thames drowning murder", "BBC"),
    (20, "New York", "Nikhil Gupta gets 19+ years over the Sikh murder plot", "BBC"),
    (21, "Cincinnati", "Fiona the hippo dies after eating a hat", "AP"),
    (22, "Washington", "US sanctions four Iranians over oil revenues", "OFAC"),
    (23, "Hormuz", "A tanker is struck and on fire in the Strait of Hormuz", "UKMTO"),
    (24, "Los Angeles", "A jury convicts the man who started the Palisades Fire", "AP"),
    (25, "Frankfurt", "ECB names Boone and Brunnermeier for its Executive Board", "Reuters"),
    (26, "Buenos Aires", "Argentina's Senate backs a disability framework, 71-0", "AP"),
    (27, "Riyadh", "A Saudi coalition intercepts Houthi missiles over Riyadh", "Reuters"),
    (28, "Barcelona", "A pill is hailed as a breakthrough for pancreatic cancer", "Reuters"),
    (29, "Gaza", "On World Children's Day, Palestinian children appeal for help", "UN"),
    (30, "Madrid", "Amnesty says Spanish police used excess force in the strike", "AP"),
    (31, "Rome", "Italian workers and students march against Meloni's government", "AFP"),
    (32, "Jeddah", "Saudi Arabia warns of thunderstorms through Tuesday", "SPA"),
    (33, "Kuala Lumpur", "Malaysia to send 10,000 Rohingya to Turkey for training", "Reuters"),
    (34, "Kharkiv", "Ukraine says it has finished a 'Bear Trap' in the Kharkiv area", "Ukrinform"),
    (35, "Islamabad", "Pakistan's minerals are worth $8-10 trillion, its minister says", "Reuters"),
    (36, "Singapore", "US presses Singapore and Malaysia on Iran sanctions", "Reuters"),
    (37, "Paris", "France seeks a UN council meeting on the Kyiv strikes", "AFP"),
    (38, "Kyiv", "The war tally: 771 Ukrainians killed, 2,300+ missing", "homevo"),
    (39, "Ankara", "Turkey welcomes the World Court's Myanmar ruling", "Anadolu"),
    (40, "Turin", "ATP semis are set: Alcaraz v Shelton, Zverev v Medvedev", "ATP"),
]

# Numbers strip: (big number, caption, bound card number)
NUMBERS = [
    ("3", "weapons cross into Poland", 1),
    ("42", "injured at Kryvyi Rih", 4),
    ("-5.28%", "Nasdaq at Friday's close", 3),
    ("372,000", "moved to shelters - Akvan", 7),
    ("EUR 1BN", "EU military aid adopted", 8),
    ("159/1", "India at stumps, Wellington", 13),
]

# UTC timeline: (slot label, text)
TIMELINE = [
    ("OVERNIGHT", "Kryvyi Rih strike: two killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due after overnight talks"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

# DATE CHECK discards — first reported Friday 20 November 2026, NOT Saturday news.
DATE_DISCARDS = [
    "Kyiv's three bridges hit",
    "Cyclone Akvan's landfall at Gopalpur",
    "COP31's final day ending with no deal",
    "Asia's AI sell-off (Taipei -6.2%)",
    "the UK-EU reset deal",
    "Phillips's 118 in the first innings",
]
DATE_NOT_YET = [
    "any final COP31 text",
    "the ATP semi-final results",
    "BepiColombo's entry into orbit around Mercury (due today)",
]

MASTHEAD_DECK = ("Missiles land in Poland - COP31 slips into overtime - "
                 "Wall Street falls into correction - Denmark exposes a plot")
# Challenger h2: red hook band under the masthead — the day's biggest story
# and its two biggest numbers, readable at first glance / 300px thumbnail.
HOOK_LINE = ("MISSILES LAND IN POLAND - 400 DRONES + 110 MISSILES OVER UKRAINE"
             " - 372,000 MOVED AS AKVAN FLOODS INDIA")
KICKER = "40 STORIES - 7 REGIONS - EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
REGION_LINE = "EUROPE 16 - ASIA 6 - AMERICAS 8 - MIDEAST 6 - AFRICA 1 - OCEANIA 1 - GLOBAL 2"
FOOTER = ("Every story here happened, or was first reported, on Saturday 21 November 2026. "
          "Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original 3D artwork"
