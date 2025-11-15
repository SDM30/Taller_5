## =========================================================================
## @author Simon Díaz Monroy (simondiaz@javeriana.edu.co)
## @author Katheryn Sofia Guasca Chavarro (ksofia.guasca@javeriana.edu.co)
## =========================================================================

import csv
import os
import subprocess
import sys

GAME_CMD = ["python3", "MineSweeper.py", "8", "8", "5"]
PLAYERS = [
    ("LogisticRegressionBot", "Player/LogisticRegressionBot.py"),
    ("RandomBot", "Player/Random.py"),
]
RESULT_FILE = "benchmark_results.csv"
PER_RUN_FILE = "benchmark_runs.csv"


def extract_metric(output, marker):
    idx = output.rfind(marker)
    if idx == -1:
        return None
    line = output[idx + len(marker):].splitlines()[0].strip()
    try:
        return float(line)
    except ValueError:
        return None


def run_game(cmd, cwd):
    completed = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    output = completed.stdout

    plays = 0
    marker = "Plays made:"
    idx = output.rfind(marker)
    if idx != -1:
        line = output[idx + len(marker):].splitlines()[0].strip()
        try:
            plays = int(line)
        except ValueError:
            plays = 0
    else:
        plays = output.count("Cell =")

    wins = 1 if "You won!" in output else 0
    losses = 1 if "You lose :-(" in output else 0
    result = "victoria" if wins else "derrota"

    accuracy = extract_metric(output, "[LogisticRegressionBot] Accuracy:")
    precision = extract_metric(output, "[LogisticRegressionBot] Precision:")
    return plays, wins, losses, result, accuracy, precision


def write_results(rows, path):
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for entry in rows:
            writer.writerow(["Tipo de jugador", entry["Tipo de jugador"]])
            writer.writerow(
                [
                    "numero de pruebas",
                    "numero de jugadas",
                    "derrotas",
                    "victorias",
                    "accuracy_promedio",
                    "precision_promedio",
                ]
            )
            writer.writerow(
                [
                    entry["numero de pruebas"],
                    entry["numero de jugadas"],
                    entry["derrotas"],
                    entry["victorias"],
                    entry.get("avg_accuracy", ""),
                    entry.get("avg_precision", ""),
                ]
            )
            writer.writerow([])


def write_per_run(base_dir, player_name, per_run_rows):
    per_run_path = os.path.join(base_dir, f"{player_name}_{PER_RUN_FILE}")
    with open(per_run_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tipo de jugador", player_name])
        writer.writerow(["prueba #", "jugadas", "resultado", "accuracy", "precision"])
        for row in per_run_rows:
            writer.writerow(
                [
                    row["test"],
                    row["plays"],
                    row["result"],
                    "" if row["accuracy"] is None else row["accuracy"],
                    "" if row["precision"] is None else row["precision"],
                ]
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3", sys.argv[0], "number_tests")
        sys.exit(1)

    number_tests = int(sys.argv[1])
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results = []

    for player_name, player_path in PLAYERS:
        stats = {
            "Tipo de jugador": player_name,
            "numero de pruebas": number_tests,
            "numero de jugadas": 0,
            "derrotas": 0,
            "victorias": 0,
            "metrics_count": 0,
            "accuracy_sum": 0.0,
            "precision_sum": 0.0,
        }
        cmd = GAME_CMD + [player_path, "--no-save-data"]
        per_run_rows = []
        for test_index in range(1, number_tests + 1):
            plays, wins, losses, result, accuracy, precision = run_game(cmd, base_dir)
            stats["numero de jugadas"] += plays
            stats["victorias"] += wins
            stats["derrotas"] += losses
            per_run_rows.append(
                {
                    "test": test_index,
                    "plays": plays,
                    "result": result,
                    "accuracy": accuracy,
                    "precision": precision,
                }
            )
            if accuracy is not None and precision is not None:
                stats["accuracy_sum"] += accuracy
                stats["precision_sum"] += precision
                stats["metrics_count"] += 1
        results.append(stats)
        write_per_run(base_dir, player_name, per_run_rows)

    output_path = os.path.join(base_dir, RESULT_FILE)
    for entry in results:
        if entry["metrics_count"] > 0:
            entry["avg_accuracy"] = entry["accuracy_sum"] / entry["metrics_count"]
            entry["avg_precision"] = entry["precision_sum"] / entry["metrics_count"]
        else:
            entry["avg_accuracy"] = ""
            entry["avg_precision"] = ""
    write_results(results, output_path)
