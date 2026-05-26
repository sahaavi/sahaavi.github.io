---
title: "Maintenance-Eye"
slug: "maintenance-eye"
date: 2026-03-01
draft: false
description: "A real-time multimodal maintenance copilot using live audio, camera input, ADK tools, and technician-confirmed actions."
tags: ["google-adk", "gemini-live-api", "multimodal", "fastapi", "applied-ai"]
cover:
  image: ""
  alt: "Maintenance-Eye"
  relative: true
weight: 1
showToc: true
---

## Overview

**Maintenance-Eye** is a real-time AI copilot for physical infrastructure maintenance. Built for the **Google Gemini Live Agent Challenge 2026**, it lets a technician point a phone camera at equipment, ask by voice, review asset context, and confirm work-order actions through a camera-and-voice inspection flow.

## Links

- [GitHub Repository](https://github.com/sahaavi/Maintenance-Eye)
- [Devpost Demo Video](https://devpost.com/software/maintenance-eye)

## Status

Maintenance-Eye is a public portfolio case study backed by the Devpost demo, repository, architecture diagram, infrastructure files, API routes, and tests.

## Demo And Review Path

The Devpost page is the primary public demo because it includes the project video. The repository documents local setup with a JSON-backed EAM fallback, so the data, API, and tool behavior can be inspected locally; live Gemini inspection and chat require Gemini credentials.

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
- **Data/artifacts:** Firestore EAM data, JSON-backed local fallback, and optional best-effort GCS storage for frame, report, and work-order artifacts
- **Infra:** Cloud Run, Docker, Terraform, GitHub Actions
- **Testing:** unit, integration, API contract, security, performance, and Playwright E2E smoke tests

## Architecture

![Maintenance-Eye architecture](https://raw.githubusercontent.com/sahaavi/Maintenance-Eye/main/docs/architecture.png)

The system uses a persistent bidirectional WebSocket to move video frames, audio, transcripts, confirmation cards, media cards, and work-order result messages between the phone client and backend. The agent calls domain-specific tools, grounds responses in maintenance data, and requires explicit confirmation before sensitive actions.

## Engineering Highlights

- **Real-time multimodal interaction** with audio in, audio out, and camera-driven reasoning
- **Nine ADK tool bindings** covering search, asset lookup, inspection history, knowledge retrieval, work-order management, safety protocols, report generation, and confirmation workflows
- **Human-in-the-loop safety** with confirmation cards for critical actions
- **Operational deployment path** with Docker, Cloud Run, Firestore, and Terraform
- **Multi-layer test coverage** across unit, integration, API contract, security, performance, and Playwright E2E smoke tests

## Why It Matters

This project demonstrates my approach to applied AI: model integration, backend tool orchestration, deployment, test coverage, and human-in-the-loop safeguards around operational workflows.
