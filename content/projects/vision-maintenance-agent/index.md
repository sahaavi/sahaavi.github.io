---
title: "Maintenance-Eye"
slug: "maintenance-eye"
date: 2026-03-01
draft: false
description: "A real-time multimodal maintenance copilot that sees, listens, speaks, and acts through tool-using workflows."
tags: ["google-adk", "gemini-live-api", "multimodal", "fastapi", "applied-ai"]
cover:
  image: ""
  alt: "Maintenance-Eye"
  relative: true
weight: 1
showToc: true
---

## Overview

**Maintenance-Eye** is a real-time AI copilot for physical infrastructure maintenance. Built for the **Google Gemini Live Agent Challenge 2026**, it lets a technician point a phone camera at equipment, speak naturally, and get grounded assistance without switching to a separate typing workflow.

## Links

- [GitHub Repository](https://github.com/sahaavi/Maintenance-Eye)
- [Devpost Demo Video](https://devpost.com/software/maintenance-eye)

## Status

Maintenance-Eye is the shipped flagship in my public portfolio. The Devpost demo video, repository, architecture diagram, infrastructure files, API routes, and tests are the evidence anchors for the case study.

## Demo And Review Path

The Devpost page is the primary public demo because it includes the project video. For hands-on review, the repository documents local setup with a JSON-backed EAM fallback so the core inspection, chat, and tool-flow architecture can still be reviewed.

## Problem

Transit and infrastructure maintenance work is physical, noisy, and time-sensitive. Technicians often need to inspect equipment, recall safety procedures, search maintenance history, and create work orders while their hands are already occupied by tools and safety gear. Traditional enterprise systems force a stop-and-type workflow that interrupts inspections and slows response time.

## What I Built

- A **real-time multimodal frontend** that streams camera frames and microphone audio from a phone-based PWA
- A **FastAPI backend** that manages WebSocket sessions, media flow, confirmation state, and operational APIs
- A **Google ADK agent** powered by Gemini 2.5 Flash Live API for native audio + vision reasoning
- A set of **tool-using maintenance workflows** covering asset lookup, knowledge retrieval, work-order actions, inspection history, and safety protocols
- A **human-in-the-loop confirmation layer** for critical actions such as creating or updating work orders

## Tech Stack

- **AI runtime:** Google ADK, Gemini 2.5 Flash Live API
- **Backend:** Python, FastAPI, WebSockets
- **Data:** Firestore, Cloud Storage, JSON fallback data layer for local dev
- **Infra:** Cloud Run, Docker, Terraform, GitHub Actions
- **Testing:** unit, integration, API contract, security, performance, and E2E coverage

## Architecture

![Maintenance-Eye architecture](https://raw.githubusercontent.com/sahaavi/Maintenance-Eye/main/docs/architecture.png)

The system uses a persistent bidirectional WebSocket to move video frames, audio, transcripts, UI cards, and tool results between the phone client and the backend. The agent does not just answer questions: it calls domain-specific tools, grounds responses in maintenance data, and requires explicit confirmation before sensitive actions.

## Proof Of Engineering Depth

- **Real-time multimodal interaction** with audio in, audio out, and camera-driven reasoning
- **Nine specialized tools** for maintenance operations, not a single-prompt wrapper
- **Human-in-the-loop safety** with confirmation cards for critical actions
- **Operational deployment path** with Docker, Cloud Run, Firestore, and Terraform
- **Reliability focus** through a multi-layer test suite and explicit backend/service boundaries

## Why It Matters

This project is the clearest public example of how I like to build AI systems: start from a real workflow, design around operational constraints, use models as one component in a broader system, and make deployment, interfaces, and failure boundaries part of the product rather than an afterthought.
