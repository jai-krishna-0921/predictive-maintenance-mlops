"""Feature path shared by training and serving.

For now this package holds the C-MAPSS data loader. The feature transforms
(rolling windows, per-regime normalization) join it here in Phase 1, so that
training and serving compute features with the same code and cannot drift apart.
"""
