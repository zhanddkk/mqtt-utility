from namedlist import namedlist as __named_list
from namedlist import NO_DEFAULT
from collections import OrderedDict


def get_fields(self):
    return getattr(self, '_fields')


def get_dict(self):
    return dict(zip(getattr(self, '_fields'), self))


def get_ordered_dict(self):
    return OrderedDict(zip(getattr(self, '_fields'), self))


def named_list(typename, field_names, default=NO_DEFAULT, rename=False, use_slots=True):
    named_class = __named_list('_' + typename, field_names, default, rename, use_slots)
    type_dict = {
        # 'fields': property(fget=get_fields, doc='Get all attributes\'s name as a tuple'),
        'fields': getattr(named_class, '_fields'),
        '__dict__': property(fget=get_dict, doc='Convert named list to dict'),
        'ordered_dict': property(fget=get_ordered_dict, doc='Convert named list to ordered dict')
    }
    # type(object_or_name, bases, dict)
    # type(object) -> the object's type
    # type(name, bases, dict) -> a new type
    # (copied from class doc)
    named_class = type(typename, (named_class, ), type_dict)
    return named_class
    pass

if __name__ == '__main__':
    test_class = named_list('TestClass', 'a, b, z, y, h, k')
    test = test_class(a=1, b=2, z=3, y=4, h=5, k=6)
    print(test.fields)
    print('--To Dict--')
    for (key, data) in test.__dict__.items():
        print(key, '=', data)
    print('--To Ordered Dict--')
    for (key, data) in test.ordered_dict.items():
        print(key, '=', data)
    pass
