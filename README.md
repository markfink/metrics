The metrics software package was born in 2010 out of my frustration about available Open Source metrics packages. There are plenty of them so it is not a problem to find one. But each and every of them has a different focus. Most metrics packages have restrictions towards available metrics and supported languages. Some prominent samples are (CCCC, SLOCCount, PyMetrics, Eclipse-Metrics, Ohcount).

My problem with all of these metrics packages is that I am going to analyse huge source repositories like the Firefox code base, the Apache code base, or the CPython code base. Those big guys usually are made out of multiple programming languages. C, C++, Java, JavaScript, Python to name a few. Because of the limited scope of the metrics packages I tried to combine the output of multiple packages. But there are more problems. Each package has a different output format (no problem for me since I am capable of Monkey-Patching, Screen-Reading, XML-Mangling, and CSV-Magic). The real problem with the metrics output of different packages is that they are also incompatible! Who could imagine something like that, every metrics package has its own philosophy what a "Line of Code" might be. Honestly if you ask a few language lawyers what a line of code might be you get at least a few different answers. So lets create another metrics package that creates metrics consistently for different languages! Yeah!!

Besides its little shortcomings I like PyMetrics a lot. PyMetrics was designed in a way to easily extend it with lexers for programming languages other than Python and custom metrics. PyMetrics contains stuff that is already handled by Pylint and which does not apply to other programming languages which I will remove. At this stage I will focus only on SLOC and McCabe metrics and keep its extensibility. Target languages are C, C++, JavaScript, and Python. PyMetrics is missing testcases and I want to handle this problem as well.

One more thing on metrics. Compared to PyMetrics I changed the SLOC metric a lot. PyMetrics was criticised in the past for its SLOC metric. I simplified to something that I understand as the common denominator for the metric packages mentioned above. This metric counts the lines but excludes empty lines and comments. This is sometimes referred to as the *source lines of code* (SLOC). In literature this is often also referred as physical lines of code.

Another thing I wanted to mention is that I borrowed the sample programming language files for the test cases from Ohcount and Firefox.

I currently have spent about two weeks working on the metrics package and I already tested it a lot. I compared the metrics results against results extracted from other metrics packages, against values I counted manually, and results from a commercial package (I Understand that I can not revile its name here because its results have been very inaccurate). From the comparison I have the impression that the results of the metrics package are pretty accurate. Nevertheless I will keep the package in alpha state so nobody will jump on it blindly. Please provide feedback if it worked for you. If something does not work as you expected please let me know. In this case it would be brilliant if you could provide a free code sample and the appropriate values in order to reproduce the problem. Please get in touch if you feel that some important feature/metric is missing, too.

For more information on Tools and the Hitchhikers Guide to Test Automation please visit:
http://www.testing-software.org/

Extended 11th Aug 2014 Steve Barnes <gadgetsteve@hotmail.com>

 - Added -r option to recurse directories.
 - Verbose mode now outputs the file being processed.
