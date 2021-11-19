import re
import subprocess

import pytest
import testinfra


@pytest.fixture(scope="session")
def host():
    image = "ghcr.io/sebastien-prudhomme/chart-tests:test1"

    output = subprocess.check_output(["docker", "run", "-d", image, "sleep", "infinity"])
    docker_id = output.decode().rstrip()

    yield testinfra.get_host(f"docker://{docker_id}")

    subprocess.check_call(["docker", "rm", "-f", docker_id])


@pytest.fixture(scope="session")
def packages(host):
    return host.pip.get_packages()


def test_grpcio_package(packages):
    assert "grpcio" in packages


def test_grpcio_health_checking_package(packages):
    assert "grpcio-health-checking" in packages


def test_mariadb_package(packages):
    assert "mariadb" in packages


def test_pytest_package(packages):
    assert "pytest" in packages


def test_pytest_version(host):
    output = host.check_output("pytest -V 2>&1")

    assert re.match(r"^pytest \d+\.\d+\.\d+$", output)


def test_requests_package(packages):
    assert "requests" in packages
