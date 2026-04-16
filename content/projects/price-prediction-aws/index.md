---
title: "Price Prediction Platform on AWS"
date: 2024-01-01
draft: false
description: "An earlier end-to-end ML deployment project for house price prediction using Flask, AWS ECR/EC2, Docker, and GitHub Actions."
tags: ["aws", "mlops", "deployment", "python", "github-actions"]
cover:
  image: ""
  alt: "Price Prediction on AWS"
  relative: true
weight: 2
showToc: true
---

## Overview

An earlier machine learning deployment project for house price prediction, built as a Flask application with an AWS deployment workflow and automated GitHub Actions pipeline.

## Architecture

- **Flask application** — serves the prediction interface and inference flow
- **AWS ECR** — stores the Docker image built by the CI pipeline
- **AWS EC2** — hosts the deployed container and self-hosted GitHub runner
- **GitHub Actions** — runs CI and pushes the deployment image

## Features

- **Interactive prediction UI** — users can change housing features and see updated predictions
- **Containerized deployment workflow** — Docker image built and pushed through GitHub Actions
- **End-to-end project structure** — data ingestion, transformation, training, and prediction pipelines in one codebase

## Tech Stack

- Python (Scikit-learn, Pandas, Flask)
- AWS (ECR, EC2)
- GitHub Actions
- Docker

## Links

- [GitHub Repository](https://github.com/sahaavi/Housing-Price-Prediction)

## Key Takeaway

This project was an early end-to-end ML deployment exercise focused on packaging a prediction model as a containerized web app with an AWS deployment workflow and CI/CD automation.
