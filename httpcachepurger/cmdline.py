#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from httpcachepurger import HTTPCachePurger

def get_parser(host, port, strict, timeout):
    """ Setup parser options """
    parser = OptionParser(usage="%prog [-h|--help] [options]")
    parser.add_option('-d', '--hostname', dest='hostname',
                      help='purge cache for host HOST', metavar='HOST',
                      default=host)
    parser.add_option('-s', '--server', dest='server', default=None, 
                      help="connect to SERVER. If not present, HOST will be resolved" + \
                      "and used as server address", metavar="SERVER")
    parser.add_option('-p', '--port', dest='port',
                      help='connect to host port PORT', metavar='PORT',
                      default=port)
    parser.add_option('-t', '--timeout', dest='timeout',
                      help='blocking operations (like connection attempts) ' + \
                           'will timeout after TIMEOUT seconds',
                      metavar='TIMEOUT', default=timeout)
    parser.add_option('-S', '--strict', dest='strict', action='store_true',
                      help='force the connection to be strict: ' + \
                      'BadStatusLine is raised if the status line ' + \
                      'cannot be parsed as a valid HTTP/1.0 or 1.1 ' + \
                      'status line',
                      metavar="STRICT", default=strict)

    return parser

def main():
    """ Main entrance point """
    parser = get_parser(host='localhost', port=80, strict=False, timeout=10)
    (opts, args) = parser.parse_args()
    if not args:
        parser.error("No urls to purge")
    client = HTTPCachePurger(opts.hostname, opts.server, opts.port, 
                             opts.strict, opts.timeout)
    client.purge(args)