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
    """지정된 디렉터리의 모든 파일 목록 가져오기"""
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


def list_files(ignorely_dir=".ignorely", target_dir="."):
    """새로운 방식: ignorely_dir에서 설정을 읽고 target_dir에서 파일 필터링
    
    Args:
        ignorely_dir (str): ignorely 설정 디렉토리 경로 (기본값: .ignorely)
        target_dir (str): 파일을 찾을 대상 디렉토리 (기본값: .)
    """
    exclude_patterns = []
    include_patterns = []
    
    # 설정 파일 경로
    exclude_tot_file = os.path.join(ignorely_dir, "exclude_tot")
    include_tot_file = os.path.join(ignorely_dir, "include_tot")
    
    # exclude_tot, include_tot 파일이 있으면 패턴 수집
    if os.path.exists(exclude_tot_file):
        exclude_patterns.extend(collect_patterns_from_file_list(exclude_tot_file))
    
    if os.path.exists(include_tot_file):
        include_patterns.extend(collect_patterns_from_file_list(include_tot_file))
    
    # target_dir에서 파일 목록 수집
    all_files = get_all_files(target_dir)
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


def export_files(output_dir, ignorely_dir=".ignorely", target_dir=".", 
                dry_run=False, flatten=False, divider="%", clean=False):
    """파일 필터링 후 복사하는 통합 함수 - 새로운 방식
    
    Args:
        output_dir (str): 복사할 대상 디렉토리
        ignorely_dir (str): ignorely 설정 디렉토리 경로 (기본값: .ignorely)
        target_dir (str): 파일을 찾을 대상 디렉토리 (기본값: .)
        dry_run (bool): 실제로 복사하지 않고 시뮬레이션만 수행
        flatten (bool): 디렉토리 구조를 평탄화할지 여부
        divider (str): flatten 모드에서 사용할 경로 구분자
        clean (bool): 복사 전에 output_dir을 정리할지 여부
    """
    # 1. 파일 필터링
    filtered_files = list_files(ignorely_dir=ignorely_dir, target_dir=target_dir)
    
    # 2. target_dir 기준으로 파일 경로 조정
    adjusted_files = []
    for file in filtered_files:
        if target_dir != ".":
            # target_dir가 현재 디렉토리가 아닌 경우 전체 경로로 조정
            adjusted_file = os.path.join(target_dir, file)
        else:
            adjusted_file = file
        adjusted_files.append(adjusted_file)
    
    # 3. 파일 복사
    copied_files = copy_files(
        files=adjusted_files,
        output_dir=output_dir,
        dry_run=dry_run,
        flatten=flatten,
        divider=divider,
        clean=clean
    )
    
    return filtered_files, copied_files


def initialize_ignorely_directory(directory=".ignorely"):
    """Initialize .ignorely directory with required files.
    
    Args:
        directory (str): Target directory to create ignorely folder. Defaults to .ignorely
    
    Returns:
        bool: True if initialization was successful, False if directory already exists
    """
    # Check if directory already exists
    if os.path.exists(directory):
        return False
        
    # Create directory
    os.makedirs(directory)
    
    # Create exclude_tot with actual file path
    exclude_tot_content = """# Exclude patterns file list
# Add paths to your exclude pattern files (e.g. .gitignore)
.gitignore
.ignorely/.excludes
"""
    
    # Create include_tot with actual file path
    include_tot_content = """# Include patterns file list
# Add paths to your include pattern files
.ignorely/.includes
"""
    
    # Create .excludes with common ignore patterns
    excludes_content = """# Common ignore patterns
.git/
output_dir/
"""
    
    # Create .includes with example patterns
    includes_content = """# Example include patterns
.ignorely/
src/
tests/
"""
    
    # Write all the files
    with open(os.path.join(directory, "exclude_tot"), "w") as f:
        f.write(exclude_tot_content)
        
    with open(os.path.join(directory, "include_tot"), "w") as f:
        f.write(include_tot_content)
        
    with open(os.path.join(directory, ".excludes"), "w") as f:
        f.write(excludes_content)
        
    with open(os.path.join(directory, ".includes"), "w") as f:
        f.write(includes_content)
        
    return True