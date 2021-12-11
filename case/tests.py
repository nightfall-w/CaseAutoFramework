def create1(i):
    return {"name": i}


def create2(i):
    return {"age": i}


templates = []
for i in range(3):
    templates.append([
        create1(i), create2(i)
    ])
print(templates)
