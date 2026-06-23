Installation
=============================

.. toctree::
   :maxdepth: 1

.. _pip-installation:

Quick installation
------------------

It is recommended to install the package inside a dedicated Python
environment (for example a Conda or a Mamba environment, say ``hofavenv``) rather than in
the base system environment, and then to begin by upgrading to the latest version of ``pip``:

.. code-block:: bash

   (hofavenv) $ python -m pip install --upgrade pip

The minimal installation of HoFa can be done as follows:

.. code-block:: bash

   (hofavenv) $ pip install hofa

This installs the HoFa package together with its required runtime
dependencies.

**Requirements:**

The package requires:

- Python 3.12+

Core runtime dependencies include:

- NumPy 2.0+
- SciPy 1.13+

**Example using Conda:**

For a minimal installation with Conda, we first create a new virtual environment:

.. code-block:: bash

   (base) $ conda create -n hofavenv python=3.14
   (base) $ conda activate hofavenv

To install the core package dependencies:

.. code-block:: bash

   (hofavenv) $ pip install numpy scipy

To install the HoFa package:

.. code-block:: bash

   (hofavenv) $ pip install hofa

Optional: To install notebook-related dependencies:

.. code-block:: bash

   (hofavenv) $ pip install jupyterlab matplotlib moviepy

Optional: To install documentation dependencies:

.. code-block:: bash

   (hofavenv) $ pip install sphinx pydata-sphinx-theme sphinx-design sphinx-autoapi myst-nb

.. _source-installation:

Installation from source
------------------------

Clone the repository:

.. code-block:: bash

   $ git clone https://github.com/CandelaCSIC/hofa
   $ cd hofa

**Reproducible environment**

A reproducible Conda environment with all dependencies **except** the HoFa
package itself is provided through the ``full-environment.yml`` file.

Create the environment with:

.. code-block:: bash

   (base) $ conda env create -f full-environment.yml -n hofavenv

The environment includes:

- Runtime dependencies,
- Jupyter notebook support, and
- documentation dependencies.

.. note::

   For a lightweight installation with the latest compatible versions of the dependencies, use ``environment.yml`` instead of ``full-environment.yml`` when creating the Conda environment.

Activate the environment:

.. code-block:: bash

   (base) $ conda activate hofavenv

Then, install the HoFa package, either :ref:`from the PyPI index <pip-installation>` or directly from source as follows:

**Installation from source**

To install the HoFa package from source, execute the following command.

.. code-block:: bash

   (hofavenv) $ pip install -e .


**Jupyter notebooks**

HoFa includes example notebooks and user guides written in
Jupyter format. You can find them directly in this website using 
the following links:

- :doc:`first_tutorial`,
- :doc:`../user_guide/tutorial_denoising`, and
- :doc:`../user_guide/tutorial_high_order_characters`

or cloning the HoFa repository from Github as explained above. 
In the latter case, the tutorials are located in ``docs/source/tutorials``.

Additional notebook-related dependencies include:

- JupyterLab
- ipykernel

If the full Conda environment is installed as explained above, notebook support is already
included.

Launch JupyterLab with:

.. code-block:: bash

   (hofavenv) $ jupyter lab


**Building the documentation**

The documentation is built using Sphinx together with MyST-NB.

To build the HTML documentation:

.. code-block:: bash

   (hofavenv) $ cd docs
   (hofavenv) /docs$ make html

The generated HTML pages will appear in:

.. code-block:: text

   docs/build/html/

