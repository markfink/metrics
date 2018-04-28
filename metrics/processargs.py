# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Process command line arguments."""

import sys
from optparse import OptionParser, BadOptionError

from . import __version__

usage_str = """python metrics [ options ] pgm1.ex1 [ pgm2.ex2 ... ]

Metrics are computed for the source code files
pgm1.ex1, pgm2.ex2, etc. At least one file name is required,
else this message appears.

Three types of output can be produced:

* Standard output for a quick summary of the main metrics.

Capitalized options negate the default option.
"""


class MyOptionParser(OptionParser):
    """Subclass OptionParser so I can override default error handler."""

    def __init__( self, *args, **kwds ):
        """Just call super class's __init__ since we aren't making changes here."""
        OptionParser.__init__( self, *args, **kwds )

    def error(self, msg):
        """Explicitly raise BadOptionError so calling program can handle it."""
        raise BadOptionError(msg)


class ProcessArgsError(Exception): pass


class ProcessArgs( object ):
    """Process command line arguments."""
    def __init__(self, *pArgs, **pKwds):
        """Initial processing of arguments."""

        # default values for possible parameters
        lib_name = ''
        in_file_list = None
        include_metrics_str = 'sloc:SLOCMetric,mccabe:McCabeMetric'
        exclude_metrics_str = None
        quiet = False
        verbose = 0
        output_format = None

        self.__dict__.update( locals() )
        del( self.__dict__['self'] )  # remove recursive self from self.__dict__
        self.__dict__.update( pKwds )
        del( self.__dict__['pKwds'] ) # remove redundant pKwds in self.__dict__

        # set up option parser
        parser = MyOptionParser('', version="%prog " + __version__)

        parser.add_option("-f", "--files",
                          dest="in_file_list",
                          default=self.in_file_list,
                          help="File containing list of path names to modules for analysis." )
        parser.add_option("-q", "--quiet",
                          action="store_true",
                          dest="quiet",
                          default=self.quiet,
                          help="suppress normal summary output to stdout. (Default is %s)" % (self.quiet) )
        parser.add_option("--format",
                          dest="output_format_str",
                          default = self.output_format,
                          choices = ["xml", "csv", "json"],
                          help="Choose an output format for a parser to read. Valid choices: xml, csv, json")

        # parse the command line/arguments for this instance
        try:
            (options, args) = parser.parse_args()
        except BadOptionError as e:
            sys.stderr.writelines("\nBadOptionError: %s\n" % str( e ))
            sys.stderr.writelines("\nThe valid options are:\n\n")
            sys.stderr.writelines(parser.format_help())
            sys.exit(1)

        args.extend(pArgs)

        # convert command line arguments into instance values
        self.__dict__.update( options.__dict__)

        if self.in_file_list:
            try:
                inf = open(self.in_file_list)
                files = [line.strip() for line in inf]
                inf.close()
                args.extend( files )
            except IOError as e:
                raise ProcessArgsError( e )

        self.in_file_names = args

        self.include_metrics = self.process_include_metrics(self.include_metrics_str)

        # standardize
        if self.output_format_str is not None:
            self.output_format_str = self.output_format_str.upper()

        if len( args ) < 1:
            print(usage_str)
            print(parser.format_help())
            e = "No souce filenames given.\n"
            # because of what I believe to be a bug in the doctest module,
            # which makes it mishandle exceptions, I have 'faked' the handling
            # of raising an exception and just return
#            if doctestSw:
#              print e
#              return
#            else:
            raise ProcessArgsError(e)

    def conflict_handler(self, *args, **kwds):
        print("args=%s" % args)
        print("kwds=%s" % kwds)

    def process_include_metrics(self, include_metrics_str):
        include_metrics = []
        try:
            metric_list = include_metrics_str.split(',')
            for a in metric_list:
                s = a.split( ':' )
                if len( s ) == 2:    # both metric class and module name given
                    include_metrics.append( s )
                elif len( s ) == 1:
                    # only the module name given. Generate default metric
                    # class name by capitalizing first letter of module
                    # name and appending "Metric" so the default metric
                    # class name for module wxYz is WxYzMetric.
                    if s[0]:
                        defName = s[0][0].upper() + s[0][1:] + 'Metric'
                        include_metrics.append((s[0], defName))
                    else:
                        raise ProcessArgsError("Missing metric module name")
                else:
                    raise ProcessArgsError("Malformed items in includeMetric string")
        except AttributeError as e:
            e = ("Invalid list of metric names: %s" %
                include_metrics_str )
            raise ProcessArgsError( e )
        return include_metrics


def testpa(pa):
    """Test of ProcessArgs.

    Usage:

    >>> pa=ProcessArgs('inFile.py')
    >>> testpa(pa)  #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    Arguments processed:
      Include Metric Modules=sloc:SLOCMetric,mccabe:McCabeMetric
      quiet=False
      verbose=0
    Metrics to be used are:
      Module sloc contains metric class SLOCMetric
      Module mccabe contains metric class McCabeMetric
    Input files:
      inFile.py
    >>>
    """
    print("""Arguments processed:
\tInclude Metric Modules=%s
\tquiet=%s
\tverbose=%s""" % (
        pa.include_metrics_str,
        pa.quiet,
        pa.verbose))
    print("Metrics to be used are:")
    for m,n in pa.include_metrics:
        print("\tModule %s contains metric class %s" % (m,n))
    if pa.in_file_names:
        print("Input files:")
        for f in pa.in_file_names:
            print("\t%s" % f)
