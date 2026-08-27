.. _maintainer_guidelines:

.. toctree::

.. contents:: **Table of Contents**
   :depth: 3
   :local:
   :backlinks: entry

HoFa's maintainer guidelines
============================================================

.. note::

   Make sure that you are a maintainer and have permission to accept and
   merge pull requests before continuing. If you are unsure, please contact
   the authors.

How to Handle a Pull Request
----------------------------

Pull requests (PRs) from contributors will appear in the *Pull requests*
tab of the repository on GitHub. Click on an **open** PR to review it.

First Step: Check the Changes on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PR page on GitHub contains a *Conversation* tab. The contributor will
have given the PR a title and added a short description of their changes.
From this point on, this tab will be the main means of communication
between the contributor and the maintainers regarding the PR.

The *Files changed* tab allows you to review all the files modified by the
PR. Pay particular attention to the following:

1. **Configuration files:** In general, a PR should not modify project
   configuration files (such as the ``.toml`` file) unless this has been
   explicitly discussed with the maintainers beforehand.

2. **Dependencies:** Contributors should not add dependencies on new
   packages unless this has been explicitly discussed with the maintainers
   beforehand.

3. **Suspicious or unexpected code:** Carefully review the changes for
   code that is unrelated to the proposed contribution or that appears
   suspicious. This is particularly important for changes to executable
   code, including both ``.py`` files and Jupyter notebooks (``.ipynb``).
   If you have any concerns, do not merge the PR. Contact the contributor
   and investigate the issue before proceeding.

.. important::

   You do not need to be able to guarantee that the code is completely free
   of malicious content. Instead, use common sense when reviewing the
   changes: check what the new code does, whether it is related to the
   proposed contribution, and whether it introduces unexpected operations
   such as accessing files, executing system commands, making network
   connections, or installing packages.

   If you have any doubts about a change, do not run or merge the PR.
   Contact the contributor and, if necessary, discuss the change with the
   other maintainers before proceeding.

Second step: Check the changes locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The following commands should be executed from a Git Bash (or another
   terminal with Git available).

Once the changes have been reviewed on GitHub and no potential security
risks have been identified, we can fetch the contributor's branch and
check it locally. This allows us to test the contribution before deciding
whether to merge it.

The following steps assume that the contributor's branch is called
``feature_X`` (or ``fix_X``) and that the pull request number is
``PR_NUMBER``.

1. **Add the contributor's repository as a remote.**

   We first tell Git where the contributor's repository is located:

   .. code-block:: bash

      $ git remote add contributor URL

   where ``URL`` will normally have the form:

   .. code-block:: text

      https://github.com/user/package.git

   This creates a remote called ``contributor``. You can choose another
   name if you prefer. At this point, Git only records the location of
   the repository; no files or commits have been downloaded yet.

2. **Fetch the contributor's branch.**

   We then fetch the branch containing the proposed changes:

   .. code-block:: bash

      $ git fetch contributor feature_X

   Here, ``contributor`` is the name of the remote created in the previous
   step, and ``feature_X`` (or ``fix_X``) is the name of the contributor's
   branch.

   This command downloads the commits needed for that branch and updates
   a remote-tracking reference called
   ``contributor/feature_X``. It does **not** create a new local branch.

3. **Create a local branch for testing.**

   We now create a new local branch from the fetched branch:

   .. code-block:: bash

      $ git checkout -b pr-PR_NUMBER contributor/feature_X

   This creates a new local branch called ``pr-PR_NUMBER`` (you can choose
   another name) starting from the current state of
   ``contributor/feature_X``. The ``checkout`` command also switches Git
   to the new branch.

   You can now test the contribution locally without modifying the
   ``master`` branch.

If you find potential problems with the contribution, please inform the
contributor through the *Conversation* tab on GitHub. The contributor can
then make additional changes to their branch and push them to GitHub.
Those changes will automatically appear in the existing pull request;
there is no need to create a new pull request.

If the contributor makes additional changes, you will need to update your
local copy before testing them. The simplest approach is to remove the
local testing branch and recreate it from the updated contributor branch.

First switch to ``master``:

.. code-block:: bash

   $ git checkout master

Then delete the local testing branch:

.. code-block:: bash

   $ git branch -D pr-PR_NUMBER

Next, fetch the updated contributor branch:

.. code-block:: bash

   $ git fetch contributor feature_X

Finally, recreate the local testing branch:

.. code-block:: bash

   $ git checkout -b pr-PR_NUMBER contributor/feature_X

You can then test the updated contribution again.

Third Step: Accepting the PR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you are satisfied with the changes and the contribution has been
tested locally, you can proceed with accepting the PR.

Check that GitHub reports that the PR can be merged without conflicts.
If there are conflicts, do not merge the PR until they have been resolved.

