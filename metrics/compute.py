"""Main computational modules for metrics."""

class ComputeMetrics(object):
    """Class used to compute basic metrics for given file."""

    def __init__(self, metric_instance, context):
        """Initialize general computational object."""
        self.metric_instance = metric_instance
        self.context = context
        self.token = None
        self.process_token_subscribers = []
        self.metrics = {}
        self.__init_metrics(metric_instance)

    def __extract_fqn(self, fqn, default='__main__'):
        """Extract fully qualified name from list."""
        result = default
        if len(fqn):
            result = fqn[-1][0]
        return result

    def process_token(self, token):
        """Handle processing after each token processed."""
        self.token = token
        for subscriber in self.process_token_subscribers:
            subscriber.process_token(self.token)

    def __call__(self, token_list):
        """This function is the start of the heavy lifting
        for computing the various metrics produced by PyMetrics.

        """
        for tok in token_list:
            token_count = self.process_token(tok)

        # collect metrics from all members of metrics_instance
        for i in self.metric_instance:
            self.metrics.update(self.metric_instance[i].metrics)
        return self.metrics

    def get_metrics(self):
        """This function return the current state of all metric instances
        parsing.
        """
        return [(m.name, m.get_metrics())
                for m in self.metric_instance.values()]

    def reset(self):
        """reset all metric counters."""
        for i in self.metric_instance:
            self.metric_instance[i].reset()

    def __init_metrics(self, metric_instance):
        """Initialize all the local variables that will be
        needed for analysing tokens.:

        """
        metric_list = []
        for m in metric_instance.keys():
            if metric_instance[m]:       # only append valid instances
                metric_list.append(metric_instance[m])
        # clear out any old data while leaving reference to same
        # thing (ie., pointers to these lists are always valid
        del self.process_token_subscribers[:]
        self.process_token_subscribers.extend(metric_list)

        return metric_list
