# Sensor Coverage under Structured Failures

**Version 3.0.1 — 28 October 2026**

Deep Bhattacharjee · Ushashi Bhattacharya · Sanjeevan Singha Roy

This is the v3 research revision of *Iterated Nerve Complexes for k-Fold Sensor Coverage*. It develops one coherent manuscript around structured failures, facet-intersection nerve models, exact disk geometry and continuous target certificates.

The original v2 is [10.20944/preprints202606.1351.v2](https://doi.org/10.20944/preprints202606.1351.v2). The companion ECoG archive cited in the paper is [10.5281/zenodo.23731783](https://doi.org/10.5281/zenodo.23731783). That DOI identifies the companion archive, not this v3.

## Paper and package

- [Manuscript source](paper/main.tex)
- [Compiled manuscript](%5BPAPER%5D%20package/SensorCoverageStructuredFailuresV3.pdf)
- [Overleaf/Hexagon TeX ZIP](%5BPAPER%5D%20package/SensorCoverageStructuredFailuresV3tex.zip)
- [Submission metadata](%5BPAPER%5D%20package/hexagonsubmissionform.md)
- [Journal preparation notes](%5BPAPER%5D%20package/journalsubmissiondetails.md)
- [AI provenance](%5BPAPER%5D%20package/aiprovenance.md)
- [Verification and scope](VERIFICATION.md)

## Results

The surviving region is defined for any downward-closed family of allowed contact failures. It includes fixed-cardinality losses, weighted deletion budgets and complete fault-domain losses. Its facet-intersection complex is related to the geometric region by classical nerve and Dowker theory; these earlier results are credited explicitly.

For closed planar disks, at most n² leftmost or circle-intersection witnesses suffice to recover every maximal nerve face. Exact rational sign tests construct those faces, including tangencies and coincident footprints. The complete dual two-skeleton determines H0 and H1 over GF(2). A separate proved margin certificate checks continuous coverage of specified triangulated targets.

The previously unfinished dense Field E now has **two-fold Betti numbers (5, 6)**. Its dual complex has **130 vertices, 4,214 edges and 94,985 triangles**, with triangle-boundary rank **4,083**. The earlier figure of **836,991** is corrected to a count of **shadow edges**; the original two-fold shadow has **1,810 vertices**.

These are proved statements under the stated finite convex-cover and disk assumptions, together with exact finite computations. This package does not claim a new general nerve theorem, a resolution of an unrelated open conjecture, a Lean formalization or guaranteed acceptance by any journal. Independent assessment of the contribution's novelty and significance remains part of research review.

## Reproduce

The scientific calculations use Python 3.12 and only its standard library:

```text
python -m unittest discover -s code -v
python code/run_fields.py
python code/verify_fields.py
python code/audit_shadow_edges.py
```

The CSV files preserve the original binary64 coordinates. All Boolean geometric tests use exact rational arithmetic on those values. The input manifest records source-array and CSV hashes.

Figures require NumPy and Matplotlib; pre-generated PDF figures are already included:

```text
python -m pip install -r requirements-figures.txt
python code/make_figures.py
```

For a first LaTeX build, run `pdflatex main.tex` three times in `paper/` until the contents and cross-references stabilize, or upload the TeX ZIP to Overleaf and select `main.tex`. There is no line numbering. Normal section, equation and page numbers remain.

## Authors

1. Deep Bhattacharjee — EGSPL, Bhubaneswar, India; itsdeep@live.com; ORCID [0000-0003-0466-750X](https://orcid.org/0000-0003-0466-750X).
2. Ushashi Bhattacharya — Dortmund, Germany; National Taiwan University, Taipei, Taiwan (details carried forward from the supplied v2).
3. Sanjeevan Singha Roy — Formerly, Birla Institute of Technology (BIT) Mesra, India; sanjeevan9905@gmail.com; ORCID [0000-0002-6148-1421](https://orcid.org/0000-0002-6148-1421).

Authors should confirm current affiliations and submission declarations before a journal submission. Author order follows the user's instructions and the v2 record. No contributions or approvals have been invented for any coauthor.

## License and source lineage

CC BY 4.0. The five synthetic input fields derive from the supplied supplementary archive for Bhattacharjee and Bhattacharya's v2. The new source records the original archive hashes and retains this attribution. The earlier ECoG work is cited with its full three-author attribution; its author list is distinct from this manuscript's author list.
