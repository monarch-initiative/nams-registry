#!/usr/bin/env bash
#
# Fetch the Cable et al. 2025 supplementary files into inputs/, and verify them.
#
# Paper: doi:10.1093/toxsci/kfae159  (PMID 39693112, PMC11879040), open access.
#
#
# WHERE THESE FILES COME FROM
# ---------------------------
# Europe PMC serves an article's supplementary files as a single zip:
#
#     https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11879040/supplementaryFiles
#
# which holds the figures plus a nested kfae159_supplementary_data.zip, and that
# inner zip holds the two files we want. So it is a zip inside a zip.
#
# This is the only automated route that works. PMC's own OA service
# (pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi) and its per-article /bin/ paths both
# answer 200 with an HTML page for this article, so neither can be scripted.
#
#
# WHY THIS VERIFIES RATHER THAN TRUSTS THE DOWNLOAD
# -------------------------------------------------
# The Europe PMC endpoint is intermittent, and it fails by returning
# **HTTP 200 with a 292-byte XML error body**:
#
#     <ns4:errorBean ...><errCode>0</errCode>
#     <errMsg>java.net.ConnectException: Connection refused</errMsg></ns4:errorBean>
#
# Observed working and then refusing within ninety seconds, from the same shell.
# So the exit status and the status code both say success while the file on disk
# is XML named .zip. Checking the status code is not enough; checking that the
# file is a zip is not enough either, since a partial transfer can still unzip.
# The sha256 of each extracted file is pinned below and is what decides.
#
# A failure here means the endpoint is down, not that the paper moved. Wait and
# retry, or download by hand from the article's Supplementary Data link:
#
#     https://doi.org/10.1093/toxsci/kfae159
#
#
# Usage:
#     ./scripts/fetch_inputs.sh          # fetch anything missing, verify everything
#     ./scripts/fetch_inputs.sh --force  # re-fetch even if the files are present
set -euo pipefail

# SUPP_URL is overridable so the failure paths below can be exercised against a
# local file:// copy of a bad response. Leave it alone for ordinary use.
SUPP_URL="${SUPP_URL:-https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11879040/supplementaryFiles}"
ARTICLE_URL='https://doi.org/10.1093/toxsci/kfae159'

# sha256 of each file as published. Pinned against an unversioned URL, so an
# upstream correction would break these -- that is the point. If a mismatch is
# real rather than a bad download, update inputs/README.md in the same change.
SHA_XLSX='f2c6c8335d1e4bc5884d25359f263b04cfa08e79c63bd6aea34f66055608e765'
SHA_DOCX='2c4c7700050e66b3913b3882661c77e936498f8e2ff0fbc8d0f4afbcd0ad50be'

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUTS="$(dirname "$HERE")/inputs"
FORCE="${1:-}"

sha_of() { shasum -a 256 "$1" | cut -d' ' -f1; }

check() {  # check <path> <expected-sha>; empty expected means report only
    local path="$1" want="$2" got
    [[ -f "$path" ]] || { echo "   missing: $path" >&2; return 1; }
    got="$(sha_of "$path")"
    if [[ -z "$want" ]]; then
        echo "   $(basename "$path")  sha256 $got  (not pinned)"
        return 0
    fi
    if [[ "$got" != "$want" ]]; then
        echo "   CHECKSUM MISMATCH: $(basename "$path")" >&2
        echo "     expected $want" >&2
        echo "     got      $got" >&2
        return 1
    fi
    echo "   $(basename "$path")  sha256 ok"
}

mkdir -p "$INPUTS"
XLSX="$INPUTS/toxsci-24-0360-File009.xlsx"
DOCX="$INPUTS/toxsci-24-0360-File010.docx"

if [[ "$FORCE" != "--force" && -f "$XLSX" && -f "$DOCX" ]]; then
    echo "==> inputs/ already holds both files; verifying"
    check "$XLSX" "$SHA_XLSX"
    check "$DOCX" "$SHA_DOCX"
    echo "==> nothing to fetch (pass --force to re-download)"
    exit 0
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "==> fetching supplementary zip from Europe PMC"
if ! curl -fsSL --retry 3 --retry-delay 5 --retry-all-errors \
        -o "$WORK/supp.zip" "$SUPP_URL"; then
    echo "   download failed outright" >&2
    echo "   fetch by hand from $ARTICLE_URL and put the files in inputs/" >&2
    exit 69
fi

size="$(wc -c < "$WORK/supp.zip" | tr -d ' ')"
echo "   got $size bytes"

# The endpoint answers 200 with an XML error body when its backend is refusing.
if ! unzip -tq "$WORK/supp.zip" >/dev/null 2>&1; then
    echo "   that is not a zip. Europe PMC answered 200 with an error body:" >&2
    head -c 400 "$WORK/supp.zip" >&2
    echo >&2
    echo "   the endpoint is down, not the article. Retry later, or fetch by hand:" >&2
    echo "     $ARTICLE_URL -> Supplementary Data" >&2
    exit 69
fi

echo "==> unpacking the nested supplementary archive"
unzip -qo "$WORK/supp.zip" -d "$WORK/outer"
INNER="$WORK/outer/kfae159_supplementary_data.zip"
[[ -f "$INNER" ]] || {
    echo "   no kfae159_supplementary_data.zip inside; package layout changed" >&2
    exit 69
}
unzip -qo "$INNER" -d "$WORK/inner"

found_xlsx="$(find "$WORK/inner" -name 'toxsci-24-0360-File009.xlsx' -print -quit)"
found_docx="$(find "$WORK/inner" -name 'toxsci-24-0360-File010.docx' -print -quit)"
[[ -n "$found_xlsx" ]] || { echo "   File009.xlsx not in the archive" >&2; exit 69; }

echo "==> verifying before installing into inputs/"
check "$found_xlsx" "$SHA_XLSX"
[[ -n "$found_docx" ]] && check "$found_docx" "$SHA_DOCX"

cp -p "$found_xlsx" "$XLSX"
[[ -n "$found_docx" ]] && cp -p "$found_docx" "$DOCX"

echo "==> installed:"
ls -la "$XLSX" ${found_docx:+"$DOCX"}
echo
echo "Provenance and sheet inventory: inputs/README.md"
