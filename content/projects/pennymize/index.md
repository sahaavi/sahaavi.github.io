---
title: "Pennymize — AI-Powered Personal Finance"
date: 2024-08-01
draft: false
description: "A personal finance SaaS for Canadian users with AI-driven expense categorization, budget forecasting, and RAG-based financial advice."
tags: ["ai-agents", "rag", "django", "python", "fintech"]
cover:
  image: ""
  alt: "Pennymize"
  relative: true
weight: 2
showToc: true
---

## Overview

**Pennymize** is a personal finance SaaS application designed for Canadian users. It combines traditional budgeting tools with AI-powered features for expense categorization, investment optimization, and personalized financial advice.

## Problem

Existing personal finance apps don't serve Canadian users well — they lack support for Canadian banks, tax structures (TFSA, RRSP), and the specific financial landscape. Most also lack intelligent automation for categorization and advice.

## AI Features

### Expense Categorization
ML models automatically categorize transactions based on merchant names, amounts, and spending patterns — learning from user corrections over time.

### Budget Forecasting
Time series models predict future spending patterns and flag potential budget overruns before they happen.

### RAG-Based Financial Advice
A Retrieval-Augmented Generation system delivers contextual financial advice by retrieving relevant information from curated financial knowledge sources and generating personalized recommendations.

## Tech Stack

- **Backend:** Python, Django, PostgreSQL
- **Frontend:** React
- **AI/ML:** Scikit-learn, RAG pipeline, LLM integration
- **Infrastructure:** Docker, GitHub Actions

## Status

Currently in active development. Core backend architecture is built. AI features are being developed as standalone components that will integrate into the main application.

## Key Takeaway

Pennymize represents the intersection of software engineering and AI — building a real product where ML/AI features are core to the value proposition, not afterthoughts.
