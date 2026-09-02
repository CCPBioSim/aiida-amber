#!/usr/bin/env python
"""Command line utility to run amber sander command with AiiDA.

Usage: aiida_sander --help
"""

import os

import click
from aiida import cmdline, engine
from aiida.plugins import CalculationFactory, DataFactory

from aiida_amber import helpers

# from aiida_amber.utils import searchprevious


def launch(params):
    """Run sander.

    Uses helpers to add amber on localhost to AiiDA on the fly.
    """

    # Prune unused CLI parameters from dict.
    params = {k: v for k, v in params.items() if v is not None}

    print(params)

    # dict to hold our calculation data.
    inputs = {
        "metadata": {
            "description": params.pop("description"),
        },
    }

    # If code is not initialised, then setup.
    if "code" in inputs:
        inputs["code"] = params.pop("code")
    else:
        computer = helpers.get_computer()
        inputs["code"] = helpers.get_code(entry_point="amber", computer=computer)

    # Prepare input parameters in AiiDA formats.
    SinglefileData = DataFactory("core.singlefile")
    inputs["mdin"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("i")))
    inputs["prmtop"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("p")))
    inputs["inpcrd"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("c")))

    if "ref" in params:
        inputs["refc"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("ref")))
    if "mtmd" in params:
        inputs["mtmd"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("mtmd")))
    if "y" in params:
        inputs["inptraj"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("y")))
    if "idip" in params:
        inputs["inpdip"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("idip")))
    if "cpin" in params:
        inputs["cpin"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("cpin")))
    if "cein" in params:
        inputs["cein"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("cein")))
    if "evbin" in params:
        inputs["evbin"] = SinglefileData(file=os.path.join(os.getcwd(), params.pop("evbin")))

    SanderParameters = DataFactory("amber.sander")
    inputs["parameters"] = SanderParameters(params)

    # check if inputs are outputs from prev processes
    # inputs = searchprevious.get_prev_inputs(inputs, ["tprfile"])

    # check if a pytest test is running, if so run rather than submit aiida job
    # Note: in order to submit your calculation to the aiida daemon, do:
    if "PYTEST_CURRENT_TEST" in os.environ:
        engine.run(CalculationFactory("amber.sander"), **inputs)
    else:
        engine.submit(CalculationFactory("amber.sander"), **inputs)


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
# Plugin options
@click.option(
    "--description",
    default="record sander data provenance via the aiida_amber plugin",
    type=str,
    help="Short metadata description",
)
# Input file options
@click.option("-i", default="mdin", type=str, help="input control data for the min/md run")
@click.option(
    "-p",
    default="prmtop",
    type=str,
    help="input molecular topology, force field, periodic box type, atom and residue names",
)
@click.option(
    "-c",
    default="inpcrd",
    type=str,
    help="input initial coordinates and (optionally) velocities and periodic box size",
)
@click.option(
    "-ref",
    type=str,
    help="input (optional) reference coords for position restraints; also used for targeted MD",
)
@click.option(
    "-mtmd",
    type=str,
    help="input (optional) containing list of files and parameters for targeted MD to multiple targets",
)
@click.option(
    "-y",
    type=str,
    help="input coordinate sets in trajectory format, when imin=5 or 6",
)
@click.option("-idip", type=str, help="input polarizable dipole file, when indmeth=3")
@click.option("-cpin", type=str, help="input protonation state definitions")
@click.option("-cein", type=str, help="input redox state definitions")
@click.option("-evbin", type=str, help="input for EVB potentials")
# Output file options
@click.option(
    "-o",
    default="mdout",
    type=str,
    help="output user readable state info and diagnostics -o stdout will send "
    "output to stdout (to the terminal) instead of to a file",
)
@click.option("-inf", default="mdinfo", type=str, help="output latest mdout-format energy info")
@click.option("-x", type=str, help="output coordinate sets saved over trajectory")
@click.option("-v", type=str, help="output velocity sets saved over trajectory")
@click.option("-frc", type=str, help="output force sets saved over trajectory")
@click.option(
    "-e",
    type=str,
    help="output extensive energy data over trajectory (not synchronized with mdcrd or mdvel)",
)
@click.option(
    "-r",
    type=str,
    help="output final coordinates, velocity, and box dimensions if any - for restarting run",
)
@click.option("-rdip", type=str, help="output polarizable dipole file, when indmeth=3")
@click.option("-cpout", type=str, help="output protonation state data saved over trajectory")
@click.option(
    "-cprestrt",
    type=str,
    help="protonation state definitions, final protonation states for restart (same format as cpin)",
)
@click.option(
    "-cerestrt",
    type=str,
    help="redox state definitions, final redox states for restart (same format as cein)",
)
@click.option("-ceout", type=str, help="output redox state data saved over trajectory")
@click.option(
    "-suffix",
    type=str,
    help="output this string will be added to all unspecified output files "
    "that are printed (for multisander runs, it will append this suffix to all "
    "output files)",
)
# Other parameters
@click.option("-O", help="Overwrite output files if they exist")
@click.option("-A", help="Append output files if they exist (used mainly for replica exchange)")
def cli(*args, **kwargs):
    """Run example.

    Example usage:

    $ aiida_sander --code amber@localhost -i input_files/01_Min.in -o 01_Min.out \
        -p parm7 -c rst7 -r 01_Min.ncrst -inf 01_Min.mdinfo

    Alternative (automatically tried to create amber@localhost code, but requires
    amber to be installed and available in your environment path):

    $ aiida_sander -i input_files/01_Min.in -o 01_Min.out \
        -p parm7 -c rst7 -r 01_Min.ncrst -inf 01_Min.mdinfo

    Help: $ aiida_sander --help
    """

    launch(kwargs)


if __name__ == "__main__":
    cli()
