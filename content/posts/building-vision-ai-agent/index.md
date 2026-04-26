---
title: "Building a Vision Maintenance AI Agent with Google Gemini"
date: 2026-03-07
draft: true
description: "How I built a multimodal AI agent for equipment diagnostics using Google Gemini's vision and language capabilities."
tags: ["computer-vision", "google-gemini", "ai-agents", "python"]
categories: ["AI Engineering"]
cover:
  image: ""
  alt: "Vision Maintenance AI Agent"
  relative: true
author: "Avishek Saha"
showToc: true
math: false
---

As part of the **Google Gemini AI Challenge 2026**, I built a multimodal AI agent that helps maintenance technicians diagnose equipment issues. Here's the story of what I built, why, and the key technical decisions along the way.

## The Problem

Maintenance technicians at transit companies spend significant time diagnosing equipment failures. They flip through thick manuals, search through past incident reports, and call senior colleagues for advice. All while the equipment sits broken and operations are impacted.

What if a technician could simply point their phone camera at a piece of equipment, describe what's happening, and get an instant diagnostic assessment with recommended next steps?

## The Architecture

The system combines three AI capabilities:

1. **Visual analysis** — Google Gemini processes camera images to identify equipment type, visible damage, and anomalies
2. **Natural language understanding** — The technician describes symptoms conversationally, and the agent extracts key diagnostic signals
3. **Knowledge retrieval** — Past maintenance records and equipment manuals are indexed for retrieval, providing historical context for each diagnosis

## Why Google Gemini?

Gemini's native multimodal capabilities make it ideal for this use case:

- **Single model, multiple modalities** — No need to chain separate vision and language models
- **Long context window** — Can process detailed equipment manuals alongside real-time inputs
- **Tool use** — The agent can call maintenance databases and work order systems

## Key Technical Decisions

### 1. Prompt Engineering Over Fine-Tuning

For this application, careful prompt engineering with few-shot examples outperformed the fine-tuning approach. The maintenance domain has clear patterns that can be captured in well-structured prompts.

### 2. Vector Database for Maintenance History

Past incidents are embedded and stored in a vector database. When a new issue comes in, the system retrieves the most similar past incidents to provide context — essentially giving the AI "memory" of how similar problems were solved before.

### 3. Structured Output for Work Orders

The agent generates structured JSON work orders that can integrate directly with existing maintenance management systems, eliminating manual data entry.

## What I Learned

Building this agent reinforced several key insights:

- **Domain expertise matters** — Understanding how maintenance technicians actually work was more important than the AI architecture
- **Multimodal is more than a feature** — When vision and language work together, the user experience is fundamentally different from text-only AI
- **Production readiness is the hard part** — Getting the AI to work in a demo is 20% of the effort. Handling edge cases, ensuring reliability, and integrating with existing systems is the other 80%

## What's Next

I'm continuing to refine the agent's diagnostic accuracy and working on integrating it with real maintenance management systems. The goal is to demonstrate that AI can meaningfully reduce diagnostic time in industrial maintenance settings.

---

*This draft is archived behind the stronger [Maintenance-Eye case study](/projects/maintenance-eye/). Follow along on [GitHub](https://github.com/sahaavi) or connect on [LinkedIn](https://linkedin.com/in/sahaavi).*
