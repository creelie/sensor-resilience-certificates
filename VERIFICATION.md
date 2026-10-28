# Verification record — v3.0.0

Theorems are stated and proved in the manuscript. The computations check specific finite inputs; neither test success nor the release label is a substitute for peer review.

## Analytic statements

- The pointwise survival condition is exactly that the active set is outside the downward-closed failure family.
- The winning-face and facet-intersection complexes are homotopy equivalent by explicit order maps. The convex-cover comparison uses the credited closed-convex nerve theorem.
- Inclusions of failure families at fixed geometry induce natural homology isomorphisms between the geometric and dual models.
- All maximal nerve faces of n closed planar disks occur at at most n² specified witnesses.
- Circle memberships and triangle target certificates reduce to exact rational radical-sign decisions.
- The winning margin is 1-Lipschitz, gives a continuous target certificate with the sharp universal triangle constant 1/sqrt(3), and obeys the stated parameter-perturbation bound.

## Checks actually run

- Python 3.12.14; ten unittest methods passed.
- Fifty seven-contact equal-radius fields: all 127 nonempty subsets per field checked against a separate enclosing-circle oracle.
- 150 small abstract nerves under four failure-rule types: 600 dual-versus-coalition Betti comparisons.
- All five supplied fields: 619,080 exact pair/triple comparisons, plus all returned-facet and one-contact-extension checks.
- All five two-fold boundary ranks recomputed with a separate set-based elimination using the opposite pivot order.
- All 25 full dual two-skeleton computations completed.
- All five original two-fold shadow vertex and edge counts independently recounted.
- Tangencies, an adjacent binary64 gap, zero radii, unequal nested radii, coincident disks, scale changes, invalid costs and a continuous triangle certificate tested.
- The final PDF was compiled, rendered and visually reviewed. The source ZIP is independently compiled after clean extraction.

## Dense Field E

| Quantity | Value |
|---|---:|
| Original disks | 95 |
| Original nerve edges | 1,810 |
| Original nerve triangles | 24,956 |
| Original two-fold shadow vertices | 1,810 |
| Original two-fold shadow edges | 836,991 |
| Dual two-fold vertices | 130 |
| Dual two-fold edges | 4,214 |
| Dual two-fold triangles | 94,985 |
| Triangle boundary rank | 4,083 |
| Graph cycle-space dimension | 4,089 |
| b0, b1 | 5, 6 |

Results and input hashes are in `results/` and `data/input-manifest.json`.

## Limits

No Lean proof is supplied. The finite computations report ordinary H0 and H1 over GF(2). Raster panels are illustrations. No unstated clinical or target-coverage conclusion follows from the Betti counts. The theorem is not asserted to be the first use of Dowker duality or a replacement for published multicover algorithms. The complete dual complex can be exponentially large, and the low-degree worst-case triangle bound is O(n^6), not linear.

The three contextual author references from Research Square, SSRN and EPRA are not proof inputs. No Qeios, Authoria or arXiv source is cited in the manuscript.
