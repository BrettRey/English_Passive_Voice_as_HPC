# English Passive Voice as HPC

Manuscript source for Brett Reynolds's paper-in-progress, "English Passive Voice as HPC."

This project argues that the English passive is better treated as a maintained, projectible construction family than as a category definable by a short classical checklist.

## Status

The paper is currently at an early draft stage. The repository contains the manuscript source, bibliography, and project notes.

## Build

This project requires XeLaTeX because the house style uses Charis SIL.

```bash
make
```

Or run the full manual build:

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

Do not use LuaLaTeX for the release build.

## Repository Contents

- `main.tex` - manuscript source
- `references.bib` - bibliography
- `docs/` - status, decisions, handoff, and source notes
- `.house-style/` - shared preamble and style rules

## License

This repository is licensed under CC BY 4.0. See [LICENSE](LICENSE).
