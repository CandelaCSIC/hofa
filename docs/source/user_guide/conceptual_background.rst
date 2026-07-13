.. _concept-background:

Conceptual background of higher-order Fourier analysis
======================================================================================

.. toctree::

.. contents:: **Table of Contents**
   :depth: 3
   :local:
   :backlinks: entry

.. note::
   This page provides an intuitive mathematical explanation of central concepts in higher-order Fourier analysis. The goal is not to be exhaustive or fully rigorous, but to provide a coherent vision of the ideas underlying the functionality of the software package. For precise mathematical results and references, please see :doc:`../user_guide/theoretical_foundations_extensions`. 

Classical Fourier analysis decomposes signals into *linear* harmonics (fixed-frequency sine and cosine waves). However, this framework struggles with signals whose *frequency content itself varies over time*, such as chirps.
In a chirp, the instantaneous frequency changes (e.g., linearly or quadratically),
so its energy is *smeared across many Fourier modes* rather than concentrated in a few.
This makes it difficult to recover or interpret the signal using traditional Fourier methods:
no single mode (or small set of modes) captures the essential structure of the chirp.

To address this, we need a way to *detect whether a signal’s structure can be
described by a small number of simple components*, or if it requires a more complex 
higher-order description. This motivates the introduction of the **Gowers norms**, which act
as "detectors" for such higher-order structure, generalizing the idea of Fourier coefficients in order
to capture polynomial phase relationships. Before introducing these norms, let us look at the case of 
*classical* Fourier analysis.

The case of classical Fourier analysis
-----------------------------------------------------

In the classical setting, we are often interested in knowing whether a signal can be represented using *a few* Fourier characters. To quantify this, we can ask *how concentrated is the signal's energy in the frequency domain*.
A natural measure of such a concentration is the **maximum magnitude of the signal's Fourier coefficients**:

.. math::  \|\hat{f}\|_\infty = \max_{k} |\hat{f}(k)|,

where :math:`\hat{f}(k)` is the Fourier coefficient corresponding to frequency :math:`k`.
If this maximum is large, the signal has a strong linear harmonic, capturing a significant part of its structure. Conversely, if :math:`\|\hat{f}\|_\infty` is small, the signal’s energy is spread across many frequencies, and Fourier methods may struggle to
capture its structure efficiently.

Classical Fourier analysis through a different lens: the Gowers :math:`U^2`-norm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To introduce this concept, let us consider a typical case of a periodic 1-dimensional signal where we have a sample of :math:`n` points. We represent such a signal with a function :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}`. Recall that :math:`\mathbb{Z}/n\mathbb{Z}` is simply the set of integers :math:`\{0,\ldots,n-1\}` with addition *modulo* :math:`n` (meaning that if we sum two elements of :math:`\{0,\ldots,n-1\}` and the result is greater than or equal to :math:`n`, then we subtract :math:`n` from the sum). Then, the Gowers :math:`U^2`-norm is defined as follows.

**The Gowers** :math:`U^2`-**norm**: Let :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` be a function. The Gowers :math:`U^2`-norm of :math:`f` is given by the formula

.. math::

   \|f\|_{U^2}^{4} = \mathbb{E}_{x,t_1,t_2\in \mathbb{Z}/n\mathbb{Z}} f(x)\overline{f(x+t_1)}\overline{f(x+t_2)}f(x+t_1+t_2)

where :math:`\mathbb{E}_{x,t_1,t_2\in \mathbb{Z}/n\mathbb{Z}}` stands for :math:`\tfrac{1}{n^{3}}\sum_{x=0}^{n-1}\sum_{t_1=0}^{n-1} \sum_{t_2=0}^{n-1}`, i.e. it is simply the average over the set :math:`(\mathbb{Z}/n\mathbb{Z})^{3}`.

We claim that **this norm plays an analogous role to that of the maximum magnitude of the Fourier coefficients**.

