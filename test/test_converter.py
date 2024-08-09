import pytest
from crimson.file_loader.converter import convert_byte_to_str


@pytest.fixture
def byte_sources():
    return [
        {"path": "file1.txt", "content": b"Hello World"},
        {"path": "file2.txt", "content": b"Python Testing"},
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
