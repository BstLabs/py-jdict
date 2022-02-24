"""JavaScript-like Python dictionary"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import date, datetime
from typing import Any, Final, Tuple, Union, get_args, get_origin, get_type_hints

from .transformer import transform

NoneType = type(None)

__version__ = "1.0.4"


class _Field:
    def __init__(self, name: str, arg: str, is_optional: bool, is_final: bool) -> None:
        """
        Initialize one field descriptor

        :param name: original field name
        :param arg: how should it look like in __init__ argument list
        :param is_optional: is it optional?
        :param is_final: is it Final (could not be changed)?
        """
        self.name = name
        self.arg = arg
        self.is_optional = is_optional
        self.is_final = is_final

    @staticmethod
    def _strip_final(t: type) -> str:
        """
        Strip Final wrapper from the field type hint

        :param t: original field type hint Final[...]
        :return: type name for built ins and origin for type hints (e.g. Mapping[...]
        """
        return repr(t) if get_origin(t) else t.__name__

    @staticmethod
    def _get_type_hint(t: type) -> Tuple[str, bool, bool]:
        """
        Determine correct type hint for __init__ argument corresponding to a field
        :param t: original type hint
        :return: type hint string, plus two flags indicating optional and final fields
        """
        origin = get_origin(t)
        if origin:
            args = get_args(t)
            is_optional = Union == origin and NoneType in args
            is_final = Final == origin
            name = _Field._strip_final(args[0]) if is_final else repr(t)
            return f'{name}{"=None" if is_optional else ""}', is_optional, is_final
        return t.__name__, False, False

    @staticmethod
    def get_field(n: str, t: type) -> _Field:
        """
        Create a field descriptor (factory method)

        :param n: field name
        :param t: field type hint
        :return: complete field descriptor
        """
        type_hint, is_optional, is_final = _Field._get_type_hint(t)
        arg = f"{n}: {type_hint}"
        return _Field(n, arg, is_optional, is_final)


def _build_pairs(fields: Tuple[_Field, ...]) -> str:
    """
    Build sequence of name=value pairs to be passed to the base class constructor
    :param fields: list of field descriptors
    :return: argument list string to format base class __init__ invocation
    """
    optionals = ", ".join(f'"{f.name}"' for f in fields if f.is_optional)
    if not optionals:
        return ", ".join(f"{f.name}={f.name}" for f in fields)
    pairs = ", ".join(f'("{f.name}", {f.name})' for f in fields)
    return f"tuple((n, v) for n, v in ({pairs}) if v is not None or n not in {{{optionals}}})"


def _configure_init(cls, fields: Tuple[_Field, ...]) -> callable:
    """
    Configure __init__ method for subclass

    :param cls: subclass
    :param fields: list of field descriptors
    :return: function performing correct initialization
    """
    args = ", ".join(f.arg for f in fields)
    pairs = _build_pairs(fields)
    name = f"{cls.__name__}__init__"
    init_fn = (
        f"def {name}(self, {args}) -> None:" + f"\n\tjdict.__init__(self, {pairs})"
    )
    ns = {}
    exec(init_fn, globals(), ns)
    return ns[name]


def _configure_setattr(fields: Tuple[_Field, ...]) -> callable:
    """
    Configure __setattr__ method for the subclass

    :param fields: list of field descriptors
    :return: function performing correct setting for mutable attributes only
    """
    mutable_attributes = {f.name for f in fields if not f.is_final}

    def _protected_setattr(self, key: str, value: Any) -> None:
        if key not in mutable_attributes:
            raise AttributeError(f"{key} is final or does not exist")
        self.__setitem__(key, value)

    return _protected_setattr


# noinspection PyPep8Naming
class jdict(dict):
    """
    The class gives access to the dictionary through the attribute name.
    """

    def __init_subclass__(cls, /, **kwargs) -> None:
        """
        Intercept subclass creation and configure a Record-type access based on field hints.
        Perhaps, implementing the same with meta-class would be more efficient and would support class hierarchy
        but at this stage, I'm not certain it's worth extra complexity
        For more details, look at https://www.python.org/dev/peps/pep-0487/

        :param kwargs: ignored in this case and just passed  to the base class
        """
        super().__init_subclass__(**kwargs)
        hints = get_type_hints(cls)
        if not hints:
            raise ValueError("Empty field list")
        fields = tuple(_Field.get_field(n, t) for n, t in hints.items())
        setattr(cls, "__init__", _configure_init(cls, fields))
        setattr(cls, "__setattr__", _configure_setattr(fields))

    def __getattr__(self, name: str) -> Any:
        """
        Method returns the value of the named attribute of an object. If not found, it returns null object.
        :param name: str
        :return: Any
        """
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name + " not in dict")

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Method sets the value of given attribute of an object.
        :param key: str
        :param value: Any
        :return: None
        """
        self.__setitem__(key, value)

    def __deepcopy__(self, memo) -> jdict:
        # Do not know why PyCharm complains about it
        # noinspection PyArgumentList
        copy = jdict((k, deepcopy(v, memo)) for k, v in self.items())
        memo[id(self)] = copy
        return copy


def patch_module(module: str) -> None:
    parsers: Final = sys.modules[module]
    filename: Final[str] = parsers.__dict__["__file__"]
    src: Final[str] = open(filename).read()
    inlined: Final = transform(src)
    code: Final = compile(inlined, filename, "exec")
    exec(code, vars(parsers))


def _json_serial(_, obj) -> Any:
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def set_codec(codec: json) -> None:
    codec._default_decoder = codec.JSONDecoder(object_pairs_hook=jdict)
    codec.JSONEncoder.default = (
        _json_serial  # need more aggressive patching due to indent
    )
