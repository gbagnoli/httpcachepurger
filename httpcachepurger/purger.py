#!/usr/bin/env python

import logging
import multiprocessing

from httplib import HTTPConnection

__all__ = [ 'HTTPCachePurger'] 

class HTTPCachePurger(object):
    """ A very simple HTTP PURGE client with basic multiprocessing support 

        :param hostname: the hostname used as ``Host`` request header.
        :param server: the address (DNS or IP) of the server to connect to. \
                If ``None``, the ``hostname`` will be resolved and used instead
        :param port: the port of the cache server
        :param strict: if ``True`` causes BadStatusLine to be raised if the status \
                line can't be parsed as a valid HTTP/1.0 or 1.1 status line. \
                See the httplib documentation for more info.
        :param timeout: Connection timeout in seconds.

    """

    def __init__ (self, hostname, server=None, port=80, strict=False, timeout=10):
        """ Create a new VarnishPurgeClient object. """ 
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

            :param urls: an iterable containing all the urls to purge as absolute 
                         paths (i.e. ``/index.html``)
            :param multiprocess: if ``True`` every request will be done concurrently 
                         using the ``multiprocessing`` module
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
