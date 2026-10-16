"""
KoeBridge for Zoom — Machine Translation (MT) Engine
"""

from typing import Dict, Any
import time


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

    def translate(self, text: str) -> Dict[str, Any]:
        """Translate text from from_code to to_code."""
        if not text.strip():
            return {"translated_text": "", "latency_ms": 0.0}

        start_time = time.perf_counter()
        if not self._is_loaded:
            if not self.load_model():
                # Fallback / Mock translation
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return {
                    "translated_text": f"[JA: {text}]",
                    "latency_ms": elapsed_ms,
                    "is_mock": True,
                }

        try:
            translated = self.translation.translate(text)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "translated_text": translated,
                "latency_ms": elapsed_ms,
                "is_mock": False,
            }
        except Exception as e:
            print(f"[MT] Translation error: {e}")
            return {
                "translated_text": text,
                "latency_ms": (time.perf_counter() - start_time) * 1000.0,
                "error": str(e),
            }
