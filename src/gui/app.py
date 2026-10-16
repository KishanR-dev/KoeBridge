"""
KoeBridge for Zoom — Main GUI Application (Tkinter / ttk)
"""

import tkinter as tk
from tkinter import ttk
import time
import queue
from typing import Optional, List
import ctypes
from ctypes import wintypes

from ..config import AppConfig
from ..audio.devices import get_audio_devices, AudioDeviceInfo
from ..pipeline.inbound import InboundPipeline
from ..pipeline.outbound import OutboundPipeline


class CaptionOverlay(tk.Toplevel):
    """
    Floating, translucent, always-on-top caption overlay window for Zoom meetings.
    Supports dynamic screen positioning, click-through pass-through, and dual-line JA+EN display.
    """

    def __init__(self, parent, font_size: int = 18):
        super().__init__(parent)
        self.title("KoeBridge — Live Zoom Captions [🔓 Draggable Mode]")

        # Dynamically center overlay on visible screen area, comfortably above Windows taskbar
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        w = min(840, max(640, screen_w - 200))
        h = 150
        x = max(0, (screen_w - w) // 2)
        y = max(40, screen_h - h - 110)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Size constraints to strictly prevent screen-covering full maximization
        self.minsize(450, 90)
        self.maxsize(min(1400, screen_w), 240)

        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.90)
        self.configure(bg="#121212")

        self._click_through = False

        self.label_var = tk.StringVar(
            value="Waiting for Japanese speech in Zoom meeting..."
        )
        self.ja_var = tk.StringVar(value="")
        self.en_var = tk.StringVar(
            value="Waiting for Japanese speech in Zoom meeting..."
        )

        # Content frame holding dual-line captions
        self.content_frame = tk.Frame(self, bg="#121212")
        self.content_frame.pack(expand=True, fill="both", padx=12, pady=6)

        # Japanese transcription line (gold/amber)
        self.ja_label = tk.Label(
            self.content_frame,
            textvariable=self.ja_var,
            font=("Segoe UI", 12),
            fg="#ffd166",
            bg="#121212",
            wraplength=800,
            justify="center",
        )
        self.ja_label.pack(side="top", fill="x", pady=(2, 2))

        # English translation line (cyan)
        self.en_label = tk.Label(
            self.content_frame,
            textvariable=self.en_var,
            font=("Segoe UI", font_size, "bold"),
            fg="#00ffcc",
            bg="#121212",
            wraplength=800,
            justify="center",
        )
        self.en_label.pack(side="top", expand=True, fill="both", pady=(2, 2))

        # Set Win32 extended style WS_EX_NOACTIVATE so overlay never steals focus from Zoom
        self._apply_win32_styles()

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

    def _apply_win32_styles(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id()) or self.winfo_id()
            GWL_EXSTYLE = -20
            WS_EX_TRANSPARENT = 0x00000020
            WS_EX_LAYERED = 0x00080000
            WS_EX_NOACTIVATE = 0x08000000

            cur = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            base = cur | WS_EX_LAYERED | WS_EX_NOACTIVATE
            if self._click_through:
                new_style = base | WS_EX_TRANSPARENT
            else:
                new_style = base & ~WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
        except Exception:
            pass

    def _update_title(self):
        mode = (
            "🔒 Click-Through to Zoom" if self._click_through else "🔓 Draggable Mode"
        )
        self.title(f"KoeBridge — Live Zoom Captions [{mode}]")

    def set_click_through(self, enabled: bool):
        self._click_through = enabled
        self._apply_win32_styles()
        self._update_title()

    def toggle_click_through(self) -> bool:
        self.set_click_through(not self._click_through)
        return self._click_through

    def update_caption(self, text: str, ja_text: str = ""):
        self.en_var.set(text)
        if ja_text:
            self.ja_var.set(f"[JA] {ja_text}")
        else:
            self.ja_var.set("")
        self.label_var.set(text)
        if not self.winfo_viewable():
            self.deiconify()


