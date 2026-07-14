
<h1 align="center">
<img src="https://hofa.es/_static/logo_hof.png" width="250">
</h1>
<div align="center">
    <h3>
          Higher-order Fourier analysis Python package
    </h3>
</div>

<p align="center">
<strong>
<a href="https://github.com/CandelaCSIC/hofa">Source repository</a> •
<a href="https://hofa.es/getting_started/installation.html">Installation guide</a> •
<a href="https://hofa.es/">Website</a> 
</strong>
</p>
<p>This is an open source project to use higher-order Fourier analysis in applied scenarios.</p>

Higher-order Fourier analysis is a theory that generalizes Fourier analysis. Roughly speaking, while Fourier analysis deals with representing functions in terms of Fourier characters, e.g. functions of the form $\exp(2\pi i \xi\cdot x)$, higher-order Fourier analysis deals with representing functions in terms of _higher-order Fourier characters_, including functions of the form $\exp(2\pi i P(x))$ for polynomials $P$. Such higher-order representations can capture more subtle structural aspects of the function that can often be missed by looking only at the function's dominant Fourier characters. These insights have already had major impact in pure mathematics, and the present project aims to facilitate exploration and application of these insights in more applied settings.

<p>
For more introduction and background on the theory of higher-order Fourier analysis, please visit the <a href="https://hofa.es/user_guide/conceptual_background.html">conceptual background</a> part of the documentation.
</p>

## Key features

- Methods for detecting higher-order structure.
- Methods for denoising functions with respect to higher-order Fourier structure.
- Methods for computing higher-order components of functions.


## Prerequisites

**HoFa** is built in Python 3.12+, the following libraries are sufficient:

- Numpy 2.0+
- SciPy 1.13+

## Useful links

- **Website:** https://hofa.es
- **Full installation guide:** https://hofa.es/getting_started/installation.html
- **Source Repository:** https://github.com/CandelaCSIC/hofa
- **Archival Repository (DOI):** https://doi.org/10.20350/digitalCSIC/18509 *(CSIC Institutional Repository)*
- **User guide:** https://hofa.es/user_guide/user_guide_index.html
- **License:** https://hofa.es/license.html
- **Recommended citation:** https://hofa.es/citing_hofa.html
- **API reference:** https://hofa.es/autoapi/index.html
- **Developer's guide:** https://hofa.es/developers_guide/for_developers.html


## Authors 

- [Pablo Candela](https://pablocandela.es/),

- [Diego González-Sánchez](https://dglez91.github.io/), and 

- [Balázs Szegedy](https://users.renyi.hu/~szegedyb/).

First released in June 2026

## Funding

This work was supported by funding from project [PID2024-156180NB-I00](https://matematicas.uam.es/~fernando.chamizo/grant/overview.html) (MICIU/AEI and the European Union).
The second-named author is funded by [HORIZON-MSCA-2024-PF-01, AlgHOF 101202161](https://doi.org/10.3030/101202161) funded by the European Union (views and opinions expressed are those of the author(s) only and do not reflect those of the European Union or the European Commission. Neither the European Union nor the European Commission can be held responsible for them). 
The third-named author was partially supported by the Hungarian Ministry of Innovation and Technology NRDI Office within the framework of the [Artificial Intelligence National Laboratory Program (MILAB, RRF-2.3.1-21-2022-00004)](https://ai.renyi.hu/).
