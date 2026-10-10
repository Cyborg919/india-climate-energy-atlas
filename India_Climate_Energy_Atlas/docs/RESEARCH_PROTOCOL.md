# Research protocol

## Primary question
How have economic development, electricity access, renewable energy consumption and per-capita CO₂ emissions changed together in India since 2000?

## Preregistered workflow
1. Retrieve the same indicator series for India and five comparison countries.
2. Save retrieval timestamp, year range, source URL, and row counts.
3. Report per-indicator coverage and missingness.
4. Plot observed annual values without silently filling gaps.
5. Report endpoint changes only when both endpoint observations exist; disclose the actual endpoints.
6. Compute pairwise correlations only on complete observations and report sample size.
7. Run sensitivity checks using a common overlapping year range across indicators.
8. Interpret associations as descriptive, not causal.
9. Avoid claiming “decoupling” unless a precise operational definition is specified and tested; distinguish absolute emissions from per-capita emissions and account for data coverage.
10. Cite World Bank indicator pages and the API retrieval date in the final write-up.

## Limitations
Country-level aggregates can hide regional differences. Indicator series may have lags, revisions, different methodologies, and missing years. Correlation does not establish causality. This analysis is not an emissions inventory or policy evaluation.
