import pytest
import subprocess
import testinfra

@pytest.fixture(scope='session')
def host(request):
    docker_id = subprocess.check_output(['docker', 'run', '-d', 'ghcr.io/sebastien-prudhomme/chart-tests:test1']).decode().strip()

    yield testinfra.get_host("docker://" + docker_id)

    subprocess.check_call(['docker', 'rm', '-f', docker_id])

def test_pytest(host):
    assert host.check_output(['pytest', '-V']) == 'pytest 6.2.5'
