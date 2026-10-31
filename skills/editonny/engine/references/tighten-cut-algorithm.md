# Pause-trimming algorithm

The waveform envelope uses 10 ms hops. Speech boundaries are measured relative to the source's own voice level, then extended through quiet sound to protect consonants and word tails. The initial minimum padding is approximately 60 ms after a word and 70 ms before the next; weak-sound reach can extend a boundary by up to 120 ms. A short 8 ms audio fade reduces clicks.

Candidate joins favor small image changes. A graphics-only reference can isolate overlay movement. Sound plans and voice-only references protect effect attacks. These are conservative measurements, not a semantic detector: review speech and intentional pauses before accepting removals.

The helper probes media, validates timing, renders to a separate output, normalizes audio, and writes the time map. Exact tunable arguments are documented by `helpers/tighten_cut.py --help`. The exported result must still be inspected in motion and listened to across each changed join.
