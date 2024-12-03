# Beyond the Hype Hackathon - Starter Pack

## Introduction

Welcome to the "Beyond the Hype" hackathon! Thanks for your time and participation in our research. We hope you enjoy the experience!

You have been assigned to use either LLMs or traditional data science techniques to tackle one of two datasets: heart attack prediction and credit card charge-off prediction.

Both datasets are binary prediction tasks (though the charge-off prediction task has multiple binary classes to predict). Your task is to create a repo with a minimum of two files: 
- `env.yaml`: Defines a conda environment.
- `__main__.py`: Contains the script to run inference.

You will submit the **repository tags** for specific versions of your solution. To be graded, `__main__.py` must follow a well-defined interface. Refer to `synthcc_example_submission` or `ha_example_submission` for guidance. Beyond that interface, you can use any method to train and tune your models.

## Starter Pack Overview

This starter pack contains the following directories:
- `ha_example_submission`
- `ha_train_set`
- `synthcc_example_submission`
- `synthcc_train_set`
- `grading`

### Dataset Assignment
- "ha" refers to the heart attack prediction dataset/task.
- "synthcc" refers to the credit card charge-off prediction dataset/task.

Since you are assigned to one dataset, focus on:
1. The corresponding training set (`ha_train_set` or `synthcc_train_set`).
2. The example submission repository (`ha_example_submission` or `synthcc_example_submission`).

The training set contains the data required to produce your model. You can use it entirely for training, split it for hyperparameter tuning, or apply other techniques. Grading will involve using held-out test data with the same schema.

The example submission repositories contain trivial working examples of submission repositories. Use these to understand submission requirements and get started with exploratory data analysis.

### Submission Requirements
1. **GitHub Repository**: Create a repository on GitHub for your solution.
2. **Branch/Tag for Each Submission**: Use Git to tag specific versions of your solution at the designated submission times.
3. **Submission File**: Upload a file listing the tags and corresponding branches created so far. Each line should represent a branch/version of the solution at a specific submission time.

### Submission Deadlines
You are required to submit your repository tags at the following times:
- **12:00 PM**
- **2:00 PM**
- **4:00 PM**
- **6:00 PM**
- **8:00 PM**
- **10:00 PM**

Submit your tags and repository details through **[https://beyond-the-hype.devpost.com/](https://beyond-the-hype.devpost.com/)**.

## Working on the Server

A Jupyter notebook file named `hpc-guide.ipynb` is provided to guide you on how to start working on the server. Follow the instructions in this file to set up your environment.

### Copying Data and Scripts
Before starting your work, ensure you **copy the data and the example scripts** to your working directory.

## Grading Scripts

The `grading` folder helps you validate your submission. These scripts simulate the grading process to check if your submission adheres to the required interface.

### Running the Grading Scripts
1. Navigate to the `grading/conda_eval` directory.
2. Run `./eval_wrapper.sh`. You may need to run `chmod 744 eval_wrapper.sh eval.sh` to grant execution permissions.

The grading scripts will validate your submission using the training sets. While the outputs are less important, ensuring the grading scripts work without errors is critical.

### Validating Example Submissions
Start by running the grading scripts on one of the example submissions. Ensure `$SUBMISSION_REPO_DIR` in `eval_wrapper.sh` points to the appropriate example submission directory.

## Additional Notes
- Place your submission repository in the root of the starter pack repo (at the same level as the `ha_example_submission` and `synthcc_example_submission` directories).
- Ensure that the repository you create on GitHub is accessible and includes all necessary files.
- Review the example submissions for guidance and use the `hpc-guide.ipynb` notebook to set up your work environment.

Good luck!
