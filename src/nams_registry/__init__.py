"""nams-registry.

This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.
"""

try:
    from nams_registry._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
