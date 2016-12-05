class NameClass(object):
    def __init__(self, name, items):
        name = str(name)
        self.new_class = None
        if type(items) is str:
            items = items.split(',')
            for i in range(len(items)):
                items[i] = items[i].strip(' ')
        class_text_head = 'class ' + name + ':\n'
        class_text_body = '    __fields = []\n'
        for item in items:
            class_text_body += '    ' + str(item) + ' = None\n'
            class_text_body += '    ' + '__fields.append(\'' + str(item) + '\')\n'
        class_text_body += '    fields = tuple(__fields)\n'
        class_text_body += '    del __fields\n'
        class_text_body += '''    def __init__(self, *args, **kwargs):
        i = 0
        for val in args:
            setattr(self, self.fields[i], val)
            if i + 1 >= len(self.fields):
                break
            i += 1
        for (key, val) in kwargs.items():
            if key in self.fields:
                setattr(self, key, val)
            else:
                pass
        pass
        \n'''
        class_text = class_text_head + class_text_body + 'self.new_class = ' + name
        # print(class_text)
        exec(class_text)
    pass
