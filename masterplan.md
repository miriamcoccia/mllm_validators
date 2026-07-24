# Your schedule — 24 July to 3 September

---

## The one big checkpoint

Around **14 August**, exactly halfway through, you'll run a small
real test — a handful of real questions through real AI models, for
real money.

This one moment tells you: does everything actually work together?
And: how much will the whole project really cost?

**After that day, show your boss the real cost estimate and get
their okay before running the full, expensive version.**

This is the single most important day in the whole month. Everything
before it is building toward that test. Everything after it is
scaling that same, proven thing up.

---

## Week 1 — starting Friday 24 July: the empty, clean workspace

**What you're doing:** setting up your project folder properly —
git, your Python tool, a few safety-net files. No real project code
yet.

**Why this matters:** doing this now, while the folder is empty,
takes an afternoon. Doing it later, once the folder is full of real
code, takes much longer and risks breaking things.

**You'll know this week worked when:** you can hand your project
folder to someone else, and on their computer, one single command
gets it running and passing its checks.

---

## Week 2 — 27–31 July: the shared vocabulary, and loading real questions

**What you're doing:**

- Defining, clearly, the six things that make a test question good
  or bad.
- Defining what "a question" and "an AI's answer" mean in your code.
- Writing the part that loads your existing question dataset
  (ScienceQA) into your project.

**Why this matters:** everything you build afterward talks about
"questions" and "answers." Getting these definitions solid now means
you won't have to go back and fix five different files later because
they each described a question slightly differently.

**You'll know this week worked when:** you can load five real test
questions with their pictures into your code, cleanly, with nothing
missing.

---

## Week 3 — 3–7 August: breaking things on purpose

**What you're doing:** building the first two, easiest ways of
damaging a picture on purpose (making it blurry, and rotating it),
each at three strengths.

Then: **you stop and look at the damaged pictures with your own
eyes.** Twenty of them. Does "slightly damaged" actually look
slightly wrong? Does "very damaged" actually look obviously wrong?

Then: writing the actual message you'll send to the AI, asking it to
check a question.

**Why this matters:** this "look at them" moment is small, but it's
one of the most important checks in the whole project. If your
"slight damage" and "obvious damage" don't actually look different
from each other, your main result later will be a flat, meaningless
line instead of a clear, convincing trend. Ten minutes of looking now
protects weeks of later work.

**You'll know this week worked when:** the damaged pictures visibly
form a ladder — barely noticeable, then medium, then obviously wrong
— and you have a message template ready to send to an AI.

---

## Week 4 — 10–14 August: the first real conversation with an AI, and THE TEST

**What you're doing:**

- Connecting to one AI company (OpenAI) for real.
- Building the "receipt number and checklist" system, so nothing
  gets sent twice and nothing gets lost if you have to stop and
  restart.
- Setting up the cost-tracking logbook (MLflow).
- **Friday 14 August: running a small real test.** About 20 real
  questions, through one real AI model, for real money.

**Why this matters:** this is the day you find out if your whole plan
actually works, end to end, on real data — not just in theory. It's
also the day you learn your true cost per question, instead of an
estimate.

**You'll know this week worked when:** you've sent real questions to
a real AI, gotten real answers back, and you can see the real cost
of that small test in your logbook.

**This is the halfway point of your month.** After this Friday, talk
to your boss with your real numbers before scaling up.

---

## Week 5 — 17–21 August: filling out the rest

**What you're doing:**

- Building the remaining four ways of damaging a question (clutter,
  irrelevant pictures, fairness bias, mismatched text-and-picture).
- Connecting to the other two AI companies (Nebius, Anthropic).
- Making the whole system properly robust — so that if part of a
  batch fails or comes back incomplete, it quietly retries just that
  part, without redoing everything.

**Why this matters:** this is where the small, proven system from
Week 4 gets widened out to the full scope of the project — more
kinds of damage, more AI companies to compare.

**You'll know this week worked when:** you have all six kinds of
damage, at all three strengths, and all three AI companies connected
and working.

---

## Week 6 — 24–28 August: the real, full run

**What you're doing:**

- Monday: double-check the full plan and its estimated cost one
  more time before committing.
- Then: kick off the real, full experiment — all your questions, all
  six kinds of damage, all three AI companies. This runs in the
  background over several days while you also start turning the
  first results into numbers.
- Turning the AI's answers into precision/recall/F1 numbers, and
  into the "does accuracy improve as damage gets more obvious" chart
  — your paper's main result.

**Why this matters:** this is the actual experiment. Everything up to
now was building the machine that runs it.

**You'll know this week worked when:** the full run has finished, and
you have real numbers and a real chart in front of you.

---

## Week 7 — 31 August – 3 September: tables, polish, and stop

**What you're doing:**

- Turning your numbers into properly formatted tables and charts,
  automatically, so you never have to hand-copy a figure.
- Writing a clear README explaining what the project does and how to
  run it.
- One final full check: does the whole thing still work cleanly from
  a completely fresh start?
- **Thursday 3 September is a genuine spare day.** Use it to catch up
  on anything that slipped, or just to breathe before you leave.

**You'll know this month worked when:** one single command produces
every table and chart you'll need, and the project would make sense
to someone opening it for the first time.

---

## If you fall behind

Falling a little behind is normal — it doesn't mean the plan failed.
If it happens, cut things in exactly this order, and stop cutting the
moment you're caught up again:

1. Skip the fourth AI company — you already weren't planning to add
   it yet.
2. Skip the hardest, riskiest kind of damage (the subtle
   text-picture edit) — ship the easier version of it instead.
3. Skip one of the fancier statistical tests — keep the simpler one.
4. Skip one extra chart — keep the main "accuracy vs damage severity"
   one, since that's the one that matters most.

**Never cut:** the small checks you write alongside your code, the
"stop and look at 20 damaged pictures" moment, and the halfway test
on 14 August. Those three things are what stop small mistakes from
turning into big, late discoveries.

---

## The two things to remember all month

1. **Don't build everything before you've tested anything.** Build a
   small working piece, test it for real, then widen it out. That's
   why 14 August exists.

2. **Your results files are the real truth. The cost logbook is just
   a summary.** If they ever disagree, trust the results files.