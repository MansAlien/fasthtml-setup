from fasthtml.common import A


def icon_link(type="edit", get=None, target=None, delete=None, href="#", swap=None, **extra):
    """
    Creates a link component with predefined icon styles.
    
    Args:
        type (str): Type of icon link ("edit" or "delete")
        get (str): Value for hx-get attribute
        target (str): Value for hx-target attribute
        delete (str): Value for hx-delete attribute
        href (str): Link href attribute
        swap (str): Value for hx-swap attribute
        **extra: Additional attributes to be passed to the A component
    
    Returns:
        A: Fasthtml A component with configured attributes
    """
    types = {
        "edit": {
            "cls": "text-blue-400 hover:text-blue-300 text-xl transition-colors px-2",
            "icon": "✎",
        },
        "delete": {
            "cls": "text-red-400 hover:text-red-300 text-xl font-bold transition-colors px-2",
            "icon": "×",
        },
    }
    
    if type not in types:
        raise ValueError(f"Invalid icon type. Must be one of: {', '.join(types.keys())}")
    
    attrs = {
        "cls": types[type]["cls"],
        "href": href,
        **extra
    }
    
    if get:
        attrs["hx_get"] = get
    if target:
        attrs["hx_target"] = target
    if delete:
        attrs["hx_delete"] = delete
    if swap:
        attrs["hx_swap"] = swap
    
    return A(
        types[type]["icon"],
        **attrs,
    )
