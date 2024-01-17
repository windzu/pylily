from argparse import ArgumentParser
from .auto_calibrator import AutoCalibrator
from .manual_calibrator import ManualCalibrator


# parse arguments
# -- mode : auto or manual
# -- config : config file path
def parse_args():
    parser = ArgumentParser(description="python implementation of Lily")
    parser.add_argument(
        "--mode",
        type=str,
        default="auto",
        help="auto or manual",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="",
        help="config file path",
    )
    return parser.parse_known_args()


def main():
    args, unknown = parse_args()

    mode = args.mode
    config = args.config

    if mode == "auto":
        auto_calibrator = AutoCalibrator(config)
        auto_calibrator.run()
    elif mode == "manual":
        manual_calibrator = ManualCalibrator(config)
        manual_calibrator.run()


if __name__ == "__main__":
    main()
