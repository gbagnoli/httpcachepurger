.. varnishpurge documentation master file, created by
   sphinx-quickstart on Wed Dec 15 17:55:31 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

VarnishPurge Client
========================================

Contents:

.. toctree::
   :maxdepth: 2

.. py:class:: VarnishPurgeClient(hostname[, server=None[, port=80[, strict=False[, timeout=10]]]])
   
   Create a new client for ``hostname``.

   :param hostname: the hostname used as ``Host`` request header.
   :param server: the address (DNS or IP) of the server to connect to. If ``None``, the ``hostname`` will be resolved and used instead
   :param port: the port of the cache server
   :param strict: if ``True`` causes BadStatusLine to be raised if the status line can't be parsed as a valid HTTP/1.0 or 1.1 status line. See the httplib documentation for more.
   :param timeout: Connection timeout in seconds.

.. py:method:: purge(urls[, multiprocess=True])
   
   Request the server to purge all the given ``urls``

   :param urls: an iterable containing all the urls to purge as absolute paths (i.e. ``/index.html``)
   :param multiprocess: if ``True`` every request will be done concurrently using the ``multiprocessing`` module

.. py:method:: join_all()
   
   Joins all the processess spawned during the purge request.

