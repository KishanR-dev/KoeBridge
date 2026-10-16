"""
KoeBridge for Zoom — Application Entrypoint
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.app import run_gui


def main():
    print("=" * 60)
    print("Starting KoeBridge for Zoom — Meeting Translator")
    print("=" * 60)
    run_gui()


if __name__ == "__main__":
    main()
