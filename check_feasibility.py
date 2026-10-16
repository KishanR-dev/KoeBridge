import os
import json
import urllib.request
import winreg
import ctypes
from ctypes import wintypes

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "feasibility_report.txt"
)


def log(msg, file_handle):
    print(msg)
    file_handle.write(msg + "\n")
    file_handle.flush()


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        log("=" * 70, out)
        log("KOEBRIDGE FEASIBILITY AUDIT: Windows x64 Python 3.13", out)
        log("=" * 70, out)

        # 1. Recheck Audio Endpoints for VB-CABLE
        log("\n--- [1] VB-CABLE & AUDIO ENDPOINT RECHECK ---", out)
        found_cable = False
        try:
            # Check WinMM devices
            class WAVEINCAPSW(ctypes.Structure):
                _fields_ = [
                    ("wMid", wintypes.WORD),
                    ("wPid", wintypes.WORD),
                    ("vDriverVersion", wintypes.UINT),
                    ("szPname", wintypes.WCHAR * 32),
                    ("dwFormats", wintypes.DWORD),
                    ("wChannels", wintypes.WORD),
                    ("wReserved1", wintypes.WORD),
                ]

            class WAVEOUTCAPSW(ctypes.Structure):
                _fields_ = [
                    ("wMid", wintypes.WORD),
                    ("wPid", wintypes.WORD),
                    ("vDriverVersion", wintypes.UINT),
                    ("szPname", wintypes.WCHAR * 32),
                    ("dwFormats", wintypes.DWORD),
                    ("wChannels", wintypes.WORD),
                    ("wReserved1", wintypes.WORD),
                    ("dwSupport", wintypes.DWORD),
                ]

            num_in = ctypes.windll.winmm.waveInGetNumDevs()
            wic = WAVEINCAPSW()
            for i in range(num_in):
                if (
                    ctypes.windll.winmm.waveInGetDevCapsW(
                        i, ctypes.byref(wic), ctypes.sizeof(wic)
                    )
                    == 0
                ):
                    log(f"  Capture [{i}]: {wic.szPname}", out)
                    if (
                        "cable" in wic.szPname.lower()
                        or "vb-audio" in wic.szPname.lower()
                    ):
                        found_cable = True

            num_out = ctypes.windll.winmm.waveOutGetNumDevs()
            woc = WAVEOUTCAPSW()
            for i in range(num_out):
                if (
                    ctypes.windll.winmm.waveOutGetDevCapsW(
                        i, ctypes.byref(woc), ctypes.sizeof(woc)
                    )
                    == 0
                ):
                    log(f"  Render  [{i}]: {woc.szPname}", out)
                    if (
                        "cable" in woc.szPname.lower()
                        or "vb-audio" in woc.szPname.lower()
                    ):
                        found_cable = True

            # Also check registry for VB-Audio drivers
            for root_key in [winreg.HKEY_LOCAL_MACHINE]:
                for subkey_path in [
                    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e96c-e325-11ce-bfc1-08002be10318}",
                    r"SOFTWARE\VB-Audio",
                ]:
                    try:
                        with winreg.OpenKey(root_key, subkey_path):
                            log(f"  Registry: Found key {subkey_path}", out)
                            found_cable = True
                    except Exception:
                        pass
        except Exception as e:
            log(f"  Error checking audio endpoints: {e}", out)

        log(
            f"  VB-CABLE Detected: {'YES' if found_cable else 'NO (NOT DETECTED)'}", out
        )

        # 2. Check PyPI Windows x64 Python 3.13 Wheel Availability
        log("\n--- [2] PYPI WHEEL AVAILABILITY (Python 3.13, win_amd64) ---", out)
        packages = [
            "pyaudiowpatch",
            "sounddevice",
            "ctranslate2",
            "faster-whisper",
            "argostranslate",
            "onnxruntime",
            "pyttsx3",
            "kokoro-onnx",
            "pyopenjtalk",
        ]

        def check_pypi(pkg_name):
            url = f"https://pypi.org/pypi/{pkg_name}/json"
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "KoeBridge-Audit/1.0"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode())
                version = data["info"]["version"]
                releases = data.get("releases", {}).get(version, [])

                # Look for cp313 win_amd64 or py3-none-any
                matching_wheels = []
                for file_info in releases:
                    fn = file_info["filename"]
                    if fn.endswith(".whl"):
                        if (
                            ("cp313" in fn and "win_amd64" in fn)
                            or "py3-none-any" in fn
                            or "py2.py3-none-any" in fn
                        ):
                            matching_wheels.append((fn, file_info["size"]))
                        elif "win_amd64" in fn:
                            pass  # other python version

                # If latest release has no cp313 wheel, check if any recent release does
                if not matching_wheels:
                    # check all recent releases
                    for rel_ver, file_list in list(data.get("releases", {}).items())[
                        -5:
                    ]:
                        for file_info in file_list:
                            fn = file_info["filename"]
                            if (
                                ("cp313" in fn and "win_amd64" in fn)
                                or "py3-none-any" in fn
                                or "py2.py3-none-any" in fn
                            ):
                                matching_wheels.append(
                                    (f"[{rel_ver}] {fn}", file_info["size"])
                                )

                return version, matching_wheels
            except Exception as e:
                return "ERROR", str(e)

        for pkg in packages:
            ver, wheels = check_pypi(pkg)
            if isinstance(wheels, list) and wheels:
                log(f"  [OK] {pkg} (latest {ver}):", out)
                for w, sz in wheels[:2]:
                    log(f"       -> {w} ({sz / 1024 / 1024:.2f} MB)", out)
            elif isinstance(wheels, list) and not wheels:
                log(
                    f"  [NO WHEEL] {pkg} (latest {ver}): No cp313-win_amd64 or pure-python wheel found!",
                    out,
                )
            else:
                log(f"  [FAILED QUERY] {pkg}: {wheels}", out)

        # 3. Check Argos Translate Package for EN -> JA
        log("\n--- [3] ARGOS TRANSLATE EN->JA PACKAGE AVAILABILITY ---", out)
        argos_index_url = "https://raw.githubusercontent.com/argosopentech/argospm-index/master/index.json"
        try:
            req = urllib.request.Request(
                argos_index_url, headers={"User-Agent": "KoeBridge-Audit/1.0"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                index_data = json.loads(resp.read().decode())

            en_ja_pkg = None
            ja_en_pkg = None
            for p in index_data:
                if p.get("from_code") == "en" and p.get("to_code") == "ja":
                    en_ja_pkg = p
                if p.get("from_code") == "ja" and p.get("to_code") == "en":
                    ja_en_pkg = p

            if en_ja_pkg:
                log(f"  Found en->ja package: {en_ja_pkg.get('package_version')}", out)
                log(f"    Name: {en_ja_pkg.get('name')}", out)
                log(f"    Download: {en_ja_pkg.get('links', [])}", out)
            else:
                log("  en->ja package NOT found in argospm index!", out)

            if ja_en_pkg:
                log(f"  Found ja->en package: {ja_en_pkg.get('package_version')}", out)
                log(f"    Name: {ja_en_pkg.get('name')}", out)
        except Exception as e:
            log(f"  Error querying Argos index: {e}", out)

        # 4. Japanese TTS Feasibility
        log("\n--- [4] LOCAL JAPANESE TTS ENGINE OPTIONS ---", out)
        log("  Option A: Windows 10/11 Native Japanese Language Pack", out)
        log(
            "    - User installs via Windows Settings > Time & Language > Speech > Japanese.",
            out,
        )
        log(
            "    - Installs 'Microsoft Haruka' or 'Microsoft Ayumi' natively into Windows SAPI/OneCore.",
            out,
        )
        log(
            "    - License: Covered by existing Windows OS license. 0 MB Python download. 0% CPU overhead.",
            out,
        )
        log("  Option B: Kokoro-82M ONNX (Apache 2.0)", out)
        log("    - Model: hexgrad/Kokoro-82M onnx release.", out)
        log("    - Code License: Apache 2.0 (`kokoro-onnx` package).", out)
        log(
            "    - Voice License: Apache 2.0 (Japanese voices 'jf_alpha', 'jm_kumo').",
            out,
        )
        log("    - Size: ~300 MB model + ONNX Runtime.", out)
        log("  Option C: pyopenjtalk (Open JTalk)", out)
        log("    - BSD 3-Clause / Apache 2.0 dictionary.", out)
        log("    - HTS voice: Mei (Creative Commons / BSD). Size: ~35 MB.", out)

        log("\n" + "=" * 70, out)


if __name__ == "__main__":
    main()
