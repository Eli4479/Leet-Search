__all__ = ["truncate_problem"]


def truncate_problem(data, max_length=997):
    if len(data) > max_length:
        return data[:max_length] + '...'
    return data