class KoeBridgeApp:
    """
    Primary desktop application window for KoeBridge for Zoom.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("KoeBridge for Zoom — Japanese ↔ English Meeting Translator")
        self.root.geometry("680x560")
        self.root.minsize(620, 500)

        # Apply clean dark-mode theme
        self._setup_styles()

        self.config = AppConfig.load()
        self.devices: List[AudioDeviceInfo] = get_audio_devices()

        self.inbound_pipeline: Optional[InboundPipeline] = None
        self.outbound_pipeline: Optional[OutboundPipeline] = None
        self._is_ptt_active = False
        self._gui_queue: queue.Queue = queue.Queue()
        self._after_id = None

        self.overlay = CaptionOverlay(
            self.root, font_size=self.config.gui.overlay_font_size
        )

        self._build_ui()
        self._refresh_power_status()
        self._process_gui_queue()
        self._start_engine_prewarm()

    def post_gui_event(self, callback):
        """Thread-safe dispatch of callback to main GUI thread."""
        self._gui_queue.put(callback)

    def _process_gui_queue(self):
        """Poll and execute pending callbacks on the main GUI thread."""
        try:
            if not self.root.winfo_exists():
                return
        except Exception:
            return

        while not self._gui_queue.empty():
            try:
                fn = self._gui_queue.get_nowait()
                fn()
            except Exception as e:
                print(f"[GUI Event Error] {e}")

        # Cancel previous scheduled poll to prevent piling up
        if self._after_id:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

        try:
            if self.root.winfo_exists():
                self._after_id = self.root.after(50, self._process_gui_queue)
        except Exception:
            pass

    def destroy(self):
        if self._after_id:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        if self.inbound_pipeline:
            try:
                self.inbound_pipeline.stop()
            except Exception:
                pass
        if self.outbound_pipeline:
            try:
                self.outbound_pipeline.stop()
            except Exception:
                pass
        if hasattr(self, "overlay") and self.overlay:
            try:
                self.overlay.destroy()
            except Exception:
                pass

    def _start_engine_prewarm(self):
        import threading

        self.outbound_status_lbl.config(
            text="Initializing AI Engines (Whisper, Argos, MeloTTS)...",
            fg="#e0a800",
        )
        self.log_message("Starting asynchronous AI engine pre-warming...")
        self._prewarm_thread = threading.Thread(
            target=self._prewarm_worker, daemon=True
        )
        self._prewarm_thread.start()

    def _prewarm_worker(self):
        try:
            from concurrent.futures import ThreadPoolExecutor
            from ..stt.engine import SttEngine
            from ..mt.engine import MachineTranslationEngine
            from ..tts.engine import LocalJapaneseTtsEngine

            def _warm_stt():
                stt = SttEngine(model_size="tiny")
                return stt.load_model()

            def _warm_mt():
                mt = MachineTranslationEngine(from_code="en", to_code="ja")
                mt_ok = mt.load_model()
                if mt_ok:
                    mt.translate("Warmup")
                return mt_ok

            def _warm_tts():
                tts = LocalJapaneseTtsEngine()
                return tts._backend == "melotts_onnx" and not getattr(
                    tts, "_is_mock", False
                )

            # Prewarm engines concurrently to reduce startup latency from ~28s to ~13s
            with ThreadPoolExecutor(max_workers=3) as executor:
                f_stt = executor.submit(_warm_stt)
                f_mt = executor.submit(_warm_mt)
                f_tts = executor.submit(_warm_tts)

                stt_ok = f_stt.result()
                mt_ok = f_mt.result()
                tts_ok = f_tts.result()

            print(f"[Prewarm Status] stt_ok={stt_ok}, mt_ok={mt_ok}, tts_ok={tts_ok}")

            def _update_ui():
                try:
                    if not self.root.winfo_exists():
                        return
                except Exception:
                    return

                cur_text = ""
                try:
                    cur_text = self.outbound_status_lbl.cget("text")
                except Exception:
                    pass

                if stt_ok and mt_ok and tts_ok:
                    if "Initializing" in cur_text or not cur_text:
                        self.outbound_status_lbl.config(
                            text="AI Engines Ready (All Local Models Active)",
                            fg="#00ffcc",
                        )
                    self.log_message(
                        "All AI backends initialized successfully: faster-whisper (tiny int8), Argos EN->JA, MeloTTS-Japanese ONNX (44.1kHz)."
                    )
                else:
                    err_parts = []
                    if not stt_ok:
                        err_parts.append("STT (mock)")
                    if not mt_ok:
                        err_parts.append("MT (mock)")
                    if not tts_ok:
                        err_parts.append("TTS (mock)")
                    err_msg = f"⚠ Degraded: {', '.join(err_parts)}"
                    if "Initializing" in cur_text or not cur_text:
                        self.outbound_status_lbl.config(text=err_msg, fg="#ff4444")
                    self.log_message(
                        f"AI Engine Warning: {err_msg}. Real inference may fail."
                    )

            self.post_gui_event(_update_ui)
        except Exception as e:
            print(f"[Prewarm Error] {e}")
            err_str = str(e)
            self.post_gui_event(
                lambda: self.outbound_status_lbl.config(
                    text=f"⚠ Init Error: {err_str[:30]}", fg="#ff4444"
                )
            )

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        self.root.configure(bg="#1e1e1e")

        style.configure(
            ".", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10)
        )
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabelframe", background="#1e1e1e", foreground="#00d2ff")
        style.configure(
            "TLabelframe.Label",
            background="#1e1e1e",
            foreground="#00d2ff",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("TButton", background=[("active", "#2a2a2a")])

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding="16")
        main_frame.pack(fill="both", expand=True)

        # Header Title & Status
        hdr_frame = ttk.Frame(main_frame)
        hdr_frame.pack(fill="x", pady=(0, 12))

        title_lbl = tk.Label(
            hdr_frame,
            text="KoeBridge for Zoom",
            font=("Segoe UI", 16, "bold"),
            fg="#00d2ff",
            bg="#1e1e1e",
        )
        title_lbl.pack(side="left")

        self.power_lbl = tk.Label(
            hdr_frame,
            text="Checking AC Power...",
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#1e1e1e",
        )
        self.power_lbl.pack(side="right", padx=6)

        # 1. Device Configuration Frame
        dev_frame = ttk.LabelFrame(
            main_frame, text=" 1. Audio Routing Configuration ", padding="12"
        )
        dev_frame.pack(fill="x", pady=(0, 12))

        # Loopback Device
        ttk.Label(dev_frame, text="Zoom Audio Source (Loopback):").grid(
            row=0, column=0, sticky="w", pady=4
        )
        self.loopback_combo = ttk.Combobox(dev_frame, width=45, state="readonly")
        self.loopback_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        # Microphone Device
        ttk.Label(dev_frame, text="Your Microphone (Outbound):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.mic_combo = ttk.Combobox(dev_frame, width=45, state="readonly")
        self.mic_combo.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        # VB-CABLE Input Device
        ttk.Label(dev_frame, text="Zoom Injection Endpoint:").grid(
            row=2, column=0, sticky="w", pady=4
        )
        self.cable_combo = ttk.Combobox(dev_frame, width=45, state="readonly")
        self.cable_combo.grid(row=2, column=1, sticky="ew", padx=8, pady=4)

        self._populate_device_combos()

        # 2. Inbound Caption Pipeline Controls
        inbound_frame = ttk.LabelFrame(
            main_frame,
            text=" 2. Inbound Translation (Zoom JA -> English Captions) ",
            padding="12",
        )
        inbound_frame.pack(fill="x", pady=(0, 12))

        in_ctrl_frame = ttk.Frame(inbound_frame)
        in_ctrl_frame.pack(fill="x")

        self.inbound_btn = tk.Button(
            in_ctrl_frame,
            text="▶ Start Inbound Captions",
            bg="#007acc",
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            command=self.toggle_inbound_pipeline,
            padx=12,
            pady=4,
        )
        self.inbound_btn.pack(side="left")

        self.overlay_btn = tk.Button(
            in_ctrl_frame,
            text="Show/Hide Overlay Window",
            bg="#333333",
            fg="#ffffff",
            command=self.toggle_overlay,
            padx=8,
            pady=4,
        )
        self.overlay_btn.pack(side="left", padx=6)

        self.click_through_btn = tk.Button(
            in_ctrl_frame,
            text="Click-Through: OFF (Draggable)",
            bg="#333333",
            fg="#ffffff",
            command=self.toggle_click_through,
            padx=8,
            pady=4,
        )
        self.click_through_btn.pack(side="left", padx=6)

        self.inbound_status_lbl = tk.Label(
            in_ctrl_frame, text="Status: Stopped", fg="#888888", bg="#1e1e1e"
        )
        self.inbound_status_lbl.pack(side="right")

        # 3. Outbound Speech Pipeline Controls (PTT)
        outbound_frame = ttk.LabelFrame(
            main_frame,
            text=" 3. Outbound Translation (English Speech -> Zoom Japanese Voice) ",
            padding="12",
        )
        outbound_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            outbound_frame,
            text="Hold the button below (or Spacebar) to speak English; release to inject Japanese into Zoom:",
        ).pack(anchor="w", pady=(0, 8))

        self.ptt_btn = tk.Button(
            outbound_frame,
            text="🎙 HOLD TO SPEAK ENGLISH (PTT)",
            bg="#28a745",
            fg="#ffffff",
            font=("Segoe UI", 12, "bold"),
            relief="raised",
            height=2,
        )
        self.ptt_btn.pack(fill="x", pady=4)

        # Bind mouse press/release to PTT
        self.ptt_btn.bind("<ButtonPress-1>", self._on_ptt_press)
        self.ptt_btn.bind("<ButtonRelease-1>", self._on_ptt_release)
        self.root.bind("<KeyPress-space>", self._on_ptt_press)
        self.root.bind("<KeyRelease-space>", self._on_ptt_release)
        self.root.bind("<FocusOut>", self._on_focus_out)
        self.root.bind(
            "<KeyPress-Escape>",
            lambda e: self._on_ptt_cancel(reason="PTT Cancelled (Escape)"),
        )

        self.outbound_status_lbl = tk.Label(
            outbound_frame,
            text="PTT Ready",
            font=("Segoe UI", 10),
            fg="#00ffcc",
            bg="#1e1e1e",
        )
        self.outbound_status_lbl.pack(anchor="w", pady=4)

        # 4. Live Activity Log
        log_frame = ttk.LabelFrame(
            main_frame, text=" Live Meeting Activity Log ", padding="8"
        )
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            height=6,
            bg="#141414",
            fg="#dddddd",
            font=("Consolas", 9),
            wrap="word",
        )
        self.log_text.pack(fill="both", expand=True)

    def _populate_device_combos(self):
        dev_names = [f"[{d.index}] {d.name}" for d in self.devices]
        if not dev_names:
            dev_names = ["No audio devices detected"]

        self.loopback_combo["values"] = dev_names
        self.mic_combo["values"] = dev_names
        self.cable_combo["values"] = dev_names

        # Auto-select appropriate defaults
        for i, d in enumerate(self.devices):
            if d.is_loopback:
                self.loopback_combo.current(i)
                break
        if not self.loopback_combo.get() and dev_names:
            self.loopback_combo.current(0)

        for i, d in enumerate(self.devices):
            if d.max_input_channels > 0 and not d.is_cable and not d.is_loopback:
                self.mic_combo.current(i)
                break
        if not self.mic_combo.get() and dev_names:
            self.mic_combo.current(0)

        for i, d in enumerate(self.devices):
            if d.is_cable and d.max_output_channels > 0:
                self.cable_combo.current(i)
                break
        if not self.cable_combo.get() and dev_names:
            self.cable_combo.current(0)

    def _refresh_power_status(self):
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
                if sps.ACLineStatus == 1:
                    self.power_lbl.config(
                        text=f"⚡ AC Power Connected ({sps.BatteryLifePercent}%)",
                        fg="#00ff66",
                    )
                else:
                    self.power_lbl.config(
                        text=f"⚠ Running on Battery ({sps.BatteryLifePercent}%) — Plug in charger!",
                        fg="#ff4444",
                    )
        except Exception:
            pass

    def log_message(self, msg: str):
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")

    def toggle_inbound_pipeline(self):
        if self.inbound_pipeline and self.inbound_pipeline._running:
            self.inbound_pipeline.stop()
            self.inbound_btn.config(text="▶ Start Inbound Captions", bg="#007acc")
            self.inbound_status_lbl.config(text="Status: Stopped", fg="#888888")
            self.log_message("Inbound caption pipeline stopped.")
        else:
            selected_idx = None
            combo_val = self.loopback_combo.get()
            if combo_val and combo_val.startswith("["):
                try:
                    selected_idx = int(combo_val.split("]")[0].replace("[", "").strip())
                except Exception:
                    pass

            self.inbound_pipeline = InboundPipeline(
                loopback_device_id=selected_idx, on_caption=self._on_inbound_caption
            )
            self.inbound_pipeline.start()
            self.inbound_btn.config(text="⏹ Stop Inbound Captions", bg="#dc3545")
            self.inbound_status_lbl.config(
                text="Status: Listening to Zoom...", fg="#00ff66"
            )
            self.log_message("Inbound caption pipeline started.")

    def _on_inbound_caption(self, text: str, timestamp: float, ja_text: str = ""):
        self.post_gui_event(lambda: self._handle_caption_ui(text, ja_text=ja_text))

    def _handle_caption_ui(self, text: str, ja_text: str = ""):
        self.overlay.update_caption(text, ja_text=ja_text)
        if ja_text:
            self.log_message(f"Zoom Caption: [JA] '{ja_text}' -> [EN] '{text}'")
        else:
            self.log_message(f"Zoom Caption: {text}")

    def toggle_overlay(self):
        if self.overlay.winfo_viewable():
            self.overlay.withdraw()
        else:
            self.overlay.deiconify()

    def toggle_click_through(self):
        is_on = self.overlay.toggle_click_through()
        if is_on:
            self.click_through_btn.config(
                text="Click-Through: ON (Pass Clicks to Zoom)",
                bg="#005f73",
                fg="#00ffcc",
            )
            self.log_message(
                "Caption Overlay: Click-through ENABLED (Mouse clicks pass directly through to Zoom)."
            )
        else:
            self.click_through_btn.config(
                text="Click-Through: OFF (Draggable)",
                bg="#333333",
                fg="#ffffff",
            )
            self.log_message(
                "Caption Overlay: Click-through DISABLED (Overlay can be moved/dragged)."
            )

    def _should_ignore_ptt_key(self, event) -> bool:
        """
        Check if a key event originates from an interactive child widget
        that should own keyboard focus (e.g. comboboxes, text log, or other buttons).
        """
        if event is None or getattr(event, "widget", None) is None:
            return False
        widget = event.widget
        if isinstance(widget, (ttk.Combobox, tk.Text, tk.Entry)):
            return True
        if isinstance(widget, tk.Button) and widget != self.ptt_btn:
            return True
        w_class = getattr(widget, "winfo_class", lambda: "")()
        if w_class in ("TCombobox", "Combobox", "Text", "Entry"):
            return True
        return False

    def _on_ptt_press(self, event=None):
        if self._should_ignore_ptt_key(event):
            return
        if self._is_ptt_active:
            return  # Prevent repeated trigger from key auto-repeat
        self._is_ptt_active = True

        if not self.outbound_pipeline:
            mic_idx = None
            mic_val = self.mic_combo.get()
            if mic_val and mic_val.startswith("["):
                try:
                    mic_idx = int(mic_val.split("]")[0].replace("[", "").strip())
                except Exception:
                    pass

            cable_idx = None
            cable_val = self.cable_combo.get()
            if cable_val and cable_val.startswith("["):
                try:
                    cable_idx = int(cable_val.split("]")[0].replace("[", "").strip())
                except Exception:
                    pass

            self.outbound_pipeline = OutboundPipeline(
                microphone_device_id=mic_idx,
                cable_input_device_id=cable_idx,
                on_status=self._on_outbound_status,
            )
            self.outbound_pipeline.start()

        self.ptt_btn.config(
            bg="#d9534f", text="🔴 RECORDING (Release to inject Japanese)..."
        )
        self.outbound_pipeline.ptt_press()

    def _on_ptt_release(self, event=None):
        if not self._is_ptt_active:
            return
        self._is_ptt_active = False

        self.ptt_btn.config(bg="#28a745", text="🎙 HOLD TO SPEAK ENGLISH (PTT)")
        if self.outbound_pipeline:
            self.outbound_pipeline.ptt_release()

    def _on_focus_out(self, event=None):
        """Handle window focus loss during active PTT recording."""
        if not self._is_ptt_active:
            return
        # Only cancel if the top-level application window itself loses focus
        if event is None or getattr(event, "widget", None) == self.root:
            self._on_ptt_cancel(reason="PTT Cancelled (Window lost focus)")

    def _on_ptt_cancel(self, reason: str = "PTT Cancelled"):
        """Abort active PTT recording without processing or audio injection."""
        if not self._is_ptt_active:
            return
        self._is_ptt_active = False

        self.ptt_btn.config(bg="#28a745", text="🎙 HOLD TO SPEAK ENGLISH (PTT)")
        if self.outbound_pipeline:
            self.outbound_pipeline.ptt_cancel(message=reason)
        else:
            self.outbound_status_lbl.config(text=f"⚠ {reason}", fg="#e0a800")
            self.log_message(reason)

    def _on_outbound_status(self, status: str, details: dict):
        self.post_gui_event(lambda: self._handle_outbound_status_ui(status, details))

    def _handle_outbound_status_ui(self, status: str, details: dict):
        msg = details.get("message", status)
        if status == "FAILED":
            self.outbound_status_lbl.config(text=f"❌ {msg}", fg="#ff4444")
            self.log_message(f"Outbound Failure: {msg}")
        elif status == "INJECTED":
            self.outbound_status_lbl.config(text=msg, fg="#00ffcc")
            self.log_message(
                f"Outbound: EN '{details.get('en_text')}' -> JA '{details.get('ja_text')}' ({details.get('total_time_ms', 0):.0f} ms)"
            )
        elif "Cancelled" in msg:
            self.outbound_status_lbl.config(text=f"⚠ {msg}", fg="#e0a800")
            self.log_message(msg)
        else:
            self.outbound_status_lbl.config(text=msg, fg="#00ffcc")


def run_gui():
    root = tk.Tk()
    _app = KoeBridgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
