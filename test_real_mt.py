"""
KoeBridge for Zoom — Test Real English to Japanese Machine Translation
"""

import time
from src.mt.engine import MachineTranslationEngine

mt = MachineTranslationEngine(from_code="en", to_code="ja")
t0 = time.perf_counter()
loaded = mt.load_model()
load_time_ms = (time.perf_counter() - t0) * 1000.0
print(f"Model loaded: {loaded} ({load_time_ms:.1f}ms)")
assert loaded is True

phrases = [
    "Hello, nice to meet you.",
    "Can you hear my voice?",
    "Thank you very much.",
    "Let's begin the meeting.",
    "I agree with this proposal.",
    "Please share your screen.",
]

print("\n--- Real English-to-Japanese Translations ---")
for p in phrases:
    res = mt.translate(p)
    print(f"EN: {p}")
    print(
        f"JA: {res['translated_text']} (latency: {res['latency_ms']:.1f}ms, is_mock: {res['is_mock']})"
    )
