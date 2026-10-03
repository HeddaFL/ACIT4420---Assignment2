"""
Purpose: write the three output files:
- analysis_summary.csv
- analysis_report.txt
- rejected_records.txt
"""

# imports
import csv
from pathlib import Path
from .errors import DataFileError

# Create the column names used in the summary files. 
SUMMARY_COLUMNS = [
    "session_id", "participant_id", "participant_name",
    "total_observations", "usable_observations", "low_quality_observations",
    "mean_heart_rate", "mean_skin_response", "mean_temperature", "mean_activity_level",
    "heart_rate_vs_baseline", "skin_response_vs_baseline", "temperature_vs_baseline",
    "classification", "classification_reason", "recovery_detected",
]

# make the results in analysis_summary.csv into one row per session with information. 
def summary_row(result):
    differences = result["baseline_differences"]
    return {
        "session_id": result["session_id"],
        "participant_id": result["participant_id"],
        "participant_name": result["participant_name"],
        "total_observations": result["total_observations"],
        "usable_observations": result["usable_observations"],
        "low_quality_observations": result["low_quality_observations"],
        "mean_heart_rate": result["heart_rate"]["average"],
        "mean_skin_response": result["skin_response"]["average"],
        "mean_temperature": result["temperature"]["average"],
        "mean_activity_level": result["activity_level"]["average"],
        "heart_rate_vs_baseline": differences["heart_rate"],
        "skin_response_vs_baseline": differences["skin_response"],
        "temperature_vs_baseline": differences["temperature"],
        "classification": result["classification"],
        "classification_reason": result["classification_reason"],
        "recovery_detected": result["recovery_detected"],
    }


# create readable lines for measurements, 
def describe_measurement(label, summary, difference, unit):
    if summary["count"] == 0:
        return f"  {label:<15}: no usable data"
    average = f"{summary['average']} {unit}".strip()   
    line = (f"  {label:<15}: average {average} "
            f"(min {summary['min']}, max {summary['max']}, n={summary['count']})")
    if difference is not None:
        line += f", {difference:+.2f} vs baseline"
    return line


# build the text that is in analysis_report.txt file, with both readable text and data. 
def build_report_text(result):

    differences = result["baseline_differences"]
    lines = [
        "=" * 67,
        f"Session {result['session_id']} with {result['participant_name']} ({result['participant_id']})",
        "=" * 67,
        f"Classification: {result['classification'].upper()}",
        f"Reason: {result['classification_reason']}",
        f"Observations used: {result['usable_observations']} of {result['total_observations']} "
        f"({result['low_quality_observations']} excluded because of low signal quality)",
        f"Recovery detected: {'yes' if result['recovery_detected'] else 'no'} "
        f"- {result['recovery_explanation']}",
        "-" * 67,
        describe_measurement("Heart rate", result["heart_rate"], differences["heart_rate"], "bpm"),
        describe_measurement("Skin response", result["skin_response"], differences["skin_response"], ""),
        describe_measurement("Temperature", result["temperature"], differences["temperature"], "C"),
        describe_measurement("Activity level", result["activity_level"], None, ""),
    ]
    return "\n".join(lines)

# Write the analysis_summary.csv with one row per session. 
def write_summary(path, results):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames = SUMMARY_COLUMNS)
        writer.writeheader()
        for result in results:
            writer.writerow(summary_row(result))

# write the analysis_report.txt 
def write_report(path, results):
    with open(path, "w", encoding="utf-8") as fh:
        if not results:
            fh.write("No sessions were analyzed.\n")
            return
        fh.write("\n\n".join(build_report_text(result) for result in results) + "\n")

# Write the rejected_records.txt with one line per rejected row.
# Each line should indicate one invalid session. 
def write_rejected(path, rejected):
    with open(path, "w", encoding="utf-8") as fh:
        if not rejected:
            fh.write("No rejected records.\n")
            return
        for record in rejected:
            fh.write(f"{record['source']} line {record['row']} "
                     f"[{record['field']}]: {record['reason']}\n")

# Create the output/ folder so the three files that needs to ne created can be stored. 
def write_outputs(output_dir, results, rejected):

    output_dir = Path(output_dir)
    summary_path = output_dir / "analysis_summary.csv"
    report_path = output_dir / "analysis_report.txt"
    rejected_path = output_dir / "rejected_records.txt"

    try:
        output_dir.mkdir(parents = True, exist_ok = True)
        write_summary(summary_path, results)
        write_report(report_path, results)
        write_rejected(rejected_path, rejected)

    except PermissionError:
        raise DataFileError(f"{output_dir}: permission denied when writing the output files") from None
    
    except OSError as error:
        raise DataFileError(f"{output_dir}: cannot write the output files ({error})") from error

    return [summary_path, report_path, rejected_path]
