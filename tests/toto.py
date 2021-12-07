import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
import mariadb
import os
import requests


def test_controller_service_connection():
    url = "https://katib-controller.katib.svc:8443/"
    verify = "/controller-tls-secret/ca.crt"

    response = requests.get(url, verify=verify)

    assert response.status_code == 404


def test_controller_metrics_service_connection():
    url = "http://katib-controller-metrics:8080/metrics"

    response = requests.get(url)

    assert response.status_code == 200


def test_db_manager_service_connection():
    target = "katib-db-manager:6789"

    channel = grpc.insecure_channel(target)
    stub = health_pb2_grpc.HealthStub(channel)

    request = health_pb2.HealthCheckRequest()
    response = stub.Check(request)

    assert response.status == health_pb2.HealthCheckResponse.SERVING


def test_ui_service_connection():
    url = "http://katib-ui:8080/katib/"

    response = requests.get(url)

    assert response.status_code == 200


def test_mariadb_service_connection():
    options = {
        "host": "katib-mariadb",
        "port": 3306,
        "user": "katib",
        "password": os.environ.get("MARIADB_PASSWORD"),
        "database": "katib"
    }

    with mariadb.connect(**options) as connection:
        assert connection.warnings == 0
