import sys
import os
import ctypes
from ctypes import wintypes
import winreg

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "probe_results.txt"
)


class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


def probe_all():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        orig_stdout = sys.stdout
        sys.stdout = Tee(orig_stdout, out_f)
        try:
            print("=" * 60)
            print("KOEBRIDGE PROBE: Environment & Capabilities")
            print("=" * 60)
            print(f"Python Executable: {sys.executable}")
            print(f"Python Version: {sys.version}")
            print(f"Platform: {sys.platform}")
            print(f"Architecture: {os.environ.get('PROCESSOR_ARCHITECTURE')}")
            print()

            # 1. Check AC Power
            print("[1] AC Power Status:")
            try:

                class SYSTEM_POWER_STATUS(ctypes.Structure):
                    _fields_ = [
                        ("ACLineStatus", wintypes.BYTE),
                        ("BatteryFlag", wintypes.BYTE),
                        ("BatteryLifePercent", wintypes.BYTE),
                        ("SystemStatusFlag", wintypes.BYTE),
                        ("BatteryLifeTime", wintypes.DWORD),
                        ("BatteryFullLifeTime", wintypes.DWORD),
                    ]

                sps = SYSTEM_POWER_STATUS()
                if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sps)):
                    ac_map = {
                        0: "Battery (Offline)",
                        1: "AC Power (Plugged in)",
                        255: "Unknown",
                    }
                    print(
                        f"  ACLineStatus: {sps.ACLineStatus} -> {ac_map.get(sps.ACLineStatus, 'Unknown')}"
                    )
                    print(f"  BatteryLifePercent: {sps.BatteryLifePercent}%")
                else:
                    print("  GetSystemPowerStatus failed")
            except Exception as e:
                print(f"  Error checking power: {e}")
            print()

            # 2. Check SAPI5 / OneCore Voices
            print("[2] Installed Windows Speech Voices (SAPI5 / OneCore):")

            def enum_reg_keys(root, path):
                voices = []
                try:
                    with winreg.OpenKey(root, path) as key:
                        num_subkeys = winreg.QueryInfoKey(key)[0]
                        for i in range(num_subkeys):
                            sub = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, sub) as vkey:
                                try:
                                    name = winreg.QueryValue(vkey, None)
                                except Exception:
                                    name = sub
                                try:
                                    desc = winreg.QueryValueEx(vkey, "")[0]
                                except Exception:
                                    desc = ""
                                try:
                                    with winreg.OpenKey(vkey, "Attributes") as akey:
                                        lang = winreg.QueryValueEx(akey, "Language")[0]
                                        gender = winreg.QueryValueEx(akey, "Gender")[0]
                                        vname = winreg.QueryValueEx(akey, "Name")[0]
                                        voices.append(
                                            {
                                                "id": sub,
                                                "name": vname,
                                                "desc": desc,
                                                "lang": lang,
                                                "gender": gender,
                                            }
                                        )
                                except Exception:
                                    voices.append(
                                        {"id": sub, "name": name, "desc": desc}
                                    )
                except Exception:
                    pass
                return voices

            sapi_voices = enum_reg_keys(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Speech\Voices\Tokens"
            )
            print(f"  SAPI5 Tokens (HKLM): {len(sapi_voices)} found")
            for v in sapi_voices:
                print(
                    f"    - {v.get('name', v.get('id'))} (Lang: {v.get('lang', 'Unknown')}, Gender: {v.get('gender', 'Unknown')})"
                )

            onecore_voices = enum_reg_keys(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens",
            )
            print(f"  OneCore Tokens (HKLM): {len(onecore_voices)} found")
            for v in onecore_voices:
                print(
                    f"    - {v.get('name', v.get('id'))} (Lang: {v.get('lang', 'Unknown')}, Gender: {v.get('gender', 'Unknown')})"
                )
            print()

            # 3. Check Windows Audio WaveIn / WaveOut devices
            print("[3] Windows WaveIn / WaveOut Devices (WinMM):")
            try:

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
                print(f"  WaveIn Devices (Recording / Microphones): {num_in}")
                wic = WAVEINCAPSW()
                for i in range(num_in):
                    if (
                        ctypes.windll.winmm.waveInGetDevCapsW(
                            i, ctypes.byref(wic), ctypes.sizeof(wic)
                        )
                        == 0
                    ):
                        print(f"    [{i}] {wic.szPname} (Channels: {wic.wChannels})")

                num_out = ctypes.windll.winmm.waveOutGetNumDevs()
                print(f"  WaveOut Devices (Playback / Outputs): {num_out}")
                woc = WAVEOUTCAPSW()
                for i in range(num_out):
                    if (
                        ctypes.windll.winmm.waveOutGetDevCapsW(
                            i, ctypes.byref(woc), ctypes.sizeof(woc)
                        )
                        == 0
                    ):
                        print(f"    [{i}] {woc.szPname} (Channels: {woc.wChannels})")
            except Exception as e:
                print(f"  Error enumerating WinMM devices: {e}")
            print()

            # 4. Check for Tkinter
            print("[4] GUI / Tkinter Check:")
            try:
                import tkinter

                tk_ver = tkinter.TkVersion
                print(f"  Tkinter is available (Tcl/Tk version: {tk_ver})")
            except Exception as e:
                print(f"  Tkinter error: {e}")
            print()

            # 5. Check pip package availability for audio/STT/TTS
            print("[5] Key Python Module Availability:")
            modules_to_test = [
                "numpy",
                "pydub",
                "pyaudio",
                "pyaudiowpatch",
                "sounddevice",
                "soundcard",
                "faster_whisper",
                "ctranslate2",
                "onnxruntime",
                "argostranslate",
                "pyttsx3",
                "win32com.client",
                "comtypes",
                "torch",
            ]
            for mod in modules_to_test:
                try:
                    __import__(mod)
                    print(f"  [INSTALLED] {mod}")
                except ImportError:
                    print(f"  [NOT INSTALLED] {mod}")
                except Exception as e:
                    print(f"  [ERROR] {mod}: {e}")
            print()
            print("=" * 60)
        finally:
            sys.stdout = orig_stdout


if __name__ == "__main__":
    probe_all()
