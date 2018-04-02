# -*- coding: utf-8 -*-
"""output in CSV format.

    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals


def format(metrics):
    """compute output in CSV format."""
    # filter out positions metric
    def report_header(metrics):
        values = list(metrics.values())[0]
        print(values)
        values.pop('positions', None)
        return 'filename,' + ','.join(values) + '\n'

    def report_metrics(metrics):
        report = ''
        for key, values in metrics.items():
            report += key + ','
            report += ','.join([str(v) for k, v in values.items() if k not in ['positions']])
            report += '\n'
        return report

    report = report_header(metrics)
    report += report_metrics(metrics)
    return report
