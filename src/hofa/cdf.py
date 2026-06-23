"""
This module contains the implementation of different *alpha* (weighting) functions to be
used as weights for different eigenspaces depending on their eigenvalues. See the :ref:`tutorial-denoising` for further information.

Conventions
-----------

- Sometimes we abreviate ``numpy`` by ``np``.
"""
import numpy as np


def relu(eigvals : np.ndarray, epsilon : float):

    r"""
    The cumulative distribution function that performs the denoising operator.

    This function computes :math:`\max(1-\tfrac{\varepsilon}{\max(\sqrt{x},\varepsilon/2)},0)` for each eigenvalue :math:`x` in ``eigvals`` where ``epsilon`` equals :math:`\varepsilon`.

    :param eigvals: A 1-D array of eigenvalues to which the cumulative distribution function of the denoising operator with parameter ``epsilon`` is applied.
    :type eigvals: np.ndarray
    :param epsilon: A small constant used to adjust the threshold behavior of the denoising operator.
    :type epsilon: float

    :return: An array of the same shape as ``eigvals``, with the weights that perform the same operation
             as the denoising operator with parameter ``epsilon``.
    :rtype: np.ndarray
    """
    return np.maximum(1-epsilon/np.maximum(epsilon/2,np.sqrt(np.maximum(eigvals,0))),0)

def cutoff(eigvals : np.ndarray, epsilon : float):

    r"""
    Apply a cutoff operator to some eigenvalues, returning a boolean mask.

    This function returns ``True`` for all eigenvalues that are greater than or equal to :math:`\varepsilon^2`, 
    and ``False`` otherwise where ``epsilon`` equals :math:`\varepsilon`. In other words, it applies the map :math:`=1_{[\varepsilon^2,\infty)}(x)` for every :math:`x` in ``eigvals``.

    :param eigvals: A 1-D array of eigenvalues to apply the cutoff function to.
    :type eigvals: np.ndarray

    :param epsilon: A threshold value. Eigenvalues greater than or equal to :math:`\varepsilon^2` are kept.
    :type epsilon: float

    :return: A boolean array of the same shape as ``eigvals``, where ``True`` indicates that the eigenvalue 
            passes the cutoff condition.
    :rtype: np.ndarray
    """

    return (eigvals>=np.square(epsilon))

def avg_cutoff(eigvals : np.ndarray, epsilon : float):

    r"""
    Apply an average cutoff function to eigenvalues, scaling them by ``epsilon``.

    This function computes :math:`\min \Big( \tfrac{ \sqrt{\max ( \varepsilon^2, x )}}{\varepsilon} - 1, 1 \Big)` for each eigenvalue :math:`x` in ``eigvals``.

    :param eigvals: A 1-D array of eigenvalues to apply the average cutoff function to.
    :type eigvals: np.ndarray

    :param epsilon: A scaling factor used in the cutoff function. Smaller values of ``epsilon`` yield a stronger cutoff.
    :type epsilon: float

    :return: An array of the same shape as ``eigvals``, with the average cutoff transformation applied element-wise.
    :rtype: np.ndarray
    """

    return np.minimum(np.sqrt(np.maximum(np.square(epsilon),eigvals))/epsilon-1,1)

def top_eig(eigvals : np.ndarray, n : int):

    """
    Give a mask that selects the top eigenvalues.

    This function returns a 1-D vector with the same shape as ``eigvals``, consisting
    of all zeroes except in the positions of the largest ``n`` terms, which are ones.

    :param eigvals: A 1-D array of eigenvalues to apply the mask function to. 
    :type eigvals: np.ndarray

    :param n: The number of eigenvalues to select.
    :type n: int

    :return: An array of the same shape as ``eigvals``, containing zeros except at the first 
            ``n`` positions, which are ones.
    :rtype: np.ndarray
    """
    n_largest = np.partition(eigvals.flatten(), -n)[-n]
    return eigvals >= n_largest


def u2_dual(eigvals : np.ndarray, unused : float):
    """
    The :math:`U^2` dual operator.

    This function returns a copy of ``eigvals``.

    :param eigvals: A 1-D array of eigenvalues.
    :type eigvals: np.ndarray

    :param unused: Not used.
    :type unused: float

    :return: A copy of ``eigvals``.
    :rtype: np.ndarray
    """
    return np.copy(eigvals)
