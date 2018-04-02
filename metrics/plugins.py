# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import logging

import pkg_resources


log = logging.getLogger(__name__)


def load_plugins(group='metrics.plugin.10'):
    """Load and installed metrics plugins.
    """
    # on using entrypoints:
    # http://stackoverflow.com/questions/774824/explain-python-entry-points
    file_processors = []
    build_processors = []
    for ep in pkg_resources.iter_entry_points(group, name=None):
        log.debug('loading \'%s\'', ep)
        plugin = ep.load()  # load the plugin
        if hasattr(plugin, 'get_file_processors'):
            file_processors.extend(plugin.get_file_processors())
        if hasattr(plugin, 'get_build_processors'):
            build_processors.extend(plugin.get_build_processors())
    return file_processors, build_processors
