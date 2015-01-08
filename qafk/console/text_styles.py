def get_pad_func ( attr ):
    @staticmethod
    def _func(string):
        return attr + string + Color.END
    return _func

class Color(object):
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BOLD = '\033[1m'
    GRAY = '\033[1;30m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    MAGENTA = '\033[1;35m'
    CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'
    CRIMSON = '\033[1;38m'

    
    underline = get_pad_func(UNDERLINE)
    bold = get_pad_func(BOLD)
    gray = get_pad_func(GRAY)
    red = get_pad_func(RED)
    green = get_pad_func(GREEN)
    yellow = get_pad_func(YELLOW)
    blue = get_pad_func(BLUE)
    magenta = get_pad_func(MAGENTA)
    crimson = get_pad_func(CRIMSON)

    
