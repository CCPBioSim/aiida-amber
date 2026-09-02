"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from aiida.orm import Dict
from voluptuous import Optional, Required, Schema

# A subset of parmed command line options
cmdline_options = {
    Required("parm"): str,  # list of prmtop files as a str
    Required("inpcrd"): str,  # list of inpcrd files as a str
    Optional("O"): bool,
    Optional("overwrite"): bool,
    Optional("l"): str,
    Optional("logfile"): str,
    Optional("prompt"): str,
    Optional("n"): bool,
    Optional("no-splash"): bool,
    Optional("e"): bool,
    Optional("enable-interpreter"): bool,
    Optional("s"): bool,
    Optional("strict"): bool,
    Optional("r"): bool,
    Optional("relaxed"): bool,
}


class ParmedParameters(Dict):
    """
    Command line options for parmed.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``ParmedParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(ParmedParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return ParmedParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        """Synthesize command line parameters.

        :param input_files: list of inputs for parmed command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("parmed")
        # required inputs
        parameters.extend(["--input", input_files["parmed_script"]])
        # parm and inpcrd are added below

        parm_dict = self.get_dict()

        # check if flags need two dashes added to front instead of one
        for key, value in parm_dict.items():
            dash = "-"
            if len(key) > 1:
                dash = "--"
            if value not in [True, False]:
                parameters.extend([dash + key, value])
            else:
                parameters.extend([dash + key])

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
