---
layout: project
title: "Text Classification with BERT"
github_repo: "username/text-classification"
featured_file: "model.py"
tags: [NLP, BERT, PyTorch, Text Classification]
---

# Text Classification with BERT

This project demonstrates how to use BERT (Bidirectional Encoder Representations from Transformers) for text classification tasks. The implementation uses PyTorch and Hugging Face's Transformers library.

## Problem Statement

Given a set of text documents, classify them into predefined categories. This is a common task in natural language processing with applications in:

- Sentiment analysis
- Topic categorization
- Spam detection
- Intent recognition

## Solution Overview

The solution leverages BERT, a powerful pre-trained language model developed by Google. The key benefits of using BERT include:

1. Contextual word embeddings
2. Bidirectional context understanding
3. Transfer learning capabilities
4. State-of-the-art performance

## Implementation

The model architecture consists of the pre-trained BERT model with a classification head on top. We fine-tune the entire model on our specific dataset.

### Model Architecture

```python
import torch
from torch import nn
from transformers import BertModel

class BertClassifier(nn.Module):
    def __init__(self, num_classes=6):
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(768, num_classes)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        x = self.dropout(pooled_output)
        logits = self.fc(x)
        return logits