from gendiff.gendiff import generate_diff
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


@pytest.fixture
def answer_plain():
    return 'tests/fixtures/answer_plain.txt'

@pytest.fixture
def answer_json():
    return 'tests/fixtures/answer_json.json'


def test_gendif_tree(file1, file2, answer):
    answer_file = open(answer, 'r')    
    answer_str = answer_file.read()
    assert generate_diff(file1, file2) == answer_str

def test_gendif_plain(file1, file2, answer_plain):
    answer_file = open(answer_plain, 'r')    
    answer_str = answer_file.read()
    assert generate_diff(file1, file2, 'plain') == answer_str

def test_gendif_json(file1, file2, answer_json):
    answer_file = open(answer_json, 'r')    
    answer_str = answer_file.read()
    assert generate_diff(file1, file2, 'json') == answer_str    