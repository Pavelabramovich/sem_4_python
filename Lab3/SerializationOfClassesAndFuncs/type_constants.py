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
    MemberDescriptorType as memdesctype
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


