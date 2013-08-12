"""output in CSV format.

    All rights reserved, see LICENSE for details.
"""

def format(metrics):
    """compute output in CSV format."""
    def report_header(metrics):
        return 'filename,' + ','.join(metrics[metrics.keys()[0]]) + '\n'

    def report_metrics(metrics):
        report = ""
        for metric in metrics.keys():
            report += metric + ','
            report += ','.join([str(m) for m in metrics[metric].values()])
            report += '\n'
        return report

    report = report_header(metrics)
    report += report_metrics(metrics)
    return report
