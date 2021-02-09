from django.test import TestCase

# Create your tests here.
data = [{'country': '国内', 'reputation': '985', 'university': '北京大学', 'university_id': 'beijig'},
        {'country': '国内', 'reputation': '211', 'university': '清华大学', 'university_id': 'qinghua'},
        {'country': '国内', 'reputation': '985', 'university': '浙江大学', 'university_id': 'zhejiang'},
        {'country': '国内', 'reputation': '211', 'university': '武汉大学', 'university_id': 'wuhan'},
        {'country': '国内', 'reputation': '其它', 'university': '邯郸大学', 'university_id': 'handan'},
        {'country': '国内', 'reputation': '其它', 'university': '沧州大学', 'university_id': 'cangzhou'},
        {'country': '国外', 'reputation': None, 'university': '哈弗大学', 'university_id': 'hafu'},
        {'country': '国外', 'reputation': None, 'university': '剑桥大学', 'university_id': 'jianqiao'},
        {'country': '国外', 'reputation': None, 'university': '牛津大学', 'university_id': 'niujin'}]

tree = []

for item in data:
    for k, v in item.items():
        if k == "country":
            if not tree:
                tree.append({'title': v, "key": v, "value": v, "children": []})
            for tree_node in tree:
                if tree_node.get('title') == v:
                    break
            else:
                tree.append({'title': v, "key": v, "value": v, "children": []})
        elif k == "reputation":
            for tree_node in tree:
                if not tree_node.get('children'):
                    tree_node['children'].append({'title': v, "key": v, "value": v, "children": []})
                for item in tree_node['children']:
                    if item.get('title') == v:
                        break
                else:
                    tree_node['children'].append({'title': v, "key": v, "value": v, "children": []})


print(tree)
