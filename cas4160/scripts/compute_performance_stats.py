from parse_tensorboard import extract_tensorboard_scalars, compute_mean_std
import numpy as np


def print_performance_stats(log_files, data_key):
    # Extract scalars from all log files
    all_scalars = [extract_tensorboard_scalars(log, data_key) for log in log_files]

    # Compute mean and std
    steps, mean, std = compute_mean_std(all_scalars, data_key)

    print(f"\nStatistics for {data_key}:")
    print("-" * 50)
    print(f"Mean values at different steps:")
    for i, (step, m, s) in enumerate(zip(steps, mean, std)):
        if i % 10 == 0:  # Print every 10th value to keep output readable
            print(f"Step {step:.0f}: Mean = {m:.4f} ± {s:.4f} (std)")

    print("\nOverall statistics:")
    print(f"Average mean across all steps: {np.mean(mean):.4f}")
    print(f"Average std across all steps: {np.mean(std):.4f}")
    print(f"Max mean: {np.max(mean):.4f}")
    print(f"Min mean: {np.min(mean):.4f}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_log_files", "-i", nargs="+", required=True)
    parser.add_argument("--data_key", "-d", type=str, required=True)
    args = parser.parse_args()

    print_performance_stats(args.input_log_files, args.data_key)
