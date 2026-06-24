def load_css():

    with open(
        "assets/style.css",
        encoding="utf-8"
    ) as f:

        css = f.read()

    return f"""
    <style>
    {css}
    </style>
    """
