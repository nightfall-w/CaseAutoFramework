from enum import Enum, unique


@unique
class Type(Enum):
    equals = 'equals'
    less_than = 'less_than'
    less_than_or_equals = 'less_than_or_equals'
    greater_than = 'greater_than'
    greater_than_or_equals = 'greater_than_or_equals'
    not_equals = 'not_equals'
    string_equals = 'string_equals'
    length_equals = 'length_equals'
    length_not_equals = 'length_not_equals'
    length_greater_than = 'length_greater_than'
    length_greater_than_or_equals = 'length_greater_than_or_equals'
    length_less_than = 'length_less_than'
    length_less_than_or_equals = 'length_less_than_or_equals'
    contain = 'contain'
    not_contain = 'not_contain'
    state_code_contain = 'state_code_contain'
    state_code_not_contain = 'state_code_not_contain'
