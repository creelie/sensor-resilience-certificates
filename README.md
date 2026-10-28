# Universal Support Theorems for Resilient Coverage

Deep Bhattacharjee\* · Ushashi Bhattacharya · Sanjeevan Singha Roy

\*Corresponding author: d.bhattacharjee@erl-forschung.de

We prove that one finite set of points decides whether sensors cover a polygonal target under every failure rule in which an extra working sensor never hurts. The set is the same for every such rule, and on a face of dimension f the weakest point is fixed by f+1 sensors. The theorem holds in any dimension for functions that share a convex part and differ by affine terms. For sensing disks it gives the exact radius and power that keep the target covered under each rule, as rational numbers, the full trade-off between radius and budget, the smallest list of sensor groups whose loss breaks coverage, exact tests under independent placement errors, and protection plans proved optimal by a matching dual certificate.

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
