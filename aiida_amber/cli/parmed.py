#!/usr/bin/env python
"""Command line utility to run amber parmed command with AiiDA.

Usage: aiida_parmed --help
"""

import os

import click
from aiida import cmdline, engine
from aiida.orm import SinglefileData
from aiida.plugins import CalculationFactory, DataFactory

from aiida_amber import helpers
from aiida_amber.data.parmed_input import ParmedInputData
from aiida_amber.utils import node_utils

# from aiida_amber.utils import searchprevious


def launch(params):
    """Run parmed.

    Uses helpers to add amber on localhost to AiiDA on the fly.
    """

    # Prune unused CLI parameters from dict.
    params = {k: v for k, v in params.items() if v not in [None, False]}

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
        inputs["code"] = helpers.get_code(entry_point="parmed", computer=computer)

    # Prepare input parameters in AiiDA formats.
    # Set the tleap script as a TleapInputData type node
    inputs["parmed_script"] = ParmedInputData(file=os.path.join(os.getcwd(), params.pop("input")))

    # Find the inputs and outputs referenced in the tleap script
    calc_inputs, calc_outputs = inputs["parmed_script"].calculation_inputs_outputs
    # add input files and dirs referenced in tleap file into inputs
    inputs.update(calc_inputs)
    inputs.update(calc_outputs)

    if "parm" in params:
        inputs["prmtop_files"] = {}
        parm_list = list(params["parm"].split())
        # params.pop("parm")
        for parmfile in parm_list:
            formatted_filename = node_utils.format_link_label(parmfile)
            # inputs["prmtop_files"] = List(parm_list)
            inputs["prmtop_files"][formatted_filename] = SinglefileData(file=os.path.join(os.getcwd(), parmfile))
    if "inpcrd" in params:
        inputs["inpcrd_files"] = {}
        inpcrd_list = list(params["inpcrd"].split())
        # params.pop("inpcrd")
        # inputs["inpcrd_files"] = List(inpcrd_list)
        for inpcrdfile in inpcrd_list:
            formatted_filename = node_utils.format_link_label(inpcrdfile)
            inputs["inpcrd_files"][formatted_filename] = SinglefileData(file=os.path.join(os.getcwd(), inpcrdfile))

    # correct the flags that should contain a dash "-"
    # rather than an underscore "_"
    if "no_splash" in params:
        del params["no_splash"]
        params["no-splash"] = True
    if "enable_interpreter" in params:
        del params["enable_interpreter"]
        params["enable-interpreter"] = True

    ParmedParameters = DataFactory("amber.parmed")
    inputs["parameters"] = ParmedParameters(params)

    # need to search previous processes properly
    # check if inputs are outputs from prev processes
    # inputs = searchprevious.append_prev_nodes(inputs, inputs["input_list"])

    # check if a pytest test is running, if so run rather than submit aiida job
    # Note: in order to submit your calculation to the aiida daemon, do:
    # pylint: disable=unused-variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        future = engine.run(CalculationFactory("amber.parmed"), **inputs)
    else:
        future = engine.submit(CalculationFactory("amber.parmed"), **inputs)


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
# Plugin options
@click.option(
    "--description",
    default="record parmed data provenance via the aiida_amber plugin",
    type=str,
    help="Short metadata description",
)
# Required inputs
@click.option(
    "-i",
    "--input",
    default="parmed.inp",
    type=str,
    help="""Script with ParmEd commands to execute.
                Default reads from stdin.
                Can be specified multiple times to process
                multiple input files.""",
)  # file in
@click.option(
    "-p",
    "--parm",
    default="prmtop",
    type=str,
    help="""List of topology files to load into ParmEd.
                Can be specified multiple times to process
                multiple topologies.""",
)  # file in
@click.option(
    "-c",
    "--inpcrd",
    default="inpcrd",
    type=str,
    help="""List of inpcrd files to load into ParmEd.
                They are paired with the topology files in the same order
                that each set of files is specified on the
                command-line.""",
)  # file in
# Required outputs


# optional output files
@click.option(
    "-l",
    "--logfile",
    type=str,
    help="""Log file with every command executed during an interactive
                ParmEd session. Default is parmed.log""",
)  # file out
# other parameters
@click.option("-O", "--overwrite", is_flag=True, help="Allow ParmEd to overwrite existing files.")
@click.option(
    "--prompt",
    type=str,
    help="String to use as a command prompt.",
)
@click.option(
    "-n",
    "--no-splash",
    is_flag=True,
    help="""Prevent printing the greeting logo.""",
)
@click.option(
    "-e",
    "--enable-interpreter",
    is_flag=True,
    help="""Allow arbitrary single Python commands or blocks of Python code
            to be run. By default Python commands will not be run as a
            safeguard for your system. Make sure you trust the source of
            the ParmEd command before turning this option on.""",
)
@click.option(
    "-s",
    "--strict",
    is_flag=True,
    help="""Prevent scripts from running past unrecognized input and
            actions that end with an error. In interactive mode, actions
            with unrecognized inputs and failed actions prevent any changes
            from being made to the topology, but does not quit the interpreter.
            This is the default behavior.""",
)
@click.option(
    "-r",
    "--relaxed",
    is_flag=True,
    help="""Scripts ignore unrecognized input and simply skip over
            failed actions, executing the rest of the script.
            Unrecognized input in the interactive
            interpreter emits a non-fatal warning.""",
)
def cli(*args, **kwargs):
    # pylint: disable=unused-argument
    # pylint: disable=line-too-long
    """Run example.

    Example usage:

    $ aiida_parmed --code parmed@localhost -i parmed.inp -p prmtop -c inpcrd

    Alternative (automatically tried to create amber@localhost code, but requires
    amber to be installed and available in your environment path):

    $ aiida_parmed -i parmed.inp -p prmtop -c inpcrd

    Help: $ aiida_parmed --help
    """

    launch(kwargs)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
