from string import Template


def generate_file_from_tpl(tpl_file, file_out, data):
    file_in = open('utils/templates/{}'.format(tpl_file))
    file_in_data = Template(file_in.read())
    file_in_data = file_in_data.substitute(data)
    file_out = open(file_out, 'w')
    file_out.write(file_in_data)
    file_out.close()
