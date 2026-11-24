"""Emit public/model.json from the data layer. Run: python3 model/build.py"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clock import build, summarize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, os.pardir, os.pardir, "data", "liability-clock", "_model.json")


def main():
    m = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print(summarize(m))
    print("\nwrote %s (%d bytes)" % (os.path.relpath(OUT), os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
