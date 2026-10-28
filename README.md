# Universal Support Theorems for Resilient Coverage

Deep Bhattacharjee\* · Ushashi Bhattacharya · Sanjeevan Singha Roy

\*Corresponding author: d.bhattacharjee@erl-forschung.de

On a polyhedral target, one finite set of points locates the maximum of every monotone max–min combination of functions that share a convex part and differ by affine terms, whatever the rule and the shared part; a maximiser on an f-dimensional face is fixed by f+1 of the functions. For sensing disks this gives exact rational coverage radii and power thresholds for every monotone failure rule, the whole radius–budget frontier, a canonical certificate of minimal contact sets with witnesses, exact robust tests under independent placement errors and dual certificates for protection.

For the rule "at least one contact" the support set reduces to the classical candidates for the largest empty circle centred in a polygon (Toussaint 1983); for "at least k contacts" it reduces to the order-k Voronoi test for k-coverage (Lee 1982; So and Ye 2005). The paper treats every monotone rule and a shared convex term at once.

## Paper

- [PDF](%5BPAPER%5D%20package/UniversalSupportTheoremsForResilientCoverage_final2.pdf) (REVTeX two-column, 32 pages)
- [LaTeX source ZIP](%5BPAPER%5D%20package/UniversalSupportTheoremsForResilientCoverage_final2-tex.zip) (`main.tex`, section files, PNG figures; `pdflatex -jobname=output main.tex`, three passes)
- [arXiv tarball](%5BPAPER%5D%20package/UniversalSupportTheoremsForResilientCoverage_final2-arxiv.tar.gz)
- [Hexagon fields](%5BPAPER%5D%20package/HEXAGON_FORM.md) and [AI provenance](%5BPAPER%5D%20package/AI_PROVENANCE.md)
- Source: [`standalone/`](standalone/main.tex)

## Checks

The finite arithmetic of the worked examples is re-checked in exact rational arithmetic (Python 3.12, 28 tests):

```text
python -m unittest discover -s code -v
```

No statement of the paper rests on these programs. `code/make_resilience_figures.py` draws the figures.

## Archive

| Release | DOI |
| --- | --- |
| v1.1.0 | [10.5281/zenodo.23742106](https://doi.org/10.5281/zenodo.23742106) |
| standalone-1.0.0 (v1.0.0) | [10.5281/zenodo.23739824](https://doi.org/10.5281/zenodo.23739824) |
| all versions (concept) | [10.5281/zenodo.23734252](https://doi.org/10.5281/zenodo.23734252) |

Earlier packages are kept in [`historical/`](historical/). The paper cites the ECoG archive [10.5281/zenodo.23731783](https://doi.org/10.5281/zenodo.23731783) and the sensor preprint [10.20944/preprints202606.1351.v2](https://doi.org/10.20944/preprints202606.1351.v2).

License: CC BY 4.0.
