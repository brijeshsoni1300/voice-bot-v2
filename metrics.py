import time

class MetricsLogger:
    def __init__(self):
        # Store metrics in a dictionary.
        # Each metric can either be a dict with "start", "end", and "duration" keys,
        # or a single timestamp from a mark event.
        self.metrics = {}

    def start(self, metric_name: str):
        """Start tracking a metric by recording the current monotonic time."""
        self.metrics[metric_name] = {"start": time.monotonic()}

    def mark(self, metric_name: str):
        """
        Record a one-off event timestamp.
        For example, you might mark when the first token is received.
        """
        self.metrics[metric_name] = time.monotonic()

    def stop(self, metric_name: str):
        """Stop tracking a metric and calculate its duration."""
        metric = self.metrics.get(metric_name)
        if metric and isinstance(metric, dict) and "start" in metric:
            end_time = time.monotonic()
            duration = end_time - metric["start"]
            self.metrics[metric_name]["end"] = end_time
            self.metrics[metric_name]["duration"] = duration
        else:
            print(f"[MetricsLogger] Warning: Metric '{metric_name}' was not started properly.")

    def log(self, metric_name: str, value):
        """Directly log a value for a given metric."""
        self.metrics[metric_name] = value

    def get(self, metric_name: str):
        """Retrieve the recorded data for a specific metric."""
        return self.metrics.get(metric_name, None)

    def report(self):
        """Prints a summary report of all tracked metrics."""
        print("==== Performance Metrics Report ====")
        for name, data in self.metrics.items():
            if isinstance(data, dict) and "duration" in data:
                print(f"{name}: {data['duration']:.3f} seconds")
            else:
                # For mark events or logged values
                print(f"{name}: {data}")
        print("======================================")

    def report_metric(self, metric_name: str) -> str:
        """Return a formatted string for a specific metric."""
        data = self.get(metric_name)
        if data is None:
            print(f"Metric '{metric_name}' not found.")
        if isinstance(data, dict) and "duration" in data:
            print(f"{metric_name}: {data['duration']:.3f} seconds")
        else:
            print(f"{metric_name}: {data}")

# Create a singleton instance for use across the project.
logger = MetricsLogger()

# Example usage:
if __name__ == "__main__":
    logger.start("LLM_Response_Time")
    # Simulate waiting for first token
    time.sleep(0.3)
    logger.mark("LLM_First_Token")
    # Simulate remaining processing time
    time.sleep(0.2)
    logger.stop("LLM_Response_Time")
    logger.report()
