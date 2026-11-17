---
title: "Detecting AI-Generated Humans via Novel Image Processing Techniques"
author: David Stump ASC BVK, Jonathan Banta, and Michael Jenkins
created: 2026-04-06
updated: 2026-04-06
tags: [paper, deepfake-detection, image-processing, AI-detection, sora, jenkins-transform]
sources:
  - "raw/LaTeX/DARPA/AI_detection.tex"
  - "raw/LaTeX/DARPA/AI_detection_v2.tex"
  - "raw/Chrotonics/Deepfake Detection/Sora/research/AI_detection.tex"
---

# Detecting AI-Generated Humans via Novel Image Processing Techniques

**David Stump ASC BVK, Jonathan Banta, and Michael Jenkins**

## Abstract

This paper presents a novel mathematical operation for image processing that highlights multiple features useful for detecting AI-generated humans. The operation reveals a clear blocky digital noise pattern in areas that should have organic, "shelved" noise patterns, in addition to other inconsistencies like inaccurate exposure and lack of fine details in areas like the sclera. The transformed and enhanced images provide a foundational basis for identifying fake content.

## Methodology

1. **Data Collection**: AI video from Sora and recreated video using DaVinci Resolve with 8.3K RAW camera
2. **Preprocessing**: Cropping, stabilization, and color matching
3. **Novel Transform and Convolution Kernel Enhancement**: Application of [[Jenkins Transform]]-based image processing technique

## Key Findings

- AI-generated images show blocky digital noise where organic "shelved" noise patterns should exist
- Exposure inconsistencies detectable after transformation
- Lack of fine details in areas like the sclera
- Technique applicable to both still images and temporal (video) data

---

## Related Concepts

- [[Deepfake Detection]]
- [[Jenkins Transform]]
