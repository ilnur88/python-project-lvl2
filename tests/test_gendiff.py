from gendiff.gendiff import generate_diff, generate_diff_yaml
import pytest


@pytest.fixture
def file1():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def file2():
    return 'tests/fixtures/file2.json'


@pytest.fixture
def answer():
    return 'tests/fixtures/answer.json'


def test_gendif_json(file1, file2, answer):
    answer_file = open(answer, 'r')    
    answer_str = answer_file.read()
    assert generate_diff(file1, file2) == '{\n    host : hexlet.io\n  - timeout : 50\n  + timeout : 20\n  - proxy : 123.234.53.22\n  - follow : false\n  + verbose : true\n}'


def test_gendif_yaml(file1, file2, answer):
    answer_file = open(answer, 'r')    
    answer_str = answer_file.read()
    assert generate_diff_yaml(file1, file2) == '{\n    host : hexlet.io\n  - timeout : 50\n  + timeout : 20\n  - proxy : 123.234.53.22\n  - follow : false\n  + verbose : true\n}'
