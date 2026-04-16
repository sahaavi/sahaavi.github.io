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

> Editor note: this draft is intentionally unpublished while the portfolio focuses on the stronger `Maintenance-Eye` project case study. If this post is republished later, it should stay aligned with the deployed system and avoid unsupported claims.

## The Problem

Maintenance technicians at transit companies spend significant time diagnosing equipment failures. They flip through thick manuals, search through past incident reports, and call senior colleagues for advice. All while the equipment sits broken and operations are impacted.

What if a technician could simply point their phone camera at a piece of equipment, describe what's happening, and get an instant diagnostic assessment with recommended next steps?

## The Architecture

The deployed system combines three core capabilities:

1. **Visual and audio input** — camera frames and microphone audio stream from a mobile web client
2. **Real-time multimodal reasoning** — Gemini Live handles live voice and visual context together
3. **Tool use with confirmation gating** — the backend orchestrates retrieval and action tools, while keeping critical actions behind explicit user confirmation

## Why Google Gemini?

Gemini's native multimodal capabilities make it ideal for this use case:

- **Single model, multiple modalities** — No need to chain separate vision and language models
- **Long context window** — Can process detailed equipment manuals alongside real-time inputs
- **Tool use** — The agent can call maintenance databases and work order systems

## Key Technical Decisions

### 1. Real-Time Interaction Over Form-Based Input

The core product decision was to build around camera, voice, and interruption-friendly interaction instead of a text-heavy workflow. For maintenance use cases, reducing context switching mattered more than making the system look like a traditional chatbot.

### 2. Tool-Oriented Backend Design

Instead of relying on a single prompt, the backend uses structured tools for asset lookup, maintenance context, work-order support, and safety guidance. That makes the system easier to reason about and keeps action-taking paths explicit.

### 3. Human-in-the-Loop Confirmation

For safety-sensitive actions, the system proposes the action but requires explicit confirmation before execution. That keeps the AI useful without pretending it should act autonomously in operational workflows.

## What I Learned

Building this agent reinforced several key insights:

- **Domain expertise matters** — Understanding how maintenance technicians actually work was more important than the AI architecture
- **Multimodal is more than a feature** — When vision and language work together, the user experience is fundamentally different from text-only AI
- **Production readiness is the hard part** — Getting the AI to work in a demo is 20% of the effort. Handling edge cases, ensuring reliability, and integrating with existing systems is the other 80%

## What's Next

The next steps are deeper enterprise-system integration, stronger offline behavior for low-connectivity settings, and more specialized workflows for different maintenance contexts.

---

*This project is part of my journey transitioning into AI Engineering. Follow along on [GitHub](https://github.com/sahaavi) or connect on [LinkedIn](https://linkedin.com/in/sahaavi).*
