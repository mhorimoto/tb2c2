#! /usr/bin/python3
#coding: utf-8
#
#
#
html_body = """
<html><body>
<p>foo = {0}</p>
</body></html>"""

import cgi
form=cgi.FieldStorage()
foo = form.getvalue('foo','N/A')
print("Content-type: text/html\n\n")
print(html_body.format(foo))
