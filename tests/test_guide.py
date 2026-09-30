"""Tests for the guide aimed at scripts and agents."""

from __future__ import annotations

from click.testing import CliRunner

from te_api import guide
from te_api.cli import create_cli


def test_guide_states_the_contract():
    text = guide.agent_guide("te-api")

    assert "exit codes" in text.lower()
    assert "TRANSPARENT_COMPANY_ID" in text
    assert "te-api describe" in text
    assert "--body-file" in text


def test_read_only_guide_leaves_out_request_bodies():
    text = guide.agent_guide("te-api-ro", read_only=True)

    assert "te-api-ro search" in text
    assert "Request bodies" not in text
    assert "only GET" in text


def test_skill_file_has_frontmatter_then_the_guide():
    text = guide.skill_file("te-api-ro", read_only=True)

    assert text.startswith("---\nname: te-api-ro\n")
    assert "read-only" in text.split("---")[1]
    assert guide.agent_guide("te-api-ro", read_only=True) in text


def test_agents_command_uses_the_binary_name():
    result = CliRunner().invoke(create_cli(read_only=True), ["agents"], prog_name="te-api-ro")

    assert result.exit_code == 0, result.output
    assert result.output.startswith("# te-api-ro: guide")


def test_root_help_points_at_search_describe_and_agents():
    result = CliRunner().invoke(create_cli(), ["--help"])

    assert "'search <words>'" in result.output
    assert "'describe <module> <verb> <resource>'" in result.output
    assert "'agents'" in result.output


def test_version_flag():
    result = CliRunner().invoke(create_cli(), ["--version"], prog_name="te-api")

    assert result.exit_code == 0
    assert result.output.startswith("te-api ")
