import threading

def init():
    global mod
    global mc
    global referer_dict
    global lock

    # Dictionary structure for referer_dict
    # Key => referer URL
    # values => another dictionary
    # This dictionary will have key as each request body parameter (like name, id etc.)
    # and value as its corresponding value
    # TODO: move to cache

    referer_dict = {}

    # Lock for the dictionary
    lock = threading.Lock()