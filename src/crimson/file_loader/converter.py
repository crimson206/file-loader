from typing import TypedDict, List, Any
from . import generate_file_contents, collect_files, ByteSourceDict


class StrSourceDict(TypedDict):
    path: str
    content: str


class MixedSourceDict(TypedDict):
    byte_sources: List[ByteSourceDict]
    str_sources: List[StrSourceDict]


def convert_byte_to_str(
    sources: List[ByteSourceDict],
    reference: Any = {
        "generate_fn": generate_file_contents,
        "collect_fn": collect_files,
    },
) -> List[StrSourceDict]:
    """
    Converts the byte content in ByteSourceDict to string content.

    For the information of `generate_fn` and `collect_fn`,
    check the reference arg dummy.
    """
    output = []

    for item in sources:
        output.append({"path": item["path"], "content": item["content"].decode("utf-8")})
    return output


def convert_textual_byte_to_str(
    sources: List[ByteSourceDict]
) -> MixedSourceDict:
    """
    Converts the byte content in ByteSourceDict to string content if it's textual
    and separates them into byte_sources and str_sources.

    Returns a MixedSourceDict with:
    - "byte_sources": List of ByteSourceDict
    - "str_sources": List of StrSourceDict
    """
    byte_sources: List[ByteSourceDict] = []
    str_sources: List[StrSourceDict] = []

    for item in sources:
        try:
            # Attempt to decode the byte content
            decoded_content = item["content"].decode("utf-8")
            str_sources.append({"path": item["path"], "content": decoded_content})
        except UnicodeDecodeError:
            # If it fails, keep it as ByteSourceDict
            byte_sources.append(item)

    return MixedSourceDict(
        byte_sources=byte_sources,
        str_sources=str_sources
    )
