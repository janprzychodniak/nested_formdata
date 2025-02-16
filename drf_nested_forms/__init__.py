__title__ = 'drf_nested_formdata'
__version__ = '1.1.7'
__author__ = 'Duke Effiom'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021'

# Version synonym
from .exceptions import ParseError
from .parsers import NestedMultiPartParser, NestedJSONParser
from .mixins import UtilityMixin
from .utils import NestedForm

VERSION = __version__