Fourier characters as maximizers of the :math:`U^2`-norm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let us focus on functions :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` whose absolute value is at most 1, i.e. :math:`|f(x)|\le 1` for all :math:`x\in \mathbb{Z}/n\mathbb{Z}`. What does it mean for such a function to have a large :math:`U^2`-norm? In fact, which ones are those that have *maximal* :math:`U^2`-norm?

From the definition above, it is clear that if a function has absolute value at most 1, then :math:`\|f\|_{U^2}\le 1`. Can this :math:`U^2`-norm be *equal* to 1, and if so, what kind of function must :math:`f` then be? 

It is not difficult to see that there exist functions with absolute values at most 1 and with :math:`U^2`-norm equal to 1. In fact, those are *essentially* the Fourier characters. More precisely, a function whose absolute value is at most 1 and such that :math:`\|f\|_{U^2}= 1` must be of the form :math:`f(x)=\exp(2\pi i \tfrac{x\xi}{n}+\alpha i)` for some :math:`\alpha\in \mathbb{R}` and some :math:`\xi\in \mathbb{Z}`.

.. admonition:: Optional Exercise

   Prove this.

This result tells us that the :math:`U^2`-norm can be used to detect whether a function is *basically* a Fourier character.

The Gowers :math:`U^2`-norm and the Fourier :math:`\ell^\infty`-norm.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More generally, for a function :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` whose absolute value is at most 1, i.e. :math:`|f(x)|\le 1` for all :math:`x\in \mathbb{Z}/n\mathbb{Z}`, we have that

.. math::
   \|\widehat{f}\|_\infty \le \|f\|_{U^2} \le \|\widehat{f}\|_\infty^{1/2}.

.. admonition:: Note: Normalization of the Fourier transform
   
   For functions :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}`, the definition of the Fourier transform that we use is the following: for each Fourier character :math:`\chi:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` the value of the Fourier transform of :math:`f` at :math:`\chi` is given by the formula

   .. math::
      \widehat{f}(\chi) := \frac{1}{n}\sum_{x=0}^{n-1} f(x)\overline{\chi(x)}.
   
   In particular, the inverse of the Fourier transform is given by :math:`f(x)=\sum_{\chi}\widehat{f}(\chi)\chi(x)`.

Recall that the size of :math:`\|\widehat{f}\|_\infty` indicates whether a function can or cannot be approximated by *a few Fourier characters*. The previous inequalities tell us that the :math:`U^2`-norm is *essentially equivalent* to the norm :math:`\|\widehat{f}\|_\infty`, and can therefore be used to similar effects.

.. admonition:: Optional Exercise

   Try to prove the previous inequalities. **Hint**: write :math:`f` as the inverse of its Fourier transform. Plug that expression into the definition of the :math:`U^2`-norm and simplify. This should yield that the :math:`U^2`-norm is equal to the :math:`\ell^4`-norm of the Fourier transform. To conclude, apply Parseval's identity.


Generalizing to higher-order structure
---------------------------------------
For higher-order structures (e.g., polynomial phases), there is no *direct* analog of
:math:`\|\hat{f}\|_\infty` in the frequency domain. However, a *natural generalization*
emerges when we shift our perspective from *frequency space* (mathematically, the *dual* of the original abelian group) to *physical space* (the original abelian group).
Instead of measuring concentration in the Fourier domain, we can work directly in the original group to define a hierarchy of
*detectors* that measure how much a function correlates with *polynomial phases* of increasing
complexity. This is precisely the role of the Gowers norms: they quantify, *directly in the physical domain*, the extent to
which a function exhibits higher-order structure.

To introduce these norms, let us stay focused on the case of periodic signals defined on :math:`n` points, 
that is, on functions :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}`:

