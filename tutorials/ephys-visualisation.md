---
title: Electrophysiology visualisation
parent: Tutorials
nav_order: 4
---

# Electrophysiology visualisation

1. Load your recording via **File → Load ephys data**.
2. Channels are displayed with their anatomical labels from the [localisation step](post-implant-localisation), allowing direct comparison of signal traces across brain regions.
3. Use the **Ephys Analysis** menu for signal analysis: **Theta Detection** and **Rippl AI** run detection directly on the loaded recording, and **Show Spiking Raster Plot** overlays externally computed spike-sorting results (a JRCLUST `_res.mat` file). The tab also includes per-channel spectrogram, all-channel spectrogram, hierarchical spike-count correlation, and current source density (CSD) views.
4. Use **Export Plots...** to save any combination of the raw/LFP trace, spike raster, spectrogram, current source density, and channel spectrogram views as image files to a folder of your choice.
5. Further preprocessing and analysis features are planned for future releases.

![Screenshot of IMPLAnT's electrophysiology visualisation tab, showing a 3D rendering of implanted electrode shanks next to colour-coded raw signal traces labelled by brain region](../assets/images/Ephys.png)

![Animated demo of IMPLAnT's electrophysiology visualisation tab, browsing channel-by-channel signal traces linked to their atlas region labels](../assets/images/output.gif)

**Ephys Analysis** — theta-event detection, ripple detection (Rippl AI), current source density, and spike-raster/correlation/spectrogram views:

<video src="../assets/videos/Ephys_Analysis_Demo.mp4" controls muted loop playsinline style="max-width:100%"></video>
