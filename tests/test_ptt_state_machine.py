"""
Unit and Regression Test Suite for PTT State Machine and Reliability
Tests:
1. Normal Spacebar press and release
2. Auto-repeat Spacebar debounce (re-entrance prevention)
3. Top-level window focus-loss cancellation (<FocusOut>)
4. Escape key cancellation (<KeyPress-Escape>)
5. Subsequent fresh PTT use after cancellation and delayed key release
6. Focus protection for child widgets (comboboxes, text log, other buttons)
7. Mouse hold-to-speak operation
8. Cancellation guarantees (audio buffer cleared, zero STT/MT/TTS/injection)
"""

import tkinter as tk
import numpy as np
import pytest

from src.gui.app import KoeBridgeApp
from src.pipeline.outbound import OutboundPipeline


@pytest.fixture(autouse=True)
def disable_engine_prewarm(monkeypatch):
    """Disable async engine pre-warming in GUI state-machine tests to prevent thread collisions."""
    monkeypatch.setattr(KoeBridgeApp, "_start_engine_prewarm", lambda self: None)


@pytest.fixture(scope="module")
def root():
    r = tk.Tk()
    r.deiconify()
    r.focus_force()
    r.update()
    yield r
    try:
        r.destroy()
    except Exception:
        pass


@pytest.fixture
def app(root):
    # Clear children from previous test
    for child in list(root.children.values()):
        try:
            child.destroy()
        except Exception:
            pass

    app_instance = KoeBridgeApp(root)
    root.focus_force()
    root.update()
    yield app_instance
    try:
        app_instance.destroy()
    except Exception:
        pass
    for child in list(root.children.values()):
        try:
            child.destroy()
        except Exception:
            pass


def test_1_normal_spacebar_press_and_release(root, app):
    # Press Spacebar
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()

    assert app._is_ptt_active is True, "PTT state must be active after Space press"
    assert "RECORDING" in app.ptt_btn.cget("text"), (
        "PTT button text must show RECORDING"
    )
    assert app.outbound_pipeline is not None, "OutboundPipeline must be initialized"
    assert app.outbound_pipeline._is_recording is True, (
        "Pipeline must be in recording state"
    )

    # Release Spacebar
    root.event_generate("<KeyRelease-space>")
    root.update()
    app._process_gui_queue()

    assert app._is_ptt_active is False, "PTT state must be inactive after Space release"
    assert "HOLD TO SPEAK" in app.ptt_btn.cget("text"), (
        "PTT button text must be restored"
    )
    assert app.outbound_pipeline._is_recording is False, (
        "Pipeline recording must be stopped"
    )


