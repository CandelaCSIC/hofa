r"""
This module contains the Numpy implementation for performing higher-order Fourier character decomposition 
using the spectral approach developed by Candela, González-Sánchez, and Szegedy. See the :ref:`tutorial-higher-order-char` for further information.

Conventions
-----------
The following conventions are used for functions and data structures in this file:

- Any finite abelian group :math:`Z` is isomorphic to :math:`Z/n_1Z \times Z/n_2Z \times ... \times Z/n_kZ`. Therefore, a function :math:`f: Z \to \mathbb{C}` is represented as a ``numpy.ndarray`` tensor with shape ``(n_1, n_2, ..., n_k)``.

- Sometimes we abreviate ``numpy`` by ``np``.
"""
import numpy as np
import scipy
from typing import Callable, List, NamedTuple
from abc import ABC, abstractmethod
import hofa.rgz as rgz
import hofa.cdf as cdf

from dataclasses import dataclass
import logging
logger = logging.getLogger(__name__)
r"""
Logger for this module.

This module-level logger is used to log messages related to the functionality
provided by this module. It follows the standard Python logging convention,
where the logger name is set to the module's name (``__name__``).

The logger can be used to output messages at various severity levels:
- DEBUG: Detailed information, typically of interest only when diagnosing problems.
- INFO: Confirmation that things are working as expected.

To configure the logging behavior (e.g., log level, output format, handlers),
users should configure the Python logging system at the application level.
For example:

:example:
    >>> import logging
    >>> # Configure basic logging to console
    >>> logging.basicConfig(level=logging.INFO)

:note: The actual output and visibility of log messages depends on the logging
       configuration set by the application using this module. By default,
       if no logging configuration is set, messages at WARNING level and above
       will be sent to stderr.
"""

class RandomSeparator(ABC):
    """
    Abstract base class for a policy to perform separation of higher order characters.

    This abstract class provides with an interface for the basic functionality
    to look for the higher-order components of a function using a randomized
    algorithm. See :ref:`tutorial-higher-order-char` for further details.
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def initial_threshold(self, f : np.ndarray, 
                          reg_res : rgz.RegularizationResult) -> float:
        """
        Compute the initial threshold for the given input and regularization result.
    
        This method should be implemented by subclasses to define how the initial
        threshold is determined based on the input data and the first regularization 
        outcome.
    
        :param f: Input array for which the threshold is computed.
        :type f: np.ndarray
        :param reg_res: Result of a regularization process of ``f``.
        :type reg_res: hofa.rgz.RegularizationResult
        :return: The computed threshold.
        :rtype: float
    
        :note: Subclasses must override this method. See :py:func:`StandardRandomSeparator.initial_threshold`.
        """
        pass

    @abstractmethod
    def iteration_threshold(self, f : np.ndarray, 
                            reg_res : rgz.RegularizationResult,
                            initial_f : np.ndarray, 
                            initial_reg_res : rgz.RegularizationResult) -> float:
        """
        Compute the threshold to be used in the loop for finding the higher order characters.
    
        This method should be implemented by subclasses to define how the iterative
        threshold is determined based on the iterative regularized function
        and the iterative regularization of such function.
    
        :param f: Input array for which the threshold is computed.
        :type f: np.ndarray
        :param reg_res: Result of a regularization process of the iteration.
        :type reg_res: rgz.RegularizationResult
        :return: The computed threshold.
        :rtype: float
    
        :note: Subclasses must override this method. See :py:func:`StandardRandomSeparator.iteration_threshold`.
        """
        pass

    @abstractmethod
    def separation_gap(self, f : np.ndarray, 
                            reg_res : rgz.RegularizationResult,
                            initial_f : np.ndarray, 
                            initial_reg_res : rgz.RegularizationResult) -> float:
        """
        Compute the gap required between top eigenvalues.

        This method should be implemented by subclasses to define how the iterative
        gap is determined based on the iterative regularized function
        and the iterative regularization of such function.
    
        :param f: Input array for which the threshold is computed.
        :type f: np.ndarray
        :param reg_res: Result of a regularization process of the iteration.
        :type reg_res: rgz.RegularizationResult
        :return: The computed gap.
        :rtype: float
    
        :note: Subclasses must override this method. See :py:func:`StandardRandomSeparator.separation_gap`.
        """
        pass

    @abstractmethod
    def get_rng():
        r"""
        Get the random number generator (RNG) instance used by this object.
    
        This abstract method should be implemented by subclasses to return the
        :class:`numpy.random.Generator` instance that is used internally for all
        randomized operations. This allows users to inspect the RNG state or use the
        same RNG for other operations to ensure reproducibility.
    
        The returned RNG should be the same instance used internally by the object for
        all randomized operations, such as generating random vectors or initializing
        iterative processes.
    
        :return: The random number generator instance used by this object.
        :rtype: numpy.random.Generator
    
        :note: Subclasses must override this method to return the RNG instance used
               internally. The RNG should be properly initialized during the object's
               construction (e.g., in :meth:`__init__`).
    
        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def max_iter(self, f : np.ndarray, 
                          reg_res : rgz.RegularizationResult) -> int:
        r"""
        Get the maximum number of iterations for the iterative process.
    
        This abstract method should be implemented by subclasses to define how the
        maximum number of iterations is determined based on the input data `f` and
        the regularization result `reg_res`. The returned value controls the maximum
        number of iterations allowed in iterative algorithms (e.g., during eigenvalue
        separation or character refinement).
    
        Subclasses may use `f` and `reg_res` to dynamically determine the maximum
        iterations, or they may return a fixed value set during initialization.
    
        :param f: Input data array, which may be used to determine the maximum iterations.
        :type f: numpy.ndarray
        :param reg_res: Regularization result object, which may be used to determine
                        the maximum iterations. This may include residuals, parameters,
                        or other metadata from the regularization process.
        :type reg_res: rgz.RegularizationResult
    
        :return: The maximum number of iterations to perform in iterative processes.
        :rtype: int
    
        :note: Subclasses must override this method. The implementation should define
               how the maximum iterations are determined, either dynamically (based on
               `f` and `reg_res`) or as a fixed value. For an example implementation, see
               :py:meth:`StandardRandomSeparator.max_iter`.
    
        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    def iterative_search(self) -> bool:
        r"""
        Check whether the algorithm should use iterative search.
    
        This abstract method should be implemented by subclasses to return a boolean
        indicating whether the algorithm should use an iterative approach for separation
        or a non-iterative (direct) method. This flag controls the overall strategy of the
        algorithm, where iterative search is generally faster and similarly accurate.
    
        The returned value should be determined based on the algorithm's configuration
        (e.g., parameters set during initialization) and the specific requirements of
        the subclass implementation.
    
        :return: True if iterative search is enabled, False if a non-iterative method
                 should be used.
        :rtype: bool
    
        :note: Subclasses must override this method. The implementation should return
               the value of the iterative search flag, which is typically set during
               initialization. For an example implementation, see
               :py:meth:`StandardRandomSeparator.iterative_search`.
    
        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        pass

