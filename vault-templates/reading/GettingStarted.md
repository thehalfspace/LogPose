# Getting Started

This vault keeps three kinds of work apart:

| Note | Folder | One per | Purpose |
|------|--------|---------|---------|
| **Source** | `2-Sources/` | work read | Understand the author accurately |
| **Reflection** | `3-Reflections/` | claim | Make and defend my own argument |
| **Journey** | `1-Journeys/` | ongoing inquiry | Track how my thinking changes across works |

A reflection is not a longer book summary. It makes a claim I can defend, and possibly revise.

## First steps

1. Create **one Journey** for the question driving my current reading.
2. Create a **Source** for the book I'm on, link it in `journeys:`, and write *What I believe before reading* before continuing.
3. Insert the **Session** template each time I sit down to read.
4. Leave Reflections alone until a claim starts to form. Don't force the first one.

## Inserting templates

1. Create the note in the right folder (right-click the folder → **New note**).
2. **Name it first.** `{{title}}` fills in whatever the file is called when the template is inserted.
3. Click into the empty note body.
4. **Cmd+P** → **Templates: Insert template** → pick **Source**, **Journey** or **Reflection**.

For a reading sitting: in the Source note, put the cursor under `## Reading sessions` and insert **Session**.

Hotkey: **Settings → Hotkeys** → search `Insert template` → assign e.g. **Cmd+Shift+T**.

- `{{date:YYYY-MM-DD}}` becomes today's date when the template is inserted. It doesn't change after that.
- Renaming a note afterwards doesn't update its `# Title` heading. Edit it by hand.
- Skip `TemplatesINDEX` in the picker; LogPose creates it.

## Sources

### Properties

| Property | What to put | Example |
|---|---|---|
| `type` | Always `source`. Leave as is; it lets me filter or query notes later. | `source` |
| `author` | The author's name | `Harry Collins` |
| `year` | Year first published | `2007` |
| `kind` | What sort of work it is | `book`, `essay`, `paper`, `lecture` |
| `status` | Where I am with it; update as I go | `queued` → `reading` → `finished` (or `abandoned`) |
| `started` | Filled in automatically on insert | `2026-09-24` |
| `finished` | Fill in when done | `2026-10-30` |
| `journeys` | Which inquiries this work serves, as links | `["[[When is expertise a legitimate form of authority?]]"]` |

`journeys` is the main link from a Source up to a Journey. The others are for my own sorting, e.g. "show me everything I finished this year".

### Workflow

1. **Before reading:** write *Why I'm reading this* and *What I believe before reading*. Don't edit the baseline later.
2. **Each sitting:** insert a Session. Quotes and paraphrases carry page numbers; my own reactions are prefixed **Me:**.
3. **While reading:** build *The author's argument* gradually, in the author's own terms and at its strongest.
4. **After finishing:** set `status: finished` and `finished:`, finalise the author's argument, then write the *Closing assessment*.

## Reflections

### When to write one

A Reflection is **not per work**. It's one note per *claim I want to defend*, so it does **not** share a Source's title.

- ❌ `3-Reflections/Rethinking Expertise.md`, which ends up as a longer summary of the book
- ✅ `3-Reflections/Expertise earns deference only where feedback is fast.md`

Write one when one of these happens:
- A question keeps coming back across sessions or across works.
- A *Closing assessment* has a "Where I'm unconvinced" point I could argue for.
- Two sources disagree and I find I have a view on who's right.

Many Sources produce no Reflection, and that's fine. One Reflection often draws on several Sources, and one Source can feed several Reflections. A rough pace is one every few works, when I have something to say. Not one per book.

**Link both ways:**
- In the Reflection, list the works under `sources:` and in *Evidence from sources*.
- In the Source, add the Reflection under *Closing assessment → Reflections this feeds*.

**Summary test:** could someone who accepts every source I cite still disagree with this thesis? If not, it's a summary, not a reflection.

### Properties

| Property | What to put |
|---|---|
| `type` | Always `reflection` |
| `status` | `draft` (thesis still forming) → `defended` (it has survived its strongest objection) → `revised` (I changed the thesis) or `abandoned` (I no longer hold it; **keep the note**, because it's a record of a change of mind) |
| `created` | Filled in automatically |
| `revised` | Date of the last real change to the thesis (fixing wording doesn't count) |
| `journey` | The inquiry this claim answers, e.g. `"[[When is expertise a legitimate form of authority?]]"` |
| `sources` | The works it relies on, e.g. `["[[Rethinking Expertise]]", "[[The Death of Expertise]]"]` |

When I revise, I add a dated line to *Revision log* saying what changed and why. If I abandon a Reflection, I record that in the Journey's *Changes of mind* too.

## Journeys

A Journey is **one question I'll keep pursuing across several works**, titled as that question.

### When to start one

- I'm about to choose a book *because of* a question, or
- two or three Sources are circling the same issue.

### Properties

| Property | What to put |
|---|---|
| `type` | Always `journey` |
| `status` | `active` → `dormant` (on hold) or `settled` (answered well enough for now) |
| `started` | Filled in automatically |

### Workflow

1. **Before reading:** write *Guiding question*, *Why this matters to me*, and my starting position under *Changes of mind*.
2. **When I choose a work:** add a row to *Reading path* with the reason I chose it. That reason is worth keeping; later it shows how my search moved.
3. **After finishing a work:** note any disagreements with earlier Sources under *Where sources disagree*.
4. **When my view shifts:** add a dated line to *Changes of mind* (the history), then rewrite *Where I stand now* (the current answer).
5. **Reading queue:** list candidate works under *Next to read* as `- Book title` followed by the todo tag. `logpose todo` gathers them into `0-Meta/TODOList.md`.

Keep only a handful of Journeys active at once.

## Inbox

`4-Inbox/` is for anything **not yet sorted**:
- a quote from an article or podcast that doesn't warrant a full Source
- a passing thought ("is peer review also a kind of expertise?")
- a book recommendation I haven't committed to yet

Go through it every week or two and move each item somewhere:
- **Into a Source**, if it relates to a work I'm reading
- **Into a Journey's *Next to read***, if it's a book I want to read
- **Into a new Reflection or Journey**, if it's become a real question or claim
- **Delete it**, if it no longer seems interesting

Keep the Inbox small. If it's growing, that's a sign to go through it.

## Maintenance

Run from the LogPose repo, always passing the reading config (without it, LogPose creates the wrong media folders):

```sh
logpose update <path-to-this-vault> --config vault-templates/reading_config.yaml
logpose todo   <path-to-this-vault> --config vault-templates/reading_config.yaml
```

`*INDEX.md` and `*TODO.md` files are regenerated by these commands. Don't hand-edit them.
