---
title: "Tokenizer From Scratch: BPE as Learned Compression"
slug: "llm-engineering-from-scratch-tokenizer"
date: 2026-06-30
lastmod: 2026-06-30
draft: false
description: "A beginner-friendly walkthrough of byte-level BPE, starting from a tiny toy example and ending with a runnable tokenizer, labeled charts, and an optional merge microscope."
summary: "A toy-example-first introduction to tokenization and byte-level BPE, followed by a small runnable tokenizer and optional deeper artifact exploration."
tags: ["tokenization", "bpe", "llm-engineering", "python", "from-scratch"]
categories: ["AI Engineering"]
series: ["LLM Engineering From Scratch"]
level: "beginner"
project: "llm-engineering-from-scratch"
repo: "https://github.com/sahaavi/llm-engineering-from-scratch"
cover:
  image: "cover.png"
  alt: "Colored token tiles representing byte-pair encoding merges"
  relative: true
author: "Avishek Saha"
showToc: true
tocOpen: true
math: false
---

## Why Tokenization Exists

Language models do not read raw text directly. They read token ids.

That means every model needs a translation layer that turns text into tokens first. This translation layer is the tokenizer.

That step matters more than it first appears. A tokenizer affects:

- how much text fits into context
- how rare words get broken apart
- how code and punctuation are preserved
- how multilingual text and emoji are represented

This project builds a tiny tokenizer by hand so the mechanism becomes visible instead of hidden behind a library.

## Toy BPE First

Byte-pair encoding, or BPE, starts with small pieces and learns larger pieces from repetition.

Take a toy example:

```text
low lower lowest
```

The teaching version of BPE asks one question again and again:

> Which adjacent pair appears most often?

If the answer is `l` + `o`, merge that pair into a larger piece. Then count pairs again on the updated sequence. Repetition keeps turning small pieces into larger reusable chunks.

The important shift is this: BPE is not "finding words." It is learning compression shortcuts from neighboring symbols.

That toy version is enough to understand the algorithm:

1. Start with small pieces.
2. Count adjacent pairs.
3. Merge the most frequent pair.
4. Repeat.

## From Toy BPE To Byte-Level BPE

The real project uses the same idea, but the starting pieces are not toy character fragments. They are raw UTF-8 bytes.

That one choice makes the tokenizer robust:

- every string can be represented
- accented text stays representable
- emoji stay representable
- multilingual text stays representable

Byte-level BPE keeps the toy algorithm but swaps in a better foundation for real text.

## A Minimal Tokenizer

The beginner-facing core for this project now lives in:

- [Tokenizer core](https://github.com/sahaavi/llm-engineering-from-scratch/blob/main/projects/01-tokenizer-from-scratch/tokenizer.py)
- [Project runner](https://github.com/sahaavi/llm-engineering-from-scratch/blob/main/projects/01-tokenizer-from-scratch/main.py)

The core idea is small enough to summarize in four moves:

1. Turn text into bytes.
2. Count adjacent byte pairs.
3. Merge the most frequent pair.
4. Replay the learned merges to encode new text.

The code snippet that matters most is the pair counter:

```python
counts.update(zip(sequence, sequence[1:]))
```

And the next crucial step is the merge pass:

```python
if index + 1 < len(sequence) and (sequence[index], sequence[index + 1]) == pair:
    merged.append(sequence[index] + sequence[index + 1])
```

Encoding is just the same merge logic replayed on new text. Decoding joins the learned byte pieces back together.

That is why the project can stay small and still feel complete: training learns the merges, encoding reuses them, and decoding proves the text can come back intact.

## What Changes On Real Inputs

The tokenizer was run on a few input types that beginners usually wonder about first:

- common text
- rare text
- code
- math notation
- emoji
- multilingual text

The pattern is consistent:

- common repeated text compresses better
- rare text often falls back to smaller pieces
- code keeps punctuation and spacing
- multilingual text and emoji can still round-trip correctly even when the individual pieces look awkward

That leads to the key lesson:

**byte-level BPE is robust because it can represent anything, but it only compresses patterns it has learned.**

Another useful distinction is:

- **Reversibility:** can the original text be recovered exactly?
- **Readability:** do the intermediate token pieces look nice to a human?

Byte-level tokenization optimizes for reversibility first.

## Explore Further

The rest of the project is there for deeper inspection, not for first-pass understanding.

`metrics.json` stores the per-example counts used to compare vocabulary sizes across the same set of inputs.

`trace.json` stores the merge-by-merge training history used by the interactive widget.

The first chart compares the same examples under two tokenizer vocabulary sizes. Fewer tokens per character means the tokenizer learned larger reusable pieces for that kind of text.

![Compression ratio chart](https://raw.githubusercontent.com/sahaavi/llm-engineering-from-scratch/main/projects/01-tokenizer-from-scratch/artifacts/compression_ratio.png)

The second chart counts how many learned token pieces are 1 byte long, 2 bytes long, and so on.

![Token length distribution](https://raw.githubusercontent.com/sahaavi/llm-engineering-from-scratch/main/projects/01-tokenizer-from-scratch/artifacts/token_length_distribution.png)

The interactive widget is an optional way to look under the hood and replay the merge history step by step.

<iframe
  title="BPE Merge Microscope"
  src="/demos/bpe-merge-microscope/"
  style="width: 100%; min-height: 760px; border: 1px solid var(--border); border-radius: 8px; background: var(--entry);"
  loading="lazy">
</iframe>

## Further Resources

- [Andrej Karpathy: Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)
- [Companion Colab notebook](https://colab.research.google.com/drive/1y0KnCFZvGVf_odSfcNAws6kcDD7HsI0L?usp=sharing)
- [karpathy/minbpe](https://github.com/karpathy/minbpe)

## Links

- [GitHub repository](https://github.com/sahaavi/llm-engineering-from-scratch)
- [Tokenizer project folder](https://github.com/sahaavi/llm-engineering-from-scratch/tree/main/projects/01-tokenizer-from-scratch)
- [Project hub](/projects/llm-engineering-from-scratch/)
- [Standalone BPE Merge Microscope](/demos/bpe-merge-microscope/)
