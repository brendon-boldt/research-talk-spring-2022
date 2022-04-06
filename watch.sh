#!/bin/sh

while inotifywait -e modify main.tex; do
    latexmk \
        -f \
        -pdf \
        -interaction=nonstopmode \
        -outdir=target/ \
        main.tex
done
