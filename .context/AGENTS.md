# Agent

- **Version:** 1.0.0
- **Author:** Cordero Core
- **Date:** September 13, 2025

## Instructions

The main developer documentation lives in the `$PACKAGE_NAME/docs` directory, where `$PACKAGE_NAME` is the name of the package. The following points summarize how to set up the environment, run checks, build docs and follow the PR workflow.

## Package and Environment Management

Pixi is the package and environment manager for this repository. It uses a single pixi.toml file to declare dependencies and tasks, so you should never install packages directly with pip or conda. Instead, add new dependencies with pixi add <package> and run predefined workflows (or tasks) using pixi run <task>. This ensures the environment is reproducible across all platforms and that tasks like testing, building, or starting the app are invoked consistently. Always check pixi.toml (or pyproject.toml) for available tasks and update it rather than hardcoding commands.

## Tests

- All tests for this each package is located in `$PACKAGE_NAME/tests`, where `$PACKAGE_NAME` is the name of the package.

## Commit Messages and Pull Requests (PRs)

Follow the conventional commit with scope style for commit and PR messages.

### Every pull request should answer:

- What changed?
- Why?
- Breaking changes?
- Server PR (if the change requires a coordinated server update)
- Comments should be complete sentences and end with a period.
