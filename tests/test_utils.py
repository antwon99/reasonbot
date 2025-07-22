import os
from unittest.mock import patch

import utils


def test_get_env_var_returns_value():
    with patch.dict(os.environ, {"X": "1"}, clear=True):
        assert utils.get_env_var("X") == "1"
        assert utils.get_env_var("MISSING", "d") == "d"


def test_is_rate_limited(tmp_path):
    lock = tmp_path / "lock"
    with patch("utils.time.time", side_effect=[0, 1, 6]):
        assert utils.is_rate_limited(lock, 5) is False
        assert utils.is_rate_limited(lock, 5) is True
        assert utils.is_rate_limited(lock, 5) is False


def test_processed_id_helpers(tmp_path):
    file = tmp_path / "ids.txt"
    utils.save_processed_id(file, "1")
    utils.save_processed_id(file, "2")
    ids = utils.load_processed_ids(file)
    assert ids == {"1", "2"}
