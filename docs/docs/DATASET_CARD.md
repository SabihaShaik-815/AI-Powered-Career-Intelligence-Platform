# CareerCast Dataset Card

## Dataset Overview

CareerCast uses a job-posting dataset as the primary source of information for career-role analysis and machine-learning model development.

The dataset contains job postings, company information, skills, industries, benefits and salary-related information.

## Dataset Statistics

| Property                                      |               Value |
| --------------------------------------------- | ------------------: |
| Job records                                   |             123,849 |
| Career roles used for advanced classification |                  17 |
| Company records                               |              24,423 |
| Main dataset                                  | `data/postings.csv` |

## Dataset Location

The primary job-posting dataset is stored at:

```text
data/postings.csv
```

Additional supporting datasets are organized under:

```text
data/
├── companies/
├── jobs/
└── mappings/
```

## Main Information Used

The job-posting data contains information such as:

* Job title
* Job description
* Company name
* Location
* Work type
* Experience level
* Skills
* Industry
* Benefits
* Salary information

## Career Role Labels

For the advanced career classification pipeline, CareerCast currently uses 17 career-role categories:

1. Accountant
2. Administrative Assistant
3. Backend Developer
4. Business Analyst
5. Customer Service Representative
6. Data Analyst
7. Data Scientist
8. DevOps Engineer
9. Frontend Developer
10. Full Stack Developer
11. Machine Learning Engineer
12. Marketing Manager
13. Product Manager
14. Project Manager
15. Registered Nurse
16. Sales Representative
17. Software Engineer

## Data Processing

The dataset is processed before machine-learning training.

The processing pipeline includes:

1. Loading the job-posting data.
2. Creating career-role labels.
3. Cleaning text fields.
4. Combining relevant textual information.
5. Removing unusable records.
6. Splitting the data into training and testing sets.
7. Converting textual information into TF-IDF features.

## Feature Engineering

CareerCast uses textual information from job postings to create machine-learning features.

The advanced training pipeline uses TF-IDF vectorization with:

```text
ngram_range = (1, 2)
max_features = 20,000
min_df = 2
max_df = 0.95
sublinear_tf = True
```

## Train/Test Dataset

The current advanced training dataset contains:

```text
Total labeled records: 15,438
Training records:      12,350
Testing records:        3,088
```

## Intended Use

The dataset is used for:

* Career-role classification
* Career prediction
* Career recommendation
* Skill analysis
* Career intelligence
* Machine-learning experimentation

## Limitations

The dataset is based on job-posting information and may contain:

* Class imbalance
* Missing information
* Duplicate or similar job postings
* Differences in job-title terminology
* Variation between companies and industries
* Geographic differences in job descriptions

Therefore, model predictions should be treated as recommendations rather than guaranteed career outcomes.

## Data Privacy

CareerCast should not expose personally identifiable information from uploaded resumes.

Resume information should be processed only for the intended career-analysis workflow.

## Reproducibility

The dataset is expected to be available at:

```text
data/postings.csv
```

The machine-learning training scripts use this dataset as the primary input.

## Milestone 4

This dataset card documents the main dataset used by CareerCast and provides information about its purpose, structure, processing and limitations for public release.
