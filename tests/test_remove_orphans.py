"""Tests for remove_orphans tool."""

import pytest

from docker_kit.tools.remove_orphans import is_orphan_container
from docker_kit.tools.remove_orphans import parse_hex_lengths


class TestParseHexLengths:
    def test_single_length(self) -> None:
        assert parse_hex_lengths("12") == {12}

    def test_multiple_lengths(self) -> None:
        assert parse_hex_lengths("12,64") == {12, 64}

    def test_with_spaces(self) -> None:
        assert parse_hex_lengths("12, 64, 8") == {8, 12, 64}

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="no lengths provided"):
            parse_hex_lengths("")

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="length must be > 0"):
            parse_hex_lengths("0")

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="length must be > 0"):
            parse_hex_lengths("-1")


class TestIsOrphanContainer:
    def test_valid_hex_suffix(self) -> None:
        assert is_orphan_container("myapp-abc123def456", {12}) is True

    def test_wrong_length(self) -> None:
        assert is_orphan_container("myapp-abc123", {12}) is False
        assert is_orphan_container("myapp-abc123", {6}) is True

    def test_no_hyphen(self) -> None:
        assert is_orphan_container("myappcontainer", {12}) is False

    def test_non_hex_suffix(self) -> None:
        assert is_orphan_container("myapp-notahexval1", {12}) is False

    def test_uppercase_hex_rejected(self) -> None:
        # Only lowercase hex is valid
        assert is_orphan_container("myapp-ABC123DEF456", {12}) is False

    def test_multiple_hyphens(self) -> None:
        # Should use last segment
        assert is_orphan_container("my-app-abc123def456", {12}) is True

    def test_multiple_allowed_lengths(self) -> None:
        assert is_orphan_container("myapp-abc123", {6, 12}) is True
        assert is_orphan_container("myapp-abc123def456", {6, 12}) is True
