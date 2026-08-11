# slopify

Takes human-written text and, with minimal edits, makes it read like AI slop.
The reverse of a Turing test: the goal is for a detector (or a person applying
[Wikipedia's Signs of AI Writing checklist](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing))
to flag the output as AI-generated.

## Design

- **Rule-based, not LLM-rewritten.** Each slop "tell" (em dashes, filler
  transitions, hedging, grandiose closers, vocabulary swaps, sentence
  fragmentation) is its own `Transform` in `slopify/transforms/`, applied as
  a targeted text edit rather than a full regeneration. This keeps edits
  minimal and preserves the original wording/voice.
- **One intensity dial (0-100)** in `SlopifyConfig` scales how often each
  transform fires; per-transform weights let you tune one relative to
  another without a dial per transform.
- **Transform log.** Every run records before/after snapshots per transform
  step (`TransformLog`). `deslopify` replays that log backwards to exactly
  undo a slopify run. It is *not* a general "clean up any AI text" tool --
  that needs a log to replay against, or a real rewrite model for arbitrary
  input.
- **`triplets` is a stub.** Rule-of-three restatement needs a paraphrase of
  content the pipeline doesn't semantically understand -- regex can't
  generate near-synonyms for an arbitrary sentence. Fill in with a
  WordNet/thesaurus lookup or a small LLM call later.

## Usage

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Bash; use .venv\Scripts\Activate.ps1 in PowerShell
pip install -e .
```

```bash
# file in, file out
slopify input.txt --intensity 70 -o output.txt

# or pipe through stdin/stdout (both default to '-')
echo "Your normal sentence here." | slopify --intensity 90

# --seed makes a run reproducible: same input + intensity + seed -> same output
slopify input.txt --intensity 70 --seed 1 -o output.txt

# --log saves a transform log so the run can be reversed later
slopify input.txt --intensity 70 --log run.json -o output.txt
deslopify output.txt --log run.json -o restored.txt
```

Run `slopify --help` / `deslopify --help` for the full flag list.

## Layout

```
src/slopify/
  config.py          # SlopifyConfig: intensity dial + per-transform weights
  pipeline.py         # Pipeline: runs transforms in order, builds the log
  transformlog.py      # TransformLog: before/after snapshots, save/load, reverse
  deslopify.py         # exact-inverse using the log
  cli.py               # `slopify` / `deslopify` console scripts
  data/                # word lists backing transforms (ai_vocabulary.json, ...)
  transforms/          # one module per slop technique
```
