from typing import TypedDict, List, Any
from . import generate_file_contents, collect_files, ByteSourceDict


class SourceDict(TypedDict):
    path: str
    content: str


def convert_byte_to_str(
    sources: List[ByteSourceDict],
    reference: Any = {
        "generate_fn": generate_file_contents,
        "collect_fn": collect_files,
    },
) -> List[SourceDict]:
    """
    The `generate_fn` returns `List[ByteSourceDict]` instead of `str`.
    It is for `collect_fn` to create non-textual files as well.
    In order to convert the byte data simply, this helper function is added.

    For the information of `generate_fn` and `collect_fn`,
    check the reference arg dummy.
    """
    output = []

    for item in sources:
        output.append({"path": item["path"], "content": item["content"].decode("utf-8")})
    return output
