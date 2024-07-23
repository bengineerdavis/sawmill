import pytest
from typer.testing import CliRunner
from sawmill.cli import app

runner = CliRunner()


def test_read_command_with_valid_file():
    result = runner.invoke(app, ["read", "--file-path", "/path/to/valid/file.txt"])
    assert result.exit_code == 0
    assert "File read successfully!" in result.stdout


def test_read_command_with_invalid_file():
    result = runner.invoke(app, ["read", "--file-path", "/path/to/invalid/file.txt"])
    assert result.exit_code != 0
    assert "Invalid file path" in result.stdout


def test_read_command_with_missing_file():
    result = runner.invoke(app, ["read"])
    assert result.exit_code != 0
    assert "Missing file path" in result.stdout


if __name__ == "__main__":
    pytest.main()