**Gowers norms**: Let :math:`k\ge 2` be an integer and let :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` be any function. Then, the Gowers :math:`U^k`-norm of :math:`f` is given by the formula

.. math::

   \|f\|_{U^k}^{2^k} = \mathbb{E}_{x,t_1,\ldots,t_k\in \mathbb{Z}/n\mathbb{Z}} \prod_{w\in \{0,1\}^{k}} \mathcal{C}^{w_1+\cdots+w_k}f(x+w_1t_1+\cdots+w_kt_k)

where :math:`\mathbb{E}_{x,t_1,\ldots,t_k\in \mathbb{Z}/n\mathbb{Z}}` stands for :math:`\tfrac{1}{n^{k+1}}\sum_{x=0}^{n-1}\sum_{t_1=0}^{n-1}\cdots \sum_{t_k=0}^{n-1}` and :math:`\mathcal{C}^{\ell}` is the conjugation operator applied :math:`\ell` times.

.. note:: 
   The Gowers norms are defined analogously for functions on **any finite abelian group**. Here we presented the notion in the simple setting of the groups :math:`\mathbb{Z}/n\mathbb{Z}` for expository reasons, but the norms may very well be defined for 2-dimensional signals (on :math:`\mathbb{Z}/n\mathbb{Z}\times \mathbb{Z}/n'\mathbb{Z}`) or for high-dimensional vector spaces, e.g. on :math:`(\mathbb{Z}/2\mathbb{Z})^d` for any :math:`d`, a case of particular interest for coding theory.

While this may at first look like a generalization for the sake of it, we soon find that it is highly relevant even with simple examples, in particular with chirps.

Chirps as maximizers of the :math:`U^3`-norm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Staying focused on functions :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` of absolute value at most 1, let us now explore the following question for the :math:`U^3`-norm, similarly to what we did for the :math:`U^2`-norm: are there functions such that :math:`\|f\|_{U^3}=1`?

The answer is **yes** and, more importantly, it can be proved (assuming that :math:`n` is odd for simplicity) that :math:`\|f\|_{U^3}=1` if and only if

.. math::

   f(x) = \exp(2\pi i \tfrac{\nu x^2+\xi x}{n}+\alpha i)

for some :math:`\alpha\in \mathbb{R}` and some :math:`\nu,\xi\in \mathbb{Z}`.

.. admonition:: Optional HARD exercise

   Try to prove this result. This is non-trivial, so do not be discouraged if you find it challenging. To begin with, it is not difficult to see that :math:`\|f\|_{U^3}=1` implies that :math:`f` must take values in the unit circle in the complex plane. Thus, we may write :math:`f(x)=\exp(2\pi\phi(x))` for some function :math:`\phi:\mathbb{Z}/n\mathbb{Z}\to \mathbb{R}/\mathbb{Z}`. From this point, the rest of the proof follows from Lemma 3.1 (p. 86) of [GreenTao2008]_.

   .. [GreenTao2008] Green B, Tao T. An inverse theorem for the Gowers :math:`U^3(G)` norm.
      *Proceedings of the Edinburgh Mathematical Society*. 2008;51(1):73-153.
      `doi:10.1017/S0013091505000325 <https://doi.org/10.1017/S0013091505000325>`_.

**Conclusion**: Chirps play a role relative to the :math:`U^3`-norm which is analogous to the role of Fourier characters relative to the :math:`U^2`-norm! 

.. important::

   The analogies do not end here: **higher-order Fourier analysis** extends tools,
   results, and algorithms of classical Fourier analysis --relating the :math:`U^2`-norm
   to linear phases-- to higher-order phase functions (e.g., chirps) via the :math:`U^k`-norms for :math:`k \geq 3`.

Indeed, the :math:`U^3`-norm acts as a detector of *quadratic structure/noise*. That is, if a function has a *small* :math:`U^3`-norm, then it does not contain significant *quadratic* information. On the other hand, if the :math:`U^3`-norm is significant, this implies that our function has significant *quadratic structure*. But what is that structure exactly? And how can we compute it? We will address these questions shortly.


