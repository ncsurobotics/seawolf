import inspect

def message(Message):
    """Returns the current line number in our program allong with a message"""
    return "NOTE // " + str(Message) + " // Line Number " + str(inspect.currentframe().f_back.f_lineno)
