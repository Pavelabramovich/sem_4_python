import builtins
import inspect
import types

from types import (
    NoneType as nonetype,
    ModuleType as moduletype,
    CodeType as codetype,
    FunctionType as functype,
    BuiltinFunctionType as bldinfunctype,
    CellType as celltype,
    MappingProxyType as mapproxytype,
    WrapperDescriptorType as wrapdesctype,
    MethodDescriptorType as metdesctype,
    GetSetDescriptorType as getsetdesctype,
    ClassMethodDescriptorType as clsmetdesctype,
    MemberDescriptorType as memdesctype,
    GeneratorType as gentype,
    EllipsisType as ellipsistype,
    NotImplementedType as notimplementedtype,
    UnionType as uniontype,
    GenericAlias as genaliastype
)

smethodtype = staticmethod
cmethodtype = classmethod
proptype = property


CODE_PROPERTIES = tuple(prop for prop in (
        'co_argcount',
        'co_posonlyargcount',
        'co_kwonlyargcount',
        'co_nlocals',
        'co_stacksize',
        'co_flags',
        'co_code',
        'co_consts',
        'co_names',
        'co_varnames',
        'co_filename',
        'co_name',
        'co_qualname',
        'co_firstlineno',
        'co_lnotab',
        'co_exceptiontable',
        'co_freevars',
        'co_cellvars'
    ) if hasattr(codetype, prop)
)

DESCRIPTOR_TYPES = (
    wrapdesctype,
    metdesctype,
    getsetdesctype,
    clsmetdesctype,
    memdesctype
)

BUILTIN_FUNCTIONS = {value.__name__: value for _, value in inspect.getmembers(builtins)
                     if isinstance(value, types.BuiltinMethodType)}

BUILTIN_CLASSES = {value.__name__: value for _, value in inspect.getmembers(builtins)
                   if inspect.isclass(value)}

BUILTINS = mapproxytype({**BUILTIN_FUNCTIONS, **BUILTIN_CLASSES})


dct = {1: 1, 2: 2, 3: 3}

DICT_OPERATIONS_TYPES = (type(dct.items()), type(dct.keys()), type(dct.values()))

ITER_TYPES = (enumerate, filter, map, range, zip)

