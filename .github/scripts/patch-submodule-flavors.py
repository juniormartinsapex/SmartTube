#!/usr/bin/env python3
"""JM APEX Tube: add the `stapex` flavor to the git-submodule modules.

`:youtubeapi` (MediaServiceCore) and `:appupdatechecker2` (SharedModules) are
git submodules checked out from upstream by CI, so the `stapex` flavor cannot
be committed in those repos. This script patches their build.gradle files
after checkout, inserting the empty `stapex {}` flavor next to the existing
`stbeta {}` / `ststable {}` / `stfdroid {}` blocks, in the same style as the
in-repo modules. It preserves each file's own line endings (CRLF today) and
is idempotent: re-running it is a no-op.

Run from the repository root, e.g. in CI right after the checkout step.
"""

import sys

FILES = [
    "MediaServiceCore/youtubeapi/build.gradle",
    "SharedModules/appupdatechecker2/build.gradle",
]

ANCHOR = "        ststable {}"
INSERT = "        stapex {}"


def main() -> int:
    for path in FILES:
        with open(path, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8")

        if "stapex" in text:
            print(f"SKIP {path}: stapex flavor already present")
            continue

        # Preserve the file's own line ending (CRLF in these files today).
        eol = "\r\n" if "\r\n" in text else "\n"
        anchor = ANCHOR + eol
        if anchor not in text:
            print(f"ERROR: anchor {ANCHOR!r} not found in {path}", file=sys.stderr)
            return 1

        text = text.replace(anchor, anchor + INSERT + eol, 1)
        with open(path, "wb") as fh:
            fh.write(text.encode("utf-8"))
        print(f"PATCHED {path}")

    print("OK: stapex flavor added to submodule modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
