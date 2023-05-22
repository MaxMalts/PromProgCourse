import os
import shutil
import pytest
from tree_utils_02.node import FileNode
from tree_utils_02.tree import Tree


def test_get_path_not_exist():
    with pytest.raises(AttributeError):
        tree = Tree()
        tree.get('test_tree_not_existing_path', False, False)
        
def test_get_not_dirs_only(tmp_path):
    file_name = 'test_tree_temp.txt'
    file_path = tmp_path / file_name
    file_path.touch()
    
    tree = Tree()
    assert FileNode(
            name=file_name,
            is_dir=False,
            children=[]
        ) == tree.get(str(file_path), False, False)

def test_get_recursive_call(tmp_path):
    file_name = 'test_tree_temp.txt'
    file_path = tmp_path / file_name
    file_path.touch()
    
    tree = Tree()
    assert None == tree.get(str(file_path), True, True)

def test_get_not_recursive_call(tmp_path):
    file_name = 'test_tree_temp.txt'
    file_path = tmp_path / file_name
    file_path.touch()
    
    with pytest.raises(AttributeError):
        tree = Tree()
        tree.get(str(file_path), True, False)

def test_get_dir(tmp_path):
    dir_name = 'test_tree_temp'
    file_name = 'temp.txt'
    (tmp_path / dir_name).mkdir()
    (tmp_path / dir_name / file_name).touch()
    
    tree = Tree()
    child_node = FileNode(
        name=file_name,
        is_dir=False,
        children=[]
    )
    assert FileNode(
            name=dir_name,
            is_dir=True,
            children=[child_node]
        ) == tree.get(str(tmp_path / dir_name), False, False)
    
def test_filter_empty_nodes(tmp_path):
    dir_name = 'test_tree_temp'
    subdir_name = 'temp_dir'
    file_name = 'temp.txt'
    (tmp_path / dir_name).mkdir()
    (tmp_path / dir_name / subdir_name).mkdir()
    (tmp_path / dir_name / file_name).touch()
        
    subdir_node = FileNode(name=subdir_name, is_dir=True, children=[])
    file_node = FileNode(name=file_name, is_dir=False, children=[])
    dir_node = FileNode(name=dir_name, is_dir=True, children=[subdir_node, file_node])
    
    tree = Tree()
    tree.filter_empty_nodes(dir_node, str(tmp_path / dir_name))