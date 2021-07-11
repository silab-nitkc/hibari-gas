green  = '\033[32m'
yellow = '\033[33m'
red    = '\033[31m'
reset  = '\033[0m'

def back_to(line_number: int):
    print('\033[{}A'.format(line_number), end='')