import os
from string import Template


def generate_file_from_tpl(tpl_file, file_out, data):
    file_in = open(tpl_file)
    file_in_data = Template(file_in.read())
    file_in_data = file_in_data.substitute(data)
    file_out = open(file_out, 'w+')
    file_out.write(file_in_data)
    file_out.close()


def generate_app_folder(files, data):
    src_path = os.path.dirname(os.path.abspath(__file__)) + '/templates/'

    dst_path = 'apps/%s' % data['name_slug']
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    init_file = open('%s/__init__.py' % dst_path, 'w+')
    init_file.close()

    for file in files:
        generate_file_from_tpl('%s/%s.tpl' % (src_path, file),
            '%s/%s.py' % (dst_path, file), data)
