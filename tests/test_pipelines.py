"""
Unit tests for Inbound and Outbound Pipelines
"""

import time
from src.pipeline.inbound import InboundPipeline
from src.pipeline.outbound import OutboundPipeline


def test_inbound_pipeline_lifecycle():
    captions_received = []

    def on_caption(text, ts):
        captions_received.append((text, ts))

    pipeline = InboundPipeline(loopback_device_id=None, on_caption=on_caption)

    started = pipeline.start()
    assert started is True
    time.sleep(0.1)
    pipeline.stop()
    assert pipeline._running is False


def test_outbound_pipeline_lifecycle():
    statuses = []

    def on_status(status, details):
        statuses.append((status, details))

    pipeline = OutboundPipeline(
        microphone_device_id=None, cable_input_device_id=None, on_status=on_status
    )

    pipeline.start()
    pipeline.ptt_press()
    time.sleep(0.1)
    pipeline.ptt_release()
    time.sleep(0.2)
    pipeline.stop()

    assert len(statuses) > 0
    assert any(s[0] == "RECORDING" for s in statuses)
