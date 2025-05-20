import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


def collect_ignore_patterns(ignore_files):
    """여러 ignore 파일에서 패턴 수집"""
    patterns = []
    for ignore_file in ignore_files:
        if os.path.exists(ignore_file):
            with open(ignore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    # 주석이나 빈 줄 무시
                    if line and not line.startswith("#"):
                        patterns.append(line)
    return patterns


def get_all_files(root_dir="."):
    """현재 디렉터리의 모든 파일 목록 가져오기"""
    files = []
    for root, _, filenames in os.walk(root_dir):
        for filename in filenames:
            path = os.path.join(root, filename)
            # 상대 경로로 변환
            rel_path = os.path.relpath(path, root_dir)
            files.append(rel_path)
    return files


def filter_files(files, patterns):
    """패턴으로 파일 필터링"""
    if not patterns:
        return files

    # GitWildMatchPattern으로 패턴 생성
    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)

    # 패턴에 맞지 않는 파일만 반환
    return [f for f in files if not spec.match_file(f)]


def list_files(ignore_files, additional_files=None):
    """모든 로직을 통합한 함수"""
    all_ignore_files = list(ignore_files)
    if additional_files:
        all_ignore_files.extend(additional_files)

    patterns = collect_ignore_patterns(all_ignore_files)
    all_files = get_all_files()
    return filter_files(all_files, patterns)


def copy_files(files, output_dir, dry_run=False):
    """파일 복사 함수"""
    import shutil

    copied_files = []
    for file in files:
        if not os.path.exists(file):
            continue

        dest_path = os.path.join(output_dir, file)
        dest_dir = os.path.dirname(dest_path)

        if not dry_run:
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            shutil.copy2(file, dest_path)

        copied_files.append((file, dest_path))

    return copied_files