class StandardRandomSeparator(RandomSeparator):
    r"""
    A standard implementation of :class:`RandomSeparator`.

    This constructor sets up the parameters and modes for the initialization,
    iteration, and separation phases of the algorithm. The values of ``param_initial``,
    ``param_iter``, and ``param_separation`` must be positive numbers.

    The values of ``mode_initial`` and ``mode_iter`` must
    be one of the following. In the sequel, let :math:`\sigma^2` be the variance
    of the input function
    
        - 'dynamic-relative': 
                             Let :math:`\rho` be the product of ``param`` multiplied by :math:`\sigma\sqrt{\log|Z|/|Z|}` where :math:`Z` is the group where the function we want to decompose is defined, and :math:`\sigma` is its standard deviation.
                             The parameter (the threshold or gap) will be then the middle
                             point of the largest gap of the eigenvalues of the 
                             regularization in the interval :math:`[\rho/2,\rho]`.
        - 'dynamic-strict': 
                           The parameter (the threshold or gap) will be
                           ``param`` multiplied by :math:`\sigma\sqrt{\log|Z|/|Z|}`.
        - 'literal-relative':
                             The parameter (the threshold or gap) will be the middle
                             point of the largest gap of the eigenvalues of the 
                             regularization in the interval :math:`[\text{param}/2,\text{param}]`.
        - 'literal-strict': 
                            The parameter will be ``param``.

    The values of ``mode_separation`` must be one of:

        - 'dynamic': 
                     The parameter (the threshold or gap) will be
                     ``param`` multiplied by :math:`\sigma\sqrt{\log|Z|/|Z|}`.

        - 'literal': 
                     The parameter will be ``param``.


    :param param_initial: Initial parameter value for the first phase of the algorithm.
                          Default is 1.2.
    :type param_initial: float or int
    :param mode_initial: Mode for the initialization phase. 
    :type mode_initial: str
    :param param_iter: Parameter value for the iteration phase of the algorithm.
                       Default is 1.2.
    :type param_iter: float or int
    :param mode_iter: Mode for the iteration phase. 
    :type mode_iter: str
    :param param_separation: Parameter value for the separation phase of the algorithm. Default is 1.2.
    :type param_separation: float or int
    :param mode_separation: Mode for the separation phase. 
    :type mode_separation: str
    :param random_state: Seed for the random number generator or a
                         :class:`numpy.random.Generator` instance for reproducibility.
                         If None, the global random state is used.
    :type random_state: int or numpy.random.Generator or None

    :note: The 'dynamic-relative' mode is the default for all phases and is recommended
           for most use cases. Other modes may require specific parameter values.

    :example:
        >>> separator = StandardRandomSeparator(
        ...     param_initial=1.5,
        ...     mode_initial='dynamic-strict'
        ... )
    """

    def __init__(
        self,
        param_initial : float | int = 1.2,  
        mode_initial : str = 'dynamic-relative', 
        param_iter : float | int = 1.2,  
        mode_iter : str = 'dynamic-relative',
        param_separation : float | int = 0.6,  
        mode_separation : str = 'dynamic',
        max_iterations : int = 20,
        iterative_search : bool = True,
        rng : int | np.random.Generator | None = None
    ):
    
        # Validate mode_initial
        if mode_initial not in ('dynamic-relative', 'dynamic-strict', 'literal-relative', 'literal-strict'):
            raise ValueError(
                f"mode_initial must be one of 'dynamic-relative', 'dynamic-strict', "
                f"'literal-relative', or 'literal-strict'. Got: {mode_initial}"
            )
    
        # Validate mode_iter
        if mode_iter not in ('dynamic-relative', 'dynamic-strict', 'literal-relative', 'literal-strict'):
            raise ValueError(
                f"mode_iter must be one of 'dynamic-relative', 'dynamic-strict', "
                f"'literal-relative', or 'literal-strict'. Got: {mode_iter}"
            )
    
        # Validate mode_separation
        if mode_separation not in ('dynamic', 'literal'):
            raise ValueError(
                f"mode_separation must be one of 'dynamic', "
                f"'literal'. Got: {mode_separation}"
            )

        # Validate param_initial
        if param_initial <= 0:
            raise ValueError(f"param_initial must be positive. Got: {param_initial}")
    
        # Validate param_iter
        if param_iter <= 0:
            raise ValueError(f"param_iter must be positive. Got: {param_iter}")
    
        # Validate param_separation
        if param_separation <= 0:
            raise ValueError(f"param_separation must be positive. Got: {param_separation}")

        self.param_initial = param_initial
        self.mode_initial = mode_initial

        self.param_iter = param_iter
        self.mode_iter = mode_iter

        self.param_separation = param_separation
        self.mode_separation = mode_separation

        self.max_iterations = 20

        self.do_iterative_search = iterative_search

        if isinstance(rng, np.random.Generator):
            self.rng = rng
        else:
            self.rng = np.random.default_rng(rng)

        self.group_size = 0

    def initial_threshold(self, f : np.ndarray, 
                            reg_res : rgz.RegularizationResult) -> float:
        r"""
        Compute the initial threshold value based on input data and regularization result.
    
        This method calculates an initial threshold for the eigenvalues of the algorithm.
        The threshold is determined based on the
        input data array ``f`` and the result of the regularization process contained in
        ``reg_res``. Depending on the values of ``self.param_initial`` and ``self.mode_initial``,
        the threshold is computed according to the rules described in :class:`StandardRandomSeparator`.
    
        :param f: Input data array for which the threshold is computed.
        :type f: numpy.ndarray
        :param reg_res: Regularization result object containing information needed
                        to compute the threshold.
        :type reg_res: rgz.RegularizationResult
    
        :return: The computed initial threshold value.
        :rtype: float
        """

        self.group_size = np.prod(f.shape)

        if self.mode_initial.startswith('dynamic'):
            sigma = np.sqrt(np.mean(np.square(np.abs(f-np.mean(f)))))
            rho =  self.param_initial*sigma*np.sqrt(np.log(self.group_size)/self.group_size)
            if self.mode_initial == 'dynamic-relative':
                return find_middle_point_of_largest_gap(reg_res.eigenvalues, rho/2, rho)
            else: # 'dynamic-strict'
                return rho
        else: # starting with 'literal'
            if self.mode_initial == 'literal-relative':
                return find_middle_point_of_largest_gap(reg_res.eigenvalues, param/2, param)
            else: # 'literal-strict'
                return param

    def iteration_threshold(self, f : np.ndarray, 
                            reg_res : rgz.RegularizationResult,
                            initial_f : np.ndarray, 
                            initial_reg_res : rgz.RegularizationResult) -> float:
        r"""
        Compute the iteration threshold value based on input data and regularization result.
    
        This method calculates an iteration threshold for the eigenvalues.
        The threshold is determined based on the
        input data array ``f`` and the result of the regularization process contained in
        ``reg_res``. Depending on the values of ``self.param_iteration`` and ``self.mode_iteration``,
        the threshold is computed according to the rules described in :class:`StandardRandomSeparator`.
    
        :param f: Input data array for which the threshold is computed.
        :type f: numpy.ndarray
        :param reg_res: Regularization result object containing information needed
                        to compute the threshold.
        :type reg_res: rgz.RegularizationResult
    
        :return: The computed initial threshold value.
        :rtype: float
        """

        if self.mode_iter.startswith('dynamic'):
            sigma = np.sqrt(np.mean(np.square(np.abs(f-np.mean(f)))))
            rho =  self.param_iter*sigma*np.sqrt(np.log(self.group_size)/self.group_size)
            if self.mode_iter == 'dynamic-relative':
                return find_middle_point_of_largest_gap(reg_res.eigenvalues, rho/2, rho)
            else: # 'dynamic-strict'
                return rho
        else: # starting with 'literal'
            if self.mode_iter == 'literal-relative':
                return find_middle_point_of_largest_gap(reg_res.eigenvalues, param/2, param)
            else: # 'literal-strict'
                return param

    def separation_gap(self, f : np.ndarray, 
                            reg_res : rgz.RegularizationResult,
                            initial_f : np.ndarray, 
                            initial_reg_res : rgz.RegularizationResult) -> float:
        r"""
        Compute the separation gap value based on input data and regularization result.
    
        This method calculates an separation gap for the eigenvalues.
        The threshold is determined based on the
        input data array ``f`` and the result of the regularization process contained in
        ``reg_res``. Depending on the values of ``self.param_separation`` and ``self.mode_separation``,
        the threshold is computed according to the rules described in :class:`StandardRandomSeparator`.
    
        :param f: Input data array for which the threshold is computed.
        :type f: numpy.ndarray
        :param reg_res: Regularization result object containing information needed
                        to compute the threshold.
        :type reg_res: rgz.RegularizationResult
    
        :return: The computed initial threshold value.
        :rtype: float
        """

        if self.mode_separation.startswith('dynamic'):
            sigma = np.sqrt(np.mean(np.square(np.abs(f-np.mean(f)))))
            return self.param_separation*sigma*np.sqrt(np.log(self.group_size)/self.group_size)
        else: # starting with 'literal'
            return param

    def get_rng(self):
        r"""
        Get the random number generator (RNG) instance used by this object.

        This method returns the :class:`numpy.random.Generator` instance that is used
        internally for all randomized operations.

        :return: The random number generator instance used by this object.
        :rtype: numpy.random.Generator
        
        :note: The returned RNG is the same instance used internally by this object.
                Modifying its state (e.g., by calling its methods) may affect the reproducibility
                of this object's operations.
        """
        return self.rng

    def max_iter(self, f : np.ndarray, 
                          reg_res : rgz.RegularizationResult) -> int:
        r"""
        Get the maximum number of iterations for the iterative process.
    
        This method returns the maximum number of iterations ``self.max_iterations``
        that will be used in iterative algorithms (e.g., during eigenvalue separation).
        The input parameters ``f`` and ``reg_res`` are accepted for consistency with the 
        abstract :class:`RandomSeparator` but are not used in this implementation.
    
        :param f: Input data array. This parameter is accepted for consistency but is not used.
        :type f: numpy.ndarray
        :param reg_res: Regularization result object. This parameter is accepted for consistency
                        but is not used.
        :type reg_res: rgz.RegularizationResult
    
        :return: The maximum number of iterations, as set during initialization.
        :rtype: int
    
        :note: This method is designed to be overridden in subclasses to allow dynamic
               determination of the maximum iterations based on ``f`` and ``reg_res``.
               In this base implementation, it simply returns ``self.max_iterations``.
        """
        return self.max_iterations

    def iterative_search(self) -> bool:
        r"""
        Check whether the algorithm should use iterative search.
    
        This method returns the value of ``self.do_iterative_search``, which determines
        whether the algorithm will use an iterative approach for separation or a
        non-iterative (direct) method.
    
        :return: True if iterative search is enabled, False otherwise.
        :rtype: bool
    
        :note: This flag is typically set during initialization and controls whether the
               algorithm will iterate to refine the separation (if True) or try to
               find all eigenvectors at once (if False). Iterative search is generally 
               faster and similarly accurate.
        """
        return self.do_iterative_search
        