Higher-order structure measured by the :math:`U^k`-norms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
  There are several ways of describing what kind of structure is detected by the Gowers norms. Here, we are going to explain the one that is related to the HoFa package. For a more complete picture see :doc:`../user_guide/theoretical_foundations_extensions`.

The case of the :math:`U^2`-norm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The best way to interpret how the HoFa package decomposes functions is first to recall how classical Fourier analysis decomposes functions depending on the magnitudes of their Fourier coefficients. Continuing with our example, let :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` be a function of absolute value at most 1. Then we have the decomposition

.. math::
   f = f_s+f_r

where 

.. math::
   f_s = \sum_{|\widehat{f}(\chi)|\text{ large}} \widehat{f}(\chi)\chi \quad \text{and} \quad f_r = \sum_{|\widehat{f}(\chi)|\text{ small}} \widehat{f}(\chi)\chi.

The term :math:`f_r` is the :math:`U^2` **noise** term, i.e. a term whose Fourier amplitudes are all small. The other term, :math:`f_s`, is the **structured** term, which has a sparse Fourier description, typically consisting in a linear combination of a few Fourier characters.

.. _concept-background-u3-case:

The case of the :math:`U^3`-norm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When we go one step higher, to the :math:`U^3`-norm, we could expect that a similar decomposition holds but with quadratic phase polynomials, e.g. :math:`\exp(2\pi i x^2)`, instead of the usual Fourier characters. It turns out that this is (almost) the case. Indeed, with respect to the :math:`U^3`-norm, we also have (approximately) a decomposition of the form 

.. math::
   f = f_s+f_r

where (as expected) :math:`f_r` is the **noise** term with respect to the :math:`U^3`-norm and

.. math::
   f_s = \sum_{\ell=0}^{M-1} g_\ell

for some *small* (i.e. bounded) integer :math:`M`, where the functions :math:`g_\ell` (:math:`\ell\in \{0,\ldots,M-1\}`) are what we call dominant **quadratic characters** of :math:`f`.

But what are these quadratic characters? Their defining feature can be explained starting again from classical Fourier characters. Note that any Fourier character :math:`\chi(x)=\exp(2\pi i r x/n)` has the property that its   **multiplicative derivatives** are constant functions, that is, for any element :math:`h\in \mathbb{Z}/n\mathbb{Z}`, the multiplicative derivative :math:`\Delta_h(\chi)(x):=\chi(x+h)\overline{\chi(x)}` equals the constant function  :math:`\exp(2\pi i r h/n)`. It can be proved that, actually, this is essentially a *defining* property of Fourier characters. Taking this idea one step higher, it turns out that quadratic characters :math:`g` can also be defined by a property concerning their multiplicative derivatives :math:`\Delta_h(g)`. But what property? 

The property in question stands in relation to quadratic Fourier analysis analogously to how the property of being a constant function stands relative to linear (classical) Fourier analysis. A good such property turns out to be that **each multiplicative derivative of**  :math:`g_\ell` **should be expressible (approximately) with only a few Fourier characters**. 

Note that this property is very much satisfied by quadratic phase polynomials (or linear chirps): if :math:`g(x)=\exp(2\pi i r x^2/n)`, then :math:`\Delta_h(g)(x)` equals the *single* Fourier character :math:`\exp(2\pi i r 2 hx/n)` multiplied by a constant (depending on :math:`h`).

.. _concept-background-important-obs-quad-char:

.. admonition:: Important observation

   In the case of classical Fourier analysis, if we multiply a (classical) Fourier character by a constant, we obtain a function whose multiplicative derivatives are also constant. Therefore, if by a *linear character* (or *character of order 1*) we mean a function whose multiplicative derivatives are constant, then we have the following fact: a linear character multiplied by a :math:`U^1`-*structured function* (i.e. a constant) is again a linear character.
   
   Now note that in the quadratic case we have a similar phenomenon. If :math:`g(x)` is a quadratic character and :math:`p(x)` is a :math:`U^2`-*structured function* (meaning essentially that :math:`p(x)` is a linear combination of a few classical Fourier characters, up to a small :math:`L^2`-error), then the product :math:`p(x)g(x)` **is also a quadratic character**. Indeed, note that every multiplicative derivative of the product takes the form :math:`p(x+h)g(x+h)\overline{p(x)g(x)} = \Delta_h(g(x))\Delta_h(p(x))`, and here, on one hand :math:`\Delta_h(g(x))` is a combination of a few Fourier characters (since :math:`g` is a quadratic character), and on the other hand this holds also for :math:`\Delta_h(p(x))` (since :math:`p` itself is a combination of a few Fourier characters).

This observation has the following consequence, relevant also to the use of the ``HoFa`` package: a sum of chirps of the form

.. math::

   \exp(2\pi i x^2/n)+\exp(2\pi i (x^2+x+4)/n)+\exp(2\pi i (x^2+10x)/n),

is actually a **single quadratic character**, and will be treated as such by ``HoFa``. Indeed, it equals :math:`\exp(2\pi i x^2/n)(1+\exp(2\pi i (x+4)/n)+\exp(20\pi i x/n))`, which falls into the class of quadratic characters described above (it is a quadratic phase function times a linear combination of a few Fourier characters).

.. important::
  More general quadratic characters may involve objects more complicated than periodic quadratic phase polynomials, such as nilsequences, as discussed in more detail in :doc:`../user_guide/theoretical_foundations_extensions`. However, quadratic phase polynomials are particularly clean examples to keep in mind, in addition to being highly relevant for applications (e.g. as chirps).

The general case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we keep climbing to higher orders, we will find that a similar picture emerges, and in general we will have decompositions of the form

.. math::
   f = f_s+f_r

where :math:`f_r` is the :math:`U^k` **noise** term and 

.. math::
   f_s = \sum_{\ell=0}^{M-1} g_\ell,

where the components :math:`g_\ell` are now the dominant components of :math:`f` of order :math:`k-1`. A notion of a function :math:`g` being a **character of order** :math:`k-1` can be defined similarly, in terms of its multiplicative derivatives being all so-called **structured functions of order** :math:`k-2`. More details on these ideas can be found in :doc:`../user_guide/theoretical_foundations_extensions`.

The generalizations of orthogonality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It turns out that such general decompositions enjoy some (approximate) notion of uniqueness and orthogonality, similar to the properties enjoyed by classical Fourier characters. Indeed, if :math:`f = \sum_{\ell=0}^{M-1} g_\ell+f_r` where the functions :math:`g_\ell` are the dominant higher-order characters of :math:`f`, then we have that they satisfy the following property:

**Approximate orthogonality**: For any two distinct :math:`g_\ell, g_{\ell'}` we have that :math:`|\langle g_\ell,g_{\ell'}\rangle|` is *small*.

And, possibly more interestingly, we have the following:

**Approximate higher-order orthogonality**: For any two distinct :math:`g_\ell, g_{\ell'}`, if we define the "higher-order product" :math:`\langle g_\ell, g_{\ell'}\rangle_{U^k}` as

.. math::
   \mathbb{E}_{x,t_1,\ldots,t_k\in \mathbb{Z}/n\mathbb{Z}} \prod_{w\in \{0,1\}^{k-1}} \mathcal{C}^{w_1+\cdots+w_{k-1}}g_\ell(x+w_1t_1+\cdots+w_{k-1}t_{k-1}) \overline{\prod_{w\in \{0,1\}^{k-1}} \mathcal{C}^{w_1+\cdots+w_{k-1}}g_{\ell'}(x+w_1t_1+\cdots+w_{k-1}t_{k-1}+t_k)}

then we have that :math:`|\langle g_\ell, g_{\ell'}\rangle_{U^k}|` is also *small*. Note that this formula is very similar to the one defining the :math:`U^k`-norm, and this is not a coincidence. Indeed, the formula for the product :math:`\langle g_\ell, g_{\ell'}\rangle_{U^k}` can be obtained from that of (the :math:`2^k` power of) the :math:`U^k`-norm replacing one of the functions in half of the product and the other function in the opposite half of the product. In particular, note that :math:`\langle f, f\rangle_{U^k} = \|f\|_{U^k}^{2^k}`.


What the HoFa package can do
--------------------------------------

Once we understand how higher-order Fourier analysis handles quadratic (and higher-order)
polynomial phase functions, the natural question arises:

**What does the HoFa package do?**

The straightforward answer is that HoFa provides the following core functionalities:

1. **Compute Gowers norms** of a function.
2. **Remove the** :math:`U^k` **noise term** from a function.
3. **Identify the dominant higher-order characters** of a function.

We now invite the reader to revisit (or try for the first time) the 
:doc:`../getting_started/first_tutorial`, equipped with the insights gained from this section.


Computational complexity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current implementation of ``HoFa`` uses a **recursive approach** with ``NumPy``, which prioritizes clarity and modularity in the codebase. While this design choice improves readability and maintainability, it does not fully exploit the potential for computational efficiency. Nevertheless, the implementation achieves **good time complexity** for typical use cases.

A **parallelized implementation** will significantly improve execution speed, particularly for large-scale computations. This parallel version will leverage multi-core processing to distribute the workload, though it will come at the cost of **increased memory usage** due to the overhead of parallel execution.

The bottleneck in both approaches is the computation of the eigenvalues and eigenvectors of a self-adjoint matrix, see :doc:`tutorial_denoising` for the actual implementation. While a naive approach for eigendecomposition usually takes :math:`O(n^3)` operations, if we are interested only in the few  *largest* eigenvalues and corresponding eigenvectors (as in the case of the ``HoFa`` package) `the computational complexity is reduced <https://ieeexplore.ieee.org/abstract/document/5165662>`_ by using the **Implicitly Restarted Lanczos Method**. This is done in ``HoFa`` by using the method `scipy.sparse.linalg.eigsh <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html>`_. 

