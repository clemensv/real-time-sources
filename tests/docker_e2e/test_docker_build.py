"""Docker build and import tests for all containerized projects.

These tests verify that:
1. Each project's Dockerfile builds successfully.
2. The main Python module can be imported inside the container (all
   dependencies are installed correctly).

Tests are parameterized by project configuration.  Each project entry
specifies the directory, the Python module to import, and any extra
build arguments.

Run with:  pytest tests/docker_e2e/test_docker_build.py -v --timeout=600
"""

import docker
import pytest
import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from helpers import build_image

# (project_dir, import_module, dockerfile)
PROJECTS = [
    ('bluesky', 'bluesky', 'Dockerfile'),
    ('chmi-hydro', 'chmi_hydro', 'Dockerfile'),
    ('gtfs', 'gtfs_rt_bridge', 'Dockerfile'),
    ('hubeau-hydrometrie', 'hubeau_hydrometrie', 'Dockerfile'),
    ('imgw-hydro', 'imgw_hydro', 'Dockerfile'),
    ('mode-s', 'mode_s_kafka_bridge', 'Dockerfile'),
    ('noaa', 'noaa', 'Dockerfile'),
    ('noaa-goes', 'noaa_goes', 'Dockerfile'),
    ('noaa-ndbc', 'noaa_ndbc', 'Dockerfile'),
    ('noaa-nws', 'noaa_nws', 'Dockerfile'),
    ('pegelonline', 'pegelonline', 'Dockerfile'),
    ('rss', 'rssbridge', 'Dockerfile'),
    ('rws-waterwebservices', 'rws_waterwebservices', 'Dockerfile'),
    ('smhi-hydro', 'smhi_hydro', 'Dockerfile'),
    ('uk-ea-flood-monitoring', 'uk_ea_flood_monitoring', 'Dockerfile'),
    ('usgs-earthquakes', 'usgs_earthquakes', 'Dockerfile'),
    ('usgs-iv', 'usgs_iv', 'Dockerfile'),
    ('waterinfo-vmm', 'waterinfo_vmm', 'Dockerfile'),
]


@pytest.fixture(scope='module', params=PROJECTS, ids=[p[0] for p in PROJECTS])
def project_image(request):
    """Build Docker image for each project (cached per module)."""
    project_dir, _module, dockerfile = request.param
    image = build_image(project_dir, dockerfile=dockerfile)
    return request.param, image


class TestDockerBuild:
    """Verify every Dockerfile builds and the main module imports."""

    def test_image_builds(self, project_image):
        """The Docker image builds without errors."""
        (_project_dir, _module, _dockerfile), image = project_image
        assert image is not None
        assert image.id is not None

    def test_module_imports(self, project_image):
        """The main Python module can be imported inside the container."""
        (project_dir, module, _dockerfile), image = project_image
        client = docker.from_env()
        cmd = f'python -c "import {module}; print(\'OK\')"'
        result = client.containers.run(image.id, command=cmd, remove=True)
        output = result.decode('utf-8', errors='replace')
        assert 'OK' in output, f'{project_dir}: import {module} failed:\n{output}'
