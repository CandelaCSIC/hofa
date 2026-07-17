Beginner Installation guide
============================

.. toctree::

.. contents:: **Table of Contents**
   :depth: 3
   :local:
   :backlinks: entry

Installing Python with Miniconda
--------------------------------

To use **HoFa**, you first need to install **Python**, the programming language it is built on. Python relies on **libraries** (also called "packages"), which are like toolboxes containing pre-written code for specific tasks (e.g., math, data analysis, or visualization).

Managing these libraries can be complex, especially if you work on multiple projects. **Miniconda** is a tool that helps you create isolated environments (like separate workspaces) for your projects. Each environment can have its own set of libraries, making it easy to switch between projects without conflicts.

To install **Miniconda**, follow the official installation guide from Anaconda:

1. Go to the `Anaconda installation page <https://www.anaconda.com/docs/getting-started/installation>`_.
2. Select your operating system (**Windows**, **macOS**, or **Linux**).
3. Download and install **Miniconda** (not Anaconda) using the provided instructions.

After installation, verify that Miniconda is working:

- **Windows**:
  Click the **Windows Start button** (or press the Windows key), scroll to the **Anaconda (Miniconda3)** folder in the program list, and open the **Anaconda Prompt**. Then run:

.. code-block:: bash

    (base) C:\some\url> conda --version

- **macOS/Linux**:
  Open **Terminal** and run:

.. code-block:: bash

    your@user:~$ conda --version

In either case, if the command returns a version number (e.g., ``conda 24.x.x``), Miniconda is installed correctly.

Creating a Python Environment for HoFa
---------------------------------------

Now that you have **Miniconda** installed, let’s set up a dedicated **workspace** (called an *environment*) for **HoFa**. Think of this workspace as a clean, isolated desk where you can organize all the **toolboxes** (libraries) you need for your project, without affecting other projects.

Step 1: Create a New Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We will create a new environment named ``hofavenv`` with Python 3.14 (or the latest stable version). This is like setting up a new desk for your project. Execute the following commands (in either Windows/Linux/macOS) to create a new environment.

.. code-block:: bash

   conda create -n hofavenv python=3.14

- ``conda create -n hofavenv``: Creates a new environment named ``hofavenv``. You may choose any name here **except** ``base``, which is reserved.
- ``python=3.14``: Specifies the Python version to use (in this case, we have fixed ``3.14``).

Now we need to ``activate`` the environment, which will allow us to work with it. To do so, execute the following line (in either Windows/Linux/macOS):

.. code-block:: bash

   conda activate hofavenv

Note that the you will see now a ``(hofavenv)`` at the beginning of your terminal command line. This means that the environment is correctly activated and we can start working with it.

Step 2: Install Core Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

    Verify that the virtual environment ``hofavenv`` is activated, i.e. you see at the beginning of your terminal ``(hofavenv)``. Otherwise, go back to the previous steps.

Now, let us add the essential **toolboxes** (libraries) required for HoFa to work. These are like the basic tools you need on your desk. To install them, execute:

.. code-block:: bash

   pip install numpy scipy

- ``numpy`` and ``scipy``: Libraries for numerical and scientific computing.

Step 3: Install HoFa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now, install the **HoFa** package itself, which is the main tool you’ll be using.

.. code-block:: bash

   pip install hofa

Optional Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Notebook Users
"""""""""""""""""""""""

If you plan to use **Jupyter Notebooks** (interactive coding environments), install these additional toolboxes. **Jupyter Notebooks** are interactive coding environments that allow you to write and execute code in a web browser, making it easy to experiment, visualize results, and document your work.

.. code-block:: bash

   pip install jupyterlab matplotlib moviepy

- ``jupyterlab``: An interactive environment for coding.
- ``matplotlib``: A library for creating plots and visualizations.
- ``moviepy``: A library for video editing and processing.

From the **HoFa website**, you can download example notebooks to test the capabilities of HoFa and explore its features interactively.

To **launch JupyterLab** execute the following:

.. code-block:: bash

   jupyter lab

This will open a new tab in your default web browser. From there, you can:

1. Navigate to the folder where your notebooks are stored.
2. Click on a notebook file (e.g., ``.ipynb``) to open it.
3. Start coding in the interactive cells!

For Documentation Builders
"""""""""""""""""""""""""""""""""

If you want to build or contribute to the **documentation**, install these toolboxes:

.. code-block:: bash

   pip install sphinx pydata-sphinx-theme sphinx-design sphinx-autoapi myst-nb

These libraries help generate and style the documentation.

To compile the documentation locally:

1. Navigate to the ``docs`` folder in your HoFa repository.
2. Run the following command:

   .. code-block:: bash

      make html

This will generate the documentation in HTML format, which you can view in your browser.


Useful Resources
----------------

- **Miniconda/Anaconda**: Learn how to manage environments (activate, deactivate, remove, etc.) in the `Conda documentation <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.

- **JupyterLab/Notebooks**: Explore the `JupyterLab documentation <https://jupyterlab.readthedocs.io/en/stable/>`_ to get started with interactive coding.

- **Sphinx**: For documentation building, refer to the `Sphinx documentation <https://www.sphinx-doc.org/en/master/>`_.