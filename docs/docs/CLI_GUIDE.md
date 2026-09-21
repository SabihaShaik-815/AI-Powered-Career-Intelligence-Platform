# CareerCast CLI Guide

## Overview

CareerCast provides a command-line interface (CLI) for interacting with the AI-Powered Career Intelligence Platform.

The CLI allows users to:

* Predict career roles from a resume
* Generate career recommendations
* Display model information
* Display the installed CareerCast version

## Installation

Install CareerCast as a Python package using:

```bash
pip install .
```

After installation, verify the CLI:

```bash
careercast --help
```

## Version

To display the installed CareerCast version:

```bash
careercast version
```

Example output:

```text
CareerCast version 1.0.0
```

The version can also be checked using:

```bash
careercast --version
```

## Help

To display all available commands:

```bash
careercast --help
```

Available commands:

```text
predict
recommend
model-info
version
```

## Career Prediction

The `predict` command is used to predict suitable career roles from resume information.

Example:

```bash
careercast predict resume.txt
```

For a PDF resume:

```bash
careercast predict resume.pdf
```

For a DOCX resume:

```bash
careercast predict resume.docx
```

The prediction pipeline analyzes the resume and generates career-role predictions.

## Career Recommendations

The `recommend` command generates Top-K career recommendations based on resume information.

Example:

```bash
careercast recommend resume.pdf
```

The recommendation pipeline ranks suitable career roles and provides recommendation information.

## Model Information

The `model-info` command displays information about the available machine-learning models.

Run:

```bash
careercast model-info
```

Example:

```text
CareerCast Model Information

available_models: ['Random Forest', 'XGBoost']
recommended_model: XGBoost
metrics:
    random_forest:
        accuracy: 71.82
        precision: 75.46
        recall: 71.82
        f1_score: 72.9

    xgboost:
        accuracy: 75.71
        precision: 79.38
        recall: 75.71
        f1_score: 76.88

best_model: XGBoost
best_accuracy: 75.71
```

## CLI Commands Summary

| Command                         | Purpose                         |
| ------------------------------- | ------------------------------- |
| `careercast --help`             | Display CLI help                |
| `careercast version`            | Display CareerCast version      |
| `careercast --version`          | Display package version         |
| `careercast predict <resume>`   | Predict career roles            |
| `careercast recommend <resume>` | Generate career recommendations |
| `careercast model-info`         | Display model information       |

## Supported Resume Formats

CareerCast supports:

* PDF
* DOCX
* TXT

## Example Workflow

A typical CLI workflow is:

```bash
careercast --help
careercast version
careercast model-info
careercast predict resume.pdf
careercast recommend resume.pdf
```

## Testing the CLI

Verify the CLI installation with:

```bash
careercast --help
```

Verify the package version:

```bash
careercast version
```

Verify model information:

```bash
careercast model-info
```

## Milestone 4

The CLI documentation is part of Milestone 4 — Packaging, Testing & Finalization.

It documents how users can interact with CareerCast through the command line after installing the package.
