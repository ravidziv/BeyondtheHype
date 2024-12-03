#!/usr/bin/env bash

# Get absolute path to `grading` folder within the starter pack. This allows the script
#  to work regardless of where you put the starter pack on your machine. I.e. don't 
#  change this, especially since you should place your submission repo in the starter pack.
#  If you are asking "why", re-read the README section on grading at the base of the starter 
#  pack.
GRADING_REPO_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )

# Example submission for synth bank data...
SUBMISSION_REPO_DIR="$GRADING_REPO_DIR/../synthcc_example_submission"  # CHANGE ME
# Example submission for heart attack data...
# SUBMISSION_REPO_DIR="$GRADING_REPO_DIR/../ha_example_submission"  # CHANGE ME
# Options are "ha" or "synthcc". If you change the above, repo dir, make sure this is correct.
DATASET="synthcc"
# DATASET="ha"

SUBMISSION_REPO_NAME=$(basename $SUBMISSION_REPO_DIR)

# The eval script needs to be run from the submission's repo, so copy the script into
#  the repo and run from there.
cp ./eval.sh $SUBMISSION_REPO_DIR
cd $SUBMISSION_REPO_DIR
./eval.sh $SUBMISSION_REPO_NAME $DATASET