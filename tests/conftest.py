import subprocess

import pytest
import testinfra

def pytest_addoption(parser):
    parser.addoption("--image", action = "store")

@pytest.fixture(scope="session")
def image(request):
    return request.config.getoption("--image")

@pytest.fixture(scope="session")
def host(image):
    command_run = ["docker", "run", "-d", image, "sleep", "infinity"]

    output = subprocess.check_output(command_run)
    docker_id = output.decode().rstrip()

    yield testinfra.get_host(f"docker://{docker_id}")

    command_rm = ["docker", "rm", "-f", docker_id]
    subprocess.check_call(command_rm)

@pytest.fixture(scope="session")
def packages(host):
    return host.pip.get_packages()
