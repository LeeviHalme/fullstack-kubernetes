from main import start_log_loop

def post_worker_init(worker):
    """
    Called after a worker has been forked.
    """
    start_log_loop()