class RandomizedSeparationResult(NamedTuple):
    r"""
    A container for the results of a randomized separation algorithm.

    This ``NamedTuple`` stores the outputs of a randomized algorithm that separates
    higher-order characters and eigenvalues. It provides information about the
    separation process, including whether the separation was successful, the
    threshold used, and the number of iterations performed.

    If the input function was :math:`f:Z\to \mathbb{C}`, then the content of
    the following attributes of this ``NamedTuple`` is as follows.

    :ivar higher_order_char: The computed higher-order characters after separation.
                             The shape of this varible is ``(f.shape,N)`` where
                             ``N`` is the number of higher-order components found.
                             If :math:`v_i` for :math:`i=0,\ldots,N-1` are the elements
                             ``higher_order_char[...,i]``, then the decomposition of the
                             structured part of :math:`f` into higher order components is
                             :math:`\sum_{i=0}^{N-1}\langle f,v_i\rangle v_i`.
    :vartype higher_order_char: numpy.ndarray

    :ivar separated_eigenvalues: The eigenvalues obtained after separation.
                                  This is a 1D numpy array of shape ``(N,)``. The
                                  eigenvalue at position ``i`` corresponds to the higher-order
                                  character ``higher_order_char[...,i]``.
    :vartype separated_eigenvalues: numpy.ndarray

    :ivar are_separated: Boolean flag indicating whether the separation was successful.
                         ``True`` if the characters and eigenvalues were successfully separated
                         according to the algorithm's criteria, ``False`` otherwise. In case
                         ``False`` is returned, the values in the other variables correspond to 
                         values found so far, which are higher-order components of the function.
    :vartype are_separated: bool

    :ivar separation_threshold: The threshold value used for the separation process.
                                 This value determines the criterion for successful separation.
                                 If the iterative search was active, it returns only the value of 
                                 the last separation threshold.
    :vartype separation_threshold: float

    :ivar total_iterations: The total number of iterations performed by the separation
                            algorithm before termination.
    :vartype total_iterations: int

    :note: The ``are_separated`` flag
           should be checked to verify if the separation was successful before using
           the results.

    :example:
        >>> # Assuming 'result' is returned by a separation function
        >>> if result.are_separated:
        ...     print("Separation successful!")
        ...     print("Higher-order characters:", result.higher_order_char)
        ...     print("Eigenvalues:", result.separated_eigenvalues)
        ... else:
        ...     print("Separation failed after", result.total_iterations, "iterations")
    """

    higher_order_char : np.ndarray
    separated_eigenvalues : np.ndarray
    are_separated : bool
    separation_threshold : float
    total_iterations : int


