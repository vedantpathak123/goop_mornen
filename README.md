# Goop Mornen 🌅

A local terminal app for tracking absurd variations of "Good Morning" — 
think *Glacial Mango*, *Gay Mosquito*, *Grouchy Marshmallow*.

## Features
- Auto-generates G_ M_ word pairs fetched live from the Datamuse dictionary API
- Tracks every word ever used — no repeats, ever
- Manually add your own variations
- Use a generated word as inspiration and craft your own
- Retire individual words from the pool
- Full history stored locally in plain text files
- Colorful, animated terminal interface

## How to run
1. Install Python 3.x from python.org
2. Run `python gm_tracker.py` in your terminal

## Files
- `gm_tracker.py` — the app
- `RUN ME.bat` — Windows double-click launcher
- `greetings.txt` — your saved variations (auto-created)
- `used_words.txt` — retired words (auto-created)

## Word bank
Live-fetched from [Datamuse API](https://api.datamuse.com) — 
thousands of real English words, no local storage needed.
