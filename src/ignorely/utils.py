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


def collect_patterns_from_file_list(pattern_file):
    """패턴 파일 목록이 담긴 파일에서 모든 패턴 수집 (파일이 없으면 빈 리스트 반환)"""
    patterns = []
    if not os.path.exists(pattern_file):
        return patterns  # 파일이 없으면 빈 파일처럼 동작
    
    with open(pattern_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # 각 라인은 패턴 파일의 경로
                patterns.extend(collect_ignore_patterns([line]))
    
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


def filter_files(files, exclude_patterns=None, include_patterns=None):
    """include/exclude 패턴으로 파일 필터링"""
    result = files[:]
    
    # Include 패턴이 있다면 먼저 적용 (include 패턴에 매치되는 것만 남김)
    if include_patterns:
        include_spec = PathSpec.from_lines(GitWildMatchPattern, include_patterns)
        result = [f for f in result if include_spec.match_file(f)]
    
    # Exclude 패턴 적용 (exclude 패턴에 매치되는 것 제거)
    if exclude_patterns:
        exclude_spec = PathSpec.from_lines(GitWildMatchPattern, exclude_patterns)
        result = [f for f in result if not exclude_spec.match_file(f)]
    
    return result


def list_files(exclude_tot_file=None, include_tot_file=None):
    """include/exclude 방식으로 파일 필터링"""
    exclude_patterns = []
    include_patterns = []
    
    # 기본값 설정
    if exclude_tot_file is None:
        exclude_tot_file = ".ignorely/exclude_tot"
    if include_tot_file is None:
        include_tot_file = ".ignorely/include_tot"
    
    # exclude_tot, include_tot 파일에서 패턴 수집
    exclude_patterns.extend(collect_patterns_from_file_list(exclude_tot_file))
    include_patterns.extend(collect_patterns_from_file_list(include_tot_file))
    
    all_files = get_all_files()
    return filter_files(all_files, exclude_patterns, include_patterns)


def copy_files(files, output_dir, dry_run=False, flatten=False, divider="%", clean=False):
    """파일 복사 함수 - 확장된 옵션 지원"""
    import shutil

    # Clean 옵션 처리
    if clean and os.path.exists(output_dir):
        if not dry_run:
            shutil.rmtree(output_dir)

    copied_files = []
    for file in files:
        if not os.path.exists(file):
            continue

        if flatten:
            # 플래튼 모드: 디렉토리 구조를 평탄화하고 divider로 경로 구분
            flat_filename = file.replace(os.path.sep, divider)
            dest_path = os.path.join(output_dir, flat_filename)
            
            # 출력 디렉토리 생성
            if not os.path.exists(output_dir) and not dry_run:
                os.makedirs(output_dir, exist_ok=True)
        else:
            # 일반 모드: 원본 디렉토리 구조 유지
            dest_path = os.path.join(output_dir, file)
            dest_dir = os.path.dirname(dest_path)

            # 하위 디렉토리 생성
            if not dry_run and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

        if not dry_run:
            shutil.copy2(file, dest_path)

        copied_files.append((file, dest_path))

    return copied_files


def export_files(output_dir, exclude_tot_file=None, include_tot_file=None, 
                 dry_run=False, flatten=False, divider="%", clean=False):
    """파일 필터링 후 복사하는 통합 함수"""
    # 1. 파일 필터링
    filtered_files = list_files(exclude_tot_file, include_tot_file)
    
    # 2. 파일 복사
    copied_files = copy_files(
        files=filtered_files,
        output_dir=output_dir,
        dry_run=dry_run,
        flatten=flatten,
        divider=divider,
        clean=clean
    )
    
    return filtered_files, copied_files