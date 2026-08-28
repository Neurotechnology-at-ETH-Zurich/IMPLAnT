---
title: During surgery
parent: Tutorials
nav_order: 2
---

# During surgery

On the day of surgery, real bregma/lambda measurements taken on the animal rarely match exactly what was picked on the pre-op MRI. **File → During Surgery** lets you pick up a saved plan and correct bregma/lambda from your manipulator's measured values to get an updated target position (in mm) for each shank.

```
 Pre-op                                    Surgery day
┌──────────────┐    ┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│ Load MRI +   │───▶│ Save         │─────▶│ During       │───▶│ Measure &    │
│ plan shanks  │    │ Trajectory   │      │ Surgery:     │    │ correct      │
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

## 1. Load the plan

Click **During Surgery** in the menu. This opens the same **Load Previous Session** picker used throughout the app — pick a prior surgery session from the list, or use **Load New File...** to browse for the saved [Trajectory Report](pre-surgical-planning) PDF instead. From there it's fully automatic:

- The Surgery tab opens immediately, showing the plan's shanks marked on a fixed dorsal skull reference photo (Bregma in red, Lambda in blue, each shank's planned insertion point in its own color) — this needs no MRI file at all.
- In the background, IMPLAnT also tries to locate the corresponding resampled MRI scan (reusing the registration already done pre-op) to additionally render the original planned trajectories in 3D. This is best-effort: if the PDF and the scan are no longer in the same folder, the 3D view is simply left empty — it doesn't block or error out, since the skull-photo view and the numeric target table are what the Surgery tab is actually for.

## 2. Measure and correct bregma/lambda

This is the actual point of the Surgery tab. The pre-op plan picked bregma/lambda **on the MRI** — on the day, the surgeon locates them physically, on the animal, using the stereotaxic manipulator zeroed at an arbitrary reference point ("null point"). Those two measurements rarely match exactly.

Type the measured values into the **Bregma** and **Lambda** groups — **RL / AP**, in mm, signed (negative values are expected and fine). These are offsets from your manipulator's null point, not anything picked on the MRI. There's no third (depth) field here — depth is carried over from the pre-op plan unchanged, since there's no intraoperative measurement to re-level it against.

{: .warning }
**Before trusting this on a real animal**, run the built-in sanity check once. Enter the *original* planned bregma/lambda mm values (found in the saved plan) as if they were the measured ones — the target table should reproduce the original plan exactly. This validates the pipeline independent of any question about your rig's specific axis/sign conventions.

## 3. Read the results

- **The target table** (RL / AP per shank) updates live as you type — these are the numbers to dial into the manipulator to reach each shank's planned target, re-anchored to your measured bregma/lambda.
- **The 3D view** (when the MRI could be located) shows the *original* planned shank positions and bregma/lambda for visual reference — it does **not** update with your correction (there's no way to place the manipulator's null point inside the MRI's own coordinate space, so this is orientation only, not a live preview of the correction).
- **The skull reference photo** shows Bregma, Lambda, and each shank's planned insertion point at a glance, plus a black dot for your manipulator's null point once you've entered measured values — a quick visual sanity check, though it's a fixed generic reference image, not the animal's own anatomy.

## Troubleshooting

- **"No trajectory data found"** — the PDF was saved before this feature existed, or isn't a trajectory report. Re-save the report from Pre-surgical Planning.
- **3D view stays empty** — the PDF and the MRI scan are no longer in the same folder, or the animal's `ind_N` id couldn't be matched to exactly one file there. This doesn't block anything else — the skull-photo view and target table still work without it; load the MRI manually via Pre-surgical Planning first if you specifically need the 3D reference.
- **Numbers look mirrored or backwards** — run the sanity check in step 2 first; if a specific axis is consistently flipped, that's a fixed, known adjustment for your rig rather than something to mentally invert every time.

---

Next: [Post-implant localisation](post-implant-localisation)