class RandomizedSearchCallback(ABC):
    r"""
    Abstract base class for callback objects used during randomized search algorithms.

    This class defines the interface for callback objects that can be used to monitor
    the progress of the randomized search algorithm at every iteration. Subclasses 
    should implement the callback methods to perform custom actions.
    """
    
    def on_iteration(self, 
                     iteration_count : int, 
                     eigenvalues_found : int,
                     number_eigenvales_separated : int,
                     iteration_rho : float,
                     separation_delta : float,
                     f_reg_iteration : rgz.RegularizationResult,
                     rnd_separator : RandomSeparator,
                     number_of_eig_already_found : int,
                     target_number_eigenvalues : int
                    ):
        r"""
        Callback method invoked after each iteration of the randomized search algorithm.

        This method is called at each iteration just after computing the regularization
        of the particular function from which we want to obtain the higher order
        characters, providing information about the current state of the algorithm. 
        Subclasses should override this method to implement custom behavior, 
        such as printing progress updates, logging metrics, or updating visualizations.

        :param iteration_count: The current iteration index (0-based).
        :type iteration_count: int
        :param eigenvalues_found: The total number of eigenvalues found so far.
        :type eigenvalues_found: int
        :param number_eigenvales_separated: The number of eigenvalues successfully separated
                                             in the current iteration.
        :type number_eigenvales_separated: int
        :param iteration_rho: The threshold used during the current iteration.
        :type iteration_rho: float
        :param separation_delta: The separation gap or threshold used during the current iteration.
        :type separation_delta: float
        :param f_reg_iteration: The regularization result object for the current iteration.
        :type f_reg_iteration: rgz.RegularizationResult
        :param rnd_separator: The random separator object.
        :type rnd_separator: RandomSeparator
        :param number_of_eig_already_found: The cumulative number of eigenvalues found
                                             before this iteration.
        :type number_of_eig_already_found: int
        :param target_number_eigenvalues: The target number of eigenvalues to find.
        :type target_number_eigenvalues: int

        :note: Subclasses must override this method to implement custom behavior.
               The base implementation does nothing.
        """
        pass

    def on_end(self, 
               iteration_count : int, 
               rnd_separator : RandomSeparator,
               number_of_eig_already_found : int,
               target_number_eigenvalues : int):
        r"""
        Callback method invoked at the end of the randomized search algorithm.

        This method is called once when the algorithm terminates, providing a summary
        of the final state. Subclasses should override this method to implement custom
        behavior, such as printing a summary, logging final results, or cleaning up resources.

        :param iteration_count: The total number of iterations performed.
        :type iteration_count: int
        :param rnd_separator: The random separator object used during the final iteration.
        :type rnd_separator: RandomSeparator
        :param number_of_eig_already_found: The total number of eigenvalues found by the algorithm.
        :type number_of_eig_already_found: int
        :param target_number_eigenvalues: The target number of eigenvalues to find.
        :type target_number_eigenvalues: int

        :note: Subclasses must override this method to implement custom behavior.
               The base implementation does nothing.
        """
        pass

