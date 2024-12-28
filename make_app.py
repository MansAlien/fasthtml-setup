from fasthtml.common import Link, fast_app, Style, Script


favicon = Link(rel="icon", href="/static/img/favicon.ico", type="image/x-icon")
font_awesome_css = Link(rel="stylesheet", href="/static/css/all.min.css")
font_awesome_js = Script(src="/static/js/all.min.js")
flowbite = Script(src="/static/js/flowbite.min.js")
hyper = Script(src="/static/js/_hyperscript.min.js")
style=Style(" body {background-color: #121212;} ")
tailwind_css = Link(rel="stylesheet", href="/static/css/output.css", type="text/css"),

app, rt = fast_app(live=True, pico=False, hdrs=(style,tailwind_css, favicon, font_awesome_css, font_awesome_js, flowbite, hyper ))
