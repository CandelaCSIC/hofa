.. _theoretical_foundations_extensions:

Theoretical foundations and extensions
================================================================

.. toctree::

.. contents:: **Table of Contents**
   :depth: 3
   :local:
   :backlinks: entry

Origins - from arithmetic progressions to higher-order structure
--------------------------------------------------------------------

Higher-order Fourier analysis arose in the area known as **arithmetic combinatorics** around the turn of the 21-st century, in connection with foundational questions in combinatorial number theory dating back to the 1930s. 

Notably, in [ErdosTuran1936]_,  `Erdős <https://en.wikipedia.org/wiki/Paul_Erd%C5%91s>`_ and `Turán <https://en.wikipedia.org/wiki/P%C3%A1l_Tur%C3%A1n>`_ considered the question of how large a subset of the interval of integers :math:`\{1, 2, \dots, N\}` can be if this set does not contain any :math:`3`-term arithmetic progression (i.e. a triple of the form :math:`a, a+d, a+2d`). Denoting the maximal size of such a subset by :math:`r(N)`, they conjectured (stating that "it is probable") that :math:`r(N)/N` tends to 0 as :math:`N` increases. They similarly considered, more generally, the quantity :math:`r_k(N)`, the greatest size of a subset of  :math:`\{1, 2, \dots, N\}` that contains no :math:`k`-term arithmetic progression. By extending their conjecture to these more general quantities, the study of the following question was initiated.

.. admonition:: Fundamental question:

  Is it true that, for every :math:`k`, the quantity :math:`r_k(N)/N` tends to 0 as :math:`N\to\infty`?

This question can be stated in the following equivalent and equally interesting form: does every subset of the natural numbers with *positive upper density* contain arbitrarily long arithmetic progressions?  (We will not detail the technical definition of upper density here, but the reader can think of it as the "proportion" of the integers occupied by the subset.)

This deceptively simple question (asking whether any "large enough" set of integers must contain extremely regular structures such as arithmetic progressions) became a cornerstone of arithmetic combinatorics. While Erdős and Turán themselves made progress on related problems, a full resolution would not arrive until the work of `Endre Szemerédi <https://en.wikipedia.org/wiki/Endre_Szemer%C3%A9di>`_ in the 1970s, which gave an affirmative answer to the question, see [Szemeredi1975]_.

.. admonition:: Szemerédi’s Theorem (1975):

  For every integer :math:`k`, the quantity :math:`r_k(N)/N` tends to 0 as :math:`N\to\infty`.

This result is a landmark in arithmetic combinatorics. It also has a natural follow-up, which is still not settled in general:

.. admonition:: A quantitative question:

  How fast does :math:`r_k(N)/N` tend to 0 as :math:`N\to\infty`? In other words, how small must a subset of :math:`\{1, 2, \dots, N\}` be if it does **not** contain any arithmetic progression of length :math:`k`?

This question shifts the focus from existence to *quantitative bounds*. For the case of *3-term arithmetic progressions* (:math:`k=3`), `Roth <https://en.wikipedia.org/wiki/Klaus_Friedrich_Roth>`_ had already provided (in 1953) a remarkably strong answer using **Fourier analysis**, introducing a method that would later inspire the development of *higher-order* Fourier analysis, see [Roth1953]_.

While Fourier analysis worked beautifully for 3-term arithmetic progressions, extending its use to longer progressions was found to be infeasible. The issue was that while the classical Fourier transform provided key simplifications of averages (or autocorrelations) of functions related to 3-term arithmetic progressions, it proved to be too blunt to analyze in similar ways the more complex autocorrelations pertaining to longer progressions.  For instance, it emerged that the analysis of :math:`k`-term progressions required fundamental harmonics strictly more general than the *linear* (or *fixed-frequency*) waves of classical Fourier analysis (such as :math:`e^{2\pi i x)}`), namely *polynomial* waves of degree :math:`k-1` like :math:`e^{2\pi i(x^{k-1} + \dots)}`. 

This led to the birth of higher-order Fourier analysis in the late 1990s, pioneered by `Gowers <https://en.wikipedia.org/wiki/William_Timothy_Gowers>`_ in his works [Gowers1998]_, [Gowers2001]_.


Gowers norms: measuring higher-order structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the heart of higher-order Fourier analysis are the `Gowers uniformity norms <https://en.wikipedia.org/wiki/Gowers_norm>`_ (or :math:`U^k`-norms, see Lemma 3.9 of [Gowers1998]_). As discussed in  :doc:`conceptual_background`, these norms can be used to measure how much a function correlates with certain generalizations of Fourier characters, which include polynomial phases of degree :math:`k-1`. Intuitively, a function with **large** :math:`U^k`-norm exhibits strong structure of order :math:`k-1` (e.g., it correlates with functions such as polynomial phases :math:`e^{2\pi ix^{k-1}}`), while a function with **small** :math:`U^k`-norm is "quasirandom" of order :math:`k-1`, meaning that its order-:math:`(k-1)` structure is negligible.

**Definition**:
Let :math:`\mathbb{Z}/N\mathbb{Z}` be a finite cyclic group, and let :math:`f: \mathbb{Z}/N\mathbb{Z} \to \mathbb{C}` be a complex-valued function. The **Gowers** :math:`U^k`-**norm** of :math:`f` is defined by the formula

.. math::
   \|f\|_{U^k}^{2^k} := \mathbb{E}_{x, h_1, \dots, h_k \in \mathbb{Z}/N\mathbb{Z}} \prod_{v \in \{0,1\}^k} \mathcal{C}^{|v|} f(x + v_1 h_1 + \dots + v_k h_k),

where:

- :math:`\mathbb{E}` denotes the average over all :math:`x, h_1, \dots, h_k\in \{0,\ldots,N-1\}`,

- :math:`\{0,1\}^k` is the set of all binary vectors of length :math:`k` (e.g., for :math:`k=2`, these are :math:`(0,0), (0,1), (1,0), (1,1)`),

- :math:`|v| = v_1 + \dots + v_k` is the sum of the entries of :math:`v`,

- :math:`\mathcal{C}` is the complex conjugation operator (i.e., :math:`\mathcal{C}f(x) = \overline{f(x)}`).

.. note:: 
   The Gowers norms can be defined similarly for any function on any finite abelian group (here we focus on groups :math:`\mathbb{Z}/N\mathbb{Z}` for a simpler exposition).

Connection to arithmetic progressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Gowers :math:`U^k`-norms have a **direct and powerful connection** to counting arithmetic progressions. To see this, let :math:`A \subset \mathbb{Z}/N\mathbb{Z}` be a subset of a finite cyclic group, let :math:`\delta = |A|/N` be the density of :math:`A`, and let :math:`1_A` be the usual indicator function (:math:`1_A(x)=1` if :math:`x\in A` and zero otherwise).

The key insight is that the :math:`U^{k-1}`-norm of :math:`1_A-\delta` controls the **number of arithmetic progressions of length** :math:`k` in :math:`A`. Specifically, if :math:`1_A-\delta` has a **small** :math:`U^{k-1}`-norm, then the number of :math:`k`-term arithmetic progressions in :math:`A` is **close to the expected number for a random set of the same density**. This is formalized in the following result, which extends the ideas underlying Roth’s theorem, see Corollary 3.3 in [Gowers1998]_:

