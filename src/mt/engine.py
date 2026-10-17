"""
KoeBridge for Zoom — Machine Translation (MT) Engine
"""

from typing import Dict, Any, Optional
import time


CONVERSATIONAL_MEETING_PHRASES = {
    # Greetings & Departures
    "hello": "こんにちは。",
    "hello everyone": "皆さんこんにちは。",
    "hello there": "こんにちは。",
    "hi": "こんにちは。",
    "hi everyone": "皆さんこんにちは。",
    "good morning": "おはようございます。",
    "good afternoon": "こんにちは。",
    "good evening": "こんばんは。",
    "goodbye": "失礼いたします。",
    "bye": "失礼します。",
    "see you": "またお会いしましょう。",
    "see you later": "それではまた後ほど。",
    "have a good day": "良い一日を。",
    # Audio & Screen Checks
    "can you hear me": "私の声が聞こえますか？",
    "can everyone hear me": "皆さんに私の声が聞こえていますか？",
    "can you hear me now": "今、私の声が聞こえますか？",
    "can you see my screen": "私の画面が見えますか？",
    "can everyone see my screen": "皆さんに私の画面が見えていますか？",
    "i will share my screen": "画面を共有します。",
    "let me share my screen": "画面を共有させていただきます。",
    # Confirmations & Acknowledgements
    "yes": "はい。",
    "yes i do": "はい、そうです。",
    "yes i understand": "はい、理解いたしました。",
    "no": "いいえ。",
    "okay": "わかりました。",
    "ok": "了解いたしました。",
    "i see": "なるほど、わかりました。",
    "i understand": "承知いたしました。",
    "understood": "理解いたしました。",
    "i agree": "賛成です。",
    "sounds good": "いいですね、賛成です。",
    "that sounds good": "いいですね、賛成です。",
    "that makes sense": "なるほど、よくわかりました。",
    "exactly": "その通りです。",
    "right": "その通りです。",
    "sure": "もちろんです。",
    # Questions & Clarifications
    "i have a question": "質問があります。",
    "may i ask a question": "質問してもよろしいですか？",
    "could you repeat that": "もう一度お願いできますか？",
    "sorry could you repeat that": "すみません、もう一度お願いできますか？",
    "could you say that again": "もう一度言っていただけますか？",
    "one moment please": "少々お待ちください。",
    "wait a moment": "少々お待ちください。",
    # Courtesy & Politeness
    "thank you": "ありがとうございます。",
    "thank you very much": "どうもありがとうございます。",
    "thanks": "ありがとうございます。",
    "you are welcome": "どういたしまして。",
    "you're welcome": "どういたしまして。",
    "excuse me": "失礼します。",
    "sorry": "申し訳ありません。",
    "i am sorry": "申し訳ございません。",
    "nice to meet you": "はじめまして、よろしくお願いします。",
    "pleased to meet you": "お会いできて光栄です。",
    "looking forward to working with you": "どうぞよろしくお願いいたします。",
}


