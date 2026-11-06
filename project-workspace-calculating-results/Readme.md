# Excercise files: 

Open the below files to continue with this excercise: 

- [calculates_results_stats.py](../data/calculates_results_stats.py)

- [calculates_results_stats_hints.py](../data/calculates_results_stats_hints.py)

## Statistics behavior and regression tests

Percentages with no applicable images are reported as `0.0`, following the
existing convention for a batch with no non-dog images. An empty batch returns
zero counts and percentages. A batch containing only non-dogs still reports
its match and non-dog accuracy; its dog and breed percentages are `0.0`.
Read these percentages together with their image counts: a zero denominator
means that category was not evaluated, rather than a measured accuracy of zero.

From the repository root, run:

```sh
python3 -m unittest discover -s tests -v
```

These tests use only the Python standard library. They cover empty, non-dog-only,
dog-only, mixed and all-incorrect results, as well as input preservation.
They do not load models, download weights or require third-party packages.