.. math::
   \big| \sum_{r \in \mathbb{Z}/N\mathbb{Z}} |A\cap (A + r)\cap \cdots\cap (A+(k-1)r)| - \delta^k N^2 \big| \leq 2^k \|1_A-\delta\|_{U^{k-1}} N^2,

In other words, if :math:`1_A-\delta` has small :math:`U^{k-1}`-norm, then :math:`A` behaves like a **random set** with respect to :math:`k`-term arithmetic progressions. This connection is the foundation of many applications of higher-order Fourier analysis, including proofs of Szemerédi’s theorem.

.. note::

   **Technical Remark:**
   The above result counts arithmetic progressions *modulo* :math:`N`, i.e. in the group :math:`\mathbb{Z}/N\mathbb{Z}` rather than in the interval :math:`\{0,1,\ldots,N-1\}\subset \mathbb{N}`. To obtain **genuine** (non-wrapping) arithmetic progressions in the integers, one can use a transference argument which shows that these problems are *essentially equivalent* up to a small worsening of some constants. This idea was pioneered by Roth in [Roth1953]_. Further details can be found in [Gowers1998]_.

.. admonition:: Key Takeaway

   The :math:`U^k`-norm measures how much :math:`f` "correlates" with generalizations of Fourier characters of order :math:`k-1`, e.g. **polynomial phase functions** of degree :math:`k-1`. Thus

   - The :math:`U^2`-norm detects **linear correlations** (like traditional Fourier analysis).
   - The :math:`U^3`-norm detects **quadratic correlations** (e.g., chirps, where the frequency changes linearly over time).
   - The :math:`U^4`-norm detects **cubic correlations**, and so on.


An overview of theoretical developments since Gowers' work
--------------------------------------------------------------------

The seminal works [Gowers1998]_, [Gowers2001]_ generated extensive and vibrant further research, which is still ongoing, with many results that fundamentally reshaped the study of structure in functions. The Gowers norms provided a powerful framework to analyze higher-order correlations, enabling mathematicians to study complex patterns that were previously inaccessible to classical methods.

Here we give an overview of some of the main principles that guided this development, describe some notable applications and impact that this had in pure mathematics, and describe some of the many connections that higher-order Fourier analysis generated with areas other than arithmetic combinatorics. 

Inverse theorems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the main principles that emerged early on in higher-order Fourier analysis is that if a function has large :math:`U^k`-norm, then it must correlate (i.e. have a large inner product) with some specific type of function of order :math:`k-1` that should generalize Fourier characters. Results of this type are known as **inverse theorems** for the Gowers norms. Determining adequate generalizations of characters became one of the central problems in the subject.

In the quadratic case (i.e. for the :math:`U^3`-norm), `Green <https://en.wikipedia.org/wiki/Ben_Green>`_ and `Tao <https://en.wikipedia.org/wiki/Terence_Tao>`_ showed that functions with large :math:`U^3`-norm correlate with functions which constitute quadratic generalizations of Fourier characters; see [GreenTao2008u3]_. Such "quadratic characters" include the familiar quadratic phase functions (e.g. :math:`e^{2\pi ix^2}`), but it turned out that they also include more general functions.

.. important::
   More generally for the :math:`U^k`-norm with :math:`k>2`, while so far we have noted that polynomial phase functions (e.g. :math:`e^{2\pi ix^{k-1}}`) are central examples of "characters of order :math:`k`", it was realized early in these developments that these functions **do not suffice** for describing the structure measured by the :math:`U^k`-norms. Already for :math:`k=3`, the work [GreenTao2008u3]_ shows how, for the simple case of functions on cyclic groups, one must take into account a larger class of functions called **nilsequences**. 

Let us describe the idea of nilsequences informally here, focusing on the case at hand of functions on cyclic groups. Roughly speaking, nilsequences on :math:`\mathbb{Z}/n\mathbb{Z}` are functions of the form :math:`F(g(x))` which generalize Fourier characters as follows: instead of a homomorphism from the abelian group into the circle group :math:`\mathbb{R}/\mathbb{Z}` (as appears in a Fourier character :math:`\exp(2\pi i r x/n)`, where the homomorphism is :math:`x\mapsto rx/n \mod 1`) the map :math:`g` is a so-called **polynomial map** from :math:`\mathbb{Z}/n\mathbb{Z}` into a more subtle space called a `nilmanifold <https://en.wikipedia.org/wiki/Nilmanifold>`_, namely a quotient space :math:`G/\Gamma` where :math:`G` is a nilpotent Lie group and :math:`\Gamma` is a lattice in :math:`G`. Then, instead of the function :math:`y\mapsto \exp(2\pi i y)` from the circle to the complex numbers, we apply the more general continuous function :math:`F` from the nilmanifold to :math:`\mathbb{C}`. The nilsequence is said to be of *step* :math:`d` if the nilpotency class of :math:`G` is at most :math:`d`.

Additionally, nilsequences are usually required to have **bounded complexity**, meaning (roughly speaking) that the nilmanifold :math:`G/\Gamma` does not have arbitrarily wild structure, and also that the Lipschitz norm of :math:`F` is *bounded*.

