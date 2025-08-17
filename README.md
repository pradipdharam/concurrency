# Concurrency and its Hazards Demonstration

This repo demonstrates key **concurrency hazards** in multithreaded programming:

- **Race Conditions**
- **Memory Visibility Issues**
- **Instruction Reordering**

Understanding these issues is essential when building thread-safe applications.


# Setup Linting and Pre-commit Hooks to enhance this repo

To ensure code quality and enforce PEP 8 compliance, install the following tools:

```sh
pip install pre-commit flake8 ruff black
pre-commit install
```

This will set up pre-commit hooks using `flake8` and `ruff` to automatically check your code before each commit.

**Steps:**
1. Run the above commands in your project root directory.
2. Make sure `.pre-commit-config.yaml` is present in the root directory with the desired configuration.
3. On each commit, your code will be checked for formatting and linting issues.

For manual checks, you can run:
```sh
pre-commit run --all