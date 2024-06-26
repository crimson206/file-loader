# src/crimson/file_loader/__init__.py
import os
from typing import *
from pathlib import Path
import shutil
import re


def search(pattern: str, text: str, flags: Optional[List[re.RegexFlag]] = None):
    combined_flags = 0
    if flags:
        for flag in flags:
            combined_flags |= flag

    compiled_pattern = re.compile(pattern, flags=combined_flags)

    is_included = compiled_pattern.search(text) is not None

    return is_included

@overload
def filter(
    pattern: str,
    paths: List[str],
    mode: Literal['include', 'exclude'] = 'include',
    flags: Optional[List[re.RegexFlag]] = None
) -> List[str]:
    '''doc1'''
    ...

@overload
def filter(
    pattern: str,
    paths: List[Path],
    mode: Literal['include', 'exclude'] = 'include',
    flags: Optional[List[re.RegexFlag]] = None
) -> List[str]:
    '''doc2'''
    ...

def filter(
    pattern: str, 
    paths: Union[List[str], List[Path]],
    mode: Literal['include', 'exclude'] = 'include',
    flags: Optional[List[re.RegexFlag]] = None
) -> List[str]:
    
    if isinstance(paths[0], Path):
        paths = _convert_paths_to_texts(paths)
    paths = _filter_base(
        pattern,
        paths,
        mode,
        flags,
    )
    
    return paths

def _filter_base(pattern: str, paths: List[str], mode: Literal['include', 'exclude'] = 'include', flags: Optional[List[re.RegexFlag]] = None) -> List[str]:
    included = []
    for path in paths:
        is_included = search(pattern, path, flags)
        if mode == 'exclude':
            is_included = not is_included
        if is_included:
            included.append(path)
    return included

def _convert_paths_to_texts(paths: List[Path]) -> List[str]:
    texts = [str(path) for path in paths]
    return texts


def get_paths(
    source: str,
):
    paths = []
    for root, _, files in os.walk(source):
        for file in files:
            file_path = Path(root) / file
            paths.append(str(file_path))
    return paths

def filter_paths(
    source: str,
    includes: List[str]=[],
    excludes: List[str]=[],
):
    paths = get_paths(source)
    
    for pattern in includes:
        paths = filter(pattern, paths, mode='include')
    
    for pattern in excludes:
        paths = filter(pattern, paths, mode='exclude')
    
    return paths

def transform_path(
  path:str,
  separator:str='%'
)->str:
    path = path.replace('/', separator)
    return path

def collect_files(
    source: str,
    out_dir: str,
    separator: str = '%',
    includes: List[str]=[],
    excludes: List[str]=[],
    path_editor: Optional[Callable[[str], str]] = None,
    overwrite: bool = True
):
    source_paths = filter_paths(source, includes, excludes)
    
    out_dir_path = Path(out_dir)
    
    if overwrite and out_dir_path.exists():
        shutil.rmtree(out_dir)
    
    out_dir_path.mkdir(parents=True, exist_ok=True)
    
    for src_path in source_paths:

        new_path = transform_path(src_path, separator)
        if path_editor:
            new_path = path_editor(new_path)
        new_path = str(Path(out_dir)/new_path)

        Path(new_path).parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src_path, new_path)
    
    print(f"Files collected from {source} to {out_dir}")

def reconstruct_folder_structure(
    source: str,
    out_dir: str,
    separator: str = '%',
    path_editor: Optional[Callable[[str], str]] = None,
    overwrite: bool = True
):

    out_dir_path = Path(out_dir)
    
    if overwrite and out_dir_path.exists():
        shutil.rmtree(out_dir)
    
    out_dir_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(source):
        for file in files:

            src_file_path = os.path.join(root, file)

            if path_editor:
                file = path_editor(file)

            relative_path = file.replace(separator, os.path.sep)
            new_file_path = os.path.join(out_dir, relative_path)
            
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            
            shutil.copy2(src_file_path, new_file_path)
    
    print(f"Folder structure reconstructed from {source} to {out_dir}")
