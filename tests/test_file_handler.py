import os
import pytest
from src.utils.file_handler import read_file, write_file, file_exists

def test_read_file_valid(tmp_path):
    # Create a test file with content
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content)
    
    content = read_file(str(test_file))
    assert content is not None
    assert isinstance(content, str)
    assert content == test_content

def test_read_file_invalid(tmp_path):
    # Create a nested directory structure
    invalid_dir = tmp_path / "path" / "to" / "invalid"
    invalid_dir.mkdir(parents=True)
    
    # Test for a non-existent file in a valid directory
    invalid_file = invalid_dir / "file.txt"
    with pytest.raises(FileNotFoundError):
        read_file(str(invalid_file))

def test_read_file_empty(tmp_path):
    # Create an empty file
    test_file = tmp_path / "empty.txt"
    test_file.write_text("")
    
    content = read_file(str(test_file))
    assert content == ''

def test_write_file(tmp_path):
    test_file = tmp_path / "test_write.txt"
    test_content = "Test content"
    
    write_file(str(test_file), test_content)
    assert test_file.read_text() == test_content

def test_file_exists(tmp_path):
    test_file = tmp_path / "test_exists.txt"
    test_file.write_text("test")
    
    assert file_exists(str(test_file)) == True
    
    non_existent = tmp_path / "non_existent.txt"
    assert file_exists(str(non_existent)) == False