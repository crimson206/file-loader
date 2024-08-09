import pytest
from crimson.file_loader.converter import (
    convert_byte_to_str,
    convert_textual_byte_to_str,
)


@pytest.fixture
def byte_sources():
    return [
        {"path": "file1.txt", "content": b"Hello World"},
        {"path": "file2.txt", "content": b"Python Testing"},
    ]


@pytest.fixture
def mixed_sources():
    return [
        {"path": "file1.txt", "content": b"Hello World"},
        {"path": "file2.txt", "content": b"Python Testing"},
        {"path": "binary.bin", "content": b"\x80\x81\x82"}  # Non-UTF-8 content
    ]


def test_convert_byte_to_str(byte_sources):
    # Call the convert_byte_to_str function
    converted_sources = convert_byte_to_str(byte_sources)

    # Expected output after conversion
    expected_sources = [
        {"path": "file1.txt", "content": "Hello World"},
        {"path": "file2.txt", "content": "Python Testing"},
    ]

    # Assert that the conversion was correct
    assert converted_sources == expected_sources


def test_empty_content():
    # Test with empty content
    byte_sources = [{"path": "empty.txt", "content": b""}]
    converted_sources = convert_byte_to_str(byte_sources)

    expected_sources = [{"path": "empty.txt", "content": ""}]
    assert converted_sources == expected_sources


def test_non_utf8_content():
    # Test with non-UTF-8 content, should raise UnicodeDecodeError
    byte_sources = [{"path": "binary.bin", "content": b"\x80\x81\x82"}]

    with pytest.raises(UnicodeDecodeError):
        convert_byte_to_str(byte_sources)


def test_convert_textual_byte_to_str(mixed_sources):
    # Call the convert_textual_byte_to_str function
    result = convert_textual_byte_to_str(mixed_sources)

    # Expected output
    expected_byte_sources = [
        {"path": "binary.bin", "content": b"\x80\x81\x82"}
    ]
    expected_str_sources = [
        {"path": "file1.txt", "content": "Hello World"},
        {"path": "file2.txt", "content": "Python Testing"},
    ]

    # Assert that the byte_sources and str_sources are correctly separated and converted
    assert result["byte_sources"] == expected_byte_sources
    assert result["str_sources"] == expected_str_sources


def test_convert_textual_byte_to_str_with_empty():
    # Test with empty content in a mixed source list
    sources = [
        {"path": "empty.txt", "content": b""},
        {"path": "file1.txt", "content": b"Hello World"}
    ]
    result = convert_textual_byte_to_str(sources)

    expected_byte_sources = []
    expected_str_sources = [
        {"path": "empty.txt", "content": ""},
        {"path": "file1.txt", "content": "Hello World"}
    ]

    assert result["byte_sources"] == expected_byte_sources
    assert result["str_sources"] == expected_str_sources


def test_convert_textual_byte_to_str_only_non_utf8():
    # Test with only non-UTF-8 content
    sources = [{"path": "binary.bin", "content": b"\x80\x81\x82"}]
    result = convert_textual_byte_to_str(sources)

    expected_byte_sources = [{"path": "binary.bin", "content": b"\x80\x81\x82"}]
    expected_str_sources = []

    assert result["byte_sources"] == expected_byte_sources
    assert result["str_sources"] == expected_str_sources
