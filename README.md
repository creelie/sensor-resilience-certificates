# Universal Support Theorems for Resilient Coverage

**Deep Bhattacharjee*** · **Ushashi Bhattacharya** · **Sanjeevan Singha Roy**

*First and corresponding author: Deep Bhattacharjee, itsdeep@live.com.*

A standalone analytical paper in amsart format: **49 pages, 13 numbered figures, 11 footnotes and seven appendices**. The title has no conjunction or punctuation. The main paper is not presented as a v3 manuscript.

## Single Hexagon package

The release **standalone-1.0.0** provides one complete outer ZIP. Extract it and upload the inner TeX ZIP to Overleaf or Hexagon; `main.tex` is at the inner archive root.

- [PDF](%5BPAPER%5D%20package/UniversalSupportTheoremsForResilientCoverage.pdf)
- [TeX ZIP](%5BPAPER%5D%20package/UniversalSupportTheoremsForResilientCoveragetex.zip)
- [Hexagon fields](%5BPAPER%5D%20package/hexagonsubmissionform.md)
- [Declarations](%5BPAPER%5D%20package/DECLARATIONS.md)
- [AI provenance](%5BPAPER%5D%20package/aiprovenance.md)
- [Journal notes](%5BPAPER%5D%20package/journalsubmissiondetails.md)
- [Analytical manuscript source](standalone/main.tex)

The user declared **all parts checked and understood by a human** and **a mix of human-written and AI-generated text**. Those statements are recorded in the Hexagon metadata. No funding and no competing interests are declared; ethics approval is not applicable to the mathematical article.

## Main result

For functions with a common continuous convex part and affine differences on a polyhedral target, one finite set supports the maximum of every nonconstant monotone lattice selector. The set is independent of the rule and common convex term. On an f-dimensional face, at most f+1 functions are needed in a full-rank tie system.

The paper derives exact sensing thresholds, power-controlled unequal-footprint results, canonical target antichains and a complete power–failure-budget frontier. It also proves monotone relabeling, product-uncertainty reductions and rational primal–dual protection certificates. Its engineering examples are symbolic derivations. No simulation or optional code check is a premise of a proof.

Classical arrangements, power diagrams, lattice polynomials, minimal cuts, nerve theory, cover decomposition and LP duality are credited explicitly. The contribution's priority and significance need independent specialist review; neither a breakthrough label nor Annals acceptance is guaranteed.

## Optional software

The mathematical article stands independently of the supplementary programs. With Python 3.12, run:

```text
python -m unittest discover -s code -v
```

There are 28 controls. One optional LP-hint test needs SciPy; the rational certificate check is independent of that solver. The new geometric routines preserve Fraction inputs and treat floats as their exact binary64 rationals. No Lean formalization is claimed.

## References and identifiers

The related archive [10.5281/zenodo.23731783](https://doi.org/10.5281/zenodo.23731783) is cited with its original authors. The original sensor paper is cited at [10.20944/preprints202606.1351.v2](https://doi.org/10.20944/preprints202606.1351.v2). The bibliography uses the requested permitted platforms and published sources; it includes no Qeios, Authoria or arXiv source.

No new Zenodo DOI or Hexagon identifier has been minted for the standalone article. Software tag `standalone-1.0.0` identifies this package, not a third preprint version.

The earlier v3 package is preserved in [historical/v3.0.1-package](historical/v3.0.1-package). Its releases remain historical records.

License: CC BY 4.0.
