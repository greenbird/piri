from typing_extensions import Final

# Objects
NAME = 'name'
ARRAY: Final = 'array'
ITERABLES: Final = 'iterables'

ATTRIBUTES: Final = 'attributes'
OBJECTS: Final = 'objects'
BRANCHING_OBJECTS: Final = 'branching_objects'
BRANCHING_ATTRIBUTES: Final = 'branching_attributes'

MAPPINGS: Final = 'mappings'
SEPARATOR: Final = 'separator'
IF_STATEMENTS: Final = 'if_statements'
CASTING: Final = 'casting'
DEFAULT: Final = 'default'

# Iterables
ALIAS: Final = 'alias'
PATH: Final = 'path'

# Mapping
# 'path' from iterables
# 'default'

# IF STATEMENT
CONDITION: Final = 'condition'
IS: Final = 'is'
IN: Final = 'in'
NOT: Final = 'not'
CONTAINS: Final = 'contains'
TARGET: Final = 'target'
THEN: Final = 'then'
OTHERWISE: Final = 'otherwise'

# Slicing
SLICING: Final = 'slicing'
FROM: Final = 'from'
TO: Final = 'to'

# Casting
# 'to' from slicing
INTEGER: Final = 'integer'
DECIMAL: Final = 'decimal'
DATE: Final = 'date'
ORIGINAL_FORMAT: Final = 'original_format'
INTEGER_CONTAINING_DECIMALS = 'integer_containing_decimals'
YMD_DATE_FORMAT: Final = r'(^(yy|yyyy)[^\w]?mm[^\w]?dd$)'
DMY_DATE_FORMAT: Final = r'(^dd[^\w]?mm[^\w]?(yy|yyyy)$)'
MDY_DATE_FORMAT = r'(^mm[^\w]?dd[^\w]?(yy|yyyy)$)'

# Casting helpers
COMMA: Final[str] = ','
PERIOD: Final[str] = '.'
EMPTY: Final[str] = ''

# ISO
ALPHA_TWO = 'alpha_2'
ALPHA_THREE = 'alpha_3'
NUMERIC = 'numeric'
OFFICIAL_NAME = 'official_name'
INVALID = 'invalid'
# NAME
