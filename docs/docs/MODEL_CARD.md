# CareerCast Model Card

## Model Overview

CareerCast is an AI-powered career intelligence platform designed to analyze resume information and recommend suitable career roles.

The platform uses machine-learning models for career prediction and recommendation.

## Models

The CareerCast advanced machine-learning system includes:

* Random Forest
* XGBoost

The existing baseline system also contains a Logistic Regression model.

## Recommended Model

Based on the currently stored model evaluation metrics, XGBoost is the recommended advanced model.

## Model Performance

The currently stored evaluation metrics are:

| Model         | Accuracy | Precision | Recall | F1 Score |
| ------------- | -------: | --------: | -----: | -------: |
| Random Forest |   71.82% |    75.46% | 71.82% |   72.90% |
| XGBoost       |   75.71% |    79.38% | 75.71% |   76.88% |

The current best stored model is:

```text
XGBoost
```

with an accuracy of:

```text
75.71%
```

## Input

The system accepts resume information containing content such as:

* Professional experience
* Technical skills
* Education
* Job-related keywords
* Career-related descriptions

Supported resume formats include:

* PDF
* DOCX
* TXT

## Processing Pipeline

The career prediction workflow consists of:

```text
Resume
   ↓
Resume Text Extraction
   ↓
Text Preprocessing
   ↓
Feature Vectorization
   ↓
Machine-Learning Model
   ↓
Career Role Prediction
   ↓
Top-K Recommendations
```

## Feature Representation

The advanced model training pipeline uses TF-IDF text representation.

The current configuration includes:

```text
Maximum features: 20,000
N-gram range: (1, 2)
Minimum document frequency: 2
Maximum document frequency: 0.95
Sublinear TF: enabled
```

## Career Classes

The advanced classification system currently contains 17 career-role categories:

* Accountant
* Administrative Assistant
* Backend Developer
* Business Analyst
* Customer Service Representative
* Data Analyst
* Data Scientist
* DevOps Engineer
* Frontend Developer
* Full Stack Developer
* Machine Learning Engineer
* Marketing Manager
* Product Manager
* Project Manager
* Registered Nurse
* Sales Representative
* Software Engineer

## Training Data

The advanced model training dataset currently contains:

```text
Labeled records: 15,438
Training records: 12,350
Testing records: 3,088
Career classes: 17
```

## Model Outputs

The system can produce:

* Predicted career role
* Top-K career recommendations
* Confidence information
* Recommendation ranking
* Skill alignment information
* Career skill-gap information

## Intended Use

CareerCast is intended to support:

* Career exploration
* Resume analysis
* Career-role recommendation
* Skill-gap identification
* Career planning
* Educational and professional guidance

The predictions are intended to assist users and should not be considered definitive career decisions.

## Limitations

Model performance may be affected by:

* Training-data imbalance
* Limited representation of some career roles
* Resume quality
* Missing information
* Vocabulary differences
* Differences between job descriptions and resumes
* Changes in employment-market trends

The model should therefore be used as a decision-support system rather than an authoritative career-placement system.

## Evaluation

CareerCast includes automated testing for its parsing, prediction and recommendation pipelines.

The current test suite contains:

```text
51 tests
51 passed
0 failed
```

The tests cover:

* Resume parsing
* Skill extraction
* Education extraction
* Prediction pipeline
* Prediction result structure
* Top-K prediction
* Recommendation pipeline
* Recommendation structure
* Edge cases
* End-to-end integration

## Model Version

Current CareerCast package version:

```text
1.0.0
```

## Model Files

The advanced model files are stored under:

```text
advanced_models/
```

Relevant model artifacts include:

```text
random_forest_model.pkl
xgboost_model.pkl
advanced_metrics.json
```

## Compatibility Note

The currently stored models were created using a different scikit-learn version from the current runtime environment. This may produce compatibility warnings when loading the serialized models.

For production release, the training and deployment environments should use compatible dependency versions.

## Ethical Considerations

Career recommendations can influence education and employment decisions. CareerCast should therefore:

* Present predictions as recommendations.
* Avoid claiming guaranteed employment outcomes.
* Avoid discriminatory recommendations.
* Protect uploaded resume information.
* Provide users with understandable recommendation information.

## Milestone 4

This model card documents the CareerCast machine-learning models, their performance, intended use, limitations, evaluation and release considerations.
