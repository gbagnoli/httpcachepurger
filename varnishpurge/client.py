#!/usr/bin/env python

import logging
import multiprocessing

from httplib import HTTPConnection

__all__ = [ 'VarnishPurgeClient'] 

class VarnishPurgeClient(object):

    def __init__ (self, hostname, server=None, port=80, strict=False, timeout=10):
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
        self.log.debug("Joining %d processes", len(self.processes))
        for p in self.processes:
            p.join()
        self.processes = []

    def __del__(self):
        self.join_all()