Nilsequences turned out to be fundamental in higher-order Fourier analysis, in particular because they enabled a first inverse theorem, valid for all Gowers norms, capturing the structure of functions with large :math:`U^k`-norm. This was the inverse theorem for functions on finite cyclic groups (or intervals of integers) proved by Green, Tao, and Ziegler (see [GreenTaoZiegler2012]_) which states essentially that if a function :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` is *1-bounded* (i.e. :math:`|f(x)|\leq 1` for all  :math:`x`) and has non-trivially large Gowers :math:`U^k`-norm, then :math:`f` correlates non-trivially with some :math:`(k-1)`-step nilsequence of bounded complexity.

The study of inverse theorems remains very active, with questions exploring this topic in general finite abelian groups in qualitative directions, or works seeking quantitative results improving the bounds in the inverse theorems. The former qualitative direction includes the topic of the Jamneshan--Tao conjecture; we do not detail this topic here but refer to the work [JamneshanTao2023]_ and subsequent papers. The latter quantitative direction includes important progress on bounds in various settings, in particular the breakthrough [LengSahSawhney2024]_ in the integer setting, and works on quantitative bounds in the finite-field setting including [Milićević2020]_ and [GowersMilićević2024]_.


Regularity lemmas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another important principle is captured in the family of results known as **regularity lemmas** (or structure theorems) for :math:`U^k` norms. Results of this type began appearing a few years after Gowers's original work, notably in work of Green [Green2004]_, Green--Tao [GreenTao2010]_, and also Szegedy [Szegedy2010]_. 

The gist of such results is that a 1-bounded function :math:`f` on a finite abelian group can be decomposed into a sum of a part :math:`f_s` that is said to be "structured of order :math:`k-1`", a part :math:`f_r` that is considered as "noise of order :math:`k-1`", and possibly additional negligible errors. The defining property of the noise part is that its :math:`U^k`-norm is small, while the notion of being "structured of order :math:`k-1`" can be captured as the property that :math:`f_s` is nearly orthogonal to any function with small :math:`U^k`-norm (i.e. nearly orthogonal to any noise of order :math:`k-1`). A rather simple and more precise formalization of this notion consists in requiring that the function :math:`f_s` be close to a function that has bounded :math:`U^k`-dual norm. Here let us not detail this further and instead refer the interested reader to [CGSS2026-spec]_ (especially Definition 2.23 therein) for further information on these ideas. 

One can then seek stronger and more precise descriptions of the structured part; for instance, in the case of cyclic groups, it is possible to describe the structured part in terms of functions on nilmanifolds of bounded complexity (see the regularity lemmas in [GreenTao2010]_).


There are strong connections between regularity lemmas and inverse theorems. In particular, there are ways to deduce results of any of these two types from results of the other type. On the other hand, regularity lemmas capture perhaps most directly the idea of separating structure from randomness, which is a profound guiding principle in this area. Regularizing functions (i.e. isolating their structured part by removing noise) is also an important goal in signal processing, and the main algorithms in this package are designed to achieve such regularizations relative to the Gowers norms (as will be discussed below).


Applications and connections in various settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Number theory**: the major initial impact of higher-order Fourier analysis occurred in combinatorial and analytic number theory. A few years after Gowers's initial major application (obtaining effective bounds for Szemerédi's theorem), notable applications were obtained by Green and Tao concerning the existence and counting of linear configurations in the set of prime numbers. A central result here is the celebrated Green--Tao Theorem, asserting that the set of primes contains arbitrarily long arithmetic progressions; see [GreenTao2008Primes]_. This has led to a plethora of further works on finding more general patterns in the primes (see for instance [TaoZiegler2008]_), and further generalizations.


**Ergodic Theory**: this area developed a structural theory for measure-preserving systems that was related, and intriguingly analogous to (though also independent from) the progress in additive combinatorics. Connections between combinatorics and ergodic theory had already started to develop well before Gowers's work, the most important result in that direction being `Furstenberg <https://en.wikipedia.org/wiki/Hillel_Furstenberg>`_’s **proof of Szemerédi’s theorem** in 1977, see [Furstenberg1977]_. Furstenberg’s proof used **multiple ergodic averages** and **recurrence properties** of measure-preserving systems.

Building on this, Host and `Kra <https://en.wikipedia.org/wiki/Bryna_Kra>`_ showed in 2005 that **multiple ergodic averages** are governed by **nilsystems**—a type of dynamical system consisting in rotations of a nilmanifold  [HostKra2005]_. They introduced **characteristic factors** that control these averages, revealing a deep connection between the structure of measure-preserving systems in ergodic theory and the structure of functions in additive combinatorics.
Interestingly, the Host--Kra approach included as a central element a sequence of seminorms for functions on measure-preserving systems, now known as the **Host-Kra seminorms**, which are analogues of the Gowers norms in ergodic theory. This analogy is part of a profound connection through which ergodic theory has had great influence on higher-order Fourier analysis.

Related foundational work was carried out independently by Ziegler, who studied **universal characteristic factors** for Furstenberg averages; see [Ziegler2007]_.

**Various settings**: in early developments of higher-order Fourier analysis, many central results focused on specific settings, consisting in special families of finite abelian groups which were highly relevant for notable applications. For instance, the family of finite cyclic groups, in which the Green--Tao--Ziegler inverse theorem was proved, was of interest for number theoretic applications such as the Green--Tao theorem. This became known as the **integer setting**.

Another important setting focused on the family of finite vector spaces over a fixed finite field, which became known as the **finite-field setting**. This attracted interest for its connections with topics in theoretical computer science (notably in the case of vector spaces :math:`\mathbb{F}_2^n`), but also because of the more algebraic nature of this setting (compared to the integer setting) which often simplified the phenomena of higher-order Fourier analysis. This setting was promoted notably by Green, and principal results in this direction included **inverse theorems** for Gowers norms over finite fields proved by Tao and Ziegler; see [TaoZiegler2010FiniteFields]_ and [TaoZiegler2012LowChar]_ (see also a more recent alternative proof [CGSS2023-p-hom]_). Like the integer setting, this setting also remains active, with various advances in the quantitative setting; see [Milićević2020]_, [Milićević2024]_, and [GowersMilićević2024]_ and with various applications pursued especially in coding theory and in quantum computing, as we will see below.

A unifying framework: nilspace theory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::
   The **algorithms implemented in this software package** were discovered via **nilspace theory**.

In the various areas and settings mentioned above, the initial proofs of the corresponding central results in higher-order Fourier analysis (such as inverse theorems) were different conceptually. A deeper understanding was then sought, especially in order to obtain a general inverse theorem valid for all finite abelian groups, and more broadly, a more unified theory of higher-order Fourier analysis. 

An important part of this program was initiated by Host and Kra ([HostKra2008]_), and consisted in identifying the fundamental properties that must be satisfied by any set equipped with what could be called **general cubic structures**, abstracting in particular from the cubes involved in Gowers norms. 

Inspired by this, Antolín Camarena and Szegedy introduced **nilspaces** ([ACS2010]_), which are axiomatic structures capturing precisely this idea of a general abstract space equipped with cubes of arbitrary dimensions. For a formal and detailed treatment of nilspaces, we refer to the papers by Candela [Candela2017a]_ and [Candela2017b]_.

Nilspace theory turned out to offer a **unifying framework** that extends the concepts of Gowers norms, nilsequences, and nilsystems to a broader class of mathematical structures. This has made it possible to formulate and develop central concepts and results of higher-order Fourier analysis in a more general way, with applications spanning **combinatorics**, **ergodic theory**, and **dynamical systems**.

Early examples of this are (unpublished) preprints of Szegedy that established inverse theorems, phrased in the nilspace-theoretic framework, for families of compact abelian groups beyond the integer and finite-field settings (see for instance [Szegedy2010]_). Later, Candela and Szegedy proved a general structure theorem for measure-theoretic structures called cubic couplings [CS2023-couplings]_, from which one could deduce in a unified way some central results from the arithmetic combinatorial direction (such as a general inverse theorem for Gowers norms on compact abelian groups implying the Green--Tao--Ziegler inverse theorem [CS2022-regularity]_) but also structure theorems in ergodic theory extending the Host--Kra structure theorem (see Theorem 5.10 [CS2023-couplings]_).

The theory of nilspaces has  been instrumental in:

- Providing a **common language** for the various approaches to higher-order Fourier analysis.
- Extending the reach of Gowers norms and Host--Kra seminorms to more general settings.
- Offering a **geometric and algebraic framework** to study higher-order structure in functions and measures.

The versatility of this theory has been further evidenced by its ability to prove results across diverse areas of mathematics, including:

- **Combinatorics**:
  In the wake of [CS2022-regularity]_, nilspace theory has yielded various results making progress towards the above-mentioned Jamneshan--Tao conjecture, such as [CGSS2025-bounded-rank]_, [CGSS2025-inv-nil]_.

