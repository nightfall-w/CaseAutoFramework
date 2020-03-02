import sys
from pathlib import Path

from standard.config import ConfigParser


class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """

    """
    [{
          id: 1,
          label: '一级 1',
          children: [{
            id: 4,
            label: '二级 1-1',
            children: [{
              id: 9,
              label: '三级 1-1-1'
            }, {
              id: 10,
              label: '三级 1-1-2'
            }]
          }]
        }, {
          id: 2,
          label: '一级 2',
          children: [{
            id: 5,
            label: '二级 2-1'
          }, {
            id: 6,
            label: '二级 2-2'
          }]
        }, 
    """

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''
        self.current_dir = []
        self.allow_format = eval(ConfigParser.get_config('case', 'allow_format'))
        self.index = 0

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0, ):
        if self.pathname.is_file() and self.pathname.suffix in self.allow_format:
            self.index += 1
            self.current_dir.append({
                'id': self.index,
                'label': self.pathname.name,
            })
            self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
        elif self.pathname.is_dir():
            self.index += 1
            self.current_dir.append({
                'id': self.index,
                'label': str(self.pathname.relative_to(self.pathname.parent)),
                'children': []
            })
            self.current_dir = self.current_dir['children']
            self.tree += '    |' * n + '-' * 4 + \
                         str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'
            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)


if __name__ == '__main__':
    dirtree = DirectionTree()
    # 命令参数个数为1，生成当前目录的目录树
    if len(sys.argv) == 1:
        dirtree.set_path(Path.cwd())
        dirtree.generate_tree()
        print(dirtree.tree)
        print(dirtree.current_dir)
    # 命令参数个数为2并且目录存在存在
    elif len(sys.argv) == 2 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为3并且目录存在存在
    elif len(sys.argv) == 3 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        dirtree.set_filename(sys.argv[2])
        dirtree.save_file()
    else:  # 参数个数太多，无法解析
        print('命令行参数太多，请检查！')
