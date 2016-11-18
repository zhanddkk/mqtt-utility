def_user_function_str = '''
def user_function(value, times)
    value += 1
    return value
'''


class RepeaterParameter:
    is_running = False
    counter = 0
    tagger_count = 1
    repeat_times = 0
    exit_times = 0
    user_function_str = def_user_function_str
    pass

if __name__ == '__main__':
    pass
