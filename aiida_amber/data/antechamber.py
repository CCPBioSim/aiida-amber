"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from aiida.orm import Dict
from voluptuous import Optional, Required, Schema

# A subset of antechamber command line options
cmdline_options = {
    Required("fi", default="mol2"): str,
    Required("o", default="output.mol2"): str,
    Required("fo", default="mol2"): str,
    Optional("c"): str,
    Optional("nc"): int,
    Optional("fa"): str,
    Optional("ao"): str,
    Optional("m"): str,
    Optional("rn"): str,
    Optional("ek"): str,
    Optional("gk"): str,
    Optional("gopt"): str,
    Optional("gsp"): str,
    Optional("gm"): str,
    Optional("gn"): str,
    Optional("gdsk"): str,
    Optional("gv"): int,
    Optional("tor"): str,
    Optional("df"): int,
    Optional("at"): str,
    Optional("du"): str,
    Optional("bk"): str,
    Optional("an"): str,
    Optional("j"): int,
    Optional("s"): int,
    Optional("eq"): int,
    Optional("pf"): str,
    Optional("pl"): str,
    Optional("seq"): str,
    Optional("dr"): str,
}


class AntechamberParameters(Dict):
    """
    Command line options for antechamber.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``AntechamberParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(AntechamberParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return AntechamberParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        """Synthesize command line parameters.

        :param input_files: list of inputs for antechamber command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("antechamber")
        # required inputs
        parameters.extend(["-i", input_files["input_file"]])
        # optional inputs
        if "charge_file" in input_files:
            parameters.extend(["-cf", input_files["charge_file"]])
        if "additional_file" in input_files:
            parameters.extend(["-a", input_files["additional_file"]])
        if "res_top_file" in input_files:
            parameters.extend(["-rf", input_files["res_top_file"]])
        if "check_file" in input_files:
            parameters.extend(["-ch", input_files["check_file"]])
        if "esp_file" in input_files:
            parameters.extend(["-ge", input_files["esp_file"]])

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
