# Analytics of page views for „Mathe für Nicht-Freaks“

This projects aims to analyze the page views of the project [“Mathe für Nicht-Freaks“](https://de.wikibooks.org/wiki/Mathe_f%C3%BCr_Nicht-Freaks) website.

## Pageview analysis

You can find all pageview analysis at https://kulla.github.io/analytics-mfnf/. The statistics are [updated daily by a GitHub Action](./github/workflows/publish.yml).

## Setup

1. Clone the repository
2. Make sure [`uv` is installed](https://docs.astral.sh/uv/getting-started/installation/)
3. Run `uv run` in the repository

## Scripts

The scripts in the [`scripts`](./scripts) folder help in creating new statistics. The scripts are:

- `./scripts/build`: Generate the pageview statistics
- `./scripts/format`: Format all python files and fix some lint errors
- `./scripts/start-jupyter-lab`: Start a Jupyter Lab server
- `./scripts/create-new-notebook <Type> <Notebook title>`: Create a new Jupyter Notebook from template. The type can be `statistic` or `test`.
- `./scripts/test`: Run all tests with `pytest`
- `./scripts/test-watch-mode`: Run all tests in watch mode
