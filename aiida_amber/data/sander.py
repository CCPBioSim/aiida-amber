"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from aiida.orm import Dict
from voluptuous import Optional, Required, Schema

# A subset of sander's command line options
cmdline_options = {
    Required("o", default="mdout"): str,
    Required("inf", default="mdinfo"): str,
    Optional("r"): str,
    Optional(
        "ref",
    ): str,
    Optional("mtmd"): str,
    Optional("x"): str,
    Optional("y"): str,
    Optional("v"): str,
    Optional("frc"): str,
    Optional("rdip"): str,
    Optional("mdip"): str,
    Optional("e"): str,
    Optional("radii"): str,
    Optional("cpin"): str,
    Optional("cpout"): str,
    Optional("cprestrt"): str,
    Optional("cein"): str,
    Optional("ceout"): str,
    Optional("cerestrt"): str,
    Optional("evbin"): str,
    Optional("idip"): str,
    Optional("amd"): str,
    Optional("scaledMD"): str,
    Optional("cph-data"): str,
    Optional("ce-data"): str,
    Optional("port"): str,
    Optional("suffix"): str,
    Optional("O"): bool,
    Optional("A"): bool,
}


class SanderParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for sander.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``SanderParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(SanderParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return SanderParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        """Synthesize command line parameters.

        :param input_files: list of inputs for sander command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("sander")
        # required inputs
        parameters.extend(["-i", input_files["mdin"]])
        parameters.extend(["-p", input_files["prmtop"]])
        parameters.extend(["-c", input_files["inpcrd"]])
        # optional inputs
        if "refc" in input_files:
            parameters.extend(["-ref", input_files["refc"]])
        if "mtmd" in input_files:
            parameters.extend(["-mtmd", input_files["mtmd"]])
        if "inptraj" in input_files:
            parameters.extend(["-y", input_files["inptraj"]])
        if "inpdip" in input_files:
            parameters.extend(["-idip", input_files["inpdip"]])
        if "cpin" in input_files:
            parameters.extend(["-cpin", input_files["cpin"]])
        if "cein" in input_files:
            parameters.extend(["-cein", input_files["cein"]])
        if "evbin" in input_files:
            parameters.extend(["-evbin", input_files["evbin"]])

        parm_dict = self.get_dict()

        for key, value in parm_dict.items():
            parameters.extend(["-" + key, value])

        return [str(p) for p in parameters]

    def __str__(self):
        """String representation of node.

        Append values of dictionary to usual representation. E.g.::

            uuid: b416cbee-24e8-47a8-8c11-6d668770158b (pk: 590)
            {'ignore-case': True}

        """
        string = super().__str__()
        string += "\n" + str(self.get_dict())
        return string
