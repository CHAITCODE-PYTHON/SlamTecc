#STEP 6 — Evaluation Module (Table + Graphs)
# This is what your sir wants. Results that prove TECC works.

# evaluate.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

os.makedirs("results", exist_ok=True)


def generate_results(raw_log):
    df = pd.DataFrame(raw_log)

    # Add correctness column (manually label or use string match)
    df["was_corrected"] = df["raw"] != df["corrected"]
    df["is_valid"] = df["corrected"] != "INVALID"

    print("\n===== RESULTS TABLE =====")
    print(df[["raw", "corrected", "confidence", "was_corrected"]].to_string(index=False))

    # Save table as CSV
    df.to_csv("results/tecc_results.csv", index=False)
    print("\nTable saved to results/tecc_results.csv")

    # ---- GRAPH 1: Confidence Distribution ----
    plt.figure(figsize=(8, 5))
    plt.hist(df["confidence"], bins=10, color="steelblue", edgecolor="black")
    plt.title("OCR Confidence Score Distribution")
    plt.xlabel("Confidence Score")
    plt.ylabel("Number of Detections")
    plt.tight_layout()
    plt.savefig("results/graph_confidence.png")
    plt.close()
    print("Graph 1 saved: confidence distribution")

    # ---- GRAPH 2: Raw vs Corrected (Before/After TECC) ----
    labels = ["Raw OCR Errors", "TECC Corrected", "Invalid/Rejected"]
    errors = df["was_corrected"].sum()
    corrected = df[df["was_corrected"] & df["is_valid"]].shape[0]
    invalid = (~df["is_valid"]).sum()
    values = [errors, corrected, invalid]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, values, color=["tomato", "mediumseagreen", "gray"])
    plt.title("TECC Error Correction Summary")
    plt.ylabel("Count")
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1,
                 str(int(bar.get_height())),
                 ha='center', fontsize=12)
    plt.tight_layout()
    plt.savefig("results/graph_correction.png")
    plt.close()
    print("Graph 2 saved: correction summary")

    # ---- GRAPH 3: Accuracy per image ----
    plt.figure(figsize=(9, 5))
    plt.plot(range(len(df)), df["confidence"], marker='o',
             color='royalblue', label="OCR Confidence")
    plt.axhline(y=0.7, color='red', linestyle='--', label="Threshold (0.7)")
    plt.title("Per-Detection OCR Confidence vs Threshold")
    plt.xlabel("Detection Index")
    plt.ylabel("Confidence Score")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/graph_perdetection.png")
    plt.close()
    print("Graph 3 saved: per detection confidence")

    return df
