HEADER_FOOTER_PHRASES = [
    r"ongoing development of oc date: █/██/████",
    r"property of dragon ball: sakido",
    r"members clearance approved",

    r"__"
]

FILLER_PHRASES = [
    # Template phrases
    "description",
    "description:",
    "name:",
    "ability type:",
    "extra effects:",
    
    # Hedging / uncertainty
    "generally under extenuating circumstances",
    "in most variants",
    "usually",
    "typically",
    "in general",
    "more often than not",
    "for the most part",
    "as a rule",
    "commonly",
    "mostly",
    "often",

    # Non-essential qualifiers
    "sometimes",
    "occasionally",
    "may be used",
    "can also be",
    "under certain conditions",
    "depending on the situation",
    "for example",
    "at times",
    "in certain situations",

    # Redundant intro phrases
    "it should be noted",
    "it is important to note",
    "note that",
    "keep in mind",

    # Casual verbal fillers
    "you know",
    "basically",
    "actually",
    "in fact",
    "like",
]

LEADING_STOPWORDS = [
    "as", "the", "in", "on", "at", "of", "for", "with", "by", 
    "and", "but", "so", "then", "if", "when", "while", "although", "because", "however"
]

NEGATION_WORDS = {"not", "cannot", "never", "without", "unable", "no", "none", "nobody", "nowhere", "neither", "nor", "isn't", "aren't", "wasn't", "weren't", "won't", "don't", "doesn't", "didn't", "shouldn't", "couldn't", "wouldn't", "mustn't", "mightn't", "immune to", "resistant to", "unaffected by", "not affected", "invulnerable to", "not affected by", "immune from", "unaffected from", "not affected from",}

# -----------------------------
# Core mechanics
# -----------------------------
CORE_KEYWORDS = {
    "strength": {"weight": 0.75, "axes": ["offense"]},
    "offense": {"weight": 0.75, "axes": ["offense"]},
    "offensive": {"weight": 0.75, "axes": ["offense"]},
    "defense": {"weight": 0.75, "axes": ["defense"]},
    "defensive": {"weight": 0.75, "axes": ["defense"]},
    "damage": {"weight": 0.3, "axes": ["offense", "core"]},
    "attack": {"weight": 0.4, "axes": ["offense", "core"]},
    "hit": {"weight": 0.3, "axes": ["offense", "core"]},
    "stun": {"weight": 1.0, "axes": ["control", "core"]},
    "effect": {"weight": 0.5, "axes": ["control", "utility"]},
}

# -----------------------------
# Frequency / cooldown / speed
# -----------------------------
FREQUENCY_KEYWORDS = {
    "cooldown": {"weight": -0.3, "axes": ["frequency", "speed"]},
    "cooldown 0": {"weight": 1.3, "axes": ["frequency"]},
    "cooldown 1": {"weight": 0.8, "axes": ["frequency"]},
    "cooldown 2": {"weight": 0.5, "axes": ["frequency"]},
    "cooldown 3": {"weight": 0.3, "axes": ["frequency"]},
    "cooldown of 0": {"weight": 1.3, "axes": ["frequency"]},
    "cooldown of 1": {"weight": 0.8, "axes": ["frequency"]},
    "cooldown of 2": {"weight": 0.5, "axes": ["frequency"]},
    "cooldown of 3": {"weight": 0.3, "axes": ["frequency"]},
    "0 post cooldown": {"weight": 1.3, "axes": ["frequency"]},
    "1 post cooldown": {"weight": 0.8, "axes": ["frequency"]},
    "2 post cooldown": {"weight": 0.5, "axes": ["frequency"]},
    "3 post cooldown": {"weight": 0.3, "axes": ["frequency"]},
    "4 post cooldown": {"weight": 0.2, "axes": ["frequency"]},
    "5 post cooldown": {"weight": 0.1, "axes": ["frequency"]},
    "6 post cooldown": {"weight": -0.1, "axes": ["frequency"]},
    "7 post cooldown": {"weight": -0.2, "axes": ["frequency"]},
    "8 post cooldown": {"weight": -0.3, "axes": ["frequency"]},
    "9 post cooldown": {"weight": -0.5, "axes": ["frequency"]},
    "10 post cooldown": {"weight": -0.8, "axes": ["frequency"]},
    "speed": {"weight": 0.6, "axes": ["speed"]},
    "move": {"weight": 0.5, "axes": ["speed"]},
    "charge": {"weight": -0.75, "axes": ["frequency", "speed"]},
    "spam": {"weight": 1.75, "axes": ["frequency", "speed"]},
    "blits": {"weight": 1.75, "axes": ["frequency", "speed"]},
    "blitz": {"weight": 1.75, "axes": ["frequency", "speed"]},
    "volley": {"weight": 1.75, "axes": ["frequency", "speed"]},
}

# -----------------------------
# Resource-based
# -----------------------------
RESOURCE_KEYWORDS = {
    "mana": {"weight": 0.75, "axes": ["utility"]},
    "ki": {"weight": 0.75, "axes": ["utility"]},
    "stamina": {"weight": 0.6, "axes": ["utility"]},
    "health": {"weight": 0.5, "axes": ["utility", "defense"]},
    "energy": {"weight": 0.6, "axes": ["utility"]},
    "rage": {"weight": 0.75, "axes": ["offense", "scaling"]},
}

