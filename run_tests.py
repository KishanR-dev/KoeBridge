"""
KoeBridge for Zoom — Test Runner
"""

import sys
import os
import pytest

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test_results.txt"
)


def main():
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        sys.stdout = f
        sys.stderr = f
        try:
            ret = pytest.main(["-v", "tests"])
        finally:
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr
    print(f"Pytest exited with code: {ret}. Results written to test_results.txt")
    return ret


if __name__ == "__main__":
    sys.exit(main())
