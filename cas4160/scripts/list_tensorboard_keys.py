from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


def list_scalar_keys(log_file):
    # Initialize an EventAccumulator with the path to the log directory
    event_acc = EventAccumulator(log_file)
    event_acc.Reload()  # Load the events from disk

    # Get list of all available tags
    tags = event_acc.Tags()

    # Print all scalar tags
    print("\nAvailable scalar keys:")
    for tag in tags["scalars"]:
        print(f"- {tag}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_log_file", "-i", type=str, required=True)
    args = parser.parse_args()

    list_scalar_keys(args.input_log_file)
