def_user_function_str = '''def user_function(value, times):
    value += 1
    return value
'''


class RepeaterParameter:
    is_running = False
    counter = 0         # interval times counter
    tagger_count = 0    # 0: repeater is invalid
    repeat_times = 0    # repeater times counter
    exit_times = 0      # 0: will not stop
    user_function_str = def_user_function_str
    pass

if __name__ == '__main__':
    pass
