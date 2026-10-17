# webredesigned-ai-automation

The spec-to-launch workspace for an AI automation consultancy website (working title; the name is decided in `02_brand`). What leaves it is a live site in `site/`.

Built on ICM: folders carry sequencing, hierarchy carries context, files carry state. If something needs explaining, the explanation goes in that folder's CONTEXT.md.

## Where things live

| Folder | What it holds |
|---|---|
| `stages/` | the pipeline, in execution order (see `CONTEXT.md`) |
| `_shared/` | factory: rules that hold for every stage |
| `docs/` | source material: research, transcripts. Read-only reference, never cited as fact on the site |
| `site/` | the website code (created in `06_build`) |

## Route by what just happened

| If | Go to | Then stop at |
|---|---|---|
| starting or resuming | `CONTEXT.md` → first stage not `approved` | human reads the output |
| a stage output was approved | next numbered stage's `CONTEXT.md` | human reads the output |
| asked for status | `status:` frontmatter in `stages/*/output/*.md` | report it |
| new source material arrives | `docs/` | add a line to `docs/CONTEXT.md` |

## The one rule

Nothing moves to the next stage until a person has read the output of the last one and set its `status: approved`.
