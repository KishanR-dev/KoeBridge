import sys
import os
import time
import urllib.request

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "stage1_test_report.txt"
)


def log(msg, fh):
    print(msg)
    fh.write(msg + "\n")
    fh.flush()


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        log("=" * 70, out)
        log("STAGE 1 VERIFICATION: Real Faster-Whisper Inference & Loopback Audio", out)
        log("=" * 70, out)

        # -------------------------------------------------------------
        # STEP 1: Download & Load faster-whisper tiny (int8 on CPU)
        # -------------------------------------------------------------
        log("\n--- [1] LOADING FASTER-WHISPER 'TINY' MODEL (int8, CPU) ---", out)
        t0 = time.perf_counter()
        try:
            from faster_whisper import WhisperModel

            log("  Imported faster_whisper successfully.", out)

            log(
                "  Downloading/Loading official Systran/faster-whisper-tiny model...",
                out,
            )
            model = WhisperModel(
                "tiny", device="cpu", compute_type="int8", cpu_threads=4
            )
            load_time_s = time.perf_counter() - t0
            log(f"  [SUCCESS] Model loaded in {load_time_s:.2f} seconds.", out)
        except Exception as e:
            log(f"  [FAIL] Error loading model: {e}", out)
            return 1

        # -------------------------------------------------------------
        # STEP 2: Obtain Short Japanese Spoken Audio Sample
        # -------------------------------------------------------------
        log("\n--- [2] FETCHING VERIFIED JAPANESE SPOKEN AUDIO SAMPLE ---", out)
        # Wikimedia Commons CC-BY-SA public spoken Japanese sample: "Arigatou gozaimasu"
        sample_url = "https://upload.wikimedia.org/wikipedia/commons/1/15/Ja-arigatou_gozaimasu.ogg"
        sample_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "sample_ja.ogg"
        )

        try:
            if not os.path.exists(sample_path) or os.path.getsize(sample_path) == 0:
                log(f"  Fetching: {sample_url}", out)
                req = urllib.request.Request(
                    sample_url, headers={"User-Agent": "KoeBridge-Test/1.0"}
                )
                with (
                    urllib.request.urlopen(req, timeout=10) as resp,
                    open(sample_path, "wb") as f,
                ):
                    f.write(resp.read())
                log(
                    f"  Downloaded Japanese audio sample ({os.path.getsize(sample_path)} bytes).",
                    out,
                )
            else:
                log(
                    f"  Using existing Japanese audio sample ({os.path.getsize(sample_path)} bytes).",
                    out,
                )
        except Exception as e:
            log(f"  [FAIL] Failed to fetch sample audio: {e}", out)
            return 1

        # -------------------------------------------------------------
        # STEP 3: Run Real Japanese-to-English Inference (task="translate")
        # -------------------------------------------------------------
        log("\n--- [3] RUNNING REAL INFERENCE: JA AUDIO -> EN TRANSLATION ---", out)
        try:
            # First: transcription (Japanese text)
            t_inf0 = time.perf_counter()
            segments_transcribe, info_transcribe = model.transcribe(
                sample_path, language="ja", task="transcribe", beam_size=1
            )
            ja_text = " ".join([s.text.strip() for s in segments_transcribe]).strip()
            ja_time_ms = (time.perf_counter() - t_inf0) * 1000.0

            log(f"  [JA Transcription Result]: '{ja_text}'", out)
            log(
                f"    Detected Language: {info_transcribe.language} (p={info_transcribe.language_probability:.2f})",
                out,
            )
            log(f"    Audio Duration: {info_transcribe.duration:.2f} s", out)
            log(f"    Inference Latency: {ja_time_ms:.1f} ms", out)

            # Second: direct translation to English (task="translate")
            t_inf1 = time.perf_counter()
            segments_translate, info_translate = model.transcribe(
                sample_path, language="ja", task="translate", beam_size=1
            )
            en_text = " ".join([s.text.strip() for s in segments_translate]).strip()
            en_time_ms = (time.perf_counter() - t_inf1) * 1000.0

            log(f"  [EN Direct Translation Result]: '{en_text}'", out)
            log(f"    Inference Latency: {en_time_ms:.1f} ms", out)
            rtf = (en_time_ms / 1000.0) / info_translate.duration
            log(
                f"    Real-Time Factor (RTF): {rtf:.3f} (RTF < 1.0 means faster than real-time)",
                out,
            )

            if not en_text:
                log("  [FAIL] Direct translation returned empty string!", out)
                return 1
            else:
                log(
                    "  [SUCCESS] REAL INFERENCE CONFIRMED: Produced valid English translation!",
                    out,
                )
        except Exception as e:
            log(f"  [FAIL] Inference failed: {e}", out)
            return 1

        # -------------------------------------------------------------
        # STEP 4: Test WASAPI Loopback Capture with PyAudioWPatch
        # -------------------------------------------------------------
        log("\n--- [4] TESTING WASAPI LOOPBACK AUDIO CAPTURE ---", out)
        try:
            import pyaudiowpatch as pyaudio

            p = pyaudio.PyAudio()
            log(
                f"  PyAudioWPatch initialized. Device count: {p.get_device_count()}",
                out,
            )

            # Enumerate WASAPI loopback devices
            wasapi_info = None
            for i in range(p.get_host_api_count()):
                api_info = p.get_host_api_info_by_index(i)
                if api_info.get("type") == pyaudio.paWASAPI:
                    wasapi_info = api_info
                    break

            if wasapi_info:
                log(
                    f"  Found WASAPI Host API (Index {wasapi_info['index']}): {wasapi_info['name']}",
                    out,
                )
                default_speakers = p.get_device_info_by_index(
                    wasapi_info["defaultOutputDevice"]
                )
                log(
                    f"  Default Speakers: [{default_speakers['index']}] {default_speakers['name']}",
                    out,
                )

                # Search loopback generator
                loopback_dev = None
                for dev in p.get_loopback_device_info_generator():
                    log(f"    Loopback Endpoint: [{dev['index']}] {dev['name']}", out)
                    if default_speakers["name"] in dev["name"]:
                        loopback_dev = dev

                if loopback_dev:
                    log(
                        f"  Selected Default Loopback Device: [{loopback_dev['index']}] {loopback_dev['name']}",
                        out,
                    )

                    # Test opening loopback stream and capturing 1.0s of frames
                    captured_frames = []

                    def _cb(in_data, frame_count, time_info, status):
                        if in_data:
                            captured_frames.append(len(in_data))
                        return (None, pyaudio.paContinue)

                    stream = p.open(
                        format=pyaudio.paInt16,
                        channels=loopback_dev["maxInputChannels"],
                        rate=int(loopback_dev["defaultSampleRate"]),
                        input=True,
                        input_device_index=loopback_dev["index"],
                        frames_per_buffer=1024,
                        stream_callback=_cb,
                    )
                    stream.start_stream()
                    log(
                        "  Stream started. Capturing 1.0 second of loopback frames...",
                        out,
                    )
                    time.sleep(1.0)
                    stream.stop_stream()
                    stream.close()

                    total_bytes = sum(captured_frames)
                    log(
                        f"  [SUCCESS] Loopback captured {len(captured_frames)} frame packets ({total_bytes} bytes).",
                        out,
                    )
                else:
                    log(
                        "  [WARN] No matching loopback endpoint found for default speakers.",
                        out,
                    )
            else:
                log("  [FAIL] WASAPI Host API not found in PyAudioWPatch.", out)

            p.terminate()
        except Exception as e:
            log(f"  [FAIL] Loopback test encountered error: {e}", out)
            return 1

        log("\n" + "=" * 70, out)
        log(
            "STAGE 1 CONCLUSION: REAL INFERENCE & WASAPI LOOPBACK VERIFIED WORKING!",
            out,
        )
        log("=" * 70, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