class PrintRandomizedSearchCallback(RandomizedSearchCallback):
    r"""
    A concrete callback class that prints progress updates during randomized search.

    This class implements the :class:`RandomizedSearchCallback` interface to provide
    real-time progress updates during the execution of a randomized search algorithm.
    It prints information about each iteration and a summary at the end of the process,
    allowing users to monitor the algorithm's progress directly in the console.

    The output is formatted to update on a single line during iterations,
    providing a clean and compact progress display. At the end of the process, a summary
    line is printed with the final results.

    :example:
        >>> callback = PrintRandomizedSearchCallback()
        >>> # Pass the callback to your randomized search function
        >>> result = spechoft(f, callback=callback)
    """
    def on_iteration(self, 
                     iteration_count : int, 
                     eigenvalues_found : int,
                     number_eigenvales_separated : int,
                     iteration_rho : float,
                     separation_delta : float,
                     f_reg_iteration : rgz.RegularizationResult,
                     rnd_separator : RandomSeparator,
                     number_of_eig_already_found : int,
                     target_number_eigenvalues : int
                    ):
        r"""
        Print progress information for the current iteration.

        This method prints a compact progress update for each iteration of the
        randomized search algorithm. The output is formatted to overwrite the
        previous line (using ``\r``), creating a dynamic progress display in the console.

        The printed information includes:
        - Current iteration count
        - Number of eigenvalues found in this iteration
        - Number of eigenvalues separated in this iteration
        - Whether iterative search is enabled
        - Cumulative number of eigenvalues found so far
        - Target number of eigenvalues

        :param iteration_count: Current iteration index (0-based).
        :type iteration_count: int
        :param eigenvalues_found: Number of eigenvalues found in this iteration.
        :type eigenvalues_found: int
        :param number_eigenvales_separated: Number of eigenvalues successfully separated
                                             in this iteration.
        :type number_eigenvales_separated: int
        :param iteration_rho: Current value of the rho parameter (not printed but available).
        :type iteration_rho: float
        :param separation_delta: Current separation delta (not printed but available).
        :type separation_delta: float
        :param f_reg_iteration: Regularization result for this iteration (not used but available).
        :type f_reg_iteration: rgz.RegularizationResult
        :param rnd_separator: Random separator object used in this iteration.
        :type rnd_separator: RandomSeparator
        :param number_of_eig_already_found: Cumulative number of eigenvalues found so far.
        :type number_of_eig_already_found: int
        :param target_number_eigenvalues: Target number of eigenvalues to find.
        :type target_number_eigenvalues: int

        """
        print(f"Iter {iteration_count}, eig vals found={eigenvalues_found}, eig vals separated={number_eigenvales_separated}, iterative search = {rnd_separator.iterative_search()}, eig vals already found = {number_of_eig_already_found}, target eig vals = {target_number_eigenvalues}", end = '\r')

    def on_end(self, 
               iteration_count : int, 
               rnd_separator : RandomSeparator,
               number_of_eig_already_found : int,
               target_number_eigenvalues : int):
        r"""
        Print a summary of the randomized search results at the end of the process.

        This method prints a summary line with the final results of the randomized
        search algorithm, including:
        - Total number of iterations performed
        - Whether iterative search was used
        - Total number of eigenvalues found
        - Target number of eigenvalues

        Unlike the iteration updates, this summary is printed as a new line to ensure
        it remains visible after the process completes.

        :param iteration_count: Total number of iterations performed.
        :type iteration_count: int
        :param rnd_separator: Random separator object used in the final iteration.
        :type rnd_separator: RandomSeparator
        :param number_of_eig_already_found: Total number of eigenvalues found.
        :type number_of_eig_already_found: int
        :param target_number_eigenvalues: Target number of eigenvalues to find.
        :type target_number_eigenvalues: int

        """
        
        print(f"Total number of iterations {iteration_count}, iterative search = {rnd_separator.iterative_search()}, eig vals found = {number_of_eig_already_found}, target num eig vals = {target_number_eigenvalues}                                                                                     ")




