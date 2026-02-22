"""
  ___  ___  ___  ___     __  __  ___  ___  _  _  ___ _  _
 / __)/ __)/ _ \| _ \   |  \/  |/ _ \| _ \| \| || __| \| |
| (_ | (_ | (_) |  _/   | |\/| | (_) |   /| .` || _|| .` |
 \___)\___)\___/|_|      |_|  |_|\___/|_|_\|_|\_||___|_|\_|

   your daily dose of absolutely ridiculous greetings
"""

import os
import sys
import random
import difflib
import urllib.request
import urllib.error
import json
import time
from datetime import date

# ── Files ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_FILE       = os.path.join(SCRIPT_DIR, "greetings.txt")
USED_WORDS_FILE = os.path.join(SCRIPT_DIR, "used_words.txt")
SIMILARITY_THRESHOLD = 0.80

# ── Colors ────────────────────────────────────────────────────────────────────
# Enable ANSI colors on Windows (VS Code terminal + cmd + Windows Terminal)
if sys.platform == "win32":
    import ctypes
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass

R    = "\033[91m"   # red
G    = "\033[92m"   # green
Y    = "\033[93m"   # yellow
B    = "\033[94m"   # blue
M    = "\033[95m"   # magenta
C    = "\033[96m"   # cyan
W    = "\033[97m"   # white
DIM  = "\033[2m"
BOLD = "\033[1m"
RS   = "\033[0m"    # reset

RAINBOW = [R, Y, G, C, B, M]

def col(color, text):
    return f"{color}{text}{RS}"

def rainbow(text):
    """Color whole words in rotating rainbow colors."""
    words = text.split()
    return " ".join(RAINBOW[i % len(RAINBOW)] + w + RS for i, w in enumerate(words))

def bold(text):  return f"{BOLD}{text}{RS}"
def dim(text):   return f"{DIM}{text}{RS}"

# ── Fun messages ──────────────────────────────────────────────────────────────
SAVE_MSGS = [
    "ABSOLUTE BANGER.", "certified fresh.", "the people will love this.",
    "shakespeare is shaking.", "bold choice. respect.",
    "your ancestors are proud.", "this one slaps different.",
    "adding to the hall of fame.", "pure genius.",
    "the dictionary never expected this.",
]

BLOCK_MSGS = [
    "nice try though.", "the council has spoken.",
    "we don't do that here.", "not on my watch.",
    "the word retirement board says NO.",
]

GENERATE_INTROS = [
    "cooking something up...",
    "consulting the word wizards...",
    "asking the internet nicely...",
    "rummaging through the dictionary...",
    "summoning today's absurdity...",
]

RETIRE_MSGS = [
    "packing their bags.",
    "gone. reduced to atoms.",
    "off to the retirement home.",
    "bye bye forever.",
    "never to be seen again.",
]

# ── Animations ────────────────────────────────────────────────────────────────
def spinner(msg, duration=1.2):
    """Show a spinner for a given duration."""
    frames = ["◐", "◓", "◑", "◒"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {col(C, frame)}  {col(Y, msg)}   ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(msg) + 10) + "\r")
    sys.stdout.flush()

def typewrite(text, delay=0.03):
    """Print text character by character."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def flash_text(text, color, times=2):
    """Flash text a few times."""
    for _ in range(times):
        sys.stdout.write(f"\r  {col(color, text)}")
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write(f"\r  {' ' * len(text)}")
        sys.stdout.flush()
        time.sleep(0.1)
    print(f"  {col(color, text)}")

def animate_banner():
    """Animate the big greeting word."""
    words = [
        "GOOP MORNEN!", "GROOD MORNING!", "GLUTEN MORNIN!",
        "GOOBER MORTEN!", "GLACIAL MANGO!", "GOOFY MONSOON!",
    ]
    w = random.choice(words)
    print()
    typewrite(f"  {rainbow(w)}", delay=0.04)
    print()

# ── ASCII Art Header ──────────────────────────────────────────────────────────
LOGO = r"""
  ___  ___  ___  ___    __  __  ___  ____  _  _  ___  _  _ 
 / __|/ _ \/ _ \| _ \  |  \/  |/ _ \| _ \ | \| || __|| \| |
