#!/usr/bin/env python

import collections
import logging
import multiprocessing
import socket

from httplib import HTTPConnection

__all__ = [ 'HTTPCachePurger']


FakeResponse = collections.namedtuple('FakeResponse', ['status', 'reason'])


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

    def __request(self, method, queue, url):
        self.log.info("%s %s Hostname: %s @%s", method, url, self.hostname, self.server)
        conn = HTTPConnection(self.server, self.port, self.strict, self.timeout)
        try:
            conn.request(method, url, headers={"Host" : self.hostname})
            response = conn.getresponse()

        except socket.error as e:
            response = FakeResponse(status=0, reason=str(e))

        self.log.debug("'%s': %s %s", url, response.status, response.reason)
        queue.put((url, response.status, response.reason))

    def execute(self, method, urls, multiprocess=False):
        """ Request the server to purge all the given urls

            :param method: Http method to use. (PURGE or BAN)
            :param urls: an iterable containing all the urls to purge as absolute \
                         paths (i.e. ``/index.html``)
            :param multiprocess: if true every request will be done concurrently \
                         using the ``multiprocessing`` module
            :type processes: boolean
        """
        method = method.upper()
        if method not in ("PURGE", "BAN"):
            raise ValueError("Invalid method %s", method)

        self.log.debug("Starting %s of urls %s , multiprocessing: %s", method, urls, multiprocess)
        if isinstance(urls, basestring) or getattr(urls, '__iter__', False):
           urls = tuple(urls)

        queue = multiprocessing.Queue()
        if multiprocess:

            processes = [multiprocessing.Process(target=self.__request, args=(method, queue, url)) for url in urls]
            for p in processes:
                p.start()

            results = [queue.get() for u in urls]

            for p in processes:
                p.join()

            return results

        results = []
        for url in urls:
            self.__request(method, queue, url)
            results.append(queue.get())

        return results

    def purge(self, urls, multiprocess=False):
        return self.execute("PURGE", urls, multiprocess)

    def ban(self, urls, multiprocess=False):
        return self.execute("BAN", urls, multiprocess)
