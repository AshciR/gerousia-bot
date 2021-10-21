from unittest.mock import patch

from gerousiabot import utils


@patch("gerousiabot.utils.logging")
def test_setup_logger(mocked_logging):
    utils.setup_logger()

    mocked_logging.getLogger.assert_called()
    mocked_logging.StreamHandler.assert_called()
    mocked_logging.FileHandler.assert_called()

    mocked_logging.StreamHandler().setLevel.assert_called()
    mocked_logging.FileHandler().setLevel.assert_called()

    assert mocked_logging.Formatter.call_count == 2

    mocked_logging.StreamHandler().setFormatter.assert_called()
    mocked_logging.FileHandler().setFormatter.assert_called()

    assert mocked_logging.getLogger().addHandler.call_count == 2
