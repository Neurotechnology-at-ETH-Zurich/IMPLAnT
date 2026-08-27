---
title: During surgery
parent: Tutorials
nav_order: 2
---

# During surgery

On the day of surgery, real bregma/lambda measurements taken on the animal rarely match exactly what was picked on the pre-op MRI. **File → During Surgery** loads the saved report PDF, locates and loads the corresponding scan automatically, and lets you correct bregma/lambda from your manipulator's measured values to get an updated target position (in mm) for each shank.

```
 Pre-op                                    Surgery day
┌──────────────┐    ┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│ Load MRI +   │───▶│ Save         │─────▶│ During       │───▶│ Measure &    │
│ plan shanks  │    │ Trajectory   │      │ Surgery:     │    │ correct      │
│ (bregma/     │    │ Report       │      │ pick the PDF │    │ bregma/      │
│ lambda,      │    │ (one PDF)    │      │              │    │ lambda       │
│ insertion    │    │              │      │              │    │              │
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

Click **During Surgery** in the menu. This opens a file picker — select the saved [Trajectory Report](pre-surgical-planning) PDF. From there it's fully automatic:

- The corresponding MRI scan is located and loaded (reusing the registration already done pre-op, so this is fast).
- The Surgery tab opens, showing the loaded plan's shanks in both a 3D reference view and a 2D axial slice view.
- If the PDF and the scan aren't in the same folder anymore, or the PDF predates this feature, you'll get a clear error instead of a silent failure — re-save the report if needed, or load the MRI manually via Pre-surgical Planning first.

## 2. Measure and correct bregma/lambda

This is the actual point of the Surgery tab. The pre-op plan picked bregma/lambda **on the MRI** — on the day, the surgeon locates them physically, on the animal, using the stereotaxic manipulator zeroed at an arbitrary reference point ("null point"). Those two measurements rarely match exactly.

Type the measured values into the **Bregma** and **Lambda** groups — **Sag / Cor / Ax**, in mm, signed (negative values are expected and fine). These are offsets from your manipulator's null point, not anything picked on the MRI.

{: .warning }
**Before trusting this on a real animal**, run the built-in sanity check once. Enter the *original* planned bregma/lambda mm values (found in the saved plan) as if they were the measured ones — the target table should reproduce the original plan exactly. This validates the pipeline independent of any question about your rig's specific axis/sign conventions.

## 3. Read the results

- **The target table** (Sag / Cor / Ax per shank) updates live as you type — these are the numbers to dial into the manipulator to reach each shank's planned target, re-anchored to your measured bregma/lambda.
- **The 3D view** shows the *original* planned shank positions and bregma/lambda for visual reference — it does **not** update with your correction (there's no way to place the manipulator's null point inside the MRI's own coordinate space, so this is orientation only, not a live preview of the correction).
- **The axial slice view** lets you scroll through the scan depth-by-depth (zoom/pan/fit buttons, a minimap, a scale bar), with each shank drawn dim where it doesn't reach the current slice and bold where it does — useful for visually confirming a shank's actual depth and trajectory against the real anatomy.

## Troubleshooting

- **"No trajectory data found"** — the PDF was saved before this feature existed, or isn't a trajectory report. Re-save the report from Pre-surgical Planning.
- **"MRI scan not found" / can't auto-load** — the PDF and the MRI scan are no longer in the same folder, or the animal's `ind_N` id couldn't be matched to exactly one file there. Load the MRI manually first.
- **Numbers look mirrored or backwards** — run the sanity check in step 2 first; if a specific axis is consistently flipped, that's a fixed, known adjustment for your rig rather than something to mentally invert every time.

---

Next: [Post-implant localisation](post-implant-localisation)
