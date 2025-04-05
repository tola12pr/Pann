repos:
  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.10.1  # Use the latest version
    hooks:
      - id: isort

  - repo: https://github.com/psf/black
    rev: 22.3.0  # Use the latest version
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-autoflake
    rev: v1.4.0  # Use the latest version
    hooks:
      - id: autoflake
        args: [--remove-all-unused-imports, --remove-unused-variables, --in-place, --expand-star-imports]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.4.0  # Use the latest version
    hooks:
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1  # Use the latest version
    hooks:
      - id: flake8

  - repo: https://github.com/hyperrealm/flynt
    rev: v0.50  # Use the latest version
    hooks:
      - id: flynt
        args: ["--all"]

  - repo: https://github.com/asottile/pyupgrade
    rev: v2.24.0  # Use the latest version
    hooks:
      - id: pyupgrade
        args: ["--py3-plus"]