- **Topological Dynamics**:
  In 2018, Glasner, Gutman, and Ye developed **topological analogues** of the Host--Kra theory through higher-order regionally proximal relations [GlasnerGutmanYe2018]_. Gutman, `Manners <https://fr.wikipedia.org/wiki/Frederick_Manners>`_, and `Varjú <https://en.wikipedia.org/wiki/P%C3%A9ter_Varj%C3%BA>`_ also developed a **structure theory for minimal dynamical systems based on nilspaces** [GutmanMannersVarju2020]_, [GutmanMannersVarju2019]_, and [GutmanMannersVarju2020b]_. 

- **Ergodic Theory**:
  Nilspace theory has enabled further results clarifying the structure of Host--Kra factors beyond their original setting of [HostKra2005]_ (see e.g. the study of Abramov systems in [CGSS2023-p-hom]_ and [JST2026]_). 

- **Probability Theory**:
  Nilspace theory also has implications in probability theory, particularly in the analysis of certain **exchangeability properties** for certain linear groups [CGSS2024-aff]_, analogous to `De Finetti’s theorem <https://en.wikipedia.org/wiki/De_Finetti%27s_theorem>`_.




Algorithmic approaches to higher-order Fourier analysis
------------------------------------------------------------------------------------------

While higher-order Fourier analysis originated in additive combinatorics and ergodic theory, it has also given rise to algorithmic developments. The basic question in this direction is the following:

.. admonition:: Question

   If a function has non-trivial higher-order structure, can one efficiently *find* that structure?

From the theoretical viewpoint, this is the question that the ``HoFa`` package aims to address. As we have seen already, ``HoFa`` includes functionality to remove :math:`U^k` noise from a function, and also to identify the function's dominant higher-order characters. Let us now describe in more detail what the package actually does mathematically speaking. Further below, we also discuss other approaches to the basic question above, focusing on the finite-field setting.

The approach of HoFa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. important::

   The main mathematical results that validate the algorithms in the ``HoFa`` package can be found in the paper [CGSS2026-spec]_.

.. note::

   In [CGSS2026-spec]_, while the general idea of the main algorithm is presented for any Gowers norm (see in particular Section 1.1), the detailed analysis and main proofs focus on the :math:`U^3` norm (quadratic Fourier analysis). However, the functionality in the package ``HoFa`` includes the general cases mentioned in Section 1.1 of [CGSS2026-spec]_. The authors plan to present, in a future publication, the :math:`U^k`-norm generalizations of the main proofs in this paper.

To begin explaining the mathematical approach in this package, let us discuss the following interesting fact: at the most basic level, the algorithms of ``HoFa`` *recover classical Fourier analysis*. For this we will use the case :math:`k=1` of the :math:`U^k`-norms, where one obtains only a *semi*-norm: for any finite abelian group :math:`Z` and any function :math:`f:Z\to\mathbb{C}`, the :math:`U^1`-seminorm is defined by :math:`\|f\|_{U^1}=|\mathbb{E}_{x\in Z}f(x)|`.

.. _simple-instance:

A simple instance of the spectral approach: recovering classical Fourier analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let us begin by recalling the denoising algorithm for functions :math:`f: \mathbb{Z}/N\mathbb{Z} \to \mathbb{C}`, with a general operator :math:`K:\mathbb{C}^{N}\to \mathbb{C}^N`. We require this operator to be *invariant*, by which we mean that for any :math:`t\in  \mathbb{Z}/N\mathbb{Z}` and any :math:`g: \mathbb{Z}/N\mathbb{Z} \to \mathbb{C}` we have :math:`K(g(\cdot+t))=K(g)(\cdot+t)` and  :math:`\overline{K(g)}=K(\overline{g})`.

.. _reg-algorithm:

**Description of the algorithm**


**Input**: A function :math:`f: \mathbb{Z}/N\mathbb{Z} \to \mathbb{C}`, a constant :math:`\varepsilon \in \mathbb{R}_{>0}`, and an operator :math:`K:\mathbb{C}^{N}\to \mathbb{C}^N`.

**Step 1. Turn the function into a rank-1 matrix.**
   - Define the rank-1 matrix :math:`M(x,y) = f(x) \otimes \overline{f(y)} \in \mathbb{C}^{N \times N}`.

**Step 2. Apply the invariant operator** :math:`K` to the diagonals.
   - For each :math:`t \in \mathbb{Z}/N\mathbb{Z}`, apply the invariant operator :math:`K` to the diagonal function :math:`x\mapsto M(x + t, x)`.

**Step 3. Eigenvalue decomposition.**
   - Perform the eigenvalue decomposition of the matrix :math:`M` to obtain the eigenvalues :math:`\mu_1, \mu_2, \ldots, \mu_{N}` and the corresponding eigenvectors :math:`v_1, v_2, \ldots, v_{N}`.

**Step 4. Extract the structured (or regularized) component of the function.**
   - Compute the regularized component of :math:`f` as :math:`f_{\text{reg}} = \sum_{\mu_i \geq \varepsilon} \langle f, v_i \rangle v_i`.
   - This step filters out the components of :math:`f` that correspond to eigenvalues below the threshold :math:`\varepsilon`.

**Output**: The regularized component :math:`f_{\text{reg}}` and the set of eigenvalues and eigenvectors :math:`\{(\mu_1, v_1), \ldots, (\mu_{N}, v_{N})\}`.

As a first illustration of the use of this algorithm, let us examine what happens if we let :math:`K` be the simplest possible operator, that is, the averaging operator :math:`K(g)=\mathbb{E}_{x\in \mathbb{Z}/N\mathbb{Z}}g(x)`.

.. admonition:: Lemma

   The above algorithm applied with the averaging operator returns the projection of :math:`f` to the span of its dominant Fourier characters.

.. note::
   
   Recall that, as elsewhere in the documentation of the ``HoFa`` package, the definition we use for the Fourier transform of functions :math:`f:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}` is given by the formula :math:`\widehat{f}(\chi) := \frac{1}{n}\sum_{x=0}^{n-1} f(x)\overline{\chi(x)}=\mathbb{E}_{x\in \mathbb{Z}/n\mathbb{Z}} f(x)\overline{\chi(x)}`, for any Fourier character :math:`\chi:\mathbb{Z}/n\mathbb{Z}\to \mathbb{C}`. In particular, the inverse of the Fourier transform is given by :math:`f(x)=\sum_{\chi}\widehat{f}(\chi)\chi(x)`.

To prove this, let us compute the resulting matrix :math:`K(M)=K(f \otimes \overline{f})(x,y)` after replacing each diagonal by the average over that diagonal, i.e. after step 2 in the above algorithm.

.. math::
   K(f \otimes \overline{f})(x,y) = \mathbb{E}_{z \in \mathbb{Z}/N\mathbb{Z}} f(x+z)\overline{f(y+z)}

