# Backup presentation — if AV fails

If the projector dies, the laptop fails, the HDMI cable disagrees, or any other equipment failure at the lectern, **this folder is the talk.**

You can deliver the entire 15-minute talk from your phone, with no projector, no slides, no internet. Here's how.

---

## Pre-conference setup (do this before you leave)

1. **Clone the repo locally on your phone.** On iOS, use Working Copy (free for read-only). On Android, use Termux + git, or any GitHub client app. You want the full repo on the phone's local storage so you do **not** depend on conference WiFi.
2. **Bookmark `papers/codawork2026/talk/README.md`** in the file viewer.
3. **Test the workflow offline:** put the phone in airplane mode and confirm you can open the README, navigate to `slides/`, navigate to `qa_bench/`, and read everything.
4. **Print the cheat sheet.** One physical copy, folded in your pocket. Belt-and-suspenders.

---

## The AV-failure protocol

If you arrive at the lectern and the projection fails:

### Step 1 — Acknowledge calmly, do not panic

> *"It looks like the projection isn't working. That's fine — the talk doesn't depend on the slides. I'll deliver it from my notes."*

The audience is on your side. Equipment failures happen.

### Step 2 — Open the README on your phone

It's at `papers/codawork2026/talk/README.md`. Hold the phone in landscape mode for better reading. Brightness up.

### Step 3 — Use the README as the script

Each beat is a section in the README. The anchor phrase is bolded. The spoken text is in blockquotes. Read through them in order. Pause between beats.

### Step 4 — Describe what would have been on the slide

For each beat, after delivering the text, take 10 seconds to **describe the visual** the audience is missing:

- *"On the slide here you would have seen the simplex with the nine carrier vertices labelled — coal, gas, oil, nuclear, hydro, wind, solar, biomass, other."*
- *"The slide here shows the per-country step-Δ Aitchison distance time series for Japan; the 2011–2012 spike is the tallest bar by a factor of three."*
- *"The slide here is the three-conjunct MC-4 claim with the three conjuncts on separate lines."*

Each slide file in `slides/` has a **"visual described"** section specifically for this purpose. You can read it verbatim if you need to.

### Step 5 — Q&A from the phone

When questions come, navigate to `qa_bench/` and tap on the relevant card. Read the answer if you blank.

---

## What the audience experiences

A talk delivered from the README + phone is **slightly slower** than a talk with slides — about 1 to 2 minutes longer. Plan for that:

- If AV fails, drop **Cut 3** (the OWID 73-country slide in Beat 7) by default to recover time.
- If still running long, **shorten Beat 5** by skipping the static-trajectory description (still deliver the deceptive-drift result and the null caveat — those are load-bearing).

The audience will **remember the AV failure as professional handling, not as a problem**, if you stay calm. The talk's content is strong. The slides are decoration.

---

## What if your phone dies too

Belt-and-suspenders contingency:

1. The printed cheat sheet (`CHEAT_SHEET.md`) in your pocket. You can deliver the entire 15-minute talk from the cheat sheet alone — that's why the moot training exists.
2. If you've done the Round 5 stand-and-deliver in `STUDY_PAGE.md`, you can deliver the talk with **no notes at all.** The anchor phrases live in your head.

The training is the real backup. The phone is the convenient backup. The slides are nice-to-have.

---

## How to study from this folder, anywhere

Same folder. Different mode:

- **On a train:** open `STUDY_PAGE.md` on your phone. Run Round 1 (just the anchors) or Round 2 (anchor + sentence).
- **At a café:** open `slides/slide_NN_xxx.md` for one slide at a time. Read the visual + the spoken text. Try to deliver from memory.
- **Before bed:** open `CHEAT_SHEET.md`. Scan it slowly. The anchors will set in overnight.
- **Walking:** put the cheat sheet up on your phone, glance at one anchor every block.
- **Standing in line:** read one Q&A bench card.

The repo is the presentation **and** the study material. They are the same files. No translation step.

---

## One sentence to remember

> ***If the projector dies, you still have the talk. The talk lives in the README.***

---

*This file is the contingency manual. The cheat sheet is the lectern card. The study page is the prep guide. The README is the talk. All four work from a phone.*
