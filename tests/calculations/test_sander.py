""" Tests for sander calculations."""
import os

from aiida.engine import run
from aiida.plugins import CalculationFactory, DataFactory

from .. import TEST_DIR


def run_sander(amber_code):
    """Run an instance of sander and return the results."""

    # profile = load_profile()
    # computer = helpers.get_computer()
    # amber_code = helpers.get_code(entry_point="amber", computer=computer)

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
    mdin = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in")
    )
    prmtop = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", "sander", "parm7")
    )
    inpcrd = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", "sander", "rst7")
    )

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


def test_process(sander_code):
    """Test running a sander calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_sander(sander_code)

    assert "stdout" in result
    assert "mdinfo" in result
    assert "mdout" in result
    assert "restrt" in result


def test_file_name_match(sander_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_sander(sander_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "sander.out"
    assert result["mdinfo"].base.repository.list_object_names()[0] == "01_Min.mdinfo"
    assert result["mdout"].base.repository.list_object_names()[0] == "01_Min.out"
    assert result["restrt"].base.repository.list_object_names()[0] == "01_Min.ncrst"