def spechoft(f : np.ndarray, 
             order : int | List[rgz.LayerRegularizer] = 2,
             rnd_separator : RandomSeparator | None = None,
             iteration_regularizers : List[rgz.LayerRegularizer] | None = None,
             rng : np.random.Generator | int | None = None,
             callback: RandomizedSearchCallback | None = None) -> RandomizedSeparationResult:
    r"""
    Find higher-order characters using a randomized algorithm with customizable regularization.

    This function implements a randomized algorithm to identify higher-order characters
    in the input data using a separation approach. We refer the reader to the online 
    documentation for a more detailed account on the theory behind this algorithm.

    The process roughly involves:
    1. Initial separation using the provided random separator and initial regularizers.
    2. Iterative trial an error until we find a separating function using the iteration-phase regularizers.
    3. Termination when an appropriate function is found or when max_iterations is reached.

    The function returns a comprehensive result object containing the separated
    higher-order characters, eigenvalues, and metadata about the separation process.

    :param f: Input data array for which to find higher-order characters.
              The function from which to obtain the higher order characters.
    :type f: numpy.ndarray
    :param order: Order of the higher-order characters to compute, or a list of layer regularizers.
                  Can be either:
                  - An integer specifying the order (default is 2).
                  - A list of :class:`rgz.LayerRegularizer` objects for more fine-grained control.
                  Default is 2.
    :type order: int or List[rgz.LayerRegularizer]
    :param rnd_separator: Random separator object to use for the separation process.
                          If None, a default random separator will be created.
                          The separator defines the strategy for separating eigenvalues and characters.
    :type rnd_separator: RandomSeparator or None
    :param iteration_regularizers: List of layer regularizers to use during the iteration phase.
                                    If None, a copy of the regularizers given in the ``order``
                                    variable is used.
    :type iteration_regularizers: List[rgz.LayerRegularizer] or None
    :param rng: Random number generator or seed for reproducibility.
                If ``None`` parameters are used for the variables ``order`` and ``iteration_regularizers``,
                then this random number generator will be used to generate them,
                ensuring predictable outcome if the ``rng`` is either a :class:`numpy.random.Generator`
                instance or an integer.
                Can be either:
                - A :class:`numpy.random.Generator` instance.
                - An integer seed (which will be used to create a Generator).
                - None, in which case the global random state is used.
                Default is None.
    :type rng: numpy.random.Generator or int or None
    :param callback: Optional callback object for monitoring progress.
                     Should be an instance of :class:`RandomizedSearchCallback`.
                     If provided, the callback's methods will be invoked during the algorithm's execution.
                     Default is None.
    :type callback: RandomizedSearchCallback or None

    :return: A named tuple containing the results of the spectral decomposition.
             The result includes:
             
             - higher_order_char: The computed higher-order characters.
             - separated_eigenvalues: The separated eigenvalues.
             - are_separated: Boolean indicating if separation was successful.
             - separation_threshold: The threshold used for separation.
             - total_iterations: Number of iterations performed.

             See :class:`RandomizedSeparationResult` for a detailed account on the structure of the output.


    :rtype: RandomizedSeparationResult

    :note: The quality of the results depends on the choice of random separator and
           regularizers. The ``'dynamic-relative'`` mode in the random separator often
           provides a good balance between speed and accuracy.

           If ``per_layer_regularizers_initial`` or ``per_layer_regularizers_iteration`` is an
           integer, default regularizers will be created for each layer.

           For reproducible results, provide a fixed seed or Generator for the ``rng`` parameter.

    :example:
        >>> import numpy as np
        >>> import hofa.char
        >>>
        >>> # Create input data
        >>> n = 501
        >>> f = np.sin(2*np.pi*x**2/n)
        >>>
        >>> # Run the algorithm with default parameters
        >>> result = hofa.char.spechoft(f)
        >>>
        >>> # Check if separation was successful
        >>> if result.are_separated:
        ...     print("Separation successful!")
        ...     print("Higher-order characters: ", result.higher_order_char)
        ... else:
        ...     print("Separation failed after ", result.total_iterations, " iterations")
    """


    # If we are not given a RNG, we create one which will be used for 
    # creating the different seeds for the LayerRegularizers and the RandomSeparator
    if not isinstance(rng, np.random.Generator):
        rng = np.random.default_rng(rng)

    # First we check if we are given an integer to use a default list of
    # regularizers
    if isinstance(order, int):
        per_layer_regularizers_initial = rgz.default_reg_list(order, rng)

    # For the iterations, we give the possibility to use a different regularizer
    # or use the same as the initial one.
    if iteration_regularizers is None:
        per_layer_regularizers_iteration = [layer_reg.copy() for layer_reg in per_layer_regularizers_initial]
    else:
        # In case the user chooses to give a custom regularizer, we check that
        # it performs decomposition of the same order.
        if len(iteration_regularizers)!=len(per_layer_regularizers_initial):
            raise ValueError(f"iteration_regularizers must have the same length {len(iteration_regularizers)} as the given order {len(per_layer_regularizers_initial)}")

    # If we are not given a custom made RandomSeparator we create our own 
    # using (if provided) the rng given by the user
    if rnd_separator is None:
        rnd_separator = StandardRandomSeparator(rng = rng.integers(0, 2**32 - 1))

    # Start of the internal logic of the algorithm
    f_reg_initial = rgz.regularize(f, per_layer_regularizers_initial)

    initial_rho = rnd_separator.initial_threshold(f, f_reg_initial)

    initial_mask = f_reg_initial.eigenvalues > initial_rho

    target_number_eigenvalues = np.sum(initial_mask)

    iteration_count = 0 

    higher_order_char_found = np.zeros((*f.shape, target_number_eigenvalues), dtype=complex)
    higher_order_eigenvalues_found = np.zeros((target_number_eigenvalues,), dtype=float)

    number_of_eig_already_found = 0

    h = f_reg_initial.regularization.copy()
    separation_delta = -1

    max_iterations = rnd_separator.max_iter(f,f_reg_initial)
    
    while( iteration_count < max_iterations and number_of_eig_already_found < target_number_eigenvalues):

        f_reg_iteration = rgz.regularize(h , per_layer_regularizers_iteration)

        iteration_rho = rnd_separator.iteration_threshold(h , f_reg_iteration, f, f_reg_initial)

        mask = f_reg_iteration.eigenvalues > iteration_rho
        
        eigenvalues_found = np.sum(mask)

        separation_delta = rnd_separator.separation_gap(h,f_reg_iteration, f, f_reg_initial)
        mask_individual_sep = individual_eigenvals_separated(f_reg_iteration.eigenvalues[mask], \
                                                                 separation_delta)

        number_eigenvales_separated = np.sum(mask_individual_sep)

        # --- logging ---
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "Iter %d | eig vals found = %d | eig vals separated = %d | iterative search = %s | minimum threshold = %.3f | separation threshold = %.3f | cummulative eig vals found = %d | target number eig vals = %d",
                iteration_count,
                eigenvalues_found,
                number_eigenvales_separated,
                rnd_separator.iterative_search(),
                iteration_rho,
                separation_delta,
                number_of_eig_already_found,
                target_number_eigenvalues
            )
        elif logger.isEnabledFor(logging.INFO):
            logger.info(
                "Iter %d | eig vals found=%d | eig vals separated=%d | iterative search = %s | cummulative eig vals found = %d | target number eig vals = %d",
                iteration_count,
                eigenvalues_found,
                number_eigenvales_separated,
                rnd_separator.iterative_search(),
                number_of_eig_already_found,
                target_number_eigenvalues
            )

        # --- callback ---
        if callback is not None:
            callback.on_iteration(iteration_count, 
                                  eigenvalues_found,
                                  number_eigenvales_separated,
                                  iteration_rho,
                                  separation_delta,
                                  f_reg_iteration,
                                  rnd_separator,
                                  number_of_eig_already_found,
                                  target_number_eigenvalues
                                 )

        # If we do not want iterative addition of eigenvectors
        # and we have not found all, we force False on the mask
        # for every eigenvalue
        if not rnd_separator.iterative_search() and number_eigenvales_separated < target_number_eigenvalues:
            mask_individual_sep = np.full(len(mask_individual_sep), False)
            number_eigenvales_separated = 0

        
        # If we have found something, we record it
        if number_eigenvales_separated > 0:

            if number_eigenvales_separated > ( target_number_eigenvalues - number_of_eig_already_found):
                mask_individual_sep[:-( target_number_eigenvalues - number_of_eig_already_found)] = np.full(len(mask_individual_sep[:-( target_number_eigenvalues - number_of_eig_already_found)]), False)

            significant_eigenvectors = f_reg_iteration.eigenvectors[...,-eigenvalues_found:]
            significant_eigenvalues = f_reg_iteration.eigenvalues[-eigenvalues_found:]
            
            eigenvectors_to_add = significant_eigenvectors[...,mask_individual_sep]
            eigenvalues_to_add = significant_eigenvalues[...,mask_individual_sep]

            # We record our new findings
            higher_order_char_found[...,number_of_eig_already_found:min(number_of_eig_already_found \
                +number_eigenvales_separated,target_number_eigenvalues)] = eigenvectors_to_add
            higher_order_eigenvalues_found[...,number_of_eig_already_found:min(number_of_eig_already_found \
                +number_eigenvales_separated,target_number_eigenvalues)] = eigenvalues_to_add

            # And we update f and f_reg_initial accordingly
            projections_to_new_eigenvectors = np.mean(f[...,None]*higher_order_char_found.conjugate(), axis=tuple(range(len(f.shape))))

            h = f-np.sum(higher_order_char_found*projections_to_new_eigenvectors, axis = -1)

            f_reg_initial = rgz.regularize(h, per_layer_regularizers_initial)

            initial_rho = rnd_separator.initial_threshold(h, f_reg_initial)

            initial_mask = f_reg_initial.eigenvalues > initial_rho

            number_of_eig_already_found+= number_eigenvales_separated

        # And if we have not managed to get a separated eigenvalue, we need to do random 
        # sampling to try to look for new candidates
        else:

            rnd_vector = random_complex_unit_vector(rnd_separator.get_rng(), np.sum(initial_mask))

            h = np.sum(f_reg_initial.eigenvectors[...,initial_mask]*rnd_vector, axis = -1)

        iteration_count+=1

    if callback is not None:
        callback.on_end(iteration_count, 
                        rnd_separator,
                        number_of_eig_already_found,
                        target_number_eigenvalues
                       )
    
    return RandomizedSeparationResult(higher_order_char = higher_order_char_found,
                                      separated_eigenvalues = higher_order_eigenvalues_found,
                                      are_separated = (number_of_eig_already_found == target_number_eigenvalues).item(),
                                      separation_threshold = separation_delta,
                                      total_iterations = iteration_count)
    

