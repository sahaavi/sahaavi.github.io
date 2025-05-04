---
layout: post
title: "Introduction to Machine Learning"
date: 2023-05-01
tags: [machine learning, data science, tutorial]
---

# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from and make decisions based on data. Instead of explicitly programming rules, machine learning algorithms build a model based on sample data to make predictions or decisions.

## Key Concepts in Machine Learning

### Supervised Learning

Supervised learning involves training a model on labeled data. The algorithm learns the mapping function from input variables to the output variable, allowing it to predict outputs for new inputs.

Example of a simple linear regression in Python:

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Sample data
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.array([1, 2, 2, 3])

# Train the model
model = LinearRegression().fit(X, y)

# Make predictions
predictions = model.predict(np.array([[3, 5]]))
print(predictions)  # Output: [4.5]