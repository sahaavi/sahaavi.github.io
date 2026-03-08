---
title: "Price Prediction Platform on AWS"
date: 2024-01-01
draft: false
description: "End-to-end ML-based house price prediction system deployed on AWS with Lambda, EC2, and S3, featuring CI/CD via GitHub Actions."
tags: ["aws", "mlops", "deployment", "python", "github-actions"]
cover:
  image: ""
  alt: "Price Prediction on AWS"
  relative: true
weight: 4
showToc: true
---

## Overview

A fully deployed machine learning system for house price prediction, built on AWS infrastructure with automated CI/CD pipelines.

## Architecture

- **AWS Lambda** — Serverless inference endpoint
- **AWS EC2** — Model training and data processing
- **AWS S3** — Model artifact and dataset storage
- **GitHub Actions** — Automated CI/CD pipeline for continuous deployment

## Features

- **Dynamic feature testing** — Users can adjust input features and get instant predictions
- **Automated deployment** — Push to main triggers model retraining and redeployment
- **Scalable inference** — Lambda-based endpoints scale automatically with demand

## Tech Stack

- Python (Scikit-learn, Pandas)
- AWS (Lambda, EC2, S3)
- GitHub Actions
- Docker

## Links

- [Project Details](https://avisaha.netlify.app/categories/project/)

## Key Takeaway

This project demonstrates end-to-end MLOps — from model development to cloud deployment with CI/CD. It covers the full lifecycle that production ML systems require.
