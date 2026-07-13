r"""
This module contains the Numpy implementation for performing higher-order Fourier regularization 
using the spectral approach developed by Candela, González-Sánchez, and Szegedy. See the :ref:`tutorial-denoising` for further information.

Conventions
-----------
The following conventions are used for functions and data structures in this file:

- Any finite abelian group :math:`Z` is isomorphic to :math:`\mathbb{Z}/n_1\mathbb{Z} \times \mathbb{Z}/n_2\mathbb{Z} \times ... \times \mathbb{Z}/n_k\mathbb{Z}`. Therefore, a function :math:`f: Z \to \mathbb{C}` is represented as a ``numpy.ndarray`` tensor with shape ``(n_1, n_2, ..., n_k)``.
  
- A :math:`Z`-matrix, where :math:`Z = \mathbb{Z}/n_1\mathbb{Z} \times ... \times \mathbb{Z}/n_k\mathbb{Z}`, is represented as a ``numpy.ndarray`` tensor with shape ``(n_1, ..., n_k, n_1, ..., n_k)``. For example, for a :math:`Z`-function :math:`f: Z \to \mathbb{C}`, the tensor product :math:`f\otimes \overline{f}`, defined as :math:`f\otimes \overline{f}(x,y)=f(x)\overline{f(y)}`, is a :math:`Z`-matrix.

- The :math:`Z`-diagonal at height :math:`t\in Z` of a :math:`Z`-matrix :math:`M` is the function :math:`x\mapsto M(x+t,x)`. We regard such a function as a subset of the :math:`Z`-matrix :math:`M` corresponding to the indices :math:`(x+t,x)` for :math:`x\in Z`. When we talk about the set of :math:`Z`-diagonals, we refer to the set of functions :math:`x\mapsto M(x+t,x)` for :math:`t\in Z`.

- The multiplicative derivative of a :math:`Z`-function :math:`f: Z \to \mathbb{C}` at a point :math:`t\in Z` is the function :math:`\Delta_tf: Z \to \mathbb{C}` defined as :math:`\Delta_tf(x):=f(x+t)\overline{f(x)}` for every :math:`x\in Z`. 

- An operator on :math:`Z`-functions is a function :math:`K: \mathbb{C}^{Z} \to \mathbb{C}^{Z}`. Given a :math:`Z`-matrix :math:`M` and an operator :math:`K`, we let :math:`\mathcal{K}(M)` be the :math:`Z`-matrix defined by replacing each :math:`Z`-diagonal :math:`M(\cdot+t,\cdot)` by :math:`K(M(\cdot+t,\cdot))`.

- Sometimes we abbreviate ``numpy`` as ``np``.
"""
import numpy as np
import scipy
from typing import Callable, List, NamedTuple
from abc import ABC, abstractmethod
import copy

import hofa.cdf