.. math::
   = \mathbb{E}_{z \in \mathbb{Z}/N\mathbb{Z}} \big( \sum_{\chi \in \widehat{\mathbb{Z}/N\mathbb{Z}}} \langle f, \chi \rangle \chi(x+z) \big) \big( \overline{\sum_{\chi' \in \widehat{\mathbb{Z}/N\mathbb{Z}}} \langle f, \chi' \rangle \chi'(y+z)} \big)

.. math::
   = \sum_{\chi, \chi' \in \widehat{\mathbb{Z}/N\mathbb{Z}}} \langle f, \chi \rangle \overline{\langle f, \chi' \rangle} \mathbb{E}_{z \in \mathbb{Z}/N\mathbb{Z}} \chi(x+z) \overline{\chi'(y+z)} 

.. math::
   = \sum_{\chi \in \widehat{\mathbb{Z}/N\mathbb{Z}}} |\langle f, \chi \rangle|^2 \chi(x)\overline{\chi(y)}.

Note that the resulting matrix is simply the sum of rank 1 pairwise orthogonal matrices whose eigenvectors are the Fourier characters and whose eigenvalues are the squared moduli of the Fourier coefficients!

The key point here is that, **in the algorithm itself**, we did not use any knowledge about Fourier characters, we simply relied on averaging and on the spectral decomposition of self-adjoint matrices (check that the resulting matrix is self-adjoint, a proof is given in Lemma 2.12 in [CGSS2026-spec]_; for a connection of this example with Principal Component Analysis, see also Remark 2.14 in [CGSS2026-spec]_).

.. important::

   The power of this algorithm lies in the fact that it does not assume any knowledge about Fourier analysis and yet it carries out a very natural Fourier-analytic operation: remove the contributions from negligible Fourier characters (i.e. those characters with corresponding coefficients of small magnitude).

.. admonition:: Key idea

   The particular choice of :math:`K` we have made here, namely the averaging operator, corresponds to performing **regularization with respect to the** :math:`U^1` norm. Thus, the algorithm transforms regularization with respect to the :math:`U^1` norm (applying this operator :math:`K`) into regularization with respect to the :math:`U^2` norm (removing the negligible Fourier characters from :math:`f`). This generalizes in a very natural way to yield the higher-order algorithm, as follows: if we let :math:`K` be an operator performing regularization with respect to the :math:`U^k`, then the output of the above algorithm should be a regularization (structured part) of :math:`f` with respect to the :math:`U^{k+1}` norm.


This is one of the critical ideas underlying the ``HoFa`` package. However, this idea needed to be rigorously proved to be correct in order to validate the algorithm. Proving this in the case of the :math:`U^3`-norm is the main content of [CGSS2026-spec]_.

Ideas in the :math:`U^3`-norm case: regularity and the Fourier denoising operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the above example, where we recovered the dominant Fourier components using the averaging operator, observe that in order to *prove* that the algorithm indeed does this, we proceeded by substituting f by its Fourier expansion. In [CGSS2026-spec]_, to *prove* the validity of the algorithm in the case of the :math:`U^3`-norm, the strategy is to substitute :math:`f` similarly by a certain theoretical decomposition of this function, but in the *quadratic* setting of the :math:`U^3`-norm (rather than in the previous classical Fourier-analytic setting of the :math:`U^2`-norm). Specifically, the decomposition that we use is a version (proved in [CS2022-regularity]_) of the above-mentioned **regularity lemma**. This result (Theorem 1.5 in [CS2022-regularity]_) tells us that any function :math:`f:\mathbb{Z}/N\mathbb{Z}\to\mathbb{C}` bounded by 1 can be written in the form

.. math::

   f = F\circ \phi+f_{r}+f_e

where (essentially)

- There exists a nilspace :math:`X` (of bounded complexity and *order 2*) such that :math:`\phi` is a so-called *nilspace morphism* from :math:`\mathbb{Z}/N\mathbb{Z}` to :math:`X` (a natural generalization of a polynomial map; see  [Candela2017a]_), and :math:`F:X\to \mathbb{C}` is a continuous map with bounded Lipschitz constant,
- :math:`f_r` is a function with small :math:`U^3`-norm and almost orthogonal to :math:`F\circ \phi`, and
- :math:`f_e` is a function with small :math:`L^1` norm and almost orthogonal to :math:`F\circ \phi`.

The error terms :math:`f_r,f_e` are negligible and we can thus treat :math:`f` as being the function :math:`F\circ \phi`. The next step consists in proving that :math:`F\circ \phi` can be decomposed into *quadratic characters* (up to a small error), that is, proving an approximate decomposition :math:`F\circ \phi \approx \sum g_i` where these *quadratic characters* :math:`g_i` satisfy two very useful properties:

1. They are pairwise almost orthogonal, i.e. :math:`|\langle g_i,g_j\rangle|` is small for :math:`i\not=j`.

2. They are pairwise almost :math:`U^3`-orthogonal, i.e. :math:`|\langle g_i,g_j\rangle_{U^3}|` is small for :math:`i\not=j`.

To understand this last statement, recall from :doc:`../user_guide/conceptual_background` that :math:`\langle g_i,g_j\rangle_{U^3}` is given by the formula

.. math::
   \mathbb{E}_{x,t_1,t_2,t_3\in \mathbb{Z}/n\mathbb{Z}} \prod_{w\in \{0,1\}^{2}} \mathcal{C}^{w_1+w_{2}}g_i(x+w_1t_1+w_{2}t_{2}) \overline{\prod_{w\in \{0,1\}^{2}} \mathcal{C}^{w_1+w_{2}}g_{j}(x+w_1t_1+w_{2}t_{2}+t_3)}

These two properties can be thought of as higher-order analogues of the following known property of classical Fourier analysis:

1. Let :math:`\chi,\chi'` be two distinct characters in the group :math:`\mathbb{Z}/N\mathbb{Z}`. Then, for every :math:`t\in \mathbb{Z}/N\mathbb{Z}` we have that :math:`\langle\chi(\cdot),\chi'(\cdot+t)\rangle=0`.

(Note that from this property we can deduce directly that :math:`\langle\chi,\chi'\rangle=0` and that :math:`\langle \chi,\chi'\rangle_{U^2}=0`.)

.. admonition:: Exercise

   Prove this last implication for classical Fourier analysis.

Once we have this decomposition of :math:`F\circ \phi`, we can write :math:`f` (approximately) as :math:`\sum g_i`. We then combine this with another major ingredient: the specific choice of invariant operator :math:`K` to be applied in Step 2 of the :ref:`Regularization algorithm <reg-algorithm>`. In this :math:`U^3`-norm case, a useful choice turns out to be what we call the **Fourier denoising operator** :math:`K_\varepsilon`. This operator essentially eliminates de Fourier components of a function that have corresponding coefficients of size less than :math:`\varepsilon`, but it does so while slightly reducing the remaining coefficients so as to ensure that certain useful analytic properties (akin to continuity) are satisfied. More precisely, for a fixed positive :math:`\varepsilon` we define the Fourier denoising operator :math:`K_\varepsilon:\mathbb{C}^N\to \mathbb{C}^N` by the formula

:math:`K_{\varepsilon}(f)=\sum_{\chi\in \widehat{\mathbb{Z}/N\mathbb{Z}}} \text{ReLU}(|\widehat{f}(\chi)|-\varepsilon) \tfrac{\widehat{f}(\chi)}{|\widehat{f}(\chi)|}\,  \chi`

:math:`=\sum_{\{\chi\in \widehat{\mathbb{Z}/N\mathbb{Z}}:|\widehat{f}(\chi)|\ge \varepsilon\}}\tfrac{|\widehat{f}(\chi)|-\varepsilon}{|\widehat{f}(\chi)|}\, \widehat{f}(\chi)\, \chi`.

We refer to Section 2.5 in [CGSS2026-spec]_) for more information on this operator.

Using the aforementioned properties of the quadratic characters :math:`g_i` and of the Fourier denoising operator, we then see that the matrix resulting from Step 2 of the algorithm essentially *diagonalizes* into a sum of rank-1 matrices of the form :math:`g_i\otimes \overline{g_i}`.

Choices of parameters in the :math:`U^3`-regularization algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main result in [CGSS2026-spec]_ that validates the :math:`U^3`-regularization algorithm (Theorem 1.1) states the following fact concerning the parameters: given a prescribed upper-bound parameter :math:`\rho` for the :math:`U^3`-norm of the noise part, the theorem guarantees the existence of a fixed parameter :math:`\varepsilon` (independent of the size of the ambient abelian group) such that, applying the Fourier-denoising operator :math:`K_\varepsilon` (in Step 2), and then eliminating the eigenspaces of :math:`K(f\otimes\overline{f})` with corresponding eigenvalues of size less than :math:`\rho` (in Step 4), the noise part will indeed be small as a power of :math:`\rho`.

In practice, it is convenient to let the threshold parameter :math:`\varepsilon` decrease dynamically with the size of the ambient group. A basic rule of thumb is that we certainly want, as a minimal requirement, the operator :math:`K_\varepsilon` to remove the Fourier coefficients coming from possible uniformly random noise present in the signal. Straightfoward arguments involving the Central Limit Theorem show that this requirement is fulfilled if we let :math:`\varepsilon` decrease approximately like :math:`\sqrt{\log(N)/N}`. These aspects will be treated in detail in [CGSS2026-app-spec]_.

Separation of individual classical Fourier components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have seen before :ref:`how to project a function to the span of its dominant Fourier characters <simple-instance>`. Is it always possible, furthermore, to **isolate and retrieve** each such Fourier character (at least up to a scalar multiple)? A first approach to this problem would be to consider the result of the :ref:`Regularization algorithm <reg-algorithm>` with :math:`K` being the averaging operator, and then simply to declare that the different eigenvectors obtained at the end of Step 4 are precisely the desired Fourier characters. 

**However, this does not work**, as we can see in the following example.

.. admonition:: Example

   Consider :math:`f = \chi + \chi'` for two Fourier characters :math:`\chi \neq \chi'` on :math:`\mathbb{Z}/N\mathbb{Z}`. Then, looking at the resulting matrix after using the :ref:`Regularization algorithm <reg-algorithm>` with :math:`K` being the averaging operator, we find that it equals :math:`\chi\otimes\chi+\chi'\otimes\chi'`. **However**, from the viewpoint of linear algebra, this just tells us that this matrix has **one eigenspace** of dimension 2 and eigenvalue equal to 1. Hence, the eigenvalue decomposition in the algorithm will return a basis for this eigenspace, but typically the eigenvectors in this basis will *not* be precisely the Fourier characters that we are looking for.

The solution proposed in [CGSS2026-spec]_ is simple: note that (following the above example) we may take a **random unit vector** in this eigenspace of eigenvalue 1. A random unit vector will be of the form :math:`a\chi+b\chi'` with :math:`|a|^2+|b|^2=1`. Then, if we **repeat** the :ref:`Regularization algorithm <reg-algorithm>` but now applying it to the function :math:`a\chi+b\chi'`, we find that the spectral decomposition of the resulting matrix will be :math:`|a|^2\chi\otimes\chi+|b|^2\chi'\otimes\chi'`. This is very useful because now, provided that :math:`a\not=b` (which happens with probability 1), we have **two different eigenspaces with different eigenvalues**, so the eigenvalue decomposition in this case will return one eigenvector for each of these distinct eigenvalues, and this vector will be a scalar multiple of the Fourier character we were looking for.

Separation of individual quadratic characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above idea works also in the case of the :math:`U^3`-norm. In this non-classical case, there are error terms of various kinds (e.g. from higher-order decomposition results), so the notion of having distinct eigenvalues needs to be strengthened to **having eigenvalues that are sufficiently separated**. Nevertheless, the same ideas apply, and this leads to the implementation of the *spectral higher-order Fourier transform* :func:`hofa.char.spechoft` in ``HoFa``.

As a further twist, recall that :func:`hofa.char.spechoft` contains two modes of functioning: we either try to find all higher-order Fourier components at once, or we find them iteratively. The iterative algorithm simply consists in applying the aforementioned idea of re-sampling a function and then, as soon as we find an isolated eigenvalue, we know that it is one of the desired higher-order components of our function, so we can remove its contribution and continue finding the rest of the components.


Other approaches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   The algorithms in this section are **not implemented** in the ``HoFa`` package, though they may be included in future developments.

.. note::

   The algorithms in this section **apply only to the finite field setting**, i.e. groups of the form :math:`(\mathbb{Z}/p\mathbb{Z})^n` for  :math:`p` a small fixed prime and :math:`n` large.

In the case of classical Fourier analysis, the Goldreich--Levin algorithm efficiently identifies all large Fourier coefficients of a Boolean function, and can therefore recover the relevant linear phases. From the perspective of additive combinatorics, this is an algorithmic form of the inverse theorem for the :math:`U^2` norm.

The emergence of higher-order Fourier analysis naturally led to the problem of constructing analogous algorithms for higher-order Gowers norms, especially the :math:`U^3`-norm over finite fields.

A first important work in this direction was that of Tulsiani and Wolf [TulsianiWolf2015]_. This can be viewed as an algorithmic counterpart of the inverse theorem for the :math:`U^3`-norm over :math:`(\mathbb{Z}/2\mathbb{Z})^n`. Roughly speaking, Tulsiani and Wolf showed that if a bounded function has significant :math:`U^3`-norm, then one can efficiently recover a quadratic phase correlating with it.

One aspect of the paper is its relationship with **Reed--Muller codes**. Quadratic phase functions are precisely the codewords of the order-2 Reed--Muller code, and the algorithms developed by Tulsiani and Wolf can therefore be interpreted as efficient decoding and self-correction procedures for these codes beyond the classical list-decoding radius.

Subsequent developments refined and optimized these ideas. Recent work of Castro-Silva and Briët revisited quadratic Goldreich--Levin algorithms from a much more quantitative and geometric perspective [BrietCastroSilva2026]_. One conceptual novelty is that the proof no longer proceeds primarily through the traditional machinery of algorithmic inverse theorems. Instead, it introduces ideas coming from **quantum learning theory and symplectic geometry**.

This is part of a more general interaction between quantum computation and higher-order Fourier analysis. Historically, the connection between Fourier analysis and quantum algorithms was already well established through the quantum Fourier transform. However, the recent developments suggest that *higher-order* Fourier analysis may also play a natural role in quantum settings. The recent algorithms of Briët and Castro-Silva explicitly exploit this connection. For more information and references, see for instance [Kuo2026]_.

These last developments are the state-of-the-art at the time of writing this documentation (2026).

Final remarks
--------------------------

In this page, we have covered an introduction to higher-order Fourier analysis from its early steps to some of its most recent results. We hope that the reader has found this page enlightening and that this package has raised their interest in studying this topic, experimenting with the software, and (hopefully) find new applications of higher-order Fourier analysis. 

We would be very glad to hear from you regarding any of these aspects, please feel free to contact us. Our email addresses can be found on our personal websites:

- `Pablo Candela <https://pablocandela.es/>`_

- `Diego González-Sánchez <https://dglez91.github.io/>`_

- `Balázs Szegedy <https://users.renyi.hu/~szegedyb/>`_

Bibliography
-------------

.. [ACS2010]
   Antolín-Camarena, O. and Szegedy B. (2010)
   *Nilspaces, nilmanifolds and their morphisms*,
   `arXiv:1009.3825v3 <https://doi.org/10.48550/arXiv.1009.3825>`_.

.. [BrietCastroSilva2026]
   Briët, J. and Castro-Silva, D. (2026)
   *A near-optimal quadratic Goldreich-Levin algorithm (extended abstract)*.
   Proceedings of the 2026 Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 6233-6239.
   `doi:10.1137/1.9781611978971.224 <https://doi.org/10.1137/1.9781611978971.224>`_.

.. [Candela2017b]
   Candela, P. (2017)
   *Notes on compact nilspaces*
   Discrete Analysis, 2017:16, 57pp. 
   `doi:10.19086/da.2106 <https://doi.org/10.19086/da.2106>`_.

.. [Candela2017a]
   Candela, P. (2017)
   *Notes on nilspaces: algebraic aspects*
   Discrete Analysis, 2017:15, 59pp.
   `doi:10.19086/da.2105 <https://doi.org/10.19086/da.2105>`_.

.. [CS2023-couplings]
   Candela, D. and Szegedy B. (2023)
   *Nilspace factors for general uniformity seminorms, cubic exchangeability and limits*
   Memoirs of the American Mathematical Society 287, no. 1425, v+101pp.
   `doi:10.1090/memo/1425 <https://doi.org/10.1090/memo/1425>`_.

.. [CS2022-regularity]
   Candela, D. and Szegedy B. (2022)
   *Regularity and inverse theorems for uniformity norms on compact abelian groups and nilmanifolds*
   Journal für die Reine und Angewandte Mathematik (Crelle's Journal) 789, 1-42. 
   `doi:10.1515/crelle-2022-0016 <https://doi.org/10.1515/crelle-2022-0016>`_.

.. [CGSS2026-app-spec]
   Candela, P., González-Sánchez, D., and Szegedy B. (2026+)
   *Spectral higher-order Fourier analysis for applications*
   In preparation.

.. [CGSS2023-p-hom]
   Candela, P., González-Sánchez, D., and Szegedy B. (2023)
   *On higher-order Fourier analysis in characteristic p*
   Ergodic Theory and Dynamical Systems, 43, 3971–4040,
   `doi:10.1017/etds.2022.119 <https://doi.org/10.1017/etds.2022.119>`_.

.. [CGSS2024-aff]
   Candela, P., González-Sánchez, D., and Szegedy B. (2024)
   *On* :math:`\mathbb{F}_2^\omega` *-affine-exchangeable probability measures*
   Studia Matematica 279, no. 1, 1-69
   `doi:10.4064/sm230505-27-8 <https://doi.org/10.4064/sm230505-27-8>`_.

.. [CGSS2025-inv-nil]
   Candela, P., González-Sánchez, D., and Szegedy B. (2025)
   *An inverse theorem for all finite abelian groups via nilmanifolds*
   `doi:10.48550/arXiv.2512.17468 <https://doi.org/10.48550/arXiv.2512.17468>`_.

.. [CGSS2026-spec]
   Candela, P., González-Sánchez, D., and Szegedy B. (2026)
   *Spectral algorithms in higher-order Fourier analysis*
   Forum of Mathematics, Sigma (2026), Vol. 14:e95 1–71,
   `doi:10.1017/fms.2026.10238 <https://doi.org/10.1017/fms.2026.10238>`_.

.. [CGSS2025-bounded-rank]
   Candela, P., González-Sánchez, D., and Szegedy B. (2026)
   *On the inverse theorem for Gowers norms in abelian groups of bounded torsion*
   accepted for publication in Discrete Analysis,
   `doi:10.48550/arXiv.2311.13899 <https://doi.org/10.48550/arXiv.2311.13899>`_.


.. [ErdosTuran1936]
   Erdős, P., and Turán, P. (1936)
   On Some Sequences of Integers.
   J. London Math. Soc. 11, no. 4, 261–264.

.. [Furstenberg1977]
   Furstenberg, H. (1977)
   *Ergodic behavior of diagonal measures and a theorem of Szemerédi on arithmetic progressions*.
   Journal d’Analyse Mathématique, 31, 204-256.
   `doi:10.1007%2FBF02813304 <https://doi.org/10.1007%2FBF02813304>`_.

.. [GlasnerGutmanYe2018]
   Glasner E., Gutman Y., and Ye X., (2018)
   *Higher order regionally proximal equivalence relations for general minimal group actions*,
   Advances in Mathematics, Volume 333, Pages 1004-1041,
   `doi:10.1016/j.aim.2018.05.023 <https://doi.org/10.1016/j.aim.2018.05.023>`_.

.. [Gowers1998]
   Gowers, W. T. (1998)
   *A new proof of Szemerédi's theorem for arithmetic progressions of length four*.
   Geom. Funct. Anal. 8, no. 3, 529–551.

.. [Gowers2001]
   Gowers, W. T. (2001)
   *A new proof of Szemerédi’s theorem*.
   Geom. Funct. Anal. 11, no. 3, 465–588.

.. [GowersMilićević2024]
   Gowers, W. T. and Milićević, L. (2024)
   *An inverse theorem for Freiman multi-homomorphisms*
   arXiv preprint.
   `doi:10.48550/arXiv.2002.11667 <https://doi.org/10.48550/arXiv.2002.11667>`_.

.. [Green2004]
   Green, B. (2004)
   *A Szemeredi-type regularity lemma in abelian groups, with applications*.
   GAFA, Geom. funct. anal. 15, 340–376 (2005). 
   `doi:10.1007/s00039-005-0509-8 <https://doi.org/10.1007/s00039-005-0509-8>`_.
   

.. [GreenTao2008u3]
   Green, B. and Tao, T. (2008)
   *An inverse theorem for the Gowers* :math:`U^3(G)` *norm*.
   Proceedings of the Edinburgh Mathematical Society, 51(1), 73-153.
   `doi:10.1017/S0013091505000325 <https://doi.org/10.1017/S0013091505000325>`_.

.. [GreenTao2008Primes]
   Green, B. and Tao, T. (2008)
   *The primes contain arbitrarily long arithmetic progressions*.
   Annals of Mathematics, 167(2), 481-547.
   `doi:10.4007/annals.2008.167.481 <https://doi.org/10.4007/annals.2008.167.481>`_.

.. [GreenTaoZiegler2012]
   Green, B., Tao, T., and Ziegler, T. (2012)
   *An inverse theorem for the Gowers* :math:`U^{s+1}[N]` *norm*.
   Annals of Mathematics, 176(2), 1231-1372.
   `doi.org/10.4007/annals.2012.176.2.11 <http://dx.doi.org/10.4007/annals.2012.176.2.11>`_.

.. [GreenTao2010]
   Green, B. and Tao, T. (2010)
   *An arithmetic regularity lemma, an associated counting lemma, and applications*.
   In: Bárány, I., Solymosi, J., Sági, G. (eds) An Irregular Mind. Bolyai Society Mathematical Studies, vol 21. Springer, Berlin, Heidelberg. 
   `doi:/10.1007/978-3-642-14444-8_7 <https://doi.org/10.1007/978-3-642-14444-8_7>`_.


.. [GutmanMannersVarju2020]
   Gutman, Y., Manners, J., and Varjú, P. (2020)
   *The structure theory of nilspaces I*.
   The structure theory of nilspaces I. JAMA 140, 299–369 (2020). 
   `doi:10.1007/s11854-020-0093-8 <https://doi.org/10.1007/s11854-020-0093-8>`_.

.. [GutmanMannersVarju2019]
   Gutman, Y., Manners, J., and Varjú, P. (2019)
   *The structure theory of nilspaces II: Representation as nilmanifolds*.
   Trans. Amer. Math. Soc. 371 (2019), 4951-4992
   `doi:10.1090/tran/7503 <https://doi.org/10.1090/tran/7503>`_.

.. [GutmanMannersVarju2020b]
   Gutman, Y., Manners, J., and Varjú, P. (2020)
   *The structure theory of nilspaces III: Inverse limit representations and topological dynamics*.
   Advances in Mathematics, Volume 365, 107059,
   `doi:10.1016/j.aim.2020.107059 <https://doi.org/10.1016/j.aim.2020.107059>`_.

.. [HostKra2005]
   Host, B. and Kra, B. (2005)
   *Nonconventional ergodic averages and nilmanifolds*.
   Annals of Mathematics, 161(1), 397-485.
   `doi:10.4007/annals.2005.161.397 <https://doi.org/10.4007/annals.2005.161.397>`_.

.. [HostKra2008]
   Host, B. and Kra, B. (2008)
   *Parallelepipeds, nilpotent groups and Gowers norms*
   Bulletin de la Société Mathématique de France, Volume 136 no. 3, pp. 405-437.
   `doi:10.24033/bsmf.2561 <https://doi.org/10.24033/bsmf.2561>`_.

.. [JamneshanTao2023]
   Jamneshan, A. and Tao, T. (2023)
   *The inverse theorem for the U^3 Gowers uniformity norm on arbitrary finite abelian groups: Fourier-analytic and ergodic approaches*.
   Discrete Anal. 2023, Paper No. 11, 48 pp.

.. [JST2026]
   Jamneshan, A., Shalom, O. and Tao, T. (2026)
   *A Host-Kra* :math:`\mathbb{F}_2^\omega` *-system of order 5 that is not Abramov of order 5, and non-measurability of the inverse theorem for the* :math:`U^6(\mathbb{F}_2^n)` *-norm*
   Math. Ann. 394, no. 1, Paper No. 11, 65 pp.

.. [Kuo2026]
   Kuo, E. J. (2026)
   *Quantum algorithms for Gowers norm estimation, polynomial testing, and arithmetic progression counting over finite abelian groups*.
   Quantum Information Processing, 25, 141.
   `doi:10.1007/s11128-026-05165-6 <https://doi.org/10.1007/s11128-026-05165-6>`_.

.. [LengSahSawhney2024]
   Leng, J., Sah, A., and Sawhney, M. (2024)
   Quasipolynomial bounds on the inverse theorem for the gowers :math:`U^{s+1}[N]`-norm
   Preprint.  arXiv:2402.17994v3 

.. [Milićević2020]
   Milićević, L. (2020)
   Quantitative inverse theorem for Gowers uniformity norms :math:`U^{5}` and :math:`U^{6}` in :math:`\mathbb{F}_2^n`.
   Canadian Journal of Mathematics 76 (2024), 1289-1338.
   `doi:10.4153/S0008414X23000391 <https://doi.org/10.4153/S0008414X23000391>`_.

.. [Milićević2024]
   Milićević, L. (2024)
   Quasipolynomial inverse theorem for the :math:`U^{4}(\mathbb{F}_p^n)` norm.
   arXiv preprint
   `doi:10.48550/arXiv.2410.08966 <https://doi.org/10.48550/arXiv.2410.08966>`_.

.. [Roth1953]
   Roth, K. F. (1953)
   *On certain sets of integers*.
   Journal of the London Mathematical Society, 28(1), 104-109.
   `doi:10.1112/jlms/s1-28.1.104 <https://doi.org/10.1112/jlms/s1-28.1.104>`_.

.. [Szemeredi1975]
   Szemerédi, E. (1975)
   *On sets of integers containing no k-term arithmetic progression*.
   Acta Arithmetica, 27(1), 199-205.
   `doi:10.4064/aa-27-1-199-245 <https://doi.org/10.4064%2Faa-27-1-199-245>`_.

.. [Szegedy2010]
   Szegedy, B. (2010)
   *On higher order Fourier analysis*.
   Preprint.
   `arXiv:1203.2260 <https://arxiv.org/abs/1203.2260>`_.

.. [TaoZiegler2008]
   Tao, T. and Ziegler, T. (2008)
   *The primes contain arbitrarily long polynomial progressions*.
   Acta Mathematica, 201(2), 213-305.
   `doi:10.1007/s11511-008-0032-5 <https://doi.org/10.1007/s11511-008-0032-5>`_.

.. [TaoZiegler2010FiniteFields]
   Tao, T. and Ziegler, T. (2010)
   *The inverse conjecture for the Gowers norm over finite fields via the correspondence principle*.
   Analysis & PDE Vol. 3, No. 1, 1-20.
   `doi:10.2140/apde.2010.3.1 <https://doi.org/10.2140/apde.2010.3.1>`_.

.. [TaoZiegler2012LowChar]
   Tao, T. and Ziegler, T. (2012)
   *The inverse conjecture for the Gowers norm over finite fields in low characteristic*
   Ann. Comb. 16 (2012), 121-188.
   `doi.org/10.1007/s00026-011-0124-3 <https://doi.org/10.1007/s00026-011-0124-3>`_.

.. [TulsianiWolf2015]
   Tulsiani, M. and Wolf, J. (2015)
   *Quadratic Goldreich-Levin Theorems*.
   SIAM Journal on Computing, 44(5), 1279-1311.
   `doi:10.1137/12086827X <https://doi.org/10.1137/12086827X>`_.

.. [Ziegler2007]
   Ziegler, T. (2007)
   *Universal characteristic factors and Furstenberg averages*.
   Journal of the American Mathematical Society, 20(1), 53-97.
   `doi:10.1090/S0894-0347-06-00532-7 <https://doi.org/10.1090/S0894-0347-06-00532-7>`_.
