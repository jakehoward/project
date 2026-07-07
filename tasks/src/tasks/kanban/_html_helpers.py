from textwrap import dedent


def build_html(body: str):
    return bytes(
        dedent(f"""\
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
            </head>
            <body>
              {body}
            </body>
        </html>
    """),
        encoding="utf-8",
    )