class LayerRegularizer(ABC):
    r"""
    Abstract base class for a regularization policy at some layer.

    This class will contain all necessary information to project a function
    onto some eigenspaces of a certain matrix where the projection to the 
    different eigenspaces is weighted according to an :py:func:`LayerRegularizer.alpha` method.

    The user must instantiate this class (or use the class :class:`StandardLayerRegularizer` provided
    by this module).

    See the :ref:`tutorial-denoising` for further information on the role of this class.
    """
    
    @abstractmethod
    def __init__(self):
        r"""
        Initialize an instance of the class.

        This is an abstract method that should be implemented by subclasses to 
        initialize any instance-specific attributes or perform any setup required
        for the object. The constructor `__init__` can have additional arguments
        to tune the behavior of the object.

        :param None: This method does not take any parameters in the base class,
                    but subclasses should define their own constructor parameters.
        
        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def setup(self, f : np.ndarray, depth : int, layer : int):
        r"""
        Method to be called once at the beginning of the regularization process.

        As input, it takes the function ``f`` to regularize, the total order ``depth`` of
        regularization, (1 for linear/classical Fourier analysis, 2 for quadratic, etc.), 
        and the position ``layer`` of this regularizer in the algorithm. That is, ``layer`` 
        will be an integer between ``0`` and ``depth``-1, representing which part of the regularization 
        process this instance of :class:`LayerRegularizer` will perform. For example, 0 means Fourier 
        regularization (acting on the squared norms of the Fourier coefficients of some multiplicative derivative), 1 means quadratic, etc.

        :param f: A array containing the function :math:`f:Z\to \mathbb{C}` to regularize.
        :type f: np.ndarray

        :param depth: An integer representing the total order of regularization. 
                    (1 for Fourier regularization, 2 for quadratic Fourier, etc.)
        :type depth: int

        :param layer: An integer specifying the position of this regularizer in the process. 
                    It will be an integer between 0 and ``depth``-1. 
                    For example, 0 means Fourier regularization, 1 means quadratic regularization, etc.
        :type layer: int

        :return: None

        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def update(self, f : np.ndarray, height : int):
        r"""
        Update the object with the provided parameters at each step of the regularization.

        This is an abstract method that should be implemented by subclasses 
        to update the state of the :class:`LayerRegularizer` object at each step of the regularization
        process. Specifically, for an instance of :class:`LayerRegularizer` where the :py:func:`setup` method
        was called with ``depth = k`` and ``layer = l``, the :py:func:`update` method will be called
        ``k-l`` times, with ``height`` between ``k`` and ``l+1``. At each call, the implementation
        of the :py:func:`update` method can modify the internal state of the :class:`LayerRegularizer` class
        using the provided function ``f``.

        For example, when doing cubic regularization (``k=3``), the :py:func:`setup` method will be called 
        with ``layer=1`` and the original function to regularize. In this case, the :py:func:`update` method will be called ``|Z| + 1`` times, once with ``height = 3`` (with ``f`` being the original function to regularize :math:`f_0`), and ``|Z|`` times with ``height=2`` (with ``f`` being :math:`\Delta_t f_0` for :math:`t \in Z`). The purpose of calling the method with these different heights is to keep track of all multiplicative derivatives made during the regularization process.

        :param f: A array representing a multiplicative derivative :math:`\Delta_{t_1}\cdots\Delta_{t_{k-h}} f_0`, where :math:`f_0` is the original function to regularize. At each step, ``f`` changes according to the value of ``height`` and the regularization depth.
        :type f: np.ndarray

        :param height: An integer representing the number of multiplicative derivatives taken.
        :type height: int

        :return: None

        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def alpha(self, eigs : np.ndarray):
        r"""
        This is the regularizer that will be used to weight the different
        eigenspaces.

        The implementation of any class can use the information about the
        specific function to regularize, see :class:`StandardLayerRegularizer`

        :param eigs: An array of eigenvalues to obtain the weights of the different eigenspaces.
        :type eigs: np.ndarray

        :return: An array of the same shape as ``eigs`` with the weights of the different eigenspaces.
        :rtype: np.ndarray

        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def eigh(self, M : np.ndarray):
        r"""
        A method to obtain some eigenvalues and eigenvectors.

        As the :py:func:`LayerRegularizer.alpha` function typically cancels the contribution of eigenspaces
        with small eigenvalues, there is usually no need to compute the full
        eigendecomposition of the matrix ``M``. Thus, instead of using a typical
        method such as ``numpy.linalg.eigh``, which would compute the full
        eigendecomposition, the user may define a custom method which is more efficient.

        :param M: A self-adjoint matrix to perform regularization on.
        :type M: np.ndarray

        :return: A tuple containing the eigenvalues and eigenvectors of the matrix `M`.
            The format of this tuple follows the `numpy` standard of ordering the
            eigenvalues increasingly and returning the corresponding ``i``-th eigenvector
            indexed by ``[...,i]``.
        :rtype: tuple of (np.ndarray, np.ndarray)

        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    def __deepcopy__(self, memo):
        r"""
        General-purpose deepcopy implementation.

        Handles both __dict__-based and __slots__-based attributes, and
        preserves cycles and shared references.

        :param dict memo: Dictionary of already-copied objects to handle recursion.
        :return: A deep copy of this object.
        :rtype: LayerRegularizer
        """
        # 1. Check memo to handle cycles
        if id(self) in memo:
            return memo[id(self)]
        
        # 2. Create a new instance without calling __init__
        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new

        # copy __dict__ and __slots__ attributes
        for attr in getattr(self, "__dict__", {}):
            setattr(new, attr, copy.deepcopy(getattr(self, attr), memo))

        for slot in getattr(self, "__slots__", ()):
            if hasattr(self, slot):
                setattr(new, slot, copy.deepcopy(getattr(self, slot), memo))
        
        return new

    def copy(self):
        r"""
        Create a deep copy of this object.

        This method returns a new instance of the concrete subclass,
        with all attributes deep-copied. Cycles and shared references
        are handled correctly.

        :return: A new independent deep copy of this object.
        :rtype: Base

        :note: Relies on the object's `__deepcopy__` implementation. Concrete
               subclasses with special internal state (e.g., RNGs) will automatically
               have their custom deepcopy logic executed.
        """
        return copy.deepcopy(self)

    
class StandardLayerRegularizer(LayerRegularizer):
    r"""
    An implementation of the :class:`LayerRegularizer` class with common functionality.

    This class contains the implementation of a :class:`LayerRegularizer` with the
    functionality described in the paper.

    :param alpha_method: A function that defines the alpha calculation method. By default, it uses 
                         :py:func:`hofa.cdf.relu` as the method. Here we can use any user-defined method
                         that has a signature of the form ``function( f : numpy.ndarray , coefficient : float | int) -> numpy.ndarray``. Examples of admisible functions are:   

                         - :py:func:`hofa.cdf.relu`

                         - :py:func:`hofa.cdf.cutoff`

                         - :py:func:`hofa.cdf.avg_cutoff`

                         - :py:func:`hofa.cdf.top_eig`

                         - :py:func:`hofa.cdf.u2_dual` 

    :type alpha_method: Callable
    :param param: A floating-point or integer parameter used for various purposes depending on the ``mode`` below. Default value is ``1.2``. 
    :type param: float | int, optional
        
    :param mode: A string representing the mode of operation. This determines how the ``alpha_method``
                 will interpret parameters and perform regularization.
                 For the rest of this explanation :math:`k` will denote the order or regularization
                 (1 classical Fourier, 2 quadratic, etc.), :math:`f_0` will be the original function
                 to regularize, :math:`f_1` will denote a multiplicative derivative, :math:`f_2` two
                 multiplicative derivatives, etc. Note that and an :class:`StandardLayerRegularizer` 
                 object of height
                 :math:`0 \le j < k` will perform regularization of height :math:`j`, which means that it will act
                 on a function :math:`f_{k-j-1}`, i.e., on the :math:`k-j-1` multiplicative derivatives
                 of the original function. In order to choose an appropriate parameter, the
                 :class:`StandardLayerRegularizer` object will keep track of all the 
                 typical deviations of the multiplicative
                 derivatives made to compute :math:`f_{k-j-1}`. Those typical deviations will be denoted
                 :math:`\sigma_0` (for :math:`f_0`), :math:`\sigma_1` (for :math:`f_1`) etc.
                 Possible values:

                 - ``'dynamic-original'``: In this mode, we use the variace of the original function but modified using the fact that we are using it on a multiplicative derivative of ome order. In this mode, the parameter passed to the ``alpha_method`` will be ``param`` multiplied by :math:`\sigma_0^{2^{k-j-1}}\sqrt{|Z|/\log|Z|}`.

                 - ``'dynamic-strict'``: In this mode, we use the variace of the function we are regularizing. In this mode, the parameter passed to the ``alpha_method`` will be: ``param`` multiplied by :math:`\sigma_{k-j-1}\sqrt{|Z|/\log|Z|}`.

                 - ``'literal'``: Uses the parameter ``param`` directly.

                 Default is 'dynamic-original'.
    :type mode: str, optional

    :param lin_alg_method: The method for computing the eigendecomposition of a matrix. Possible values:

                            - ``'sparse'``: Uses ``scipy.sparse.linalg.eigsh`` to compute eigenvalues.

                            - ``'full'``: Uses ``numpy.linalg.eigh`` to compute eigenvalues.

                            Default is ``'sparse'``.
    :type lin_alg_method: str, optional

    :param num_eigen: The number of eigenvalues and eigenvectors to compute when using ``'sparse'`` 
                       method in ``lin_alg_method``. Possible values:

                       - ``'dynamic'``: Computed dynamically according to a heuristic.

                       - an ``int``: Specifies the number of eigenvalues to compute.

                       Default is ``'dynamic'``.
    :type num_eigen: str | int, optional
    :param rng: Either an integer seed, a np.random.Generator, or None.
                It is used for deterministic behaviour of scipy.sparse.linalg.eigsh
    :type rng: int | np.random.Generator | None
    """
    
    def __init__(self, 
                 alpha_method : Callable = hofa.cdf.relu ,  
                 param : float | int = 1.2,  
                 mode : str = 'dynamic-original', 
                 lin_alg_method : str = 'sparse',
                 num_eigen : str | int = 'dynamic',
                 rng : int | np.random.Generator | None = None
                ):
        self.alpha_method = alpha_method
        self.param = param
        if mode not in ['dynamic-original', 'dynamic-strict', 'literal']:
            raise Exception('Unknown mode!')
        self.mode = mode
        if lin_alg_method not in ['sparse', 'full']:
            raise Exception('Unknown linear algebra method!')
        self.lin_alg_method = lin_alg_method
        self.num_eigen = num_eigen
        
        self.total_depth = 0
        self.layer = 0
        self.array_sigma_sq = np.zeros(0)
        self.group = 'no group'
        self.group_size = 0

        if isinstance(rng, np.random.Generator):
            self.rng = rng
        else:
            self.rng = np.random.default_rng(rng)

        self._initialized = False

    def setup(self, f : np.ndarray, depth : int, layer : int):
        r"""
        Setup method of all :class:`StandardLayerRegularizer` in a list to perform regularization

        This method will records some important information that this object
        will need in order to perform the regularization. Namely, it records 
        the size of the group, the total order of regularization, the position of this 
        regularizer in the process, and initialize an array to keep track of the variances 
        of the different multiplicative derivatives involved in the process (to be used 
        for computing the parameter for the :py:func:`StandardLayerRegularizer.alpha`).

        :param f: An array containing the original function ``f`` to regularize.
        :type f: np.ndarray

        :param depth: An integer representing the total order of regularization, 
            i.e., ``1`` for Fourier regularization, ``2`` for quadratic Fourier, etc.
        :type depth: int

        :param layer: An integer specifying the position of this regularizer in the process.
            It will be an integer between ``0`` and ``depth``-1, with ``0`` meaning that
            it will do the Fourier regularization part, ``1`` the quadratic, etc.
        :type layer: int

        :return: None

        """

        self.group = f.shape
        self.group_size = np.prod(self.group)
        self.total_depth = depth
        self.layer = layer
        self.array_sigma_sq = np.zeros(depth-layer)

        self._initialized = True

    def _require_initialized(self):
        r"""
        Ensures that the StandardLayerRegularizer has been properly initialized before use.
    
        This method checks whether the internal state of the instance of 
        StandardLayerRegularizer has been initialized
        via the :py:func:`StandardLayerRegularizer.setup` method. 
        It is intended to be called at the beginning of any method
        that requires access to the runtime state, such as 
        :py:func:`StandardLayerRegularizer.update` or other internal operations.
    
        :raises RuntimeError: If the LayerRegularizer has not been initialized with :py:func:`StandardLayerRegularizer.setup`.
    
        This method does **not** modify any internal state. Its sole purpose is to enforce
        the correct usage pattern: construction → setup → algorithm execution.
        """
        if not self._initialized:
            raise RuntimeError(
                "StandardLayerRegularizer has not been initialized. "
                "Call setup(...) before using it."
            )

    def update(self, f : np.ndarray, height : int):
        r"""
        Update the object with the provided parameters at each step of the
        regularization.

        This method records the variance of the different multiplicative derivatives
        to be used later in :py:func:`StandardLayerRegularizer.alpha`. More precisely,
        ``depth=k`` and ``layer=l`` be the parameters that were used to
        call the :py:func:`StandardLayerRegularizer.setup` function for this object.
        Let ``height=h`` and :math:`Z` be the group where ``f`` is defined. 
        Recall that this object has to perform regularization of functions
        of the form :math:`\Delta_{t_1}\cdots\Delta_{t_{k-l-1}} f_0`. Then this
        method will keep track of the variances of :math:`f_0`, 
        :math:`\Delta_{t_{k-l-1}} f_0`, ..., :math:`\Delta_{t_1}\cdots\Delta_{t_{k-l-1}} f_0`
        so that this information is used when :py:func:`StandardLayerRegularizer.alpha` is called.

        :param f: A multiplicative derivative of the form :math:`\Delta_{t_1}\cdots\Delta_{t_{k-h}} f_0`.
                
        :type f: np.ndarray

        :param height: An integer between ``l+1`` and ``k`` representing the number 
            of multiplicative derivatives taken.
        :type height: int

        :return: None
        :rtype: None
        """

        self._require_initialized()
        
        if self.mode == 'literal':
            return
        elif self.mode == 'dynamic-original' and height < self.total_depth:
            return
        else:
            self.array_sigma_sq[self.total_depth-height] = np.mean(np.square(np.abs(f-np.mean(f))))


    def alpha(self, eigs : np.ndarray):
        r"""
        This method applies the :py:attr:`alpha_method` with a parameter computed according to
        :py:attr:`mode` and :py:attr:`param` as explained in :class:`StandardLayerRegularizer`.

        :param eigs: An array of eigenvalues to obtain the weights of the different eigenspaces.
        :type eigs: np.ndarray

        :return: An array of the same shape as ``eigs`` with the weights of the different eigenspaces.
        :rtype: np.ndarray
        """

        self._require_initialized()
        
        if self.mode == 'dynamic-original':
            sigma = (self.array_sigma_sq[0])**(2**(self.total_depth-self.layer-2))
            return self.alpha_method(eigs,self.param*sigma*np.sqrt(np.log(self.group_size)/self.group_size))
        elif self.mode == 'dynamic-strict':
            sigma = np.sqrt(self.array_sigma_sq[-1])
            return self.alpha_method(eigs,self.param*sigma*np.sqrt(np.log(self.group_size)/self.group_size))
        else:
            return self.alpha_method(eigs,self.param)

    
    def eigh(self, M : np.ndarray):
        r"""
        A method to obtain a number of eigenvalues and eigenvectors.

        Depending on :py:attr:`lin_alg_method` given in the constructor, this method will use either
        ``numpy.linalg.eigh`` or ``scipy.sparse.linalg.eigsh`` to compute (part of) the 
        eigendecomposition of a matrix ``M``.

        :param M: A self-adjoint matrix to perform regularization.
        :type M: np.ndarray

        :return: A tuple containing the eigenvalues and eigenvectors.
        :rtype: tuple(np.ndarray, np.ndarray)

        :note: The returned tuple of eigenvalues and eigenvectors follow
            the same format as ``numpy.linalg.eigh``.
        """

        self._require_initialized()

        if self.lin_alg_method == 'full':
            return np.linalg.eigh(M)
        elif self.num_eigen == 'dynamic':
            number_of_eigenvectors = np.floor(
                self.group_size/(np.log(self.group_size)*self.param**2)
            ).astype(int)
        else:
            number_of_eigenvectors = self.num_eigen
        
        # Fix ARPACK starting vector
        v0 = self.rng.standard_normal(M.shape[0])
        eig_vals, eig_vects = scipy.sparse.linalg.eigsh(M, k = number_of_eigenvectors, v0=v0)

        # It seems, even though the documentation of scipy.sparse.linalg.eigsh
        # says that the returned value is in ascending order, that this is
        # not always the case. Thus, we have to manually order eigenvalues and eigenvectors 
        # increasingly
        idx = eig_vals.argsort()          # ascending
        return eig_vals[idx], eig_vects[:, idx]

    def __deepcopy__(self, memo):
        r"""
        Deepcopy implementation that creates a new RNG for the copy.

        :param dict memo: Dictionary of already-copied objects to handle recursion.
        :return: A new copy of this object with an independent RNG.
        :rtype: StandardLayerRegularizer
        """
        if id(self) in memo:
            return memo[id(self)]

        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new

        # Copy all attributes except RNG
        for attr, value in getattr(self, "__dict__", {}).items():
            if attr != "rng":
                setattr(new, attr, copy.deepcopy(value, memo))

        # Create a new RNG with a seed derived from the current RNG
        new_seed = self.rng.integers(0, 2**32 - 1)
        new.rng = np.random.default_rng(new_seed)

        return new

class RegularizationResult(NamedTuple):
    r"""
    A class containing the output of the regularization algorithm

    This class contains the 3 outputs of the regularization algorithm.
    That is, the regularization of the function, the eigenvalues
    of the matrix :math:`\mathcal{K}(f \otimes \overline{f})` in increasing order,
    where :math:`K` si the operator that performs regularization
    of order :math:`k-1`, and their corresponding eigenvectors.

    :param regularization: The result of the regularization, it has the same 
        shape as the ``np.ndarray`` representing the function :math:`f`.

    :type regularization: np.ndarray
    
    :param eigenvalues: A 1-dimensional array of shape ``(N,)`` with the eigenvalues in 
        increasing order.
    :type eigenvectors: np.ndarray
    
    :param eigenvectors: The corresponding eigenvectors. It has shape
        ``(f.shape, N)`` where ``N`` is the number of eigenvalues returned. The eigenvector
        at position :math:`i` is located in ``eigenvectors[...,i]`` and corresponds
        to ``eigenvalues[i]``.
    :type mode: np.ndarray

    """
    
    regularization : np.ndarray
    eigenvalues : np.ndarray
    eigenvectors : np.ndarray

def regularize(f : np.ndarray, per_layer_regularizers : List[LayerRegularizer] | int = 2, rng : int | np.random.Generator | None = None) -> RegularizationResult:

    r"""
    Perform the regularization of a function using certain :class:`LayerRegularizer` s.

    The behaviour of this function depends on the number and type of ``per_layer_regularizers``.
    If ``per_layer_regularizers`` is an integer, then it is used a default list of 
    :class:`LayerRegularizer` s given by :py:func:`default_reg_list` is used.
    Otherwise it is used the list provided by the user. It returns the result
    of the regularization algorithm and returns a :class:`RegularizationResult` object
    containing the regularization of ``f``, the eigenvalues of the matrix 
    :math:`\mathcal{K}(f \otimes \overline{f})`, where :math:`K` si the operator that performs regularization
    of order :math:`k-1`, and its corresponding eigenvectors.
    The eigenvalues are a ``N`` dimensional ``numpy.andarray`` where ``N``
    is the number of eigenvalues returned by the :py:func:`RegularizationResult.eigh` 
    method of ``per_layer_regularizers[-1]`` and are returned in increasing order. 
    The eigenvectors are returned as a ``numpy.andarray`` of shape ``(f.shape,N)``. 
    The eigenvalue in position ``i`` corresponds to the eigenvector indexed at
    ``[...,i]``. There is some special behaviour in the following cases.
    
    - If ``len(per_layer_regularizers)=0``, 
        this function returns as a regularization an
        ``numpy.andarray`` array with shape equal to that of ``f``, the average of ``f``
        as the sole eigenvalue and the constant 1 ``numpy.andarray`` of shape ``f.shape``
        as the sole eigenvector.
    
    - If ``len(per_layer_regularizers)=1``, 
        this function returns the squares of the 
        Fourier coefficients along with the full Fourier basis of the group :math:`Z` as
        the eigenvalues (ordered in increasing order) and the full set of Fourier
        characters of :math:`Z` as the eigenvectors.

    :param f: An array representing the function to regularize.
    :type f: numpy.ndarray

    :param per_layer_regularizers: A list of :class:`LayerRegularizer` objects that will be set up using 
        the array ``f`` or an integer to use a default list of such length. The 
        :class:`LayerRegularizer` object at index ``i`` will perform regularization of order ``i+1``. 
        That is, ``per_layer_regularizers[0]`` will act on multiplicative derivatives of the form :math:`\Delta_{t_1}\cdots\Delta_{t_{k-1}} f` where ``len(per_layer_regularizers)=k``. 
        Similarly, ``per_layer_regularizers[1]`` will act on multiplicative derivatives of the form :math:`\Delta_{t_1}\cdots\Delta_{t_{k-2}} f`, etc.

    :type per_layer_regularizers: list of LayerRegularizer objects or an integer.

    :param rng: To have predictable behaviour in case the user uses an integer in the list of
                regularizers.
    :type rng: int | np.random.Generator | None

    :return: The regularization of ``f`` according to ``per_layer_regularizers`` and the eigenvalues 
        and eigenvectors corresponding to the last step in the process, see :class:`RegularizationResult` for more information on the format of the output.
    :rtype: RegularizationResult

    """

    # First we check if we are given an integer and we need to use a default
    # list of `LayerRegularizer`s or a custom one made by the user.
    if isinstance(per_layer_regularizers, int):
        total_depth = per_layer_regularizers
        
        # If the user provides us with an rng and an integer for detault use, 
        # we use such rng to endow the StandardLayerRegularizer with
        # the same starting seeds
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        internal_per_layer_regularizers = default_reg_list(per_layer_regularizers, rng = rng)
    else:
        total_depth = len(per_layer_regularizers)
        internal_per_layer_regularizers = per_layer_regularizers

    # We convert the type of `f` to complex
    f = f.astype(complex)

    if total_depth == 0:
        # In case of 0-th order regularization the mean of `f` is returned
        # along with the mean of `f` and the constant 1 function as eigenvector.

        avg = np.mean(f)
        return RegularizationResult(avg*np.ones_like(f), avg, np.ones_like(f))

    # Otherwise, we prepare all `LayerRegularizer` by calling the `setup` method
    # of each.
    for i in range(total_depth):
        internal_per_layer_regularizers[i].setup(f, total_depth, i)
        
    if total_depth == 1:
        # In case of 1-st order Fourier analysis, the Fourier basis along
        # with the squares of the modules of the Fourier coefficients are returned.
        
        shape = f.shape
        group_size = np.prod(shape)
        eigenvectors_frequencies = np.eye(group_size).reshape((*shape,group_size))
        eigenvectors = np.fft.ifftn(eigenvectors_frequencies, axes=tuple(range(f.ndim)), norm="forward")
        
        regularized_f, eig_vals, _ = regularize_after_setup(f, internal_per_layer_regularizers)

        index_vector = np.argsort(eig_vals.reshape(group_size))
        eigenvectors_sorted = eigenvectors[..., index_vector]
        
        return RegularizationResult(regularized_f, eig_vals[index_vector], eigenvectors_sorted)
        
    else:

        # If we have 2 or more `LayerRegularizer`s we need to apply the
        # regularization algorithm. We do it internally by calling
        # an specific function that works only when the `LayerRegularizer`s
        # are already set up.
        return RegularizationResult(*regularize_after_setup(f, internal_per_layer_regularizers))

    
def regularize_after_setup(f : np.ndarray, per_layer_regularizers : List[LayerRegularizer]):

    r"""
    Internal process that implements the main steps of the regularization.

    This function, which requires being called with :class:`LayerRegularizer` s
    already set up, performs the main recursive step in the regularization
    algorithm. See the :ref:`tutorial-denoising` for further information.

    :param f: An array representing the function to regularize.
    :type f: np.ndarray

    :param per_layer_regularizers: A list of :class:`LayerRegularizer` objects.
    :type per_layer_regularizers: List[LayerRegularizer]

    :return: The result of the regularization of ``f``, the eigenvalues, and the
        eigenvectors of the last regularization step. It follows the usual convention
        of having the eigenvector in the position ``[...,i]`` corresponds to the ``i`` th
        eigenvalue.

    :rtype: tuple(np.ndarray,np.ndarray,np.ndarray)

    """

    # We begin by updating all `LayerRegularizer`s with the appropriate
    # function that they are treating currently. The first time
    # it will be `f` and succesively it will be its multiplicative
    # derivatives :math:`\Delta_{t_1}\cdots\Delta_{t_k}f`
    total_depth = len(per_layer_regularizers)
    for i in range(total_depth):
        per_layer_regularizers[i].update(f, total_depth)

    # If we have depth 1, we need to perform classical Fourier analysis
    # We do so using the Fast Fourier Transform, which is much faster
    # and precise than calculating eigenvales and vectors using a matrix
    # (even though mathematically these processes are equivalent)
    if total_depth == 1:

        # Compute all Fourier coefficients of f
        fourier_coeffs = np.fft.fftn(f,norm="forward")

        # Norm squared of the coefficients
        norm_squared_coeffs = np.abs(fourier_coeffs)**2

        # We calculate the new weights according to the cumulative distribution function given
        # We first try to do it as a vectorized map
        try:
            weights = per_layer_regularizers[0].alpha(norm_squared_coeffs)
        except: # Otherwise we apply per_layer_regularizers[0] pointwise
            dim_f = norm_squared_coeffs.shape
            norm_squared_coeffs = norm_squared_coeffs.reshape((-1))
            for i in range(len(norm_squared_coeffs)):
                norm_squared_coeffs[i] = per_layer_regularizers[0].alpha(norm_squared_coeffs[i])
            weights = norm_squared_coeffs.reshape(dim_f)
        
        modified_coeffs = weights * fourier_coeffs

        return np.fft.ifftn(modified_coeffs, norm="forward"), norm_squared_coeffs, 0

    else: 
        # If `len(per_layer_regularizers)` is at least 2, we need to iteratively compute the
        # corresponding regularized matrix. To do so, we need to call recursively
        # to this function to perform the regularization algorithm in all
        # Z-diagonals of the matrix :math:`f\otimes \overline{f}`
        # After this is done, we project to the appropriate eigenspaces
        # with a weight determined by `per_layer_regularizers[-1]`.
        eig_vals, eig_vects =  regularize_and_decompose(f, lambda x : regularize_after_setup(x,per_layer_regularizers[:-1])[0], per_layer_regularizers[-1])
        return weighed_projection(f, eig_vals, eig_vects, per_layer_regularizers[-1]),eig_vals,eig_vects

def regularize_and_decompose(f : np.ndarray, K : Callable , layer_regularizer : LayerRegularizer ):
    r"""
    Compute the eigenvalues and eigenvectors of a regularized :math:`Z`-matrix.

    This function takes a :math:`Z`-function ``f`` (represented as a ``numpy.ndarray``), 
    computes the :math:`Z`-matrix :math:`M = f \otimes \overline{f}`, applies a regularizer ``K`` 
    to the :math:`Z`-diagonals of ``M`` to form the :math:`Z`-matrix :math:`\mathcal{K}(M)`, and 
    then returns the eigenvalues in increasing order and eigenvectors of :math:`\mathcal{K}(M)`
    ordered according to its corresponding eigenvalue.

    :param f: A :math:`Z`-function, represented as a ``numpy.ndarray``.
    :type f: np.ndarray

    :param K: A regularizer, i.e., an operator that acts on :math:`Z`-functions. 
        The operator ``K`` must be "invariant," meaning 
        :math:`K(f(\cdot+t)) = K(f)(\cdot+t)` and :math:`K(\overline{f}) = \overline{K(f)}`
        If these conditions are not met, the behavior of the function is unpredictable. 
    :type K: Callable

    :param layer_regularizer: The regularizer that contains the method for computing 
        the eigendecomposition of the matrix once the diagonals are regularized.
    :type layer_regularizer: LayerRegularizer

    :return: 
        - A ``numpy.ndarray`` of shape ``(total_dim,)`` , where ``total_dim`` is the 
            product of the elements in ``f.shape``, i.e., the size of the group :math:`Z` 
            containing the eigenvalues of the :math:`Z`-matrix :math:`\mathcal{K}(M)`, 
            appropriately normalized and ordered increasingly. 
        - A ``numpy.ndarray`` of shape ``(f.shape, total_dim)``, where ``total_dim`` 
            is as before and ``eigenvectors[...,i]`` is the eigenvector corresponding 
            to ``eigenvalue[i]``.
    :rtype: tuple (np.ndarray, np.ndarray)

    :note: The operator ``K`` must satisfy the invariance conditions for predictable behavior.

    """
    g = f
    
    # Compute M = g otimes g* 
    M = t_prod_itself(g)

    # Apply the operator K to all Z-diagonals of M
    M = apply_on_diag(M,K)

    dim_g = g.shape

    # Compute the size of the group Z
    total_dim = 1
    for i in range(len(dim_g)):
        total_dim*=dim_g[i]

    # We need M as a (usual) matrix to apply an eigenvalue decomposition
    M = M.reshape((total_dim,total_dim))

    eigenvalues, eigenvectors = layer_regularizer.eigh(M)

    # We need to reshape the eigenvectors so that they are Z-functions
    eigenvectors_reshaped = eigenvectors.reshape(*dim_g, eigenvalues.shape[0])

    # We need to normalize according to our convention of Z-matrices
    return eigenvalues/total_dim, eigenvectors_reshaped*np.sqrt(total_dim)

def weighed_projection(f : np.ndarray, eigvals : np.ndarray, eigvects : np.ndarray, layer_regularizer : LayerRegularizer):

    r"""
    Projects a function to certain eigenspaces with weights depending on eigenvalues.

    This function first computes a weight for each eigenvalue, represented by ``eigvals``. 
    Then, it projects ``f`` to all eigenspaces. Such projections are summed in a weighted 
    manner depending on the weights computer by the ``layer_regularizer`` variable according to
    its ``alpha`` method.

    :param f: A :math:`Z`-function, represented as a ``numpy.ndarray``. The function 
        :math:`f: Z \to \mathbb{C}` is assumed to be provided in this form.
    :type f: numpy.ndarray

    :param eigvals: A dimensional array of eigenvalues. It must have shape 
        ``(N,)``.
    :type eigvals: np.ndarray

    :param eigvects: An array of orthonormal eigenvectors. It must have shape 
        ``(f.shape, N)`` where ``N`` is the dimension of ``eigvals``.
    :type eigvects: np.ndarray

    :param layer_regularizer: A regularizer to be used to weight the corresponding eigenspaces.
    :type layer_regularizer: LayerRegularizer

    :return: A ``numpy.ndarray`` of shape equal to ``f.shape`` with the weighted 
        projection of ``f`` to the eigenspaces weighted according to ``layer_regularizer``.
    :rtype: np.ndarray

    :note: This function is meant to be used in conjunction with ``eig(f,K)``. 
        Undefined behaviour otherwise.

    """
    
    dim_f = f.shape
    try: # If the alpha function can be vectorized, we do it like that
        weights = layer_regularizer.alpha(eigvals)
    except: # Otherwise we apply layer_regularizer pointwise
        weights = np.zeros_like(eigvals)
        for i in range(len(eigvals)):
            weights[i] = layer_regularizer(eigvals[i])
    
    projections_to_eigenvectors = np.mean(f[...,None]*eigvects.conjugate(), axis=tuple(range(len(dim_f))))
    
    weighted_projections = projections_to_eigenvectors*weights*eigvects

    return np.sum(weighted_projections, axis = -1)

def default_reg_list(k : int, rng : int | np.random.Generator | None = None):
    r"""
    Returns a list of pre-defined regularizers.

    This function gives back a list with pre-defined regularizers that have been tested in practice.
    Namely, it returns a list of :class:`StandardLayerRegularizer` where all but the two last ones are
    initialized with ``num_eigen = 6``, the previous to the last one using the empty constructor,
    and the last one uses ``alpha_method = hofa.cdf.cutoff``.

    :param k: The length of the list, which corresponds to the order fo the regularization. If ``k`` equals 1 then this function retunrs a default list of regularizars to perform usual Fourier regularization, if ``k`` equals 2 it returns a list to perform quadratic Fourier regularization, etc. If smaller or equal to ``0`` is the same as passing ``0``.
    :type k: int

    :param rng: A random number generator for reproducibilty purposes. It is used to fix the seed of the :class:`StandardLayerRegularizer`.
    :type rng: int | np.random.Generator | None

    :return: A list of default LayerRegularizers of length ``k``
    :rtype: List[LayerRegularizer]
    """

    if not isinstance(rng, np.random.Generator):
        rng = np.random.default_rng(rng)

    per_layer_regularizers = []
    for i in range(k-2):
        per_layer_regularizers.append(StandardLayerRegularizer(num_eigen = 6, rng= rng.integers(0, 2**32 - 1)))
    if k>1:
        per_layer_regularizers.append(StandardLayerRegularizer(rng = rng.integers(0, 2**32 - 1)))
    per_layer_regularizers.append(StandardLayerRegularizer(alpha_method = hofa.cdf.cutoff, rng = rng.integers(0, 2**32 - 1)))
    return per_layer_regularizers

def move_diag_to_rows(M : np.ndarray):
    r"""
    Creates a new :math:`Z`-matrix where each row is a :math:`Z`-diagonal of ``M``.

    Inverse of :py:func:`move_rows_to_diag`. This function takes a :math:`Z`-matrix ``M`` of 
    shape ``(n_1, ..., n_k, n_1, ..., n_k)``, and returns a new matrix 
    whose rows are the :math:`Z`-diagonals of ``M``. The output matrix has the same 
    shape as ``M``. The returned matrix does not share memory with the input ``M``.

    :param M: A :math:`Z`-matrix of shape ``(n_1, ..., n_k, n_1, ..., n_k)``, where 
        :math:`n_i \ge 1`. Undefined behavior occurs if this condition is not met.
    :type M: numpy.ndarray

    :return: A :math:`Z`-matrix of the same shape as ``M``, where the elements of ``M[i, i+z]`` 
        are transferred to the output position ``[z, i]``.
    :rtype: numpy.ndarray

    :note: This function reverses the operation performed by :py:func:`move_rows_to_diag`.

    """

    dim_f = (M.shape[:int(len(M.shape)/2)])
    tam = len(dim_f)
    ones = np.ones(len(dim_f),dtype=int)
    identity = np.eye(len(dim_f),dtype=int)
    
    list_of_indices = []

    # The idea of the following code is to use broadcasting and advanced 
    #indexing to create the output. The idea is better shown in the case of 
    # Z = Z/n. This first loop will create a np.ndarray of shape (1,n) 
    # containing [0,1,...,n-1]. E.g., for n= 5 list of indices will contain 
    # array([[0, 1, 2, 3, 4]])
    
    for i in range(tam):
        index = np.concatenate((ones,((dim_f[i]-1)*identity[i]+ones)), axis=0)
        
        list_of_indices.append(
            np.arange(dim_f[i]).reshape(index)
        )

    # Continuing with the above example of Z= Z/n, this loop creates a 
    # np.ndarray of shape (n,n) with a shifted version of in every row. 
    # e.g., for n = 5 it will append to list_of_indices:
    # array([[0, 1, 2, 3, 4],
    #   [1, 2, 3, 4, 0],
    #   [2, 3, 4, 0, 1],
    #   [3, 4, 0, 1, 2],
    #   [4, 0, 1, 2, 3]])
    
    for i in range(tam):

        index = np.concatenate(((dim_f[i]-1)*identity[i]+ones,ones))
        
        list_of_indices.append(
            (list_of_indices[i]+list_of_indices[i].reshape(index)) % (dim_f[i])
        )

    # When this last line is executed, advanced indexing and broadcasting occur.
    # Going back to the n=5 example, first vector array([[0, 1, 2, 3, 4]]) 
    # is broadcasted to have shape (5,5).
    # Afterwards, advanced indexing occurs and the next line is executed
    #
    #     array([[0, 1, 2, 3, 4]   array([[0, 1, 2, 3, 4],
    #        [0, 1, 2, 3, 4],        [1, 2, 3, 4, 0],
    # M[     [0, 1, 2, 3, 4],   ,    [2, 3, 4, 0, 1],      ]
    #        [0, 1, 2, 3, 4],        [3, 4, 0, 1, 2],
    #        [0, 1, 2, 3, 4],        [4, 0, 1, 2, 3]])
    #
    # Note that then each row of the resulting matrix will contain 
    # the desired diagonal of M. The same idea works for other shapes 
    # corresponding to different abelian groups.
    
    return M[(*list_of_indices,)]

def move_rows_to_diag(M : np.ndarray):
    r"""
    Reconstructs the :math:`Z`-matrix from its row representation.

    Inverse of :py:func:`move_diag_to_rows`. This function takes a :math:`Z`-matrix ``M`` of shape 
    ``(n_1, ..., n_k, n_1, ..., n_k)``, and returns a new matrix 
    where the rows of ``M`` become the :math:`Z`-diagonals of the returned matrix. 
    The output matrix has the same shape as ``M``, and the returned values 
    do not share memory with the input matrix.

    :param M: A :math:`Z`-matrix of shape ``(n_1, ..., n_k, n_1, ..., n_k)``, 
        where :math:`n_i \ge 1`. Undefined behavior occurs if this condition is not met.
    :type M: numpy.ndarray

    :return: A :math:`Z`-matrix of the same shape as ``M``, such that for each pair ``[i, z]``, 
        ``output[i, i+z]`` equals ``M[z, i]``.
    :rtype: numpy.ndarray

    :note: This function reverses the operation performed by :py:func:`move_diag_to_rows`.

    """
    
    dim_f = (M.shape[:int(len(M.shape)/2)])
    tam = len(dim_f)
    ones = np.ones(len(dim_f),dtype=int)
    identity = np.eye(len(dim_f),dtype=int)
    
    list_of_indices = []

    # For more detail of the next loop, see the code of move_diag_to_rows
    for i in range(tam):
        index = np.concatenate(((dim_f[i]-1)*identity[i]+ones,ones))
        list_of_indices.append(
            np.arange(dim_f[i]).reshape(index)
        )

    # For more detail of the next loop, see the code of move_diag_to_rows
    list_of_indices2 = []
    for i in range(tam):

        index = np.concatenate((ones,((dim_f[i]-1)*identity[i]+ones)))

        list_of_indices2.append(
            (-(list_of_indices[i])+(list_of_indices[i]).reshape(index)) % (dim_f[i])
        )
    list_of_indices = list_of_indices2+list_of_indices

    # For more detail of the next loop, see the code of move_diag_to_rows. 
    # Here list_of_indices is slightly different to perform the inverse 
    # operation as in move_diag_to_rows, but otherwise the idea is the same.
    
    return M[(*list_of_indices,)]

def apply_on_diag(M : np.ndarray , K : Callable):
    r"""
    Apply a regularizer to all :math:`Z`-diagonals of a :math:`Z`-matrix.

    This function applies the operator ``K`` to each :math:`Z`-diagonal of the input 
    :math:`Z`-matrix ``M``. The operation is performed on the diagonals indexed by 
    ``[i, i+z]``, where the operator ``K`` is applied to the corresponding 
    values of ``M[i, i+z]``.

    :param M: A :math:`Z`-matrix of shape ``(n_1, ..., n_k, n_1, ..., n_k)``, 
        where :math:`n_i \ge 1`. Undefined behavior occurs if this condition is not met.
    :type M: numpy.ndarray

    :param K: A regularizer operator that acts on :math:`Z`-functions. The operator ``K`` 
        must be "invariant".
    :type K: Callable

    :return: A :math:`Z`-matrix of the same shape as ``M``, where for each pair ``[i, z]``, 
        ``output[i, i+z]`` equals ``K(M[i, i+z])``.
    :rtype: np.ndarray

    :note: The operator ``K`` must satisfy the invariance conditions for 
        predictable behavior.

    """
    
    M_reshaped = move_diag_to_rows(M)

    half_dim = int(len(M_reshaped.shape)/2)
    dim_f = M_reshaped.shape[:int(len(M_reshaped.shape)/2)]

    new_dim = tuple([-1]+list(dim_f))

    # For convenience, we reshape the matrix M_reshaped so that we only have to 
    # iterate through a single dimension.
    M_first_dims_flatten = np.reshape(M_reshaped,new_dim)

    # We apply the regularizer K on each of the Z-diagonals of the original matrix M
    for i in range(M_first_dims_flatten.shape[0]):
        M_first_dims_flatten[i] = K(M_first_dims_flatten[i])

    # We then put it back to its original shape, still with the diagonals in the rows
    M_back_to_normal_dims = np.reshape(M_first_dims_flatten, tuple(2*list(dim_f)))

    # And we put the diagonals back to their original positions.
    return move_rows_to_diag(M_back_to_normal_dims)

def t_prod_itself(g : np.ndarray):
    r"""
    Compute the outer product of a :math:`Z`-function with itself conjugate.

    This function takes a :math:`Z`-function ``g`` and returns the :math:`Z`-matrix formed 
    by computing the outer product of ``g`` with its conjugate transpose, 
    denoted as :math:`g\otimes \overline{g}`.

    :param g: A :math:`Z`-function. The shape of ``g`` must be compatible for the outer 
        product operation.
    :type g: numpy.ndarray

    :return: A :math:`Z`-matrix of shape ``(g.shape, g.shape)``, representing the outer 
        product of ``g`` and its conjugate transpose.
    :rtype: numpy.ndarray

    :note: The outer product is performed element-wise, and the resulting matrix 
        has a shape of ``(g.shape, g.shape)``.

    """

    dim_1 = tuple(list(g.shape)+[1]*len(g.shape))
    dim_2 = tuple([1]*len(g.shape)+list(g.shape))
    
    return (g.reshape(dim_1))*(np.conj(g).reshape(dim_2))


