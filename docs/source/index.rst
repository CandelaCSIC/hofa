.. hofa documentation master file, created by
   sphinx-quickstart on Mon Jun 1 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HoFa documentation
================================

**Version:** 0.1.0

**Useful links:** :doc:`getting_started/installation`, `Source repository <https://github.com/CandelaCSIC/hofa>`_

HoFa is a Python library for **H**\igher-**o**\rder **F**\ourier **a**\nalysis.

.. note::

   This project is under active development.
   

.. toctree::
   :hidden:
   :maxdepth: 8
   
   getting_started/getting_started_index
   user_guide/user_guide_index
   autoapi/index
   developers_guide/for_developers


.. grid:: 1 2 2 2
    :gutter: 4
    :padding: 2 2 0 0
    :class-container: sd-text-center


    .. grid-item-card:: Getting started
         :class-card: intro-card
         :shadow: md

         Here you will find an accessible introduction to *higher-order Fourier analysis*, an area of mathematics that has produced major advances since the 2000s. You will also learn the basics of how to use this theory for applications via the HoFa package.

         +++

         .. button-ref:: getting_started/getting_started_index
               :ref-type: doc
               :click-parent:
               :color: primary
               :expand:

               To the starting guide

    .. grid-item-card::  User guide
         :class-card: intro-card
         :shadow: md

         This guide delivers comprehensive coverage of the core concepts of HoFa, accompanied by valuable context and detailed explanations. This section assumes concepts from the starting guide.

         +++

         .. button-ref:: user_guide/user_guide_index
               :ref-type: doc
               :click-parent:
               :color: primary
               :expand:

               To the user guide

    .. grid-item-card::  API reference
         :class-card: intro-card
         :shadow: md

         A detailed description of all methods and classes in HoFa. This section assumes familiarity with the key concepts and ideas of the starting guide and the user guide.

         +++

         .. button-ref:: autoapi/index
               :ref-type: doc
               :click-parent:
               :color: primary
               :expand:

               To the reference guide

    .. grid-item-card::  Developer's guide
         :class-card: intro-card
         :shadow: md

         Help us develop HoFa! 

         +++

         .. button-ref:: developers_guide/for_developers
               :ref-type: doc
               :click-parent:
               :color: primary
               :expand:

               To the developer's guide

HoFa is developed in `GitHub <https://github.com/CandelaCSIC/hofa>`_ but the **official archival version** (DOI) is hosted in the `CSIC Institutional Repository <https://doi.org/10.20350/digitalCSIC/18509>`_.

About the original authors
^^^^^^^^^^^^^^^^^^^^^^^^^^

This package was originally developed by the following team:

.. list-table::
   :widths: 33 33 33
   :header-rows: 0
   :stub-columns: 0

   * - **Pablo Candela**
     - **Diego González Sánchez**
     - **Balázs Szegedy**
   * - | **Affiliation:** Instituto de Ciencias Matemáticas (ICMAT), CSIC, Madrid, Spain
       | `Website <https://www.pablocandela.es/>`__
     - | **Affiliation:** Université Paris Cité and Sorbonne Université, CNRS, IMJ-PRG, F-75013 Paris, France
       | `Website <https://dglez91.github.io/>`__
     - | **Affiliation:** HUN-REN Alfréd Rényi Institute of Mathematics, Budapest, Hungary
       | `Website <https://users.renyi.hu/~szegedyb/>`__

Funding 
^^^^^^^^^^^^^^^^

This work was supported by funding from project `PID2024-156180NB-I00 <https://matematicas.uam.es/~fernando.chamizo/grant/overview.html>`_ (MICIU/AEI and the European Union).
The second-named author is funded by `HORIZON-MSCA-2024-PF-01, AlgHOF 101202161 <https://doi.org/10.3030/101202161>`_ funded by the European Union [#f1]_. 
The third-named author was partially supported by the Hungarian Ministry of Innovation and Technology NRDI Office within the framework of the `Artificial Intelligence National Laboratory Program (MILAB, RRF-2.3.1-21-2022-00004). <https://ai.renyi.hu/>`_ 

.. [#f1] Views and opinions expressed are those of the author(s) only and do not reflect those of the European Union or the European Commission. Neither the European Union nor the European Commission can be held responsible for them.
