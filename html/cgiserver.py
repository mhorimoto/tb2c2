#! /usr/bin/python3
#coding: utf-8
#
#   Version 1.3d
#
import http.server
import socketserver
PORT = 16580
Handler = http.server.CGIHTTPRequestHandler
httpd = http.server.HTTPServer(("", PORT), Handler)
httpd.serve_forever()