Using this method, if we want to compute the :math:`m\ll n` largest eigenvalues and corresponding eigenvectors of an :math:`n\times n` matrix, the computational complexity is :math:`O(mn^2)`. This improvement is already implemented in ``HoFa``, which enables tunable ways of computing the eigendecomposition of a self-adjoint matrix.

Assuming that for the eigendecompositions present in the algorithm we only require the largest :math:`m` eigenvalues (which typically can be fixed, or allowed to grow up to :math:`O(\log n)`, say), the complexity of the main algorithms in ``HoFa`` (namely :func:`hofa.rgz.regularize` to **remove the** :math:`U^k` **noise term**, and :func:`hofa.char.spechoft` to **identify the dominant higher-order characters**), is as follows (for an imput of size :math:`n`):

+----------------------------+---------------------------------+-----------------------------------------+
|                            |   Quadratic (:math:`U^3`) case  | General (:math:`U^k`) case              |
+============================+=================================+=========================================+
| **Recursive (Current)**    | Time: :math:`O(mn^2+n^2\log(n))`| Time: :math:`O(mn^{k-1}+n^{k-1}\log(n))`|
|                            | Memory: :math:`O(n^2)`          | Memory: :math:`O(kn^2)`                 |
+----------------------------+---------------------------------+-----------------------------------------+
| Parallelized (Theoretical) | Time: :math:`O(mn^2)`           | Time: :math:`O(kmn^2)`                  |
|                            | Memory: :math:`O(n^3)`          | Memory: :math:`O(n^k)`                  |
+----------------------------+---------------------------------+-----------------------------------------+

.. important::
   To implement the parallelized version, a parallelized **Implicitly Restarted Lanczos Method** should be implemented. **However**, this is only necessary for the general case (cubic or higher order), but for the **quadratic case** (for the :math:`U^3`-norm), it suffices to have a non-parallelized version. We are currently working to implement this functionality in ``HoFa``.
