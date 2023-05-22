
import os
from tree_utils_02.size_node import FileSizeNode
from tree_utils_02.size_tree import BLOCK_SIZE, SizeTree


def test_construct_filenode_is_dir():
    size_tree = SizeTree()
    
    assert FileSizeNode(
            name='filename',
            is_dir=True,
            children=[],
            size=BLOCK_SIZE
        ) == size_tree.construct_filenode('filename', True)

def test_construct_filenode_not_dir(tmp_path):
    file_content = 'content'
    file_name = 'test_size_tree_temp.txt'
    file_path = tmp_path / file_name
    file_path.write_text(file_content)
    
    size_tree = SizeTree()
    assert FileSizeNode(
            name=file_name,
            is_dir=False,
            children=[],
            size=len(file_content)
        ) == size_tree.construct_filenode(str(file_path), False)
    
def test_update_filenode():
    child_node = FileSizeNode(
            name='child',
            is_dir=False,
            children=[],
            size=3
        )
    parent_node = FileSizeNode(
            name='parent',
            is_dir=True,
            children=[child_node],
            size=6
        )
    
    size_tree = SizeTree()
    res = size_tree.update_filenode(parent_node)
    
    parent_node.size += child_node.size
    assert parent_node == res