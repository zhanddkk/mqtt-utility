class NameClass(object):
    def __init__(self, name, items):
        name = str(name)
        self.new_class = None
        class_text_head = 'class ' + name + ':\n'
        class_text_body = '    __fields = []\n'
        for item in items:
            class_text_body += '    ' + str(item) + ' = None\n'
            class_text_body += '    ' + '__fields.append(\'' + str(item) + '\')\n'
        class_text_body += '    fields = tuple(__fields)\n'
        class_text_body += '    del __fields\n'
        class_text_body += '''    def __init__(self, *args):
        i = 0
        for val in args:
            setattr(self, self.fields[i], val)
            if i + 1 >= len(self.fields):
                break
            i += 1
        pass
        \n'''
        class_text = class_text_head + class_text_body + 'self.new_class = ' + name
        # print(class_text)
        exec(class_text)
    pass
