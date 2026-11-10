PRIORITY_ORDER = ("express", "standard", "bulk")


def next_job(queues: dict):
    for name in PRIORITY_ORDER:
        job = queues[name].receive()
        if job is not None:
            return name, job
    return None
