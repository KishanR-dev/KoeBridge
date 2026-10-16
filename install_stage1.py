import sys
import subprocess
import os

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "install_log.txt"
)


def main():
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--only-binary",
        ":all:",
        "pyaudiowpatch",
        "faster-whisper",
    ]
    print(f"Running: {' '.join(cmd)}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"Executing: {' '.join(cmd)}\n\n")
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            out.write(line)
            out.flush()
        proc.wait()
        out.write(f"\nExit code: {proc.returncode}\n")
    print(f"Finished with exit code {proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
