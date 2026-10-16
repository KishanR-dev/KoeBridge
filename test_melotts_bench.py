"""
KoeBridge for Zoom — MeloTTS-Japanese Synthesis Benchmarks
"""
import onnxruntime as ort
import numpy as np
import time, os, wave

# Load tokens
with open("models/tts_melotts_ja/tokens.txt", encoding="utf-8") as f:
    tokens = {line.split()[0]: int(line.split()[1]) for line in f}

punct_map = {"。": ".", "、": ",", "？": "?", "！": "!", "?": "?", "!": "!", ".": ".", ",": ","}

# Load lexicon
lexicon = {}
with open("models/tts_melotts_ja/lexicon.txt", encoding="utf-8") as f:
    for line in f:
        splits = line.strip().split()
        if not splits:
            continue
        w = splits[0]
        items = splits[1:]
        half = len(items) // 2
        phones = items[:half]
        tones = [int(t) for t in items[half:]]
        lexicon[w] = (phones, tones)


def tokenize_ja(text):
    phones, tones = [], []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in punct_map:
            p = punct_map[ch]
            if p in tokens:
                phones.append(tokens[p])
                tones.append(0)
            i += 1
            continue
        if ch in (" ", "\t", "\n", "\r"):
            if "_" in tokens:
                phones.append(tokens["_"])
                tones.append(0)
            i += 1
            continue
        matched = False
        for l in range(min(15, n - i), 0, -1):
            sub = text[i : i + l]
            if sub in lexicon:
                p_list, t_list = lexicon[sub]
                for p, t in zip(p_list, t_list):
                    if p in tokens:
                        phones.append(tokens[p])
                        tones.append(t)
                i += l
                matched = True
                break
        if not matched:
            i += 1
    return phones, tones


sess = ort.InferenceSession("models/tts_melotts_ja/model.onnx", providers=["CPUExecutionProvider"])

sentences = [
    "ありがとうございます。",
    "会議を始めましょう。",
    "画面をシェアしてください。",
    "この提案に同意します。",
]

print("--- MeloTTS-Japanese Synthesis Benchmarks ---")
for idx, text in enumerate(sentences):
    t0 = time.perf_counter()
    phones, tones = tokenize_ja(text)

    # Interleave blanks
    new_phones = [0] * (2 * len(phones) + 1)
    new_tones = [0] * (2 * len(tones) + 1)
    new_phones[1::2] = phones
    new_tones[1::2] = tones

    x = np.array([new_phones], dtype=np.int64)
    x_lengths = np.array([len(new_phones)], dtype=np.int64)
    tones_arr = np.array([new_tones], dtype=np.int64)
    sid = np.array([0], dtype=np.int64)
    noise_scale = np.array([0.6], dtype=np.float32)
    length_scale = np.array([1.0], dtype=np.float32)
    noise_scale_w = np.array([0.8], dtype=np.float32)

    outputs = sess.run(
        ["y"],
        {
            "x": x,
            "x_lengths": x_lengths,
            "tones": tones_arr,
            "sid": sid,
            "noise_scale": noise_scale,
            "length_scale": length_scale,
            "noise_scale_w": noise_scale_w,
        },
    )
    latency_ms = (time.perf_counter() - t0) * 1000.0
    audio = outputs[0][0][0]
    duration_s = len(audio) / 44100.0
    rms = np.sqrt(np.mean(audio**2))

    wav_name = f"out_phrase_{idx+1}.wav"
    int16_audio = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(wav_name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(int16_audio.tobytes())

    print(f'Phrase {idx+1}: "{text}"')
    print(
        f"  Duration: {duration_s:.2f} s | Rate: 44100 Hz | Latency: {latency_ms:.1f} ms | RMS: {rms:.4f} | WAV: {wav_name}"
    )