class MachineTranslationEngine:
    """
    Offline Machine Translation Engine (Argos Translate EN -> JA).
    """

    _SHARED_TRANSLATIONS: Dict[tuple, Any] = {}

    def __init__(self, from_code: str = "en", to_code: str = "ja"):
        self.from_code = from_code
        self.to_code = to_code
        self.translation = None
        self._is_loaded = False

    def load_model(self) -> bool:
        if self._is_loaded and self.translation is not None:
            return True

        cache_key = (self.from_code, self.to_code)
        if cache_key in MachineTranslationEngine._SHARED_TRANSLATIONS:
            self.translation = MachineTranslationEngine._SHARED_TRANSLATIONS[cache_key]
            self._is_loaded = True
            return True

        try:
            import argostranslate.package
            import argostranslate.translate

            installed_languages = argostranslate.translate.get_installed_languages()
            from_lang = next(
                (lang for lang in installed_languages if lang.code == self.from_code),
                None,
            )
            to_lang = next(
                (lang for lang in installed_languages if lang.code == self.to_code),
                None,
            )

            if from_lang and to_lang:
                translation = from_lang.get_translation(to_lang)
                if translation:
                    MachineTranslationEngine._SHARED_TRANSLATIONS[cache_key] = (
                        translation
                    )
                    self.translation = translation
                    self._is_loaded = True
                    print(
                        f"[MT] ArgosTranslate {self.from_code}->{self.to_code} loaded."
                    )
                    return True

            print(
                f"[MT] ArgosTranslate package {self.from_code}->{self.to_code} not found in local cache."
            )
            return False
        except ImportError:
            print("[MT] argostranslate not installed. Running in mock mode.")
            return False
        except Exception as e:
            print(f"[MT] Error loading argostranslate: {e}")
            return False

    def _normalize_conversational_input(self, text: str) -> Optional[str]:
        """Check if English text matches known conversational meeting phrases."""
        norm = text.strip().lower()
        # Remove trailing punctuation for matching
        norm_clean = norm.rstrip(".!?,")
        if norm_clean in CONVERSATIONAL_MEETING_PHRASES:
            return CONVERSATIONAL_MEETING_PHRASES[norm_clean]
        return None

    def _filter_argos_hallucinations(
        self, orig_text: str, ja_text: str
    ) -> Dict[str, Any]:
        """
        Check for known Argos Translate OpenNMT web crawl artifacts (e.g. website footers).
        Returns a dict with 'is_uncertain', 'translated_text', and optional 'error'.
        Never invents fallback translations (e.g. 'よろしくお願いします。' or '申し訳ありません。').
        """
        orig_lower = orig_text.lower().strip()
        norm_clean = orig_lower.rstrip(".!?,")

        # Check for web crawl footer artifacts
        has_contact_artifact = (
            "お問い合わせ" in ja_text
            and "contact" not in orig_lower
            and "inquiry" not in orig_lower
        )
        has_site_disclaimer = (
            "このコンテンツはただ今" in ja_text or "アメリカ英語 のみ" in ja_text
        )
        has_legal_boilerplate = any(
            bp in ja_text
            for bp in [
                "プライバシーポリシー",
                "利用規約",
                "クッキーの設定",
                "すべての権利を保有",
            ]
        )

        if has_contact_artifact or has_site_disclaimer or has_legal_boilerplate:
            # Check if the ENTIRE phrase is an exact known meeting phrase
            if norm_clean in CONVERSATIONAL_MEETING_PHRASES:
                return {
                    "is_uncertain": False,
                    "translated_text": CONVERSATIONAL_MEETING_PHRASES[norm_clean],
                }

            # Do NOT match first words. Do NOT invent 'よろしくお願いします。' or '申し訳ありません。'.
            # Return an explicit uncertain result to reject injection.
            return {
                "is_uncertain": True,
                "translated_text": "",
                "raw_translation": ja_text,
                "error": "Web crawl footer artifact detected in MT output.",
            }

        # Ensure sentence has appropriate Japanese punctuation
        ja_clean = ja_text.strip()
        if ja_clean and not ja_clean.endswith(("。", "？", "！", "?", "!")):
            if orig_text.strip().endswith("?") or any(
                orig_lower.startswith(w)
                for w in ["can ", "could ", "would ", "is ", "are ", "do ", "does "]
            ):
                ja_clean += "？"
            else:
                ja_clean += "。"

        return {
            "is_uncertain": False,
            "translated_text": ja_clean,
        }

    def translate(self, text: str) -> Dict[str, Any]:
        """Translate text from from_code to to_code."""
        if not text.strip():
            return {"translated_text": "", "latency_ms": 0.0}

        start_time = time.perf_counter()

        # 1. Check conversational meeting phrases first for 100% idiomatic Japanese
        conv_ja = self._normalize_conversational_input(text)
        if conv_ja:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "translated_text": conv_ja,
                "latency_ms": elapsed_ms,
                "is_mock": False,
                "is_uncertain": False,
            }

        if not self._is_loaded:
            if not self.load_model():
                # Fallback / Mock translation
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return {
                    "translated_text": f"[JA: {text}]",
                    "latency_ms": elapsed_ms,
                    "is_mock": True,
                    "is_uncertain": False,
                }

        try:
            translated = self.translation.translate(text)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            # Filter known hallucinations and ensure safety
            filter_res = self._filter_argos_hallucinations(text, translated)
            if filter_res.get("is_uncertain"):
                return {
                    "translated_text": "",
                    "raw_translation": translated,
                    "latency_ms": elapsed_ms,
                    "is_mock": False,
                    "is_uncertain": True,
                    "error": filter_res.get(
                        "error", "Translation rejected due to uncertainty."
                    ),
                }

            return {
                "translated_text": filter_res.get("translated_text", translated),
                "latency_ms": elapsed_ms,
                "is_mock": False,
                "is_uncertain": False,
            }
        except Exception as e:
            print(f"[MT] Translation error: {e}")
            return {
                "translated_text": text,
                "latency_ms": (time.perf_counter() - start_time) * 1000.0,
                "error": str(e),
            }
