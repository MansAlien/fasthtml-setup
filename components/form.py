from fasthtml.common import Input


def input(id=None, name=None, holder=None, itype="text", cls=None):
    type = {
        "text": """
            border text-sm rounded-lg block w-full
            p-4 bg-surface-20 border-surface-30 placeholder-surface-50
            text-white focus:ring-blue-500 focus:border-blue-500
            transition-all hover:bg-surface-30
        """,
    }

    attrs = {
        "cls": f"{cls} {type[itype]}",
    }

    if id:
        attrs["id"] = id
    if name:
        attrs["name"] = name
    if holder:
        attrs["placeholder"] = holder
    if itype:
        attrs["type"] = itype
    
    return Input(
        **attrs,
    )
