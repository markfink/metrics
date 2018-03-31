# -*- coding: utf-8 -*-
"""output in CSV format.

    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals


def format(metrics):
    """compute output in CSV format."""
    def report_header(metrics):
        values = list(metrics.values())[0]
        return 'filename,' + ','.join(values) + '\n'  # metrics[metrics.keys()[0]]

    def report_metrics(metrics):
        report = ''
        for key, values in metrics.items():  #.keys():
            report += key + ','
            report += ','.join([str(m) for m in values.values()])  #  metrics[metric].values()
            report += '\n'
        return report

    report = report_header(metrics)
    report += report_metrics(metrics)
    return report
