"""Test the Biomni gate in the deep-research wrapper.

DisMech and deep-research-client are in the `research` dependency group, which
`just test` does not install, so both are stubbed here. That makes these tests
cover this repository's side of the contract only: that the wrapper hands the
policy a command line the policy can recognise, and acts on its answer.

The reason to pin it is that getting it wrong is silent. DisMech's
``requests_biomni_research`` looks for the ``research`` subcommand among the
arguments it is given, and this wrapper adds that word only later, when it
builds the client's ``sys.argv``. Passing the caller's arguments alone leaves
the test permanently false: no error, no refusal, just an explanation that
never prints (fixed in #121). Whether DisMech still reads its arguments that
way is checked by running the real thing, which needs the group installed.
"""

import sys
import types

import pytest

from nams_registry import deep_research

DETAIL = "Biomni is disabled by default because it ..."


def install_policy(monkeypatch, *, enabled, seen):
    """Stub dismech.deep_research_policy, recording the arguments it is given.

    ``requests_biomni_research`` keeps DisMech's own requirement: the arguments
    have to include the ``research`` subcommand, not only the provider flag.
    """

    def requests_biomni_research(arguments):
        seen.append(list(arguments))
        if "research" not in arguments:
            return False
        joined = " ".join(arguments)
        return "--provider biomni" in joined or "--provider=biomni" in joined

    policy = types.SimpleNamespace(
        BIOMNI_DISABLED_DETAIL=DETAIL,
        configure_biomni_environment=lambda: enabled,
        requests_biomni_research=requests_biomni_research,
    )
    dismech = types.ModuleType("dismech")
    dismech.deep_research_policy = policy
    monkeypatch.setitem(sys.modules, "dismech", dismech)
    monkeypatch.setitem(sys.modules, "dismech.deep_research_policy", policy)


def install_client(monkeypatch, calls):
    """Stub deep_research_client.cli, recording the argv it would be run with."""
    cli = types.ModuleType("deep_research_client.cli")
    cli.app = lambda: calls.append(list(sys.argv))
    client = types.ModuleType("deep_research_client")
    client.cli = cli
    monkeypatch.setitem(sys.modules, "deep_research_client", client)
    monkeypatch.setitem(sys.modules, "deep_research_client.cli", cli)


@pytest.mark.parametrize("flag", ["--provider biomni", "--provider=biomni"])
def test_biomni_is_refused_with_the_reason(monkeypatch, capsys, flag):
    """Without the opt-in, an explicit Biomni run is refused, and says why."""
    seen, calls = [], []
    install_policy(monkeypatch, enabled=False, seen=seen)
    install_client(monkeypatch, calls)

    assert deep_research.main([*flag.split(), "a query"]) == 2
    assert DETAIL in capsys.readouterr().err
    assert not calls, "the client ran despite the refusal"
    # The policy was asked about a full client command line, subcommand and
    # all. Drop the subcommand and the refusal goes quiet.
    assert seen and seen[0][0] == "research"


def test_the_opt_in_passes_through(monkeypatch):
    """With the opt-in, the wrapper does not stand in the way."""
    seen, calls = [], []
    install_policy(monkeypatch, enabled=True, seen=seen)
    install_client(monkeypatch, calls)

    assert deep_research.main(["--provider", "biomni", "a query"]) == 0
    assert calls == [
        ["deep-research-client", "research", "--provider", "biomni", "a query"]
    ]


def test_another_provider_is_not_gated(monkeypatch):
    """A run that never asks for Biomni reaches the client unchanged."""
    seen, calls = [], []
    install_policy(monkeypatch, enabled=False, seen=seen)
    install_client(monkeypatch, calls)

    assert deep_research.main(["--provider", "mock", "a query"]) == 0
    assert calls == [
        ["deep-research-client", "research", "--provider", "mock", "a query"]
    ]


def test_a_missing_dependency_names_the_recipe(monkeypatch, capsys):
    """Run without the group, the wrapper says which recipe installs it."""
    monkeypatch.setitem(sys.modules, "dismech", None)
    monkeypatch.setitem(sys.modules, "dismech.deep_research_policy", None)

    with pytest.raises(SystemExit) as exit_info:
        deep_research.main(["--provider", "mock", "a query"])
    message = str(exit_info.value)
    assert "just deep-research --provider mock a query" in message
    assert "`research` dependency group" in message
