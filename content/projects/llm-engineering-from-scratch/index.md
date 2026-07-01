---
title: "LLM Engineering From Scratch"
slug: "llm-engineering-from-scratch"
date: 2026-06-30
draft: false
description: "A project-first learning series that rebuilds LLM mechanics from tokenization to evaluation with runnable code, plots, failures, and interactive demos."
tags: ["llm-engineering", "machine-learning", "python", "from-scratch", "ai-engineering"]
cover:
  image: "cover.png"
  alt: "Abstract BPE token tiles used as the cover for LLM Engineering From Scratch"
  relative: true
weight: 3
showToc: true
---

## Overview

**LLM Engineering From Scratch** is a public learning series that rebuilds core LLM mechanics one project at a time. Each project pairs a small runnable implementation with plots, stress cases, explanations, and a reproducible artifact.

Roadmap inspiration: [Ahmad Osman](https://x.com/TheAhmadOsman) ([@TheAhmadOsman](https://x.com/TheAhmadOsman)) and his article, ["Step-By-Step LLM Engineering Projects (2026 Edition)"](https://x.com/TheAhmadOsman/article/2058745340895870985). The repository uses the article as a roadmap reference; the implementations, experiments, traces, demos, and writeups are independent.

## Links

- [GitHub Repository](https://github.com/sahaavi/llm-engineering-from-scratch)
- [Tokenizer From Scratch Blog Post](/posts/llm-engineering-from-scratch-tokenizer/)
- [BPE Merge Microscope Demo](/demos/bpe-merge-microscope/)

## Status

The first project, **Tokenizer From Scratch**, is implemented with a byte-level BPE tokenizer, deterministic artifacts, and an interactive static demo. The planned sequence continues through embeddings, positional methods, attention, Transformer blocks, training loops, and objectives.

## Series Pattern

Each project ships five kinds of evidence:

1. **Implementation** - readable Python from scratch.
2. **Notebook** - a runnable experiment and explanation path.
3. **Plots** - charts that show behavior instead of only claiming it.
4. **Failure gallery** - examples where the implementation gets stressed.
5. **Article/demo** - a technical post with an interactive or visual artifact.

## Roadmap

| # | Project | Hard concept | Status |
|---:|---|---|---|
| 1 | Tokenizer from scratch | Tokenization is a learned compression tradeoff. | Implemented |
| 2 | One-hot vectors and learned embeddings | IDs gain meaning through learned vector geometry. | Planned |
| 3 | Positional methods | Attention needs order. | Planned |
| 4 | Scaled dot-product attention | Attention is weighted retrieval from context. | Planned |
| 5 | Multi-head attention | Heads can learn different relational patterns. | Planned |
| 6 | One decoder block | LLM behavior emerges from interacting parts. | Planned |
| 7 | Mini-former | The training loop is the lesson. | Planned |
| 8 | Language-model objectives | Objective choice shapes capabilities and failures. | Planned |

## Why It Matters

Frameworks are useful, but they can hide the mechanisms that make LLM systems work or fail. This series makes those mechanisms visible through code, plots, traces, failure cases, and short explanations that compound into a deeper engineering foundation.
