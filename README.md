# Beyond the Hype Hackathon - Starter Pack

## Introduction

Welcome to the "Beyond the Hype" hackathon! Thanks for your time and participation in our
research. We hope you enjoy the experience!

You have been assigned to use either LLMs
or traditional data science techniques to tackle one of two datasets: heart attack prediction
and credit card charge-off prediction.

Both datasets are binary prediction tasks (though the charge-off prediction task has multiple
binary classes to predict). Your task is to create a repo with a minimum of two files: 
`env.yaml` and `__main__.py`. The former creates a conda env that the latter uses to run
inference. You will send a tag of that repo to us periodically so that we can grade your
performance. In order to be graded, `__main__.py` must follow a well-defined interface. 
Take a look at `synthcc_example_submission` or `ha_example_submission` to learn more. 
Beyond that inference interface, you can do whatever you like
to train and tune your models.

## Starter Pack Overview

This starter pack has five directories:
- ha_example_submission
- ha_train_set
- synthcc_example_submission
- synthcc_train_set
- grading

"ha" is how we refer to the heart attack prediction dataset/task. "synthcc" is how we refer to
the credit card charge-off prediction dataset/task.

Since you are assigned to one dataset, you should only care about three of the five directories.

Depending on the dataset/task you are assigned to one of the `ha_train_set` and 
`synthcc_train_set` folders contain all the data you have to produce a model. You can
use it all for training, split off some for hyperparameter tuning, do RAG on it, etc. The
choices are yours, albeit constrained to the LLM or non-LLM techniques you are assigned. 
When we grade your submission, we will feed `__main__.py` held out test
data with the same schemas as what you see in the train set (except, of course, you will
not have access to `labels.csv`).

The `ha_example_submission` and `synthcc_example_submission` contain trivial working examples
of submission repositories. Check them out for information on the submission requirements
and exploratory data analysis to get you started.

See [Grading Scripts](#grading-scripts) for details on how you can make sure your code
will work before submitting it.

## Grading Scripts
The `grading` folder helps you validate that your submission will work before submitting. 
E.g. if you got the `__main__.py` interface wrong, the grading scripts will fail. You MUST
try the `grading` scripts before submission, because if your submission fails the grading
scripts on our end, you will get the lowest possible score for that submission.

Because you don't have access to the test sets, the grading scripts run inference on 
the training sets located in `ha_train_set` or `synthcc_train_set`. The outputs are 
not so important as the fact of the grading scripts working or not.

The `grading` folder is an almost exact copy of the scripts we will use to grade your 
submissions. The main difference is that your `grading` folder's scripts "know" where 
the train datasets are relative to them and the submission repos. They use that knowledge 
to provide the train sets as input to the submission's `__main__.py` file. For that 
reason, **if you want to validate that your submission works with the grading scripts, 
you must put it in the root of the starter pack repo, i.e. at the same level as 
`ha_example_submission` and `synthcc_example_submission`**

As a good sanity check, start by running the grading scripts on one of the example 
submission repos. Open `eval_wrapper.sh` to confirm that $SUBMISSION_REPO_DIR points to one of
the example submissions (it should be a relative path with respect to the grading folder). 

To use the grading scripts, `cd` into `grading/conda_eval` and then simply run 
`./eval_wrapper.sh`. You may need to `chmod 744 eval_wrapper.sh eval.sh` first.