To accept the PR, select **Squash and merge**. This combines all the
commits in the PR into a single commit and adds the resulting changes to
the ``master`` branch of the official repository.

Fourth Step: Releasing a New Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Merging a pull request does not necessarily mean that a new version of
the package has to be released. The maintainers can decide when a new
version should be published. In general, several small changes can be
included in a single release, while important changes should preferably
be released in a timely manner.

The following procedure describes how to manually release a new version
of the package.

Update the local ``master`` branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Releases are always made from the official ``master`` branch. Before
preparing a release, make sure that your local ``master`` branch is up to
date:

.. code-block:: bash

   $ git checkout master
   $ git pull origin master

Update the version and changelog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package version is specified in the following files and **all** of them should be updated:

- ``pyproject.toml``
- ``CITATION.cff``
- ``docs/source/conf.py``
- ``docs/source/index.rst``

For example:

.. code-block:: toml

   version = "0.1.0"

Update this value to the new version number.

The project follows `Semantic Versioning
<https://semver.org/>`_. The version has the form ``X.Y.Z``:

* ``X`` (major version) is increased when making incompatible or
  backwards-incompatible changes.
* ``Y`` (minor version) is increased when adding new functionality in a
  backwards-compatible manner.
* ``Z`` (patch version) is increased when making backwards-compatible bug
  fixes or other small changes.

For example, a release could change the version from ``0.1.0`` to
``0.1.1`` for a bug fix, or from ``0.1.0`` to ``0.2.0`` for a new
backwards-compatible feature.

Also update 

- ``CHANGELOG.md``. 

Add a new section for the new version and
summarize the relevant changes, fixes, and new features since the
previous release. Follow the format used by the previous entries in the
file.

Commit the release
^^^^^^^^^^^^^^^^^^

Once ``pyproject.toml``, ``CHANGELOG.md``, and the other files have been updated, commit
the changes:

.. code-block:: bash

   $ git add CHANGELOG.md pyproject.toml
   $ git commit -m "Release vX.Y.Z"

Push the release commit to the official repository:

.. code-block:: bash

   $ git push origin master

Create a Git tag
^^^^^^^^^^^^^^^^

Create a tag identifying the commit corresponding to the new version:

.. code-block:: bash

   $ git tag -a vX.Y.Z -m "Release vX.Y.Z"

Then push the tag to the official repository:

.. code-block:: bash

   $ git push origin vX.Y.Z

The tag provides a permanent reference to the exact version of the code
that was released.

Create a GitHub Release
^^^^^^^^^^^^^^^^^^^^^^^

Go to the repository on GitHub and open the *Releases* section. Create a
new release using the tag ``vX.Y.Z``.

The release description should contain a summary of the changes in this
version. The corresponding section of ``CHANGELOG.md`` can be copied
into the release description.

Publish the new version to PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package must now be built and uploaded to PyPI. Follow the official
`Python Packaging User Guide
<https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_
for the detailed procedure.

Make sure that the version being published matches the version in
``pyproject.toml`` and the GitHub release.

Update the documentation website
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the new release contains changes to the documentation, rebuild the
Sphinx documentation and manually deploy the updated documentation to
the project website.

Follow the project's documentation/deployment instructions for the exact
commands required to build and publish the website.

Release checklist
^^^^^^^^^^^^^^^^^

Before considering the release complete, check that:

* ``pyproject.toml``, ``CITATION.cff``, ``docs/source/conf.py``, ``docs/source/index.rst`` contains the new version number.
* ``CHANGELOG.md`` contains an entry for the new version.
* The release commit has been pushed to ``master``.
* The ``vX.Y.Z`` tag has been created and pushed.
* A corresponding GitHub Release has been created.
* The new version has been published to PyPI.
* The documentation website has been updated, if necessary.

Fifth Step (Optional): Clean Up the Local Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the PR has been accepted and there is no longer any need to test
the contribution locally, it is recommended to remove the temporary
branch and remote that were created for the review.

First, switch back to the ``master`` branch:

.. code-block:: bash

   $ git checkout master

Then delete the local testing branch:

.. code-block:: bash

   $ git branch -d pr-PR_NUMBER

Finally, remove the contributor's remote:

.. code-block:: bash

   $ git remote remove contributor

After these steps, the temporary ``pr-PR_NUMBER`` branch and
``contributor`` remote will have been removed from your local repository.
Your normal ``master`` branch and ``origin`` remote are unaffected.

.. note::

   If Git refuses to delete ``pr-PR_NUMBER`` because it contains commits
   that have not been merged into another local branch, make sure that
   you no longer need the branch and then use:

   .. code-block:: bash

      $ git branch -D pr-PR_NUMBER

   The ``-D`` option forces the deletion of the local branch. It does not
   delete anything from the contributor's repository or from GitHub.