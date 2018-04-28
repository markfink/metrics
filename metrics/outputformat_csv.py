# -*- coding: utf-8 -*-
"""output in CSV format.

    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals


def format(file_metrics, build_metrics):
    """Compute output in CSV format (only file_metrics)."""
    # TODO maybe we need different output for build_metrics in csv format, too?
    # filter out positions metric
    def report_header(file_metrics):
        values = list(file_metrics.values())[0]
        print(values)
        values.pop('block_positions', None)
        return 'filename,' + ','.join(values) + '\n'

    def report_metrics(file_metrics):
        report = ''
        for key, values in file_metrics.items():
            report += key + ','
            report += ','.join([str(v) for k, v in values.items() if k not in ['block_positions']])
            report += '\n'
        return report

    report = report_header(file_metrics)
    report += report_metrics(file_metrics)
    return report
