"""nams-source-repository.

This is a repository of NAMs sources collected in support of a NAMs landscape analysis.
"""

try:
    from nams_source_repository._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
