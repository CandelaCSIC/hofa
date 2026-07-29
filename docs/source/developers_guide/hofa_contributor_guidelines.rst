.. _contribution_guidelines:

.. toctree::

HoFa's contributor guidelines
============================================================

Communication 
-----------------------

Contributions are always welcome!

If you are planning to work on a new feature, a major refactoring, or an API change, please contact the authors by email before you start implementing it. A brief discussion helps ensure that the proposed contribution aligns with the project's goals and avoids duplicated work.

Please keep communication constructive, respectful, and focused on the technical aspects of the project.

At this stage of the project, email is the preferred communication channel. As the project grows, additional channels such as GitHub Issues, GitHub Discussions, or Discord may be introduced.

Discussing API Changes
~~~~~~~~~~~~~~~~~~~~~~

Please do not submit pull requests that introduce changes to the public API without prior discussion with the project maintainers. API changes can affect existing users and often require careful consideration regarding design, documentation, and backward compatibility.

Preparing for development
-------------------------

To contribute to the project, first create your own fork of the official repository by clicking the **Fork** button in the top-right corner of the GitHub repository page.

Clone **your fork** to your local machine:

.. code-block:: bash

    $ git clone URL_TO_YOUR_FORK

You can obtain the clone URL (HTTPS or SSH) from the green **Code** button on your fork's GitHub page. By default, Git names this remote repository ``origin``.

Next, configure the original project repository as a second remote named ``upstream``:

.. code-block:: bash

    $ git remote add upstream https://github.com/CandelaCSIC/hofa.git

You can verify that both remotes have been configured correctly by running:

.. code-block:: bash

    $ git remote -v

The output should contain both:

- ``origin`` - your personal fork.
- ``upstream`` - the official project repository.

Create and activate a Python virtual environment using your preferred method.

Then install the project in editable mode:

.. code-block:: bash

    $ pip install -e .

If additional development dependencies are required in the future, they will be documented here.

You are now ready to start contributing.

Coding Standards and Documentation
----------------------------------------------------------

To ensure that the project remains maintainable, understandable, and useful to the scientific community, all contributions should follow the guidelines below.

General Coding Standards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Follow the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ coding style whenever possible.
- Use clear, descriptive names for variables, functions, classes, and modules. Well-written code should be largely self-explanatory.
- Add comments only where they improve readability or clarify non-obvious implementation details. Avoid comments that merely restate what the code already expresses.
- Keep functions and classes focused on a single responsibility whenever practical.

Documentation
~~~~~~~~~~~~~~~~~~~~~~

All new public functionality must be properly documented.

Every public function, class, or method should include a complete docstring following the project's documentation conventions so that it is correctly rendered by the automatic documentation system (AutoAPI).

Docstrings should clearly describe:

- the purpose of the functionality,
- all parameters,
- return values,
- possible exceptions (when applicable),
- usage notes,
- and illustrative examples whenever appropriate.

Contributions lacking adequate documentation may be requested to improve their docstrings before being merged.

Mathematical Background
~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the goals of this project is not only to provide implementations of mathematical methods, but also to explain the underlying ideas.

If a contribution introduces a new mathematical method, algorithm, or theoretical concept that is unlikely to be familiar to the intended audience, contributors should also include an accompanying reStructuredText (.rst) page for the User Guide.

The documentation should:

- explain the motivation behind the method,
- introduce the underlying mathematical ideas,
- describe how the implementation relates to the theory,
- include references to the relevant scientific literature,
- and provide enough detail for readers with a bachelor's-level background in a scientific or engineering discipline to understand the method.

The documentation is not expected to be a complete mathematical treatment. When appropriate, contributors should refer readers to the original literature or standard references for additional details.

Demonstrating New Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At present, the project does not yet provide a comprehensive automated test suite.

Until such a framework is available, contributors introducing new functionality are requested to provide a Jupyter notebook demonstrating their contribution.

These notebooks should:

- explain the purpose of the new functionality,
- illustrate its typical use through realistic examples,
- discuss the obtained results,
- and highlight any important limitations or practical considerations.

These notebooks form part of the project's documentation and may be published alongside the online User Guide. Contributors are therefore encouraged to maintain the same level of clarity, organization, and presentation quality expected for the rest of the documentation.

Normal contribution workflow
------------------------------

Local development
~~~~~~~~~~~~~~~~~

When developing new features or fixing bugs, please follow these guidelines.

1. Keep your local ``master`` branch up to date.

   Before starting any new work, switch to your local ``master`` branch and
   update it from the official repository::

      $ git checkout master
      $ git pull upstream master

2. Create a new branch for your work.

   Never develop directly on ``master``. Instead, create a new branch from the
   updated ``master`` branch::

      $ git checkout -b feature_my_new_feature

   Choose a short but descriptive branch name. Prefixes such as ``feature_``
   and ``fix_`` are encouraged.

3. Keep your branch up to date.

   If the project's ``master`` branch has changed while you were working,
   update your branch before opening a pull request. First update your local
   ``master`` branch as described above, then switch back to your development
   branch and rebase it::

      $ git checkout feature_my_new_feature
      $ git rebase master

   Rebasing keeps your changes on top of the latest version of the project and
   makes pull requests easier to review.

If you have never used ``git rebase`` before, we recommend spending a few
minutes reading about it before contributing. It is a very useful Git command,
but it is important to understand what it does before using it.

Submitting pull requests
~~~~~~~~~~~~~~~~~~~~~~~~

Once you are happy with your changes, push your development branch to your
GitHub fork::

   $ git push origin feature_my_new_feature

GitHub will then offer you the option to open a pull request.

A pull request is simply a request to merge your branch into the official
project. Your changes will **not** be merged automatically. Instead, the
project maintainers will review your contribution, discuss any suggested
changes with you if necessary, and merge it once it is ready.

When opening a pull request, please include a brief description of your
changes. Explaining what the contribution does, why it was made, and mentioning
any related issues (if applicable) helps reviewers understand your work.

Pull requests do not have to contain a finished feature. If you would like
feedback while your work is still in progress, you are welcome to open a draft
pull request or clearly indicate that the contribution is still under
development.


