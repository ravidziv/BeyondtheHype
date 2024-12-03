#!/usr/bin/env bash

# Instructions:
# Use eval_wrapper.sh
# -- OR --
# 1) Copy this file into the directory of the repo to be graded
# 2) CD into that directory
# 3) Run the script copy.

# -------------------------------------------

# Configure variables for input to submission's __main__.py

# Toggling between synthcc and ha switches which grading python script we use.
DATASET=$2

SUBMISSION_REPO_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# IMPORTANT NOTE: This works only if you place your submission repo -- example or 
#  otherwise -- at the root of the starter pack directory.
GRADING_REPO_DIR="$SUBMISSION_REPO_DIR/../grading"
if [[ $DATASET == "synthcc" ]]; then
    # For synth bank data...
    TEST_SET_INPUTS_DIR="$SUBMISSION_REPO_DIR/../synthcc_train_set"
    TEST_SET_LABELS_PATH="$TEST_SET_INPUTS_DIR/labels.csv"
    # Test set should not be modified by team-provided script. Yes, the script could
    #  change these chmod values, but that won't help anyone make better inferences. This
    #  chmodding is more to prevent accidents.
    chmod 444 $TEST_SET_INPUTS_DIR/account_state_log.csv
    chmod 444 $TEST_SET_INPUTS_DIR/payments_log.csv
    chmod 444 $TEST_SET_INPUTS_DIR/account_state_log.csv
elif [[ $DATASET == "ha" ]]; then
    # For heart attack data...
    TEST_SET_INPUTS_DIR="$SUBMISSION_REPO_DIR/../ha_train_set"
    TEST_SET_LABELS_PATH="$TEST_SET_INPUTS_DIR/labels.csv"
    chmod 444 $TEST_SET_INPUTS_DIR/inputs.csv
else
    printf "Value for DATSET is $DATASET, which is neither 'ha' or 'synthcc'. It must be one of those."
    exit 1
fi

SUBMISSION_REPO_NAME=$1
RESULTS_DIR="$GRADING_REPO_DIR/bth-results-$SUBMISSION_REPO_NAME"
mkdir $RESULTS_DIR  # Ensure dir exists for user to write to.
chmod -R 744 $RESULTS_DIR  # Results dir must be written to by team-provided script.

# -------------------------------------------

# Install and activate hackathon team's conda env.
SUBMISSION_ENV_NAME=`python << EOF
import yaml
import os
assert os.path.isfile("./env.yaml"), "./env.yaml does not exist"
with open("./env.yaml", "r") as f:
    env = yaml.safe_load(f)
assert env is not None, "./env.yaml is empty"
assert "name" in env.keys(), "./env.yaml does not contain a 'name'"
print(env["name"])
EOF
`
# if conda env list | grep -q "^$SUBMISSION_ENV_NAME "; then
#     printf "\nEnvironment '$SUBMISSION_ENV_NAME' exists. Deleting and re-installing.\n"
#     conda activate base
#     conda env remove -n $SUBMISSION_ENV_NAME
# fi
# printf "\nCreating environment '$SUBMISSION_ENV_NAME'.\n"
# conda env create -f env.yaml

printf "\nInitializing conda in the shell may throw errors unrelated "\
    "to the environment used for grading. As long as the grading script does not , " \
    "error, this is fine.\n"
source ~/opt/miniconda3/bin/activate

printf "\nActivating environment '$SUBMISSION_ENV_NAME'\n"
conda activate $SUBMISSION_ENV_NAME

# -------------------------------------------

printf "\nRunning team-provided submission script.\n"
python __main__.py --bth_test_set $TEST_SET_INPUTS_DIR --bth_results $RESULTS_DIR

# -------------------------------------------

printf "\nCreating grading conda env if it needs to be created.\n"
GRADING_ENV_NAME="grading-env" 
if conda env list | grep -q "^$GRADING_ENV_NAME "; then
    printf "Environment '$GRADING_ENV_NAME' exists."
else
    printf "Creating environment '$GRADING_ENV_NAME'."
    conda env create -f $GRADING_REPO_DIR/grading_env.yaml
fi

printf "\nActivating grading conda env.\n"
conda activate $GRADING_ENV_NAME

# -------------------------------------------

printf "\nRunning grading script.\n"
if [[ $DATASET == "ha" ]]; then
    python "$GRADING_REPO_DIR/grade_ha_submission.py" \
        --results_dir $RESULTS_DIR \
        --test_labels_path $TEST_SET_LABELS_PATH \
        --grading_output_dir "$GRADING_REPO_DIR/grading_results"
elif [[ $DATASET == "synthcc" ]]; then
    python "$GRADING_REPO_DIR/grade_synthbank_submission.py" \
        --results_dir $RESULTS_DIR \
        --test_labels_path $TEST_SET_LABELS_PATH \
        --grading_output_dir "$GRADING_REPO_DIR/grading_results"
else
    printf "Value for DATSET is $DATASET, which is neither 'ha' or 'synthcc'. It must be one of those."
    exit 1
fi
