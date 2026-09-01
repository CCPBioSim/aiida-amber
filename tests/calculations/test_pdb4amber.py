""" Tests for pdb4amber calculations."""
import os

from aiida.engine import run
from aiida.orm import SinglefileData, List
from aiida.plugins import CalculationFactory, DataFactory

from .. import TEST_DIR


def run_pdb4amber(pdb4amber_code):
    """Run an instance of pdb4amber and return the results."""

    # Prepare input parameters
    Pdb4amberParameters = DataFactory("amber.pdb4amber")
    parameters = Pdb4amberParameters(
        {
            "out": "test.pdb",
            "logfile": "test.log",
            "dry": True,
            "reduce": True,
            "leap-template": True,
            
        }
    )

    inp = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files/pdb4amber", "Protein.pdb")
    )

    # create list of expected output files
    prefix = "test"
    output_filenames = [f"{prefix}.pdb", f"{prefix}.log", f"{prefix}_water.pdb",
                        f"{prefix}_sslink", "leap.template.in",
                        f"{prefix}_nonprot.pdb", f"{prefix}_renum.txt"]

    # set up calculation
    inputs = {
        "code": pdb4amber_code,
        "parameters": parameters,
        "input_file": inp,
        "pdb4amber_outfiles": List(output_filenames),
        "metadata": {
            "description": "pdb4amber test",
        },
    }

    result = run(CalculationFactory("amber.pdb4amber"), **inputs)

    return result


def test_process(pdb4amber_code):
    """Test running a pdb4amber calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_pdb4amber(pdb4amber_code)

    assert "stdout" in result
    assert "test_pdb" in result
    assert "test_sslink" in result
    assert "test_nonprot_pdb" in result
    assert "test_renum_txt" in result
    assert "test_water_pdb" in result
    assert "leap_template_in" in result


def test_file_name_match(pdb4amber_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_pdb4amber(pdb4amber_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "pdb4amber.out"
    assert result["test_pdb"].base.repository.list_object_names()[0] == "test.pdb"
    assert result["test_sslink"].base.repository.list_object_names()[0] == "test_sslink"
    assert result["test_nonprot_pdb"].base.repository.list_object_names()[0] == "test_nonprot.pdb"
    assert result["test_renum_txt"].base.repository.list_object_names()[0] == "test_renum.txt"
    assert result["test_water_pdb"].base.repository.list_object_names()[0] == "test_water.pdb"
    assert result["leap_template_in"].base.repository.list_object_names()[0] == "leap.template.in"
