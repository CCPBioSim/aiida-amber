:html_theme.sidebar_secondary.remove:

aiida-amber
===========

.. ccpbiosim-hero::
   :logo-light: images/aiida-amber-logo.svg
   :logo-dark: images/aiida-amber-logo.svg
   :logo-alt: aiida-amber logo
   :tagline: aiida-amber
   :button: user_guide/index | Get started
   :github: CCPBioSim/aiida-amber

   AiiDA plugin that wraps Amber molecular dynamics executables

The Amber plugin for `AiiDA`_ captures and shares the full provenance of data
when parameterising and running molecular dynamics simulations.

Quick start
-----------

.. tab-set::

   .. tab-item:: pip

      .. code-block:: bash

         pip install aiida-amber

   .. tab-item:: Conda

      .. code-block:: bash

         conda install -c ccpbiosim aiida-amber

Explore the documentation
-------------------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🚀 User Guide
      :link: user_guide/index
      :link-type: doc

      Install aiida-amber and run Amber with AiiDA.

   .. grid-item-card:: 👩‍💻 Developer Guide
      :link: developer_guide/index
      :link-type: doc

      Setting up a development environment and contributing.

   .. grid-item-card:: 📖 API
      :link: reference/aiida_amber/index
      :link-type: doc

      Reference for the aiida-amber package.

   .. grid-item-card:: 🌐 AiiDA Documentation
      :link: https://aiida.readthedocs.io

      The documentation for AiiDA itself.

.. toctree::
   :maxdepth: 2
   :hidden:

   User Guide <user_guide/index>
   Developer Guide <developer_guide/index>
   API <reference/aiida_amber/index>
   AiiDA Documentation <https://aiida.readthedocs.io>

Citing
------

If you use this plugin for your research, please cite the following work:

.. highlights:: TBD, watch this space.

If you use AiiDA for your research, please cite the following work:

.. highlights:: Giovanni Pizzi, Andrea Cepellotti, Riccardo Sabatini, Nicola Marzari,
  and Boris Kozinsky, *AiiDA: automated interactive infrastructure and database
  for computational science*, Comp. Mat. Sci 111, 218-230 (2016);
  https://doi.org/10.1016/j.commatsci.2015.09.013; http://www.aiida.net.

``aiida-amber`` is released under the MIT license.

Contact
-------

Please contact Jas Kalayan jas.kalayan@stfc.ac.uk  or James Gebbie-Rayet james.gebbie@stfc.ac.uk for information concerning ``aiida-amber`` and the `AiiDA mailing list <http://www.aiida.net/mailing-list/>`_ for questions concerning ``aiida``.

Funding
-------

Contributors to aiida-amber were supported by

.. image::  images/psdi-logo.png
   :height: 100px
   :target: https://www.psdi.ac.uk/

.. image:: images/ccpbiosim-logo-white-background.png
   :height: 100px
   :target: https://www.ccpbiosim.org/

.. image:: images/cosec-logo.png
   :height: 100px
   :target: https://www.scd.stfc.ac.uk/Pages/CoSeC.aspx

.. _AiiDA: http://www.aiida.net
