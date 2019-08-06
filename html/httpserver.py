#! /usr/bin/python3
#coding: utf-8
#
#   Version 1.3d
#
import http.server
import socketserver
PORT = 16580
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()