| (_ | (_) | (_)| |__/ | |\/| | (_) |   / | .` || _| | .` |
 \___|\___|\___/|_|    |_|  |_|\___/|_|_\ |_|\_||___||_|\_|
"""

SUN = [
    col(Y, "        \\   |   /        "),
    col(Y, "     \\   ") + col(R, "( ͡° ͜ʖ ͡°)") + col(Y, "   /     "),
    col(Y, "  ─────── ") + col(R, "  SUN  ") + col(Y, " ───────  "),
    col(Y, "     /   ") + col(R, "  uwu  ") + col(Y, "   \\     "),
    col(Y, "        /   |   \\        "),
]

def header():
    os.system("cls" if os.name == "nt" else "clear")
    print(col(Y, LOGO))
    for line in SUN:
        print(line)
    print()
    print(col(DIM, "  " + "·" * 50))
    print()

# ── Menu ──────────────────────────────────────────────────────────────────────
MENU_ITEMS = [
    ("1", "👀", "View all greetings",                W),
    ("2", "✏ ", "Add a greeting manually",            G),
    ("3", "🎲", "Auto-generate a new one",            C),
    ("4", "🔍", "Search greetings",                   B),
    ("5", "🗑 ", "Delete a greeting",                  R),
    ("6", "💀", "View retired words",                 M),
    ("7", "🚫", "Manually retire a word",             Y),
    ("8", "🔁", "Reset everything",                   R),
    ("Q", "👋", "Quit",                               Y),
]

def show_menu(greetings, used_words):
    total   = len(greetings)
    retired = len(used_words)
    print(f"  {col(G, bold(str(total)))} saved  {col(DIM,'·')}  {col(R, bold(str(retired)))} words retired  {col(DIM,'·')}  {col(C,'live word bank')}\n")
    print(col(DIM, "  " + "┌" + "─" * 40 + "┐"))
    for key, icon, label, color in MENU_ITEMS:
        print(f"  {col(DIM,'│')}  {col(color, bold(f'[{key}]'))}  {icon}  {col(color, label):<35}{col(DIM,'│')}")
    print(col(DIM, "  " + "└" + "─" * 40 + "┘"))
    print()

# ── Datamuse ──────────────────────────────────────────────────────────────────
DATAMUSE_URL = "https://api.datamuse.com/words?sp={letter}*&max=1000&md=f"

def fetch_words_online(letter):
    url = DATAMUSE_URL.format(letter=letter.lower())
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GoopMornen/2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        words = []
        for entry in data:
            w = entry.get("word", "")
            if w.isalpha() and 4 <= len(w) <= 12 and w == w.lower():
                words.append(w.capitalize())
        return sorted(set(words)) if words else None
    except Exception:
        return None

# ── Storage ───────────────────────────────────────────────────────────────────
def load_used_words():
    if not os.path.exists(USED_WORDS_FILE):
        return set()
    with open(USED_WORDS_FILE, "r", encoding="utf-8") as f:
        return set(l.strip().lower() for l in f if l.strip() and not l.startswith("#"))

def retire_words(greeting):
    parts = greeting.strip().split()
    if len(parts) != 2:
        return
    with open(USED_WORDS_FILE, "a", encoding="utf-8") as f:
        for w in parts:
            f.write(w.lower() + "\n")

def init_used_words_file():
    if not os.path.exists(USED_WORDS_FILE):
        with open(USED_WORDS_FILE, "w", encoding="utf-8") as f:
            f.write("# Retired Words\n\n")

def load_greetings():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f]
    return [l for l in lines if l and not l.startswith("#")]

def save_greeting(greeting):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(greeting + "\n")

def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("# Goop Mornen — Variation Log\n\n")

# ── Validation ────────────────────────────────────────────────────────────────
def validate_format(text):
    words = text.strip().split()
    if len(words) != 2:
        return False, "Must be exactly 2 words."
    w1, w2 = words
    if w1[0].upper() != 'G':
        return False, f"'{w1}' must start with G."
    if w2[0].upper() != 'M':
        return False, f"'{w2}' must start with M."
    return True, ""

def normalise(text):
    return text.strip().lower()

def similarity(a, b):
    return difflib.SequenceMatcher(None, normalise(a), normalise(b)).ratio()

def check_duplicate(candidate, existing):
    nc = normalise(candidate)
    for entry in existing:
        ne = normalise(entry)
        if ne == nc:
            return True, entry
        if similarity(nc, ne) >= SIMILARITY_THRESHOLD:
            return True, entry
    return False, None

def check_word_retired(candidate, used_words):
    for w in candidate.strip().split():
        if w.lower() in used_words:
            return True, w
    return False, None

# ── Auto-generate ─────────────────────────────────────────────────────────────
def auto_generate(existing, used_words):
    g_all = fetch_words_online('g')
    if g_all is None:
        return None, "no_internet"
    m_all = fetch_words_online('m')
    if m_all is None:
        return None, "no_internet"

    avail_g = [w for w in g_all if w.lower() not in used_words]
    avail_m = [w for w in m_all if w.lower() not in used_words]

    if not avail_g or not avail_m:
        return None, "exhausted"

    used_pairs = set(normalise(e) for e in existing)
    for _ in range(300):
        g = random.choice(avail_g)
        m = random.choice(avail_m)
        candidate = f"{g} {m}"
        if normalise(candidate) in used_pairs:
            continue
        blocked, _ = check_duplicate(candidate, existing)
        if not blocked:
            return candidate, None
    return None, "no_fresh"

# ── Screens ───────────────────────────────────────────────────────────────────
def show_all(greetings):
    header()
    print(col(W, bold("  YOUR COLLECTION\n")))
    if not greetings:
        print(col(Y, "  nothing here yet... add some! go on."))
    else:
        cols = 2
        for i in range(0, len(greetings), cols):
            row = greetings[i:i+cols]
            line = ""
            for j, g in enumerate(row):
                num = col(DIM, f"{i+j+1:>3}.")
                word = rainbow(g) if (i+j) % 5 == 0 else col(random.choice(RAINBOW), g)
                line += f"  {num} {word:<40}"
            print(line)
    print()
    print(col(DIM, f"  total: {len(greetings)} greetings saved"))
    print()
    input(col(C, "  press enter to go back..."))

def show_retired(used_words):
    header()
    print(col(M, bold("  HALL OF RETIREMENT  💀\n")))
    if not used_words:
        print(col(Y, "  no words retired yet. get going!"))
    else:
        g_ret = sorted(w for w in used_words if w.startswith('g'))
        m_ret = sorted(w for w in used_words if w.startswith('m'))
        print(col(G, f"  G words gone ({len(g_ret)}):"))
        if g_ret:
            for i in range(0, len(g_ret), 6):
                chunk = g_ret[i:i+6]
                print("    " + col(DIM, "  ") + "  ".join(col(DIM, w.capitalize()) for w in chunk))
        else:
            print(col(DIM, "    none yet"))
        print()
        print(col(M, f"  M words gone ({len(m_ret)}):"))
        if m_ret:
            for i in range(0, len(m_ret), 6):
                chunk = m_ret[i:i+6]
                print("    " + col(DIM, "  ") + "  ".join(col(DIM, w.capitalize()) for w in chunk))
        else:
            print(col(DIM, "    none yet"))
    print()
    input(col(C, "  press enter to go back..."))

def do_manual_add(greetings, used_words):
    header()
    print(col(G, bold("  ADD MANUALLY  ✏\n")))
    print(f"  {col(Y, 'rule:')} exactly 2 words  {col(DIM,'·')}  first = G  {col(DIM,'·')}  second = M")
    print(f"  {col(DIM, 'e.g.')}  {col(G, 'Green Mango')}  {col(DIM,'/')}  {col(C, 'Gay Mosquito')}  {col(DIM,'/')}  {col(M, 'Glacial Muffin')}\n")

    raw = input(col(W, "  > ")).strip()
    if not raw:
        return greetings, used_words

    candidate = " ".join(w.capitalize() for w in raw.split())

    ok, err = validate_format(candidate)
    if not ok:
        print(col(R, f"\n  nope! {err}"))
        print(col(DIM, f"  {random.choice(BLOCK_MSGS)}"))
        input(col(C, "\n  press enter to go back..."))
        return greetings, used_words

    word_blocked, retired_word = check_word_retired(candidate, used_words)
    if word_blocked:
        print(col(R, f"\n  BLOCKED!  '{retired_word.capitalize()}' is permanently retired."))
        print(col(DIM, f"  {random.choice(BLOCK_MSGS)}"))
        input(col(C, "\n  press enter to go back..."))
        return greetings, used_words

    blocked, match = check_duplicate(candidate, greetings)
    if blocked:
        print(col(R, f"\n  BLOCKED!  too similar to '{match}'"))
        print(col(DIM, f"  {random.choice(BLOCK_MSGS)}"))
        input(col(C, "\n  press enter to go back..."))
        return greetings, used_words

    # Save
    save_greeting(candidate)
    retire_words(candidate)
    greetings.append(candidate)
    w1, w2 = candidate.split()
    used_words.add(w1.lower())
    used_words.add(w2.lower())

    print()
    flash_text(f"SAVED: {candidate}", G, times=3)
    print(col(Y, f"  {random.choice(SAVE_MSGS)}"))
    print(col(DIM, f"  '{w1}' and '{w2}' are now {random.choice(RETIRE_MSGS)}"))
    input(col(C, "\n  press enter to go back..."))
    return greetings, used_words

def do_auto_generate(greetings, used_words):
    while True:
        header()
        print(col(C, bold("  AUTO-GENERATE  🎲\n")))

        intro = random.choice(GENERATE_INTROS)
        spinner(intro, duration=1.5)

        candidate, reason = auto_generate(greetings, used_words)

        if not candidate:
            if reason == "no_internet":
                print(col(R, "  no internet! can't fetch the word bank."))
                print(col(Y, "  you can still add manually with [2]."))
            elif reason == "exhausted":
                print(col(R, "  all words retired! you absolute legend."))
            else:
                print(col(R, "  couldn't find a fresh combo. try deleting some."))
            input(col(C, "\n  press enter to go back..."))
            return greetings, used_words

        w1, w2 = candidate.split()

        print(f"  {col(DIM, 'today we present...')}\n")
        time.sleep(0.4)
        typewrite(f"  {rainbow(bold(candidate))}", delay=0.06)
        print()
        print(col(DIM, f"  saving will retire '{w1}' and '{w2}' forever."))
        print()
        print(f"  {col(G, bold('[Y]'))} save it   {col(C, bold('[R]'))} regenerate   {col(M, bold('[I]'))} use as inspiration   {col(Y, bold('[N]'))} discard & go back")
        print()

        choice = input(col(W, "  your call: ")).strip().lower()

        if choice in ("", "y", "yes"):
            save_greeting(candidate)
            retire_words(candidate)
            greetings.append(candidate)
            used_words.add(w1.lower())
            used_words.add(w2.lower())
            print()
            flash_text(f"SAVED: {candidate}", G, times=3)
            print(col(Y, f"  {random.choice(SAVE_MSGS)}"))
            print(col(DIM, f"  '{w1}' and '{w2}' — {random.choice(RETIRE_MSGS)}"))
            input(col(C, "\n  press enter to go back..."))
            return greetings, used_words

        elif choice in ("i", "inspiration", "inspire"):
            print()
            print(col(M, f"  inspired by: {rainbow(candidate)}"))
            print(col(DIM,  "  type your own version. same rules: G_ M_."))
            print(col(DIM,  "  only your saved words will be retired. generated words stay free."))
            print()
            raw = input(col(W, "  your version: ")).strip()
            if not raw:
                print(col(Y, "  nothing entered. going back."))
                input(col(C, "\n  press enter to go back..."))
                return greetings, used_words

            custom = " ".join(w.capitalize() for w in raw.split())

            # Validate format
            ok, err = validate_format(custom)
            if not ok:
                print(col(R, f"\n  nope! {err}"))
                input(col(C, "\n  press enter to go back..."))
                return greetings, used_words

            cw1, cw2 = custom.split()

            # Check BOTH custom words strictly against retired list
            # (no exceptions — generated words are irrelevant here)
            word_blocked, retired_word = check_word_retired(custom, used_words)
            if word_blocked:
                print(col(R, f"\n  BLOCKED! '{retired_word.capitalize()}' is already retired."))
                print(col(DIM,  "  nothing saved. nothing retired."))
                input(col(C, "\n  press enter to go back..."))
                return greetings, used_words

            # Check for duplicate pair
            dup_blocked, match = check_duplicate(custom, greetings)
            if dup_blocked:
                print(col(R, f"\n  BLOCKED! too similar to '{match}'."))
                print(col(DIM,  "  nothing saved. nothing retired."))
                input(col(C, "\n  press enter to go back..."))
                return greetings, used_words

            # All good — retire only words that appear in the saved custom pair
            # If the inspired word reuses a generated word, that word is retired too
            save_greeting(custom)
            retire_words(custom)
            greetings.append(custom)
            used_words.add(cw1.lower())
            used_words.add(cw2.lower())

            # Figure out which generated words are now free vs retired
            freed  = [w for w in (w1, w2) if w.lower() not in used_words]
            reused = [w for w in (w1, w2) if w.lower() in used_words]

            print()
            flash_text(f"SAVED: {custom}", G, times=3)
            print(col(Y, f"  {random.choice(SAVE_MSGS)}"))
            if freed and reused:
                print(col(DIM, f"  '{cw1}' and '{cw2}' retired. '{', '.join(freed)}' back in the pool. '{', '.join(reused)}' also retired (you used it)."))
            elif freed:
                print(col(DIM, f"  '{cw1}' and '{cw2}' retired. '{', '.join(freed)}' back in the pool."))
            else:
                print(col(DIM, f"  '{cw1}' and '{cw2}' retired. all generated words were reused — none back in pool."))
            input(col(C, "\n  press enter to go back..."))
            return greetings, used_words

        elif choice in ("r", "regen", "regenerate"):
            continue

        else:
            print(col(Y, "  discarded. their sacrifice was not in vain."))
            input(col(C, "\n  press enter to go back..."))
            return greetings, used_words

def do_search(greetings):
    header()
    print(col(B, bold("  SEARCH  🔍\n")))
    query = input(col(W, "  search for: ")).strip().lower()
    if not query:
        return
    results = [g for g in greetings if query in g.lower()]
    print()
    if not results:
        print(col(Y, f"  nothing found for '{query}'. tough luck."))
    else:
        print(col(G, f"  found {len(results)} match(es):\n"))
        for g in results:
            highlighted = g.lower().replace(query, col(Y, bold(query)))
            print(f"    {col(C, '»')}  {g}")
    print()
    input(col(C, "  press enter to go back..."))

def do_delete(greetings, used_words):
    header()
    if not greetings:
        print(col(Y, "  nothing to delete. add some first!"))
        input(col(C, "  press enter to go back..."))
        return greetings, used_words

    print(col(R, bold("  DELETE  🗑\n")))
    for i, g in enumerate(greetings, 1):
        print(f"  {col(DIM, str(i).rjust(3)+'.')}  {col(W, g)}")
    print()
    print(col(DIM, "  note: words stay retired even after deletion."))
    print()

    raw = input(col(W, "  enter number to delete (blank = cancel): ")).strip()
    if not raw:
        return greetings, used_words
    try:
        idx = int(raw) - 1
        if not (0 <= idx < len(greetings)):
            raise ValueError
    except ValueError:
        print(col(R, "  invalid number."))
        input(col(C, "  press enter to go back..."))
        return greetings, used_words

    removed = greetings.pop(idx)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("# Goop Mornen — Variation Log\n\n")
        for g in greetings:
            f.write(g + "\n")

    print(col(R, f"\n  deleted: {removed}"))
    print(col(DIM, "  rip. it had a good run."))
    input(col(C, "\n  press enter to go back..."))
    return greetings, used_words


def do_retire_word(used_words):
    header()
    print(col(Y, bold("  MANUALLY RETIRE A WORD  🚫\n")))
    print(col(DIM, "  type any G or M word to permanently ban it from auto-generate."))
    print(col(DIM, "  won't affect already saved greetings.\n"))
    raw = input(col(W, "  word to retire (blank = cancel): ")).strip()
    if not raw:
        return used_words
    word = raw.strip().lower()
    if not word.isalpha():
        print(col(R, "\n  letters only please."))
        input(col(C, "\n  press enter to go back..."))
        return used_words
    if not (word.startswith('g') or word.startswith('m')):
        print(col(R, f"\n  '{word.capitalize()}' doesn't start with G or M."))
        input(col(C, "\n  press enter to go back..."))
        return used_words
    if word in used_words:
        print(col(Y, f"\n  '{word.capitalize()}' is already retired!"))
        input(col(C, "\n  press enter to go back..."))
        return used_words
    with open(USED_WORDS_FILE, "a", encoding="utf-8") as f:
        f.write(word + "\n")
    used_words.add(word)
    print(col(R, f"\n  '{word.capitalize()}' is now permanently retired."))
    print(col(DIM, "  gone. reduced to atoms."))
    input(col(C, "\n  press enter to go back..."))
    return used_words


def do_reset(greetings, used_words):
    header()
    print(col(R, bold("  RESET EVERYTHING  🔁\n")))
    print(col(Y,  "  this will permanently delete:"))
    print(col(W,  "    - all saved greetings"))
    print(col(W,  "    - all retired words"))
    print(col(DIM,"  the app will be back to factory fresh.\n"))
    print(col(R,  "  THIS CANNOT BE UNDONE.\n"))
    confirm = input(col(W, "  type RESET to confirm (blank = cancel): ")).strip()
    if confirm != "RESET":
        print(col(Y, "\n  cancelled. your data is safe."))
        input(col(C, "\n  press enter to go back..."))
        return greetings, used_words
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("# Goop Mornen - Variation Log\n\n")
    with open(USED_WORDS_FILE, "w", encoding="utf-8") as f:
        f.write("# Retired Words\n\n")
    print(col(G, "\n  wiped. fresh start. go nuts."))
    input(col(C, "\n  press enter to go back..."))
    return [], set()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    init_file()
    init_used_words_file()

    greetings  = load_greetings()
    used_words = load_used_words()

    for g in greetings:
        for w in g.strip().split():
            used_words.add(w.lower())

    # Intro animation
    header()
    animate_banner()
    time.sleep(0.5)

    while True:
        header()
        show_menu(greetings, used_words)
        choice = input(col(W, "  choose: ")).strip().lower()

        if choice == "1":
            show_all(greetings)
        elif choice == "2":
            greetings, used_words = do_manual_add(greetings, used_words)
        elif choice == "3":
            greetings, used_words = do_auto_generate(greetings, used_words)
        elif choice == "4":
            do_search(greetings)
        elif choice == "5":
            greetings, used_words = do_delete(greetings, used_words)
        elif choice == "6":
            show_retired(used_words)
        elif choice == "7":
            used_words = do_retire_word(used_words)
        elif choice == "8":
            greetings, used_words = do_reset(greetings, used_words)
        elif choice in ("q", "quit", "exit"):
            header()
            print()
            typewrite(rainbow("  goopbye!👋"), delay=0.05)
            print()
            time.sleep(0.5)
            break

if __name__ == "__main__":
    main()