// Entry program for the news-image-20261119 bounty (Node 22, stdlib only).
// The poster is drawn ahead of time by draw_poster.py and shipped in this
// repository as entry.png. This program only copies that file into the
// output directory, so both grading runs produce byte-identical output:
// no network, no randomness, no timestamps anywhere in the path.
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
