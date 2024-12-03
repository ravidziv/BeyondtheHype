import argparse
import os
import pathlib
from typing import List, Dict, Callable

import pandas as pd
from sklearn.metrics import f1_score


def etl_predictions_csv(
        csv_path: str, 
        prediction_windows_months: List[int],
    ) -> pd.DataFrame:
    """Validate the hackathon team's submission and cast prediction cols to int.

    :param csv_path: Path to results.csv
    :type csv_path: str
    :param prediction_windows_months: List of numbers of months over which charge-off is
        predicted
    :type prediction_windows_months: List[int]
    :return: Loaded and validated predictions CSV with predictions cast to int
    :rtype: pd.DataFrame
    """

    assert os.path.isfile(csv_path), f"{csv_path=} is not a file."
    pred_df = pd.read_csv(csv_path)
    assert "agent_id" in pred_df.columns, (
        "`agent_id` must be a column name in results.csv."
    )
    for months in prediction_windows_months:
        col_name = f"charge_off_within_{months}_months"
        assert col_name in pred_df.columns, (
            f"`{col_name}` must be a column name in results.csv"
        )
        months_col = pred_df[col_name]
        assert pd.api.types.is_numeric_dtype(months_col), (
            f"Column `{col_name}` in results.csv does not consist of numbers: "
            f"{months_col.head()=}"
        )
        assert (months_col % 1 == 0).all(), (
            f"Column `{col_name}` in results.csv does not consist of integers: "
            f"{months_col.head()=}"
        )
        assert months_col.isin({0, 1}).all(), (
            f"Column `{col_name}` in results.csv does not consist of 0s and 1s: "
            f"{months_col.head()=}"
        )
        # Cast to int dtype if it isn't already.
        pred_df[col_name] = pred_df[col_name].astype(int)
    return pred_df


def compare_pred_and_label_agents(
        pred_df: pd.DataFrame, 
        label_df: pd.DataFrame
    ):
    """Raise an error if the sets of agents in predictions and labels aren't the same.

    :param pred_df: DF of predictions
    :type pred_df: pd.DataFrame
    :param label_df: DF of labels
    :type label_df: pd.DataFrame
    """
    pred_agents = set(pred_df.agent_id)
    label_agents = set(label_df.agent_id)
    if pred_agents > label_agents:
        raise ValueError(
            f"Predictions have more agents than labels. Agents in pred but not in "
            f"labels: {pred_agents - label_agents}"
        )
    elif label_agents > pred_agents:
        raise ValueError(
            f"Labels have more agents than predictions. Agents in labels but not in "
            f"pred: {label_agents - pred_agents}"
        )
    if pred_agents != label_agents:
        raise ValueError(
            f"Labels and preds have different sets of agents. Agents in labels but not "
            f"in pred: {label_agents - pred_agents}.\nAgents in pred but not in labels: "
            f"{pred_agents - label_agents}"
        )
    
    if len(pred_df) != len(label_df):
        raise ValueError(
            f"Labels and preds have different numbers of rows. There should be one row "
            f"per test set example in need of a prediction. {len(pred_df)=}; "
            f"{len(label_df)=}"
        )


def main(
        results_dir: str, 
        test_labels_path: str,
        grading_output_dir: str,
        prediction_windows_months: List[int] = [3, 6, 9, 12]
    ):
    # Load and check schema of predictions.
    csv_path = os.path.join(results_dir, "results.csv")
    pred_df = etl_predictions_csv(csv_path, prediction_windows_months)

    assert os.path.isfile(test_labels_path), f"{test_labels_path=} is not a file."
    label_df = pd.read_csv(test_labels_path)

    compare_pred_and_label_agents(pred_df, label_df)

    merged_df = pd.merge(
        pred_df, 
        label_df, 
        on="agent_id", 
        how="inner", 
        suffixes=("_pred", "_label")
    )
    print(merged_df.info())

    # F1 works well in unbalanced env with few positives because if the user attempts to max 
    #  recall by predicting all pos, precision will fall dramatically. Likewise, could try 
    #  to max precision by predicting few positives, but then recall would suffer. And 
    #  neither metric is skewed by the large quantity of actual negatives because they do 
    #  not consider true negatives, which are likely abundant in any model trained on this
    #  data.
    metrics: Dict[str, Callable] = {"f1": f1_score}
    col_names: Dict[int, str] = {
        months: f"charge_off_within_{months}_months" for months in prediction_windows_months
    }
    grading_df = pd.DataFrame(
        index=pd.Index(data=metrics.keys(), name="metric_name"), 
        columns=list(col_names.values()) + ["avg"]
    )
    for metric_name, metric_fn in metrics.items():
        avg_metric_val = 0  # across diff months windows
        for months in prediction_windows_months:

            col_name = col_names[months]
            preds = merged_df[col_name + "_pred"]
            labels = merged_df[col_name + "_label"]

            metric_val = metric_fn(labels, preds)
            print(f"{metric_name} for {months} months: {metric_val}")

            grading_df.loc[metric_name, col_name] = metric_val

            avg_metric_val += metric_val / len(prediction_windows_months)

        print(f"Average {metric_name} score across prediction windows: {avg_metric_val}")
        grading_df.loc[metric_name, "avg"] = metric_val

    # Write grading outputs to a CSV.
    if not os.path.isdir(grading_output_dir):
        pathlib.Path(grading_output_dir).mkdir(parents=True)
    grading_csv_name = os.path.basename(results_dir + ".csv")
    grading_df.to_csv(os.path.join(grading_output_dir, grading_csv_name), index=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results_dir", 
        type=str,
        required=True,
        help=(
            "Directory containing a file results.csv with the following column names: "
            "[agent_id, charge_off_within_3_months, charge_off_within_6_months, "
            "charge_off_within_9_months, charge_off_within_12_months]. The latter four "
            "columns correspond to binary predictions (1 or 0) "
            "of whether charge-off happens over 3, 6, 9, and 12 months, respectively. "
            "Each row has all four predictions for *one* test set agent. Note that this is the "
            "path to the directory containing the CSV, not the CSV itself, in case we "
            "decide we need additional outputs in the future."
        )
    )
    parser.add_argument(
        "--test_labels_path",
        type=str,
        required=True,
        help=(
            "Path to CSV file containing the following columns: [agent_id, "
            "charge_off_within_3_months, charge_off_within_6_months, "
            "charge_off_within_9_months, charge_off_within_12_months]"
        )
    )
    parser.add_argument(
        "--grading_output_dir",
        type=str,
        required=True,
        help="Path to directory in which grading output CSV is written."
    )
    args = parser.parse_args()
    main(args.results_dir, args.test_labels_path, args.grading_output_dir)