#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import os

shebang_to_upsert = '#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python\n'
shebang_pattern_list = ['#!', 'bin']
BASE_DIR = os.path.join(os.path.dirname(__file__), '../')
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.py') and not f.startswith('__init__'):
            file_path = os.path.join(root, f)
            with open(file_path, 'r') as original:
                first_line = original.readline()
                if first_line == shebang_to_upsert:
                    continue
                if all(map(lambda x: x in first_line.split('/'), shebang_pattern_list)):
                    # update the shebang
                    first_line = ''
                data = original.read()
                with open(file_path, 'w') as modified:
                    modified.write(shebang_to_upsert + first_line + data)
                    print('%r updated with shebang' % f)