def find_middle_point_of_largest_gap(x_array : np.ndarray, lower_end : float, upper_end : float) -> float:
    r"""
    Find the midpoint of the largest gap in a filtered array within specified bounds.

    This auxiliary function identifies the largest gap between consecutive elements in a filtered
    version of the input array, where only elements within the range ``[lower_end, upper_end]``
    are considered. The midpoint of this largest gap is then returned. 

    :param x_array: Input array of values. Can contain any real numbers.
    :type x_array: numpy.ndarray
    :param lower_end: Lower bound of the range to consider. Values in ``x_array`` below this are ignored.
                      Its value must be lower than ``upper_end``, undefined behaviour otherwise.
    :type lower_end: float
    :param upper_end: Upper bound of the range to consider. Values in ``x_array`` above this are ignored.
                      Its value must be higher than ``lower_end``, undefined behaviour otherwise.
    :type upper_end: float

    :return: The midpoint of the largest gap in the filtered and extended array.
             This is returned as a Python float scalar.
    :rtype: float

    :note: If all elements in x_array are outside the ``[lower_end, upper_end]`` range,
           the function will return the midpoint between ``lower_end`` and ``upper_end``.
           If there are no gaps (all elements are identical), the function will
           return one of the boundary points.

    :example:
        >>> import numpy as np
        >>> import hofa.char
        >>> x = np.array([1.0, 2.0, 3.5, 4.0, 6.0, 7.0, 11.0])
        >>> c = hofa.char.find_middle_point_of_largest_gap(x, 3.0, 7.0)
        >>> print(c)
        5.0
    """
    # Filter x to only include elements in [lower_end, upper_end]
    mask = (x_array >= lower_end) & (x_array <= upper_end)
    x_filtered = x_array[mask]
    # Concatenate lower_end, x_filtered, upper_end
    extended = np.concatenate(([lower_end], x_filtered, [upper_end]))
    # Compute gaps
    gaps = extended[1:] - extended[:-1]
    # Find the largest gap
    max_gap_index = np.argmax(gaps)
    # The optimal c is the midpoint of the largest gap
    c = (extended[max_gap_index] + extended[max_gap_index + 1]) / 2
    return c.item()


