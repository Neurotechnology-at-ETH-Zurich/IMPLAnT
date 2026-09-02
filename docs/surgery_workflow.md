# From Pre-op Planning to the Operating Room

This walks through the full lifecycle of a trajectory plan: designing it on
an MRI scan before surgery, handing it off as a single file, and using it
on surgery day to get exact manipulator coordinates from real, measured
landmarks. Every screen along the way also has its own "?" button with
step-by-step instructions — this page is the map connecting those screens,
not a replacement for them.

```
 Pre-op                                    Surgery day
┌──────────────┐    ┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│ Load MRI +   │───▶│ Save         │─────▶│ Intra        │───▶│ Measure &    │
│ plan shanks  │    │ Trajectory   │      │ operative:   │    │ correct      │
│ (bregma/     │    │ Report       │      │ pick session │    │ bregma/      │
│ lambda,      │    │ (one PDF)    │      │ or PDF       │    │ lambda       │
│ insertion    │    │              │      │              │    │ (RL/AP)      │
│ points)      │    │              │      │              │    │              │
└──────────────┘    └──────────────┘      └──────────────┘    └──────┬───────┘
                                                                       ▼
                                                              ┌──────────────┐
                                                              │ Read target  │
                                                              │ mm per shank,│
                                                              │ dial into    │
                                                              │ manipulator  │
                                                              └──────────────┘
```

## 1. Pre-op: plan the trajectory

Use **Pre-surgery Planning** to load the animal's MRI and place each
shank's insertion and deepest point, same as always. This step is entirely
unchanged and has its own in-app instructions (the "?" button on that
page) — the only thing worth calling out here is that **the resulting
plan is what everything downstream is built from**, including the exact
numbers the surgery-day view will show you.

## 2. Save a Trajectory Report

Once the plan looks right, save it via the report button. This produces a
single PDF that does two things at once:

- **A human-readable report** — one page per shank (coronal/sagittal views
  with a numeric caption), a shank geometry page, and a summary page.
- **A machine-readable copy of the plan**, embedded invisibly inside the
  same PDF (a JSON attachment) — this is what the Intraoperative tab actually
  reads back on surgery day. You never interact with this directly; it's
  just why the PDF is a self-contained handoff artifact rather than the
  human-readable pages being the only thing that exists.

The PDF is named after the animal (e.g. `trajectory_planning-sub-X-ind_2.pdf`)
and, **importantly, is saved in the same folder as the MRI scan it came
from** — the Intraoperative tab locates the scan automatically using that folder
plus the animal's `ind_N` id, so keeping the PDF alongside the scan (not
moved to some other folder) is what makes surgery day a one-click load.

## 3. Intraoperative: load the plan

Click **Intraoperative** in the menu. This opens the same **Load Previous
Session** picker used throughout the app — pick a prior surgery session
from the list, or use **Load New File...** to browse for the saved report
PDF instead. From there it's fully automatic:

- The Intraoperative tab opens immediately, showing the plan's shanks marked on
  a fixed dorsal skull reference photo (Bregma in red, Lambda in blue,
  each shank's planned insertion point in its own color) — this needs no
  MRI file at all.
- In the background, IMPLAnT also tries to locate the corresponding
  resampled MRI scan (reusing the registration already done pre-op) to
  additionally render the original planned trajectories in 3D. This is
  best-effort: if the PDF and the scan are no longer in the same folder,
  the 3D view is simply left empty — it does not block or error out,
  since the skull-photo view and the numeric target table are what the
  Intraoperative tab is actually for.

## 4. Measure and correct bregma/lambda

This is the actual point of the Intraoperative tab. The pre-op plan picked
bregma/lambda **on the MRI** — on the day, the surgeon locates them
physically, on the animal, using the stereotaxic manipulator zeroed at an
arbitrary reference point ("null point"). Those two measurements rarely
match exactly.

Type the measured values into the **Bregma** and **Lambda** groups —
**RL / AP**, in mm, signed (negative values are expected and fine). These
are offsets from your manipulator's null point, not anything picked on
the MRI. There is no longer a third (depth/DV) field here — depth is
carried over from the pre-op plan unchanged, since there's no
intraoperative measurement to re-level it against.

> **Before trusting this on a real animal**: run the built-in sanity
> check once. Enter the *original* planned bregma/lambda mm values
> (found in the saved plan) as if they were the measured ones — the
> target table should reproduce the original plan exactly. This validates
> the pipeline independent of any question about your rig's specific
> axis/sign conventions.

## 5. Read the results

- **The target table** (RL / AP per shank) updates live as you type —
  these are the numbers to dial into the manipulator to reach each
  shank's planned target, re-anchored to your measured bregma/lambda.
- **The 3D view** (when the MRI could be located) shows the *original*
  planned shank positions and bregma/lambda for visual reference — it
  does **not** update with your correction above (there's no way to place
  the manipulator's null point inside the MRI's own coordinate space, so
  this is orientation only, not a live preview of the correction).
- **The skull reference photo** shows Bregma, Lambda, and each shank's
  planned insertion point at a glance, plus a black dot for your
  manipulator's null point once you've entered measured values — useful
  as a quick visual sanity check, though it's a fixed generic reference
  image, not the animal's own anatomy.

## Troubleshooting

- **"No trajectory data found"** — the PDF was saved before this feature
  existed, or isn't a trajectory report. Re-save the report from
  Pre-surgery Planning.
- **3D view stays empty** — the PDF and the MRI scan are no longer in the
  same folder, or the animal's `ind_N` id couldn't be matched to exactly
  one file there. This doesn't block anything else — the skull-photo view
  and target table still work without it; load the MRI manually via
  Pre-surgery Planning first if you specifically need the 3D reference.
- **Numbers look mirrored or backwards** — the manipulator's own axis
  identity/sign conventions haven't been independently verified against
  every physical rig. Run the sanity check in step 4 first; if a specific
  axis is consistently flipped, that's a fixed, known adjustment — flag it
  so it can be corrected in code rather than mentally inverting it every
  time.
