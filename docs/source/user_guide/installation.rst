============
Installation
============

This page goes through the steps for installing the required packages to use the Amber plugin for AiiDA.

Python Virtual Environment
++++++++++++++++++++++++++

We recommend setting up a Python virtual environment via Conda, which can be installed by downloading the relevant installer `here <https://docs.conda.io/en/latest/miniconda.html>`_.
If you're using Linux, install conda via the terminal with::

    bash Miniconda3-latest-Linux-x86_64.sh

Then add the conda path to the bash environment by appending the following to your ``.bashrc`` file::

    export PATH="~/miniconda3/bin:$PATH"

Options for AiiDA Installation
++++++++++++++++++++++++++++++

Our AiiDA plugin has been tested with AiiDA ``v2.4.0``, we recommend to `install <https://aiida.readthedocs.io/projects/aiida-core/en/v2.4.0/intro/install_conda.html#intro-get-started-conda-install>`_ this version of AiiDA in a conda environment. If you are using a linux OS, execute the following in the terminal, which installs AiiDA via an initial mamba installation

.. code-block:: bash

    conda install -c conda-forge mamba
    mamba create --name aiida-2.4.0 -c conda-forge aiida-core=2.4.0 aiida-core.services=2.4.0

Plugin Installation
+++++++++++++++++++

To install the AiiDA-amber plugin, activate the conda environment created previously and install our plugin via Pip,

.. code-block:: bash

    conda activate aiida-2.4.0
    pip install aiida-amber

Alternative Installation via Conda
++++++++++++++++++++++++++++++++++

The AiiDA-Amber plugin is also available via the CCPBioSim Anaconda channel.

To install using Conda:

.. code-block:: bash

    conda activate aiida-2.4.0
    conda install -c CCPBioSim aiida-amber

Or using mamba:

.. code-block:: bash

    mamba install -c CCPBioSim aiida-amber