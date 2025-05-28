
import os

def log(*args):
    """
    Log the arguments to a file named 'log.txt' in append mode.
    Each log entry is written on a new line.
    """
    with open('log.txt', 'a') as f:
        f.write(' '.join(map(str, args)) + '\n')
        f.flush()
