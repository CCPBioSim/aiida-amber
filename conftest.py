"""pytest fixtures for simplified testing."""
import pytest

pytest_plugins = "aiida.tools.pytest_fixtures"


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get sander code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="sander",
    )


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get tleap code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="tleap",
    )


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get antechamber code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="antechamber",
    )


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get pdb4amber code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="pdb4amber",
    )


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get parmed code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="parmed",
    )


@pytest.fixture(scope="function")
def gromacs_code(aiida_code, aiida_localhost):
    """Get bash code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="bash",
    )
