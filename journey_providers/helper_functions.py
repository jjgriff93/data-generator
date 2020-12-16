# Simple helper functions to make delay amounts easier to construct & more readable


def minutes(amount: int):
    """
    Helper function to convert minutes to seconds (for delay period)
    """
    return amount * 60


def hours(amount: int):
    """
    Helper function to convert minutes to seconds (for delay period)
    """
    return amount * 60 * 60


def days(amount: int):
    """
    Helper function to convert minutes to seconds (for delay period)
    """
    return amount * 60 * 60 * 24
