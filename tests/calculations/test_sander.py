"""Tests for sander calculations."""

import os

from aiida.engine import run
from aiida.orm import Dict
from aiida.plugins import CalculationFactory, DataFactory

from .. import TEST_DIR


def run_sander_min(amber_code):
    """Run an instance of sander minimisation and return the results."""

    # Prepare input parameters
    SanderParameters = DataFactory("amber.sander")
    parameters = SanderParameters(
        {
            "o": "01_Min.out",
            "r": "01_Min.ncrst",
            "inf": "01_Min.mdinfo",
        }
    )

    SinglefileData = DataFactory("core.singlefile")
    mdin = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in"))
    prmtop = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "top.parm7"))
    inpcrd = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7"))

    # set up calculation
    inputs = {
        "code": amber_code,
        "parameters": parameters,
        "mdin": mdin,
        "prmtop": prmtop,
        "inpcrd": inpcrd,
        "metadata": {
            "description": "sander test",
        },
    }

    result = run(CalculationFactory("amber.sander"), **inputs)

    return result


def run_sander_md(amber_code):
    """Run an instance of sander MD and return the results."""

    # Prepare input parameters
    SanderParameters = DataFactory("amber.sander")
    parameters = SanderParameters(
        {
            "o": "02_md.out",
            "r": "02_md_out.ncrst",
            "inf": "02_md.mdinfo",
            "x": "02_md.nc",
        }
    )

    SinglefileData = DataFactory("core.singlefile")
    mdin = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "02_md.in"))
    prmtop = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "top.parm7"))
    inpcrd = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7"))

    # set up calculation
    inputs = {
        "code": amber_code,
        "parameters": parameters,
        "mdin": mdin,
        "prmtop": prmtop,
        "inpcrd": inpcrd,
        "metadata": {
            "description": "sander test",
        },
    }

    result = run(CalculationFactory("amber.sander"), **inputs)

    return result


def test_process_min(sander_code):
    """Test running a sander minimisation calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_sander_min(sander_code)

    assert "stdout" in result
    assert "mdinfo" in result
    assert "mdout" in result
    assert "restrt" in result


def test_file_name_match_min(sander_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_sander_min(sander_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "sander.out"
    assert result["mdinfo"].base.repository.list_object_names()[0] == "01_Min.mdinfo"
    assert result["mdout"].base.repository.list_object_names()[0] == "01_Min.out"
    assert result["restrt"].base.repository.list_object_names()[0] == "01_Min.ncrst"


def test_process_md(sander_code):
    """Test running a sander MD calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_sander_md(sander_code)

    assert "stdout" in result
    assert "mdinfo" in result
    assert "mdout" in result
    assert "restrt" in result
    assert "mdcrd" in result
    assert "simulation_metadata" in result


def test_file_name_match_md(sander_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_sander_md(sander_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "sander.out"
    assert result["mdinfo"].base.repository.list_object_names()[0] == "02_md.mdinfo"
    assert result["mdout"].base.repository.list_object_names()[0] == "02_md.out"
    assert result["restrt"].base.repository.list_object_names()[0] == "02_md_out.ncrst"
    assert result["mdcrd"].base.repository.list_object_names()[0] == "02_md.nc"
    assert isinstance(result["simulation_metadata"], Dict)
