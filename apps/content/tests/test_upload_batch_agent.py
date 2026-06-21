import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import requests
from django.test import SimpleTestCase

from scripts import process_upload_batch as agent
from scripts.process_upload_batch import (
    load_batch,
    load_local_state,
    publish_and_confirm,
    save_local_state,
)


class UploadBatchAgentTests(SimpleTestCase):
    def test_load_batch_accepts_contract_and_rejects_unsafe_names(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "batch.json"
            path.write_text(
                json.dumps({
                    "schema": "profeonline.upload-batch/v1",
                    "batch_id": "abc",
                    "files": ["clase.mp4"],
                }),
                encoding="utf-8",
            )
            self.assertEqual(load_batch(path)["files"], ["clase.mp4"])
            path.write_text(
                json.dumps({
                    "schema": "profeonline.upload-batch/v1",
                    "batch_id": "abc",
                    "files": ["../clase.mp4"],
                }),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_batch(path)

    def test_local_state_roundtrip_preserves_video_id_for_resume(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            state = {
                "batch_id": "abc",
                "files": {"clase.mp4": {"video_id": "abcdefghijk"}},
            }
            save_local_state(path, state)
            self.assertEqual(
                load_local_state(path)["files"]["clase.mp4"]["video_id"],
                "abcdefghijk",
            )


class PublishAndConfirmTests(SimpleTestCase):
    def test_returns_true_and_does_not_revert_on_success(self):
        with mock.patch.object(agent, "publish_video") as publish, \
                mock.patch.object(agent, "confirm_publication") as confirm, \
                mock.patch.object(agent, "set_video_unlisted") as revert:
            ok = publish_and_confirm(
                mock.Mock(), "http://x", "tok", 1, "vid123",
                {"youtube_title": "t", "youtube_description": "d"},
            )
        self.assertTrue(ok)
        publish.assert_called_once()
        confirm.assert_called_once()
        revert.assert_not_called()

    def test_reverts_to_unlisted_when_confirmation_fails(self):
        with mock.patch.object(agent, "publish_video"), \
                mock.patch.object(
                    agent, "confirm_publication",
                    side_effect=requests.HTTPError("boom"),
                ), \
                mock.patch.object(agent, "set_video_unlisted") as revert:
            ok = publish_and_confirm(
                mock.Mock(), "http://x", "tok", 1, "vid123", {},
            )
        self.assertFalse(ok)
        revert.assert_called_once()
