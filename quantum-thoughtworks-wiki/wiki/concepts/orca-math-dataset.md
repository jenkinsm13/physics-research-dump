---
title: "Orca Math Dataset"
created: 2026-04-06
updated: 2026-04-06
tags: [dataset, ML, finetuning, math, training-data]
sources: ["[[Autoencoder Experiments]]"]
---

# Orca Math Word Problems Dataset (200K)

A 773 MB training dataset stored in `raw/Chrotonics/orca-math-word-problems-200k/`, likely downloaded for **LLM fine-tuning experiments**.

## Contents

| File | Format | Purpose |
|------|--------|---------|
| `orca-math-word-problems-200k.jsonl` | JSONL | Full 200K problem set |
| `orca-math-word-problems-200k-converted.jsonl` | JSONL | Converted format |
| `orca-math-word-problems-200k-converted-train-test.jsonl` | JSONL | Train/test split |
| `orca-math-word-problems-200k-converted-validate.jsonl` | JSONL | Validation split |
| `orca-math-word-problems-11k-converted-train/` | Directory | Smaller 11K subset |
| `orca-math-word-problems-11k-converted-train.jsonl` | JSONL | 11K training set |
| `train-00000-of-00001.parquet` | Parquet | Parquet format copy |
| `convert_format.py` / `convert.py` | Python | Conversion scripts |
| `How_to_count_tokens_with_tiktoken.ipynb` | Notebook | Token counting guide |

## Likely Purpose

Given this is stored alongside the [[Autoencoder Experiments]] and other ML work in the Chrotonics directory, this dataset was likely downloaded for:
1. Fine-tuning a local LLM (via [[Unhinged Mode]] or similar Ollama-based pipeline) on mathematical reasoning
2. Evaluating model performance on structured word problems
3. Token counting experiments (as suggested by the tiktoken notebook)

## Disk Note

> [!warning] Large Dataset
> At 773 MB, this is the largest single item in the raw/ directory. Consider whether it should be archived to external storage rather than remaining on the internal SSD when `raw/` is deleted.

## Related Articles

- [[Autoencoder Experiments]] -- ML experiments in the same directory
- [[Unhinged Mode]] -- local LLM pipeline

## Sources

- `raw/Chrotonics/orca-math-word-problems-200k/`