def eigenvals_separated(eig_vals, delta) -> bool:
    r"""
    Check if eigenvalues are sufficiently separated based on a minimum gap threshold.

    This function determines whether the eigenvalues in the input array are separated by
    at least the specified threshold ``delta``. It computes the gaps between consecutive
    eigenvalues and checks if all gaps are greater than ``delta``.

    If there are fewer than 2 eigenvalues, the function returns ``True`` by convention,
    as separation is trivially satisfied.

    :param eig_vals: 1D array of eigenvalues, sorted in ascending order.
                     The function assumes the input is sorted; if not, results may be incorrect.
    :type eig_vals: numpy.ndarray
    :param delta: Minimum required gap between consecutive eigenvalues.
                  If all gaps are greater than ``delta``, the eigenvalues are considered separated.
    :type delta: float

    :return: True if all gaps between consecutive eigenvalues are greater than ``delta``,
             or if there are fewer than 2 eigenvalues. False otherwise.
    :rtype: bool

    :note: This function assumes that ``eig_vals`` is sorted in ascending order.
           If the input is not sorted, call ``np.sort(eig_vals)`` first or sort the array
           before passing it to this function.

    :example:
        >>> import numpy as np
        >>> import hofa.char
        >>> eig_vals = np.array([1.0, 2.5, 4.0, 5.5])
        >>> print(hofa.char.eigenvals_separated(eig_vals, 1.0))  # True, all gaps > 1.0
        True
        >>> print(hofa.char.eigenvals_separated(eig_vals, 1.5))  # False, gap between 2.5 and 4.0 is 1.5 (not > 1.5)
        False
        >>> print(hofa.char.eigenvals_separated(np.array([1.0]), 1.0))  # True, fewer than 2 eigenvalues
        True
    """

    if len(eig_vals)<2:
        return True

    gaps = eig_vals[1:] - eig_vals[:-1]
    return (delta < np.min(gaps)).item()


def random_complex_unit_vector(rng: np.random.Generator, dim : int) -> np.ndarray:
    r"""
    Generate a random complex vector with unit :math:`\ell^2` norm.

    This function creates a random unit complex vector of the specified dimension.

    :param rng: Random number generator instance for reproducibility.
                Use :func:`numpy.random.default_rng` to create a generator with a seed
                for reproducible results.
    :type rng: numpy.random.Generator
    :param dim: Dimension of the complex vector to generate, must be at least 1.
    :type dim: int

    :return: A complex vector of shape ``(dim,)`` with unit norm.
             Each element is a complex number with real and imaginary parts
             drawn from a standard normal distribution.
    :rtype: numpy.ndarray

    :note: The returned vector has a unit :math:`\ell^2` norm, meaning that the sum of the
           squared magnitudes of all components equals 1.

    :example:
        >>> import numpy as np
        >>> import hofa.char
        >>> rng = np.random.default_rng(seed=42)  # For reproducibility
        >>> vec = hofa.char.random_complex_unit_vector(rng, dim=5)
        >>> print(vec.shape) 
        (5,)
        >>> print(np.isclose(np.linalg.norm(vec), 1.0))
        True
    """
    
    # Generate random complex vector (Gaussian distribution)
    real = rng.standard_normal(dim)
    imag = rng.standard_normal(dim)
    z = real + 1j * imag

    # Normalize to unit norm
    norm = np.linalg.norm(z)  # L2 norm
    return z / norm


def individual_eigenvals_separated(eigenvals: np.ndarray, threshold: float) -> np.ndarray:
    """Return a boolean mask indicating which eigenvalues are separated from their neighbors by at least ``threshold``.

    Args:
        eigenvals: 1D array of shape ``(n,)`` containing real numbers in increasing order.
        threshold: Minimum distance required for an eigenvalue to be considered separated.

    Returns:
        np.ndarray: Boolean mask of shape ``(n,)``, where ``res[i]`` is ``True`` if ``eigenvals[i]`` is separated from its neighbors.
    """
    n = eigenvals.size
    res = np.ones(n, dtype=bool)  # Initialize all as True (endpoints will be handled separately)

    # Handle interior points (i=1 to i=n-2)
    res[1:n-1] = (
        (eigenvals[1:n-1] - eigenvals[0:n-2] >= threshold) &
        (eigenvals[2:n] - eigenvals[1:n-1] >= threshold)
    )

    # Handle left endpoint (i=0)
    if n >= 2:
        res[0] = (eigenvals[1] - eigenvals[0] >= threshold)

    # Handle right endpoint (i=n-1)
    if n >= 2:
        res[-1] = (eigenvals[-1] - eigenvals[-2] >= threshold)

    return res

