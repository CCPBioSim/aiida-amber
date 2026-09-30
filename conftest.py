"""pytest fixtures for simplified testing."""

import pytest
import os
import shutil

pytest_plugins = "aiida.tools.pytest_fixtures"


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(aiida_profile_clean):
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def sander_code(aiida_code, aiida_localhost):
    """Get sander code."""
    sander_path = shutil.which("sander")
    amberhome = os.path.dirname(os.path.dirname(sander_path))
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable=sander_path,
        prepend_text=f"export AMBERHOME={amberhome}",
    )


@pytest.fixture(scope="function")
def tleap_code(aiida_code, aiida_localhost):
    """Get tleap code."""
    tleap_path = shutil.which("tleap")
    amberhome = os.path.dirname(os.path.dirname(tleap_path))
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable=tleap_path,
        prepend_text=f"export AMBERHOME={amberhome}",
    )


@pytest.fixture(scope="function")
def antechamber_code(aiida_code, aiida_localhost):
    """Get antechamber code."""
    antechamber_path = shutil.which("antechamber")
    amberhome = os.path.dirname(os.path.dirname(antechamber_path))
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable=antechamber_path,
        prepend_text=f"export AMBERHOME={amberhome}",
    )


@pytest.fixture(scope="function")
def pdb4amber_code(aiida_code, aiida_localhost):
    """Get pdb4amber code."""
    pdb4amber_path = shutil.which("pdb4amber")
    amberhome = os.path.dirname(os.path.dirname(pdb4amber_path))
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable=pdb4amber_path,
        prepend_text=f"export AMBERHOME={amberhome}",
    )


@pytest.fixture(scope="function")
def parmed_code(aiida_code, aiida_localhost):
    """Get parmed code."""
    parmed_path = shutil.which("parmed")
    amberhome = os.path.dirname(os.path.dirname(parmed_path))
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable=parmed_path,
        prepend_text=f"export AMBERHOME={amberhome}",
    )


@pytest.fixture(scope="function")
def bash_code(aiida_code, aiida_localhost):
    """Get bash code."""
    return aiida_code(
        "core.code.installed",
        label="amber",
        computer=aiida_localhost,
        filepath_executable="bash",
    )
