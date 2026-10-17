"""
Regression tests for translation safeguards in Inbound and Outbound pipelines.

Covers:
1. Known greeting hallucination normalization (e.g. 'こんにちは' -> 'Hello.').
2. Legitimate sentences containing 'end' or 'bye' preserved intact without false replacement.
3. Unknown technical question handling (no first-word keyword hijack).
4. Argos web crawl footer hallucination rejection (no 'よろしくお願いします。' fallback).
5. Uncertain translations strictly rejected from TTS synthesis and Zoom audio injection.
"""

from unittest.mock import MagicMock
import numpy as np
from src.pipeline.inbound import InboundPipeline
from src.mt.engine import MachineTranslationEngine
from src.pipeline.outbound import OutboundPipeline


def test_inbound_greeting_hallucination_normalization():
    """Verify that only exact standalone greetings with known hallucination signatures are normalized."""
    pipeline = InboundPipeline()

    # Positive case: Exact standalone greeting with known Whisper hallucination
    assert (
        pipeline._normalize_inbound_translation("こんにちは", "This is the end.")
        == "Hello."
    )
    assert (
        pipeline._normalize_inbound_translation(
            "こんにちわ。", "Thank you for watching"
        )
        == "Hello."
    )
    assert pipeline._normalize_inbound_translation("どうもこんにちは", "") == "Hello."
    assert (
        pipeline._normalize_inbound_translation(
            "ありがとうございます", "Please subscribe."
        )
        == "Thank you."
    )


def test_inbound_legitimate_sentence_with_end_or_bye_preserved():
    """Verify that sentences containing 'end', 'bye', or 'this is' are NOT falsely converted."""
    pipeline = InboundPipeline()

    # Legitimate sentence with 'end'
    s1_ja = "ミーティングの終了時間は5時です"
    s1_en = "The meeting will end at 5 PM."
    assert pipeline._normalize_inbound_translation(s1_ja, s1_en) == s1_en

    # Legitimate sentence with 'This is the end'
    s2_ja = "これで本日の発表を終了します"
    s2_en = "This is the end of today's presentation."
    assert pipeline._normalize_inbound_translation(s2_ja, s2_en) == s2_en

    # Legitimate sentence with 'bye'
    s3_ja = "バイバイ、それではまた来週"
    s3_en = "Bye bye, see you next week."
    assert pipeline._normalize_inbound_translation(s3_ja, s3_en) == s3_en

    # Negative question: '質問がありません' (I have no questions) must not become 'I have a question.'
    s4_ja = "質問がありません"
    s4_en = "I have no questions."
    assert pipeline._normalize_inbound_translation(s4_ja, s4_en) == s4_en


def test_inbound_generic_hallucination_exposes_uncertainty():
    """Verify that YouTube end-card hallucinations on non-greeting audio preserve Japanese text rather than inventing English."""
    pipeline = InboundPipeline()

    # Non-greeting audio where Whisper produced YouTube end-screen artifact
    ja_text = "次の議題について検討しましょう"
    en_hallucination = "Thank you for watching this video."
    normalized = pipeline._normalize_inbound_translation(ja_text, en_hallucination)

    # Uncertainty exposed by showing original Japanese transcription
    assert normalized == f"[JA: {ja_text}]"


def test_outbound_conversational_exact_phrases_supported():
    """Verify that exact conversational meeting phrases translate to natural idiomatic Japanese."""
    mt = MachineTranslationEngine()

    res1 = mt.translate("Can you hear me?")
    assert res1["translated_text"] == "私の声が聞こえますか？"
    assert not res1.get("is_uncertain")

    res2 = mt.translate("Thank you very much.")
    assert "ありがとうございます" in res2["translated_text"]
    assert not res2.get("is_uncertain")


def test_outbound_unknown_technical_question_no_first_word_substitution():
    """Verify that an unknown sentence starting with 'can' or 'what' does NOT get replaced by a first-word match."""
    mt = MachineTranslationEngine()
    # Mock underlying translation to simulate normal non-hallucinatory translation
    mt._is_loaded = True
    mt.translation = MagicMock()
    mt.translation.translate.return_value = (
        "今日のKubernetesデプロイメントを完了できますか？"
    )

    input_text = "Can we finish the Kubernetes deployment today?"
    res = mt.translate(input_text)

    # Must NOT be replaced with "私の声が聞こえますか？"
    assert res["translated_text"] != "私の声が聞こえますか？"
    assert "Kubernetes" in res["translated_text"]
    assert not res.get("is_uncertain")


def test_outbound_argos_website_footer_hallucination_rejected():
    """Verify that if Argos produces a website footer for an unknown sentence, it is rejected and never falls back to 'よろしくお願いします。'."""
    mt = MachineTranslationEngine()
    mt._is_loaded = True
    mt.translation = MagicMock()

    # Simulate Argos outputting the 'お問い合わせ' (Contact us) footer
    mt.translation.translate.return_value = "お問い合わせはこちら"

    input_text = "How do we scale the PostgreSQL connection pool?"
    res = mt.translate(input_text)

    # Must be flagged as uncertain, must NOT be 'よろしくお願いします。'
    assert res.get("is_uncertain") is True
    assert res["translated_text"] == ""
    assert "よろしくお願いします" not in res.get("raw_translation", "")
    assert "artifact detected" in res.get("error", "").lower()


def test_outbound_pipeline_rejects_uncertain_translation_zero_tts():
    """Verify that an uncertain translation halts the pipeline: emits FAILED, zero TTS calls, zero audio playback."""
    events = []

    def on_status(status, details):
        events.append((status, details))

    pipeline = OutboundPipeline(on_status=on_status)

    # Mock STT to return valid English speech
    pipeline.stt.transcribe = MagicMock(
        return_value={
            "text": "How do we scale the database connection pool?",
            "is_mock": False,
        }
    )

    # Mock MT to return an uncertain / website artifact translation
    pipeline.mt.translate = MagicMock(
        return_value={
            "translated_text": "",
            "raw_translation": "お問い合わせ",
            "is_mock": False,
            "is_uncertain": True,
            "error": "Web crawl footer artifact detected in MT output.",
        }
    )

    # Mock TTS and OutputRenderer to spy on whether they get invoked
    pipeline.tts.synthesize = MagicMock()
    pipeline.output_renderer.play = MagicMock()

    # Feed 1.0s dummy audio into buffer and process
    pipeline._record_buffer = [np.zeros(16000, dtype=np.float32)]
    pipeline._process_recorded_speech()

    # 1. Verify pipeline emitted FAILED status
    failed_events = [e for e in events if e[0] == "FAILED"]
    assert len(failed_events) == 1
    assert "Outbound MT Rejected" in failed_events[0][1]["message"]
    assert "Web crawl footer artifact" in failed_events[0][1]["message"]

    # 2. Strict safety check: TTS and OutputRenderer must have ZERO calls
    assert pipeline.tts.synthesize.call_count == 0
    assert pipeline.output_renderer.play.call_count == 0
