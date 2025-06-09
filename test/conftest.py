from test_helper import TestProjectDir, create_basic_python_project

def test_list_files_basic():
    with TestProjectDir("test_list_files_basic") as project:
        # 프로젝트 구조 생성
        create_basic_python_project(project)
        
        # 테스트 실행
        files = list_files()
        
        assert "main.py" in files
        assert "main.cpython-39.pyc" not in files  # excluded
        assert "app.log" not in files              # excluded