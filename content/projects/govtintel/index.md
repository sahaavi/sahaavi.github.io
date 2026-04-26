---
title: "GovtIntel"
slug: "govtintel"
date: 2026-04-01
draft: false
description: "An in-progress federal procurement intelligence RAG system for contract analysis, currently at ingestion, retrieval, API, prompt, and evaluation scaffolding stage."
tags: ["rag", "retrieval", "fastapi", "python", "in-progress"]
cover:
  image: ""
  alt: "GovtIntel"
  relative: true
weight: 2
showToc: true
---

## Status

**GovtIntel is in progress.** It should be read as a current build, not as shipped product proof yet.

The current repository has the structure for a federal procurement intelligence engine: ingestion modules, BM25 and vector retrieval scaffolding, prompt templates, FastAPI routes, typed models, and tests. The analysis endpoint is still a stub while the full RAG pipeline, demo, and evaluation suite are being completed.

## What It Is For

Federal procurement data is useful but hard to scan quickly. The goal of GovtIntel is to turn contract records into structured intelligence briefs: contractor patterns, agency spending questions, market-entry signals, and evidence-backed answers over procurement data.

## Current Build

- USAspending ingestion scaffolding
- BM25 retrieval and vector retrieval modules
- FastAPI application and `/api/v1/analyze` route
- Prompt templates for procurement intelligence answers
- Test coverage for ingestion, retrieval, generation prompts, models, and API routes

## Truth Boundary

This project is not positioned as a shipped flagship. Until there is a working demo and evaluation evidence, the honest framing is:

- **In progress**
- **RAG/procurement intelligence system**
- **Repository shows architecture and implementation scaffolding**
- **Not yet a completed public product**

## Tech Stack

- Python
- FastAPI
- Pydantic
- BM25 retrieval
- Vector retrieval scaffolding
- Prompt templates
- pytest

## Links

- [GitHub Repository](https://github.com/sahaavi/GovtIntel)

## Next Milestones

- Wire the analysis route to the full RAG pipeline
- Add a small reproducible demo dataset
- Publish retrieval and answer-quality evaluation results
- Add a case-study walkthrough once the demo is reliable
