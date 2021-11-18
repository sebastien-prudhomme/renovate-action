import subprocess

import pytest
import testinfra


@pytest.fixture(scope="session")
def host(request):
    image = "ghcr.io/sebastien-prudhomme/chart-tests:test1"

    docker_id = subprocess.check_output(["docker", f"run -d {image}"]).decode().strip()

    yield testinfra.get_host(f"docker://{docker_id}")

    subprocess.check_call(f"docker rm -f {docker_id}")


def test_pytest(host):
    assert host.check_output("pytest -V") == "pytest"
