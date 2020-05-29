# from django.test import TestCase
import json


# Create your tests here.
def assert_delimiter(key_str, response_json):
    """
    分隔符处理
    """
    # TODO
    hierarchy = key_str.split('.')
    try:
        response = json.loads(response_json)
        result = response
        for tier in hierarchy:
            result = result.get(tier, dict())
            print(result)
        return result
    except Exception as es:
        return None


assert_delimiter("a.b.c", '{"a":1,"b":"4"}')
