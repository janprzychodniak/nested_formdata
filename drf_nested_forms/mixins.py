import re

# Nested Form data deserializer utility class
# --------------------------------------------

class UtilityMixin(object):
    _nested_re = re.compile(r'((.+)(\[(.*)\])+)|(\[(.*)\]){2,}')
    _namespace_re = re.compile(r'^([\w]+)(?=\[)')
    _list_re = re.compile(r'\[[0-9]+\]')
    _number_re = re.compile(r'[0-9]+')
    _dict_re = re.compile(r'\[(([^A-Za-z]*)([^0-9]+)([0-9]*))+\]')

    @staticmethod
    def strip_bracket(string=''):
        return string.replace('[', '').replace(']', '')

    @staticmethod
    def split_nested_str(string=''):
        return [key + ']' for key in string.split(']') if key != '']

    @staticmethod
    def str_is_empty_list(string=''):
        return string == '[]'

    @staticmethod
    def str_is_empty_dict(string=''):
        return string == '{}'

    def str_is_dict(self, string=''):
        return bool(self._dict_re.fullmatch(string))

    def str_is_list(self, string=''):
        return bool(self._list_re.fullmatch(string))

    def str_is_number(self, string=''):
        return bool(self._number_re.fullmatch(string))

    def str_is_nested(self, string=''):
        return bool(self._nested_re.fullmatch(string))

    def str_is_namespaced(self, string=''):
        return bool(self._namespace_re.match(string))

    def get_namespace(self, string=''):
        namespace = self._namespace_re.match(string)

        if namespace:
            return namespace.group(0)

        return None

    def strip_namespace(self, string=''):
        """
        Strip namespace from key if any 
        """
        namespace = self._namespace_re.match(string)

        if namespace:
            splited_string = string.split(namespace.group(0))
            return ''.join(splited_string)

        return string

    def extract_index(self, string=''):
        number = self._number_re.search(string)

        if number:
            return int(number.group(0))

        return None

    def replace_specials(self, string):
        """
        Replaces special characters like null, booleans
        also changes numbers from string to integer
        """
        
        # we have no interest in any value that is not a string
        if not isinstance(string, str):
            return string

        if string == 'null':
            return None
        elif string == 'true':
            return True
        elif string == 'false':
            return False
        elif self.str_is_number(string):
            return int(string)
        elif self.str_is_empty_list(string):
            return []
        elif self.str_is_empty_dict(string):
            return {}
        else:
            return string

    def get_key(self, nested_key, position=0):
        """
        Get key from a nested key
        """
        if self.str_is_nested(nested_key):
            nested_key = self.strip_namespace(nested_key)
            keys = self.split_nested_str(nested_key)
            return keys[position]

        return ''

    def initialize(self, nested_keys, **kwargs):
        """
        It return the appropiate container `[]`|`{}`
        based on the key provided
        """
        use_first_key = kwargs.get('use_first_key', False)

        if use_first_key:
            key = self.get_key(next(iter(nested_keys)))

            if self.str_is_list(key):
                return []
            
            return {}
        else:
            for nested_key in nested_keys:
                condition = (
                    not self.str_is_nested(nested_key),
                    self.str_is_namespaced(nested_key),
                    self.str_is_dict(self.get_key(nested_key)),
                )

                if any(condition):
                    return {}

            return []

    def get_index(self, key):
        """
        Get the nested sub key index
        """
        if self.str_is_dict(key):
            return self.strip_bracket(key)
        elif self.str_is_empty_list(key):
            # an empty list always has it index as '0'
            return 0

        return self.extract_index(key)

    def key_is_last(self, current_key, data, is_type_of='non_nested'):
        """
        Checks if current key is the last in the data
        """
        nested_keys = list(data.keys())
        current_index = nested_keys.index(current_key)
        next_index = current_index + 1

        def object_type(is_obj):
            is_last = True

            if next_index < len(nested_keys):
                next_key = self.get_key(nested_keys[next_index])
                if is_obj(next_key):
                    is_last = False

            return is_last

        def namespace():
            is_last = True

            if next_index < len(nested_keys):
                next_key = nested_keys[next_index]
                if self.str_is_namespaced(next_key):
                    current_namespace = self.get_namespace(current_key)
                    next_namespace = self.get_namespace(next_key)

                    if current_namespace == next_namespace:
                        is_last = False

            return is_last

        def non_nested():
            is_last = True

            if next_index < len(nested_keys):
                if not self.str_is_nested(nested_keys[next_index]):
                    is_last = False

            return is_last

        if is_type_of == 'list':
            return object_type(self.str_is_list)
        elif is_type_of == 'namespace':
            return namespace()
        elif is_type_of == 'dict':
            return object_type(self.str_is_dict)
        else:
            return non_nested()
