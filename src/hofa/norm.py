r"""
This module contains the Numpy implementation for computing Gowers norms 
on functions defined on finite abelian groups represented by ``numpy.ndarray``.

Conventions
-----------
The following conventions are used for functions in this file:

- Any finite abelian group :math:`Z` is isomorphic to :math:`\mathbb{Z}/n_1\mathbb{Z} \times \mathbb{Z}/n_2\mathbb{Z} \times ... \times \mathbb{Z}/n_k\mathbb{Z}`. Therefore, a function :math:`f: Z \to \mathbb{C}` is represented as a ``numpy.ndarray`` tensor with shape ``(n_1, n_2, ..., n_k)``.

- Sometimes we abreviate ``numpy`` by ``np``.
"""
import numpy as np
import hofa.rgz

def u_pow(f : np.ndarray, k : int):
    r"""
    The :math:`2^k` power of the Gowers :math:`U^k` norm of ``f``.

    :param f: A function :math:`f: Z \to \mathbb{C}` defined on a finite abelian group :math:`Z`.
    :type f: np.ndarray

    :param k: An integer representing the order of the Gowers norm.
    :type k: int

    :return: The :math:`2^k` power of the :math:`U^k` norm of ``f``.
    :rtype: float

    """

    if k<= 1:
        mean = np.mean(f)
        return (np.abs(mean)**2).item()
    elif k == 2:
        return np.sum(np.pow(np.abs(np.fft.fftn(f,norm = "forward")),4))
    else:

        M = hofa.rgz.move_diag_to_rows(hofa.rgz.t_prod_itself(f))

        half_dim = len(f.shape)
        dim_f = f.shape
        new_dim = tuple([-1]+list(dim_f))

        M_first_dims_flatten = np.reshape(M,new_dim)

        diag_norms = np.zeros(M_first_dims_flatten.shape[0])
        for i in range(M_first_dims_flatten.shape[0]):
            diag_norms[i] = u_pow(M_first_dims_flatten[i],k-1)

        return np.mean(diag_norms)


def u(f : np.ndarray, k : int):
    r"""
    The Gowers :math:`U^k` norm of ``f``.

    :param f: A function :math:`f: Z \to \mathbb{C}` defined on a finite abelian group :math:`Z`.
    :type f: np.ndarray

    :param k: An integer representing the order of the Gowers norm.
    :type k: int

    :return: The :math:`U^k` norm of ``f``.
    :rtype: float
    """

    return np.power(u_pow(f,k),1/np.power(2,k))



    