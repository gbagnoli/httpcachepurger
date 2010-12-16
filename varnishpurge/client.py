#!/usr/bin/env python

import logging
import multiprocessing

from httplib import HTTPConnection

__all__ = [ 'VarnishPurgeClient'] 

class VarnishPurgeClient(object):
    """ A very simple HTTP PURGE client with basic multiprocessing support """

    def __init__ (self, hostname, server=None, port=80, strict=False, timeout=10):
        """ Create a new VarnishPurgeClient object. 
        hostname - The hostname used as Host: request header.
        server - The address of the server to connect to. If None, the hostname 
        is used instead.
        port - The port to connect to (default 80)
        strict - causes BadStatusLine to be raised if the status line can't be parsed as
        a valid HTTP/1.0 or 1.1 status line. See the httplib documentation for more.
        timeout - Connection timeout in seconds.
        """
        self.log = logging.getLogger(__name__)
        self.hostname = hostname
        self.server = server if server else self.hostname
        self.port = port
        self.strict = strict
        self.timeout = timeout
        self.processes = []

    def __call__(self, url):
        self.log.info("PURGE %s Hostname: %s @%s", url, self.hostname, self.server)
        conn = HTTPConnection(self.server, self.port, self.strict, self.timeout)
        conn.request("PURGE", url, headers={"Host" : self.hostname})
        response = conn.getresponse()
        self.log.debug("'%s': %s %s", url, response.status, response.reason)

    def purge(self, urls, multiprocess=True):
        """ Request the server to purge all the given urls
        urls - an iterable containing all the urls to purge as absolute paths (i.e. /index.html)
        multiprocess - if True every request will be done concurrently using the multiprocessing module
        """

        if isinstance(urls, basestring) or getattr(urls, '__iter__', False):
           urls = tuple(urls)
        
        for url in urls:
            if multiprocess:
                p = multiprocessing.Process(target=self, args=(url,))
                p.start()
                self.processes.append(p)
            else:
                self(url)
    
    def join_all(self):
        """ Joins all the processess spawned during the purge request. """
        self.log.debug("Joining %d processes", len(self.processes))
        for p in self.processes:
            p.join()
        self.processes = []

    def __del__(self):
        self.join_all()
