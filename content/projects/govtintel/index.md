---
title: "GovIntel"
slug: "govtintel"
date: 2026-04-01
draft: false
description: "A local-first federal procurement intelligence RAG system that turns USAspending contract awards into citation-grounded market briefs."
tags: ["rag", "retrieval", "fastapi", "streamlit", "python"]
cover:
  image: "https://raw.githubusercontent.com/sahaavi/GovtIntel/main/docs/assets/govintel-ui.png"
  alt: "GovIntel Streamlit UI showing a generated procurement intelligence brief"
  relative: false
  hiddenInList: true
weight: 2
showToc: true
---

## Overview

**GovIntel** is a local-first federal procurement intelligence system. It imports public USAspending contract awards, stores them in PostgreSQL, builds a Chroma-backed retrieval index, and generates citation-grounded market briefs through a FastAPI API and Streamlit UI.

I built GovIntel as a reviewable RAG application with ingestion, indexing, retrieval, analytics, generation, citation checks, Dockerized local setup, CI, tests, and a walkthrough.

## Links

- [GitHub Repository](https://github.com/sahaavi/GovtIntel)
- [UI Walkthrough](https://youtu.be/-qqBq8bCaSg)

## Status

GovIntel provides a reviewable end-to-end path: seed contract data, build the retrieval index, run the FastAPI service, open the Streamlit UI, ask a procurement question, and inspect cited award evidence.

I focused this portfolio version on engineering completeness: local setup, retrieval, generation, citation checks, tests, and a walkthrough, rather than production hosting or benchmark claims.

## Review Path

The walkthrough shows agency and NAICS inputs, a 1-10 year range control, a DHS cybersecurity question, a generated brief, and cited contract evidence. For hands-on review, the repository documents local setup through `make db-up`, `make db-seed`, `make index`, `make run`, and `make ui`.

## Problem

Federal procurement data is useful but hard to scan quickly. The goal of GovIntel is to turn contract records into structured intelligence briefs: contractor patterns, agency spending questions, strategic implications from contractor rankings, quarterly spend trends, concentration, and cited award evidence.

## What I Built

- Async USAspending award ingestion with pagination and idempotent PostgreSQL upserts
- Typed Pydantic models for awards, analysis requests, contractor summaries, retrieved evidence, and generated briefs
- Chroma-backed vector indexing with sentence-transformer embeddings
- BM25 keyword retrieval, vector retrieval, hybrid merge, and cross-encoder reranking
- SQL analytics for top contractors, quarterly spend trends, and market concentration
- Versioned prompt templates and structured JSON generation
- Fail-closed citation validation before returning a brief
- FastAPI `/api/v1/analyze` endpoint with optional `X-API-Key` protection
- Streamlit UI for choosing filters, generating briefs, and inspecting cited contract evidence
- Docker Compose stack for PostgreSQL, the API, and the UI

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Pydantic v2
- **Data:** PostgreSQL 16, SQLAlchemy asyncio, asyncpg
- **Retrieval:** ChromaDB, sentence-transformers, BM25, hybrid retrieval, cross-encoder reranking
- **Generation:** Gemini provider path, structured JSON prompts, optional Hugging Face provider path
- **Frontend:** Streamlit
- **Operations:** Docker Compose, GitHub Actions, Ruff, mypy, pytest, pytest-cov
- **Optional extensions:** Langfuse tracing, Pinecone mirroring, offline evaluation and QLoRA utilities

## Architecture

The system flow is:

1. Pull bounded USAspending award data into normalized contract models.
2. Persist contract rows in PostgreSQL.
3. Build local retrieval indexes with Chroma vector search and BM25 keyword search.
4. Merge and rerank retrieval candidates.
5. Compute SQL analytics for contractor ranking, spend trend, and market concentration.
6. Render a procurement-intelligence prompt with retrieved context and analytics.
7. Generate a structured brief through the selected provider.
8. Validate citations against retrieved contract evidence before returning the answer.
9. Serve results through FastAPI and the Streamlit UI.

## Engineering Highlights

- **End-to-end application path** with ingestion, indexing, API, Streamlit UI, evidence inspection, and regression tests
- **Guarded RAG design** that rejects briefs whose citation list references award IDs outside the retrieved contract evidence
- **Hybrid retrieval stack** combining lexical recall, vector retrieval, deduplication, and reranking
- **Structured analytics layer** for contractor rankings, spend trends, and market concentration
- **Provider boundaries** that keep external LLM use explicit and configurable
- **Quality gates** through Ruff, strict mypy, and pytest with a 90% coverage threshold across API, retrieval, generation, ingestion, frontend, evaluation, observability, and training tests

## Evaluation and Quality

GovIntel includes evaluation fixtures and an ablation harness; I use them as methodology evidence rather than headline quality claims.

## Why It Matters

GovIntel demonstrates my RAG and data-systems work: retrieval, structured generation, analytics, citation validation, API design, local deployment, and evaluation scaffolding over real procurement data.
