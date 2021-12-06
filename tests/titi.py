import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
import mariadb
import os
import requests



def test_controller_service_connection():
    url = 'https://{{ include "katib.controller.fullname" . }}.{{ .Release.Namespace }}.svc:{{ .Values.controller.service.port }}/'
    verify = '/controller-tls-secret/ca.crt'

    response = requests.get(url, verify=verify)

    assert response.status_code == 404


def test_controller_metrics_service_connection():
    url = 'http://{{ include "katib.controller.metrics.fullname" . }}:{{ .Values.controller.metrics.service.port }}/metrics'

    response = requests.get(url)

    assert response.status_code == 200


def test_db_manager_service_connection():
    target = '{{ include "katib.dbManager.fullname" . }}:{{ .Values.dbManager.service.port }}'

    channel = grpc.insecure_channel(target)
    stub = health_pb2_grpc.HealthStub(channel)

    request = health_pb2.HealthCheckRequest()
    response = stub.Check(request)

    assert response.status == health_pb2.HealthCheckResponse.SERVING


def test_ui_service_connection():
    url = 'http://{{ include "katib.ui.fullname" . }}:{{ .Values.ui.service.port }}/katib/'

    response = requests.get(url)

    assert response.status_code == 200


def test_mariadb_service_connection():
    options = {
        'host': '{{ include "katib.mariadb.host" . }}',
        'port': {{ include "katib.mariadb.port" . }},
        'user': '{{ include "katib.mariadb.username" . }}',
        'password': os.environ.get('MARIADB_PASSWORD'),
        'database': '{{ include "katib.mariadb.database" . }}'
    }

    with mariadb.connect(**options) as connection:
        assert connection.warnings == 0