def test_2_auto_repeat_spacebar_debounce(root, app):
    # Initial press
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True

    # Simulate 5 typematic auto-repeat keypresses without release
    for _ in range(5):
        root.event_generate("<space>")
        root.update()
        app._process_gui_queue()
        assert app._is_ptt_active is True

    # Release
    root.event_generate("<KeyRelease-space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False


def test_3_focus_loss_cancellation(root, app):
    # Press Space
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True
    assert app.outbound_pipeline._is_recording is True

    # Simulate top-level OS window losing focus
    root.event_generate("<FocusOut>")
    root.update()
    app._process_gui_queue()

    assert app._is_ptt_active is False, "FocusOut must cancel PTT active flag"
    assert "HOLD TO SPEAK" in app.ptt_btn.cget("text"), "Button must reset to normal"
    assert app.outbound_pipeline._is_recording is False, "Recording must be stopped"
    assert len(app.outbound_pipeline._record_buffer) == 0, "Buffer must be emptied"
    assert "Window lost focus" in app.outbound_status_lbl.cget("text")


def test_4_escape_key_cancellation(root, app):
    # Press Space
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True
    assert app.outbound_pipeline._is_recording is True

    # Press Escape
    root.event_generate("<KeyPress-Escape>")
    root.update()
    app._process_gui_queue()

    assert app._is_ptt_active is False, "Escape must cancel PTT active flag"
    assert "HOLD TO SPEAK" in app.ptt_btn.cget("text"), "Button must reset to normal"
    assert app.outbound_pipeline._is_recording is False, "Recording must be stopped"
    assert len(app.outbound_pipeline._record_buffer) == 0, "Buffer must be emptied"
    assert "Escape" in app.outbound_status_lbl.cget("text")


def test_5_subsequent_ptt_use_after_cancellation_and_delayed_release(root, app):
    # 1. Start and cancel
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True

    root.event_generate("<FocusOut>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False

    # 2. Delayed key release arrives after cancellation (must be safely ignored)
    root.event_generate("<KeyRelease-space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False
    assert app.outbound_pipeline._is_recording is False

    # 3. New fresh Space press must work cleanly
    root.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True, (
        "Subsequent press after cancellation must succeed"
    )
    assert app.outbound_pipeline._is_recording is True

    root.event_generate("<KeyRelease-space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False


def test_6_child_widget_focus_protection(root, app):
    # Dropdown comboboxes must not trigger PTT on spacebar
    for combo in (app.loopback_combo, app.mic_combo, app.cable_combo):
        combo.focus_set()
        root.update()
        combo.event_generate("<space>")
        root.update()
        app._process_gui_queue()
        assert app._is_ptt_active is False, (
            f"Combobox {combo} must not activate PTT on Space"
        )

    # Text log must not trigger PTT on spacebar
    app.log_text.focus_set()
    root.update()
    app.log_text.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False, "Log text must not activate PTT on Space"

    # Other buttons (e.g. Inbound / Overlay) must not trigger PTT on spacebar
    for btn in (app.inbound_btn, app.overlay_btn):
        btn.focus_set()
        root.update()
        btn.event_generate("<space>")
        root.update()
        app._process_gui_queue()
        assert app._is_ptt_active is False, (
            f"Button {btn} must not activate PTT on Space"
        )

    # Focusing PTT button itself allows spacebar
    app.ptt_btn.focus_set()
    root.update()
    app.ptt_btn.event_generate("<space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True, "PTT button must activate on Space when focused"
    app.ptt_btn.event_generate("<KeyRelease-space>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False


def test_7_mouse_hold_to_speak(root, app):
    # Mouse Button-1 Press
    app.ptt_btn.event_generate("<ButtonPress-1>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is True, "Mouse Button-1 press must activate PTT"
    assert app.outbound_pipeline._is_recording is True

    # Mouse Button-1 Release
    app.ptt_btn.event_generate("<ButtonRelease-1>")
    root.update()
    app._process_gui_queue()
    assert app._is_ptt_active is False, "Mouse Button-1 release must deactivate PTT"
    assert app.outbound_pipeline._is_recording is False


def test_8_cancellation_guarantees_zero_processing_and_empty_buffer():
    # Test OutboundPipeline directly to verify no processing/injection on cancel
    outbound = OutboundPipeline()

    # Monkeypatch processing methods to detect any unwanted execution
    processed_called = []
    outbound._process_recorded_speech = lambda: processed_called.append("processed")
    outbound.output_renderer.play_audio = (
        lambda *args, **kwargs: processed_called.append("injected")
    )

    # Start recording and simulate incoming audio data
    outbound.ptt_press()
    assert outbound._is_recording is True

    fake_chunk = np.ones(16000, dtype=np.float32) * 0.1
    with outbound._lock:
        outbound._record_buffer.append(fake_chunk)

    assert len(outbound._record_buffer) == 1

    # Cancel recording
    outbound.ptt_cancel()

    assert outbound._is_recording is False, "is_recording must be False after cancel"
    assert len(outbound._record_buffer) == 0, "Buffer must be empty after cancel"
    assert len(processed_called) == 0, "No processing or injection should have occurred"

    # Now call ptt_release after cancel (simulating delayed release)
    outbound.ptt_release()

    assert len(processed_called) == 0, (
        "Delayed release after cancel must not trigger processing"
    )
    assert len(outbound._record_buffer) == 0
