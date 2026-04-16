---
title: "Maintenance-Eye"
date: 2026-03-01
draft: false
description: "A deployed multimodal maintenance copilot for field technicians, built with Google ADK, Gemini Live API, FastAPI, Firestore, and Cloud Run."
tags: ["computer-vision", "google-gemini", "ai-agents", "python"]
cover:
  image: ""
  alt: "Vision Maintenance AI Agent"
  relative: true
weight: 1
showToc: true
---

## What I Built

**Maintenance-Eye** is a real-time multimodal maintenance copilot for field technicians. A technician can point a phone camera at equipment, speak naturally, and get back live visual analysis, voice responses, equipment lookup, maintenance context, and work-order support.

This project was built for the **Google Gemini Live Agent Challenge** and is deployed as a working web application.

## Why This Workflow Matters

Maintenance work happens in noisy, high-stakes environments where technicians are moving, inspecting, and handling tools. Traditional maintenance software assumes the user can stop, type, search, and document everything manually.

I wanted to explore a different interface: an AI system that can see, listen, speak, and help the technician act without forcing a context switch away from the inspection itself.

## What Is Live Today

The deployed system currently supports:

- live camera and microphone input from a mobile web app
- real-time multimodal reasoning with **Gemini 2.5 Flash Live**
- voice interaction with barge-in interruption
- tool-based lookup across assets, work orders, inspection history, safety protocols, and knowledge-base content
- human-in-the-loop confirmation for critical actions
- deployment on **Google Cloud Run** with **Firestore** as the backing store

## System Architecture

The frontend is a mobile-friendly web app that streams camera frames and microphone audio over WebSocket to a **FastAPI** backend. The backend uses **Google ADK** to manage the agent loop and pass real-time media to the **Gemini Live API**. Agent tools handle structured retrieval and work-order operations, and responses stream back as audio, text, and confirmation UI cards.

## Agent Tools and Safety Controls

This is not a single-prompt demo. The agent uses dedicated tools for asset lookup, inspection history, knowledge retrieval, work-order support, safety protocol access, and action confirmation.

For safety-sensitive actions, the system keeps a human in the loop: the agent can propose an action, but the technician must explicitly confirm it before execution.

## Technical Challenges

The hardest engineering problems were not model selection. They were systems problems:

- handling bidirectional real-time streaming reliably
- making voice interaction usable with interruption
- normalizing noisy ASR output for equipment IDs and maintenance terms
- designing tool flows that help the user act without letting the model overstep safety boundaries

## Demo and Repository

- **Live Demo:** [https://maintenance-eye-swrz6daraq-uc.a.run.app](https://maintenance-eye-swrz6daraq-uc.a.run.app)
- **Repository:** [https://github.com/sahaavi/Maintenance-Eye](https://github.com/sahaavi/Maintenance-Eye)

## What I'd Improve Next

Next steps would be tighter EAM integration, stronger offline behavior for low-connectivity environments, and more domain-specific agent flows by maintenance discipline.
