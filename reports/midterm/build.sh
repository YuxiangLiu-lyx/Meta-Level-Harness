#!/bin/sh
# Local typesetting only: no model, solver, or network calls.
set -eu
cd "$(dirname "$0")"
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
cp build/main.pdf main.pdf
