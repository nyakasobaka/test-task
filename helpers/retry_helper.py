from time import sleep

import wrapt


class retry:

    def __init__(self, tries=4, delay=3, exceptions=Exception, action_before_retry=None):
        """
           Retry calling the decorated function
           Args:
               exceptions: The exception to check. may be a tuple of
                   exceptions to check.
               tries: Number of times to try (not retry) before giving up.
               delay: Initial delay between retries in seconds.
               action_before_retry: Lambda function or string which will be executed before each retry
           """
        self.tries = tries
        self.delay = delay
        self.exceptions = exceptions
        self.action_before_retry = action_before_retry

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        delay = self.delay

        for attempt in range(1, self.tries + 1):
            try:
                return wrapped(*args, **kwargs)
            except self.exceptions as error:
                if attempt == self.tries:
                    raise
                sleep(delay)
                if self.action_before_retry:
                    self.action_before_retry()
