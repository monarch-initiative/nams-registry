"""Open a GitHub review issue for each resource that does not have one.

Each issue is the discussion thread for one resource. Its URL is written
to the resource's ``discussion_issue`` field, which the resource table
links to. Each issue body ends with a hidden marker naming the resource's
id; an existing labelled issue with that marker is reused, so running this
again does not open duplicates.

Requires the GitHub CLI (``gh``), logged in with permission to open
issues in the repository. Use ``--dry-run`` to see what would be done.
"""

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import time

import yaml

REPOSITORY = "monarch-initiative/nams-registry"
LABEL = "resource-review"
LABEL_COLOR = "1d76db"
LABEL_DESCRIPTION = "Discussion of one resource in the registry"
SITE = "https://monarch-initiative.github.io/nams-registry/resources/"
MARKER = re.compile(r"<!-- nams-registry: (\S+) -->")

BODY = """{byline}

This issue is the discussion thread for **{name}** (`{id}`) in the NAMs registry.

- Registry entry: [resources/{id}.yaml](https://github.com/{repository}/blob/main/resources/{id}.yaml)
- Homepage: {homepage}

**Current classification** (as of {today}; the registry entry is the up-to-date record)

- Holds NAMs: {holds_nams}
- Priority: {priority}

Use this issue to discuss:

- **Holds NAMs:** does the resource hold NAMs, and are they its primary content? (`primary`, `secondary`, `none`, or `unclear`). Explain the choice in `relevance_note`.
- **DisMech integration:** has any of its content been incorporated into DisMech, or does DisMech have tooling for it?
- **Priority:** choose a level for extraction priority (`high`, `medium`, or `low`). Explain the choice in `priority_rationale`.

Decisions are recorded by editing the entry's YAML file in a pull request that refers to this issue.

If this resource needs information the registry has no field for, open a separate issue labelled `schema-change`.

<!-- nams-registry: {id} -->
"""


def gh(*args):
    """Run a gh command and return its output."""
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"gh {args[0]} {args[1]} failed: {result.stderr.strip()}")
    return result.stdout


def byline():
    """Return the line that opens each issue, marking it as written by Claude Code.

    It names the person the issue is written for, taken from git's
    user.name, rather than an @-mention, so it sends no notification.
    """
    result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    name = result.stdout.strip()
    for_whom = f" for {name}" if name else ""
    return f"🤖 *Written by [Claude Code](https://claude.com/claude-code){for_whom}.*"


def title_for(resource):
    """Return the issue title for a resource."""
    return f"Comments and edits on {resource['name']}"


def body_for(resource):
    """Return the issue body for a resource."""
    priority = resource.get("priority")
    return BODY.format(
        byline=byline(),
        name=resource["name"],
        id=resource["id"],
        repository=REPOSITORY,
        homepage=resource.get("homepage_url") or "not recorded",
        today=datetime.date.today().isoformat(),
        holds_nams=f"`{resource['holds_nams']}`" if resource.get("holds_nams") else "not yet evaluated",
        priority=f"`{priority}`" if priority else "not set",
    )


def existing_issues():
    """Map resource id to the URL of its review issue, for issues already open or closed."""
    issues = json.loads(gh(
        "issue", "list", "--repo", REPOSITORY, "--label", LABEL, "--state", "all",
        "--limit", "1000", "--json", "body,url",
    ))
    found = {}
    for issue in issues:
        marker = MARKER.search(issue["body"] or "")
        if marker:
            found[marker.group(1)] = issue["url"]
    return found


def ensure_label():
    """Create the review label if the repository does not have it."""
    labels = json.loads(gh("label", "list", "--repo", REPOSITORY, "--limit", "1000", "--json", "name"))
    if LABEL not in {label["name"] for label in labels}:
        gh("label", "create", LABEL, "--repo", REPOSITORY,
           "--color", LABEL_COLOR, "--description", LABEL_DESCRIPTION)


def with_issue(resource, url, today):
    """Return the resource with discussion_issue set, keeping its field order."""
    updated = {}
    for key, value in resource.items():
        if key in ("discussion_issue",):
            continue
        if key == "activity_status":
            updated["discussion_issue"] = url
        updated[key] = value
    updated.setdefault("discussion_issue", url)
    updated["last_modified_date"] = today
    return updated


def main(argv=None):
    """Open the missing issues and record their URLs."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default="resources", help="Directory of resource files (default: resources)")
    parser.add_argument("--dry-run", action="store_true", help="Report what would be done without doing it")
    parser.add_argument("--only", metavar="ID", help="Handle only the resource with this id")
    args = parser.parse_args(argv)

    today = datetime.date.today().isoformat()
    found = existing_issues()
    if not args.dry_run:
        ensure_label()

    opened, linked, skipped = 0, 0, 0
    for path in sorted(glob.glob(os.path.join(args.resources, "*.yaml"))):
        with open(path) as fh:
            resource = yaml.safe_load(fh)
        if args.only and resource["id"] != args.only:
            continue
        if resource.get("discussion_issue"):
            skipped += 1
            continue
        url = found.get(resource["id"])
        if url:
            action = "link existing"
        else:
            action = "open"
        print(f"{action:13s} {resource['id']}{'  ' + url if url else ''}")
        if args.dry_run:
            continue
        if not url:
            # The REST API, not `gh issue create`, which uses GraphQL and
            # has timed out on this repository.
            url = json.loads(gh(
                "api", f"repos/{REPOSITORY}/issues",
                "-f", f"title={title_for(resource)}",
                "-f", f"body={body_for(resource)}",
                "-f", f"labels[]={LABEL}",
            ))["html_url"]
            opened += 1
            time.sleep(1)  # stay well under GitHub's limit on creating content
        else:
            linked += 1
        with open(path, "w") as fh:
            yaml.safe_dump(with_issue(resource, url, today), fh, sort_keys=False, allow_unicode=True)

    if args.dry_run:
        print("Dry run: nothing was opened or written.")
    else:
        print(f"Opened {opened}, linked {linked} existing, skipped {skipped} that already had an issue.")


if __name__ == "__main__":
    main()
