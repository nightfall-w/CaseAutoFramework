def equals(result, expect):
    if str(result) == str(expect):
        return True
    else:
        return False


def less_than(result, expect):
    try:
        if int(result) < int(expect):
            return True
        else:
            return False
    except Exception:
        return False


def less_than_or_equals(result, expect):
    try:
        if int(result) <= int(expect):
            return True
        else:
            return False
    except Exception:
        return False


def greater_than(result, expect):
    try:
        if int(result) > int(expect):
            return True
        else:
            return False
    except Exception:
        return False


def greater_than_or_equals(result, expect):
    try:
        if int(result) >= int(expect):
            return True
        else:
            return False
    except Exception:
        return False


def not_equals(result, expect):
    try:
        if int(result) != int(expect):
            return True
        else:
            return False
    except Exception:
        return False


def length_equals(result, expect):
    try:
        if len(result) == len(expect):
            return True
        else:
            return False
    except Exception:
        return False


def length_greater_than(result, expect):
    try:
        if len(result) > len(expect):
            return True
        else:
            return False
    except Exception:
        return False


def length_greater_than_or_equals(result, expect):
    try:
        if len(result) >= len(expect):
            return True
        else:
            return False
    except Exception:
        return False


def length_less_than(result, expect):
    try:
        if len(result) < len(expect):
            return True
        else:
            return False
    except Exception:
        return False


def length_less_than_or_equals(result, expect):
    try:
        if len(result) <= len(expect):
            return True
        else:
            return False
    except Exception:
        return False


def contain(result, expect):
    try:
        if expect in result:
            return True
        else:
            return False
    except Exception:
        return False


def not_contain(result, expect):
    try:
        if expect not in result:
            return True
        else:
            return False
    except Exception:
        return False
