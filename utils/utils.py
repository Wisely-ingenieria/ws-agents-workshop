import os
from datetime import datetime
from numpy import dot
from numpy.linalg import norm

def vector_similarity(v1, v2):
    cos_sim = dot(v1, v2)/(norm(v1)*norm(v2))
    return cos_sim

class Logger:
    def __init__(self, log_file=None, log_dir='./logs'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            log_file = f"log_{timestamp}.log"
        
        self.log_file = os.path.join(log_dir, log_file)

    def _write_log(self, level, msg, verbose):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cleaned_msg = msg.encode('utf-8', errors='replace').decode('utf-8')
        log_entry = f"{timestamp} [{level}] {cleaned_msg}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        if verbose:
            print(log_entry.strip())

    def info(self, msg, verbose=False):
        self._write_log("INFO", msg, verbose)

    def warn(self, msg, verbose=False):
        self._write_log("WARN", msg, verbose)

    def error(self, msg, verbose=True):
        self._write_log("ERROR", msg, verbose)