# -----------------------------
# Buffs / debuffs / effects
# -----------------------------
BUFF_KEYWORDS = {
    "invulnerability": {"weight": 1.5, "axes": ["defense", "unique"]},
    "kill": {"weight": 1.5, "axes": ["offense", "unique", "control"]},
    "one hit": {"weight": 1.5, "axes": ["offense", "unique", "control"]},
    "heal": {"weight": 0.75, "axes": ["defense", "utility"]},
    "shield": {"weight": 0.9, "axes": ["defense"]},
    "protect": {"weight": 0.75, "axes": ["defense"]},
    "absorb": {"weight": 0.75, "axes": ["defense"]},
    "reflect": {"weight": 0.75, "axes": ["defense"]},
    "nullify": {"weight": 1.25, "axes": ["defense", "unique"]},
    "prevent": {"weight": 1.0, "axes": ["defense"]},
    "counter": {"weight": 1.0, "axes": ["defense", "control"]},
    "weaken": {"weight": 0.6, "axes": ["control"]},
    "drain": {"weight": 0.75, "axes": ["control", "utility"]},
}

# -----------------------------
# Movement / targeting
# -----------------------------
MOVEMENT_KEYWORDS = {
    "insta": {"weight": 1.25, "axes": ["unique", "speed"]},
    "instant": {"weight": 1.25, "axes": ["unique", "speed"]},
    "teleport": {"weight": 1.0, "axes": ["utility", "speed", "versatility"]},
    "dash": {"weight": 0.75, "axes": ["utility", "speed", "versatility"]},
    "blink": {"weight": 1.0, "axes": ["speed", "utility"]},
    "sprint": {"weight": 0.75, "axes": ["speed"]},
    "slow": {"weight": -0.75, "axes": ["speed"]},
    "root": {"weight": -0.75, "axes": ["speed"]},
}

# -----------------------------
# Conditional / triggers
# -----------------------------
CONDITIONAL_KEYWORDS = {
    "requires": {"weight": -0.6, "axes": ["speed"]},
    "triggers": {"weight": 0.75, "axes": ["control"]},
    "activates": {"weight": 0.6, "axes": ["control"]},
    "overrides": {"weight": 1.25, "axes": ["unique", "control"]},
    "replace": {"weight": 1.0, "axes": ["unique", "control"]},
    "conditional": {"weight": 0.6, "axes": ["control"]},
}

# -----------------------------
# Misc / descriptors
# -----------------------------
MISC_KEYWORDS = {
    "enhance": {"weight": 0.5, "axes": ["scaling", "utility"]},
    "augment": {"weight": 0.5, "axes": ["scaling", "utility"]},
    "boost": {"weight": 0.6, "axes": ["scaling", "utility"]},
    "suppress": {"weight": 0.75, "axes": ["control"]},
    "channel": {"weight": 0.6, "axes": ["utility"]},
    "release": {"weight": 0.6, "axes": ["utility"]},
    "power": {"weight": 0.3, "axes": ["scaling"]},
    "empower": {"weight": 0.75, "axes": ["scaling"]},
    "amplify": {"weight": 0.6, "axes": ["scaling"]},
    "negate": {"weight": 1.0, "axes": ["control", "defense"]},
    "ceaseless": {"weight": 0.9, "axes": ["control","scaling","utility"]},
    "endless": {"weight": 0.9, "axes": ["control","scaling","utility"]},
    "overwhelm": {"weight": 1.0, "axes": ["control","offense", "control"]},
    "immune": {"weight": 1.0, "axes": ["control","defense"]},
    "immunity": {"weight": 1.0, "axes": ["control","defense"]},
    "invulnerable": {"weight": 1.0, "axes": ["control","defense"]},
    "bypass": {"weight": 1.0, "axes": ["control", "utility"]},
    "splits": {"weight": 0.75, "axes": ["control", "utility"]},
}

# -----------------------------
# Multi-word keywords
# -----------------------------
MULTIWORD_KEYWORDS = {
    "power of the shot": {"weight": 1.25, "axes": ["offense", "scaling"]},
    "one shot": {"weight": 1.5, "axes": ["offense"]},
    "burst damage": {"weight": 1.0, "axes": ["offense", "scaling"]},
    "damage power": {"weight": 0.9, "axes": ["offense"]},
    "immune to damage": {"weight": 1.25, "axes": ["defense", "utility"]},
    "damage reduction": {"weight": 1.0, "axes": ["defense"]},
    "area denial": {"weight": 0.75, "axes": ["defense", "control"]},
    "area of effect": {"weight": 1.0, "axes": ["utility", "control"]},
    "crowd control": {"weight": 1.25, "axes": ["utility", "control"]},
    "movement restriction": {"weight": 0.9, "axes": ["control", "defense"]},
    "high cost": {"weight": -0.75, "axes": ["frequency", "utility"]},
    "long cooldown": {"weight": -1.0, "axes": ["frequency"]},
    "short cooldown": {"weight": 0.75, "axes": ["frequency"]},
    "true damage": {"weight": 1.25, "axes": ["offense", "unique"]},
    "ignore defense": {"weight": 1.0, "axes": ["offense", "scaling"]},
    "cannot move": {"weight": -1.0, "axes": ["speed", "utility"]},
    "requires charge": {"weight": -0.75, "axes": ["frequency", "scaling"]},
    "limit movement": {"weight": 1.0, "axes": ["control", "defense"]},
}

# -----------------------------
# Merge everything together
# -----------------------------
MECHANIC_KEYWORDS = {
    **CORE_KEYWORDS,
    **FREQUENCY_KEYWORDS,
    **RESOURCE_KEYWORDS,
    **BUFF_KEYWORDS,
    **MOVEMENT_KEYWORDS,
    **CONDITIONAL_KEYWORDS,
    **MISC_KEYWORDS,
    **MULTIWORD_KEYWORDS,
}
VALID_VERBS = [
    "is", "has", "can", "does", "will", "makes", "become"
]