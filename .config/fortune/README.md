# Thinking Tools — fortune deck

A 48-card open-source mental-models deck (homage to The Unstuck Box).
Shown as the fish shell greeting via `fortune -s ~/.config/fortune/thinking-tools`.

## Files
- `build_deck.py` — **source of truth.** Edit cards here.
- `thinking-tools` — generated cookie file (do not hand-edit).
- `thinking-tools.dat` — generated strfile index (do not hand-edit).

## To change a card
1. Edit `DECK` in `build_deck.py` (keep each card < 160 chars for `fortune -s`).
2. Run `python3 build_deck.py` — regenerates the cookie file, `.dat`, and HTML report.
3. Commit all three files together. Never edit `thinking-tools`/`.dat` by hand — they desync.
