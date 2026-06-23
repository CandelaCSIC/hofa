A quick introduction to higher-order Fourier analysis
=====================================================================

.. toctree::
  :maxdepth: 4

`Fourier analysis <https://en.wikipedia.org/wiki/Fourier_analysis>`_ is one of the most important tools in modern science. From signal processing and imaging to quantum mechanics and data analysis, it provides a common language for understanding complicated phenomena by decomposing them into simple, oscillatory components.

At its core, classical Fourier analysis represents a function as a combination of basic harmonics such as

.. math::

    \exp(2\pi i \xi x),

which describe pure, single-frequency oscillations. Over the past few decades, however, developments in pure mathematics have revealed that this linear picture is sometimes too restrictive. These advances have given rise to a family of ideas collectively known as *higher-order Fourier analysis*.

Roughly speaking, higher-order Fourier analysis extends the classical theory by allowing nonlinear phases. Instead of only linear oscillations, one considers higher-order harmonics such as

.. math::

    \exp(2\pi i \xi x^2),

and, more generally, phases given by polynomials or structured nonlinear functions. While this may look like a small formal change, it leads to a much richer and more flexible way of describing complex behavior.

**But why do we need such decompositions?** The short answer is **sparsity** (or efficiency).

This is often the first question that arises when encountering higher-order Fourier analysis. After all, classical Fourier methods are already extremely powerful. In many practical settings we work with the `Discrete Fourier Transform <https://en.wikipedia.org/wiki/Discrete_Fourier_transform>`_, and in that context every function can be represented uniquely as the inverse Fourier transform of its frequency data.

The subtle point is not whether a representation exists, but how *efficient* that representation is. Classical Fourier analysis guarantees a decomposition, but it does not guarantee that the function can be well approximated using only a small number of Fourier modes. For some signals and data sets, the relevant structure is spread thinly across many frequencies, making Fourier-based representations sometimes inefficient or opaque.

Higher-order Fourier analysis emerges precisely when we ask a sharper question: does a given function admit a simple, *sparse* (i.e. low-complexity, efficient) description once we allow richer building blocks? By moving beyond linear harmonics and incorporating higher-order oscillatory patterns, one can often capture hidden structure using far fewer components. This shift --from mere existence to efficiency and interpretability-- is what makes higher-order Fourier analysis both powerful and broadly relevant across scientific disciplines.


A practical example: chirps
----------------------------------

To make these ideas more concrete, let us look at a simple but important class of signals known as `chirps <https://en.wikipedia.org/wiki/Chirp>`_. Informally, a chirp is a signal whose frequency changes over time. Such signals arise naturally in many scientific and engineering contexts, including radar and sonar, optics, acoustics, and communications.

A familiar Fourier harmonic oscillates at a constant rate: its peaks and troughs repeat with perfect regularity. A chirp behaves differently. At the beginning it may oscillate slowly, but as time goes on the oscillations become faster and faster. This gradual change in frequency is precisely what distinguishes a chirp from a pure tone.

A prototypical mathematical model of a chirp is given by the function

.. math::

   f(x) = \sin(\phi(x)),

where :math:`\phi` is a function with a non-constant derivative. The simplest non-trivial choice corresponds thus to :math:`\phi(x)=ax^2`. This is what is known as a *linear chirp*. Despite its simple formula, this signal already illustrates a fundamental limitation of classical Fourier analysis. Because the frequency is constantly changing, no single Fourier mode :math:`\exp(2\pi i \xi x)` captures its behavior. In fact, even on a finite interval, an accurate Fourier-based approximation requires many different frequencies.

From the point of view of higher-order Fourier analysis, however, this signal is extremely simple. It is described exactly by two *quadratic phases*: :math:`\sin(ax^2)=\tfrac{\exp(ai x^2)-\exp(-ai x^2)}{2i}`. In this sense, the apparent complexity of the chirp from the point of view of classical Fourier analysis is an artifact of the latter rather than an intrinsic property of the signal.

This example highlights the core motivation behind higher-order Fourier analysis. By enlarging the class of basic building blocks (from linear oscillations to higher-order ones) we can often reveal hidden structure and obtain far more efficient descriptions of signals that naturally arise in scientific practice.


Why higher-order Fourier analysis?
----------------------------------

The example of chirp signals points to a broader message: many signals that arise naturally in scientific practice are not random, but neither are they well described by a small number of classical Fourier modes. Instead, they exhibit *higher-order structure*, i.e. regular patterns that involve nonlinear oscillations or correlations that classical Fourier analysis does not detect.

Higher-order Fourier analysis provides a systematic framework for identifying and exploiting such structure. Rather than relying solely on linear harmonics, it enlarges the collection of basic building blocks to include higher-order oscillatory patterns, such as polynomial phases and their generalizations. Within this framework, several complementary tools play a central role. For instance, `Gowers norms <https://en.wikipedia.org/wiki/Gowers_norm>`_ act as detectors of higher-order structure, enabling a subtle distinction between signals that are genuinely random and those that contain hidden nonlinear patterns. When such structure is present, it can often be modeled using highly structured objects known as `nilsequences <https://en.wikipedia.org/wiki/Nilsequence>`_, that generalize classical Fourier harmonics similarly to how chirps generalize pure tones.

Taken together, these ideas lead to powerful decomposition principles: a complex signal can often be separated into a structured component, captured by higher-order harmonics, and a remaining part that behaves like noise. This perspective transforms higher-order Fourier analysis from a purely abstract theory into a practical analytical lens; one that is well suited for studying signals and data sets whose essential features lie beyond the reach of classical Fourier methods.

What to expect from the HoFa package
----------------------------------------

This project is aimed at scientists, engineers, and researchers from a wide range of disciplines who are interested in applying ideas from higher-order Fourier analysis to concrete problems. No prior knowledge of higher-order Fourier analysis is required. The material is designed to provide a *gentle but substantial* introduction to the subject, while at the same time equipping readers with practical tools that can be directly integrated into their own work.

Rather than presenting higher-order Fourier analysis as a purely abstract theory, the emphasis throughout is on intuition, structure, and applicability. In broad terms, the project is organized as follows:

- **A first encounter through computation.**  
  The project begins with a hands-on introduction in the form of a Jupyter notebook: :doc:`first_tutorial`. This notebook offers an intuitive entry point to higher-order Fourier analysis and the HoFa package through concrete examples, numerical experiments, and visualizations. The focus is on developing familiarity with key concepts and phenomena before engaging with formal definitions.

- **Mathematical foundations.**  
  For readers who wish to understand the theoretical underpinnings in greater depth, a dedicated section develops the mathematical foundations of higher-order Fourier analysis. Topics include higher-order structure, uniformity norms, and generalized notions of Fourier decomposition. See :doc:`../user_guide/conceptual_background`.

- **Applications, examples, and software tools.**  
  The final part of the project consists of a collection of additional notebooks and examples explaining and illustrating the capabilities of the HoFa package. There you will find detailed explanations of the software code and how it relates to the theoretical foundations of higher-order Fourier analysis. See the :doc:`../user_guide/user_guide_index`.

The components of the project are designed to be as modular as possible. Readers may follow the material sequentially, or focus on the aspects most relevant to their interests, whether these are computational, theoretical, or application-driven. The overarching aim is to lower the barrier to using higher-order Fourier analysis as a practical analytical tool in scientific research.


