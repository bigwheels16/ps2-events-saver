import config
import time

#from google.api import label_pb2 as ga_label
#from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3


# https://cloud.google.com/monitoring/docs/samples/monitoring-create-metric#monitoring_create_metric-python
# https://cloud.google.com/monitoring/api/v3/kinds-and-types
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/jkbff2"
#descriptor = ga_metric.MetricDescriptor()
#descriptor.type = "custom.googleapis.com/test/num_messages_received"
#descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.CUMULATIVE
#descriptor.value_type = ga_metric.MetricDescriptor.ValueType.INT64
#descriptor.description = "This is a simple example of a custom metric."

#labels = ga_label.LabelDescriptor()
#labels.key = "TestLabel"
#labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
#labels.description = "This is a test label for my medium blog"
#descriptor.labels.append(labels)

#descriptor = client.create_metric_descriptor(
#    name=project_name, metric_descriptor=descriptor
#)

def create_time_series(name):
    # https://cloud.google.com/monitoring/custom-metrics/creating-metrics#writing-ts
    series = monitoring_v3.TimeSeries()
    series.metric.type = f"custom.googleapis.com/ps2-events-saver/{name}"

    # https://cloud.google.com/monitoring/api/resources#tag_gke_container
    series.resource.type = "gke_container"
    series.resource.labels["zone"] = "us-west1-b"
    series.resource.labels["instance_id"] = "TODO"
    series.resource.labels["cluster_name"] = "cluster-2"
    series.resource.labels["namespace_id"] = "TODO"
    series.resource.labels["pod_id"] = "TODO"
    series.resource.labels["container_name"] = "TODO"

    series.metric.labels["application"] = "ps2-events-saver"
    series.metric.labels["instance"] = config.DB_USERNAME()

    return series

def publish_time_series(series, value):
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point({"interval": interval, "value": {"int64_value": value}})
    series.points = [point]
    client.create_time_series(name=project_name, time_series=[series])
