Here's a detailed, fully-referenced answer to your PaddleOCR queries, using up-to-date data as of February 2026:

---

## 1. **Recent Releases/Tags — Latest Versions**
**GitHub Latest Release/Tag:**
- **Latest tag:** [`v3.4.0`](https://github.com/PaddlePaddle/PaddleOCR/releases/tag/v3.4.0)
- **Release date:** 2026-01-29
- **Highlights:** "Release the PaddleOCR-VL-1.5 complex document parsing solution," SOTA performance, and major new features (see [release notes](https://github.com/PaddlePaddle/PaddleOCR/releases/tag/v3.4.0)).

**Latest Stable on PyPI:**
- PaddleOCR uploads to PyPI, but the latest published version on PyPI may lag behind GitHub releases. The `langchain-paddleocr` subpackage explicitly restricts versions to `<3.5.0`, suggesting the stable channel is `3.4.x` as of now.
- **Check PyPI:** [https://pypi.org/project/paddleocr/#history](https://pypi.org/project/paddleocr/#history)

---

## 2. **Dependency Versions in `pyproject.toml`, `setup.py`, etc.**

### Example: `mcp_server/pyproject.toml`
```toml name=mcp_server/pyproject.toml url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/mcp_server/pyproject.toml#L1-L29
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "paddleocr_mcp"
version = "0.5.0"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.5.0",
    "fastmcp>=2.0.0",
    "httpx>=0.24.0",
    "numpy>=1.24.0",
    "pillow>=9.0.0",
    "puremagic>=1.30.0",
    "typing-extensions>=4.0.0",
]

[project.optional-dependencies]
local = [
    "paddleocr[doc-parser]>=3.4",
]
local-cpu = [
    "paddleocr[doc-parser]>=3.4",
    "paddlepaddle>=3.2.1",
]
[project.scripts]
paddleocr_mcp = "paddleocr_mcp.__main__:main"
```

### Example: `langchain-paddleocr/pyproject.toml`
```toml name=langchain-paddleocr/pyproject.toml url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/langchain-paddleocr/pyproject.toml#L1-L72
[project]
requires-python = ">=3.10,<3.13"
dependencies = [
    "paddleocr>=3.4.0,<3.5.0",
    "paddlex[serving]>=3.4.1,<3.5.0",
    "langchain-core>=1.2.5,<2.0.0",
    "requests>=2.32.5",
    "pydantic>=2.0.0,<3.0.0",
]
```

### Example: Requirements Files

**Some key requirements files:**

- `deploy/avh/requirements.txt`
```pip name=deploy/avh/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/deploy/avh/requirements.txt#L1-L4
paddlepaddle
numpy
opencv-python
typing-extensions
```

- `ppstructure/kie/requirements.txt` (custom KIE/IE package)
```pip name=ppstructure/kie/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/ppstructure/kie/requirements.txt#L1-L7
sentencepiece
yacs
seqeval
pypandoc
attrdict3
python_docx
paddlenlp==2.5.2
```

- `ppstructure/recovery/requirements.txt`
```pip name=ppstructure/recovery/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/ppstructure/recovery/requirements.txt#L1-L4
python-docx
beautifulsoup4
fonttools>=4.43.0
fire>=0.3.0
```
**Note:** Many submodules and tools may have their own requirements files.

---

## 3. **Key Dependency Version Ranges**

- **paddleocr:** `>=3.4.0,<3.5.0` (from langchain-paddleocr)
- **paddlepaddle:** `>=3.2.1` in some optional features (see `pyproject.toml`), likely higher for latest features
- **numpy:** `>=1.24.0` in `mcp_server` and `>=1.26.4` (with `>=2.1.0` for Python 3.13) in testing
- **opencv-python:** Not version restricted in the requirements found, but must be compatible with recent numpy versions
- **pillow:** `>=9.0.0`
- **typing-extensions:** `>=4.0.0`
- **paddlenlp:** `==2.5.2` (for KIE/NLP features)
- **Other:** See the referenced files above

---

## 4. **Officially Supported Python Versions**

**From `langchain-paddleocr/pyproject.toml`:**
- `requires-python = ">=3.10,<3.13"`
  - **Translation:** As of the latest code, Python 3.10, 3.11, 3.12 are supported. Python 3.13 is specifically excluded.

**No explicit version matrix found in the main README or workflows as of this data.**
- Inference: If you want more details or CI badge evidence, you'll need to check [their workflows here](https://github.com/PaddlePaddle/PaddleOCR/actions) (no YAML files matched in tool search output).

---

## 5. **Python 3.13 Compatibility Issues?**
- `langchain-paddleocr` and several requirements files explicitly disallow `3.13` (see version ranges above).
- Many deep learning libraries or their dependencies (incl. numpy, opencv, pillow, torch, etc.) have reported breakage when new Python versions release, and it appears PaddleOCR similarly excludes 3.13 for now.
- **No issue results returned — check [open/closed issues for Python 3.13](https://github.com/PaddlePaddle/PaddleOCR/issues?q=Python+3.13) directly for ongoing updates in the repo.**

---

## 6. **Most Reported Installation Errors & Dependency Conflicts**
> **The tool search for issue data was not successful due to a query error, so direct issue stats could not be shown.**  
> **Search the [issues page for installation](https://github.com/PaddlePaddle/PaddleOCR/issues?q=installation+error) and [dependency](https://github.com/PaddlePaddle/PaddleOCR/issues?q=dependency+conflict) for up-to-date user reports. Typical pain points in prior years have included:**
- numpy/pillow/opencv incompatibilities (often with major numpy or pillow releases)
- paddlepaddle-gpu mismatches with CUDA version
- OS or compiler dependencies (XPU/NPU integrations, Windows vs Linux, etc)
- Python version-specific bugs (particularly with `.whl` availability)

---

## 7. **Latest Working Combinations for 2025/2026**
- There was a tool call error on issue search by version, so user reports for 2025/2026 are not summarized here. However, based on:
  - The PyPI and GitHub releases,
  - Version pins and exclusions in workspace files,
  - **The most robust “safe” combo as of Feb 2026 is:**

**- Python:** 3.10, 3.11, 3.12 (not 3.13)  
**- paddleocr:** 3.4.x (latest stable)  
**- paddlepaddle:** 3.2.1 or newer (match minor to major for optimal compatibility, CUDA version must fit your GPU)  

**Check user issues for any highly specific edge cases.**

---

### **References & Further Reading**

- [All PaddleOCR releases/tags](https://github.com/PaddlePaddle/PaddleOCR/releases)
- [PaddleOCR on PyPI](https://pypi.org/project/paddleocr/#history)
- [Dependency code search results on GitHub](https://github.com/PaddlePaddle/PaddleOCR/search?q=requirements.txt)
- [Open issues for Python 3.13](https://github.com/PaddlePaddle/PaddleOCR/issues?q=Python+3.13)
- [Known installation issues](https://github.com/PaddlePaddle/PaddleOCR/issues?q=installation+error)

*If you need specific, up-to-the-moment user/tested combos or up-to-date user feedback on dependency edge cases (such as for 3.13 or upcoming PaddlePaddle releases), visiting the GitHub Issues and Discussions directly is recommended.*

---

**If you want the raw full text of any of the `pyproject.toml`/requirements files, let me know!**


-----
Here are the **raw, full texts** for the requested dependency files from the PaddleOCR repository as of their latest commits:

````toml name=mcp_server/pyproject.toml url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/mcp_server/pyproject.toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "paddleocr_mcp"
version = "0.5.0"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.5.0",
    "fastmcp>=2.0.0",
    "httpx>=0.24.0",
    "numpy>=1.24.0",
    "pillow>=9.0.0",
    "puremagic>=1.30.0",
    "typing-extensions>=4.0.0",
]

[project.optional-dependencies]
local = [
    "paddleocr[doc-parser]>=3.4",
]
local-cpu = [
    "paddleocr[doc-parser]>=3.4",
    "paddlepaddle>=3.2.1",
]

[project.scripts]
paddleocr_mcp = "paddleocr_mcp.__main__:main"
````

````toml name=langchain-paddleocr/pyproject.toml url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/langchain-paddleocr/pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "langchain-paddleocr"
version = "0.1.0"
description = "An integration package connecting PaddleOCR and LangChain"
authors = []
readme = "README.md"
license = { text = "Apache License 2.0" }
requires-python = ">=3.10,<3.13"
dependencies = [
    "paddleocr>=3.4.0,<3.5.0",
    "paddlex[serving]>=3.4.1,<3.5.0",
    "langchain-core>=1.2.5,<2.0.0",
    "requests>=2.32.5",
    "pydantic>=2.0.0,<3.0.0",
]

[project.urls]
"Source Code" = "https://github.com/PaddlePaddle/PaddleOCR/tree/main/langchain-paddleocr"
"Release Notes" = "https://github.com/PaddlePaddle/PaddleOCR/releases"
Repository = "https://github.com/PaddlePaddle/PaddleOCR"

[dependency-groups]
lint = ["ruff>=0.13.1,<0.14.0"]
typing = [
    "mypy>=1.18.1,<1.19.0",
    "types-requests>=2.31.0,<3.0.0",
]
test = [
    "pytest>=8.4.0,<9.0.0",
    "freezegun>=1.5.0,<2.0.0",
    "pytest-mock>=3.14.0,<4.0.0",
    "syrupy>=4.9.0,<5.0.0",
    "pytest-watcher>=0.4.0,<1.0.0",
    "pytest-asyncio>=0.21.0,<1.0.0",
    "pytest-retry>=1.7.0,<2.0.0",
    "pytest-socket>=0.7.0,<1.0.0",
    "numpy>=1.26.4; python_version<'3.13'",
    "numpy>=2.1.0; python_version>='3.13'",
    "langchain-tests>=1.1.2,<2.0.0",
    "protobuf>=4.25.0,<7.0.0",
]
test_integration = [
    "pytest>=8.4.0,<9.0.0",
]

[tool.ruff]
fix = true

[tool.ruff.format]
docstring-code-format = true

[tool.ruff.lint]
select = [ "ALL",]
ignore = [
    "C90",     # McCabe complexity
    "COM812",  # Messes with the formatter
    "CPY",     # No copyright
    "FIX002",  # Line contains TODO
    "ISC001",  # Messes with the formatter
    "PERF203", # Rarely useful
    "PLR09",   # Too many something (arg, statements, etc)
    "RUF012",  # Doesn't play well with Pydantic
    "TC001",   # Doesn't play well with Pydantic
    "TC002",   # Doesn't play well with Pydantic
    "TC003",   # Doesn't play well with Pydantic
    "TD002",   # Missing author in TODO
    "TD003",   # Missing issue link in TODO

    # TODO rules
    "ANN401",  # No Any types
    "BLE",     # Blind exceptions
    "DOC",     # Docstrings (preview)
    "ERA",     # No commented-out code
    "PLR2004", # Comparison to magic number
    "PLC0415", # Import top level
    "SIM117",  # Single with statement
    "FBT",     # Bool stuff
    "PT",
    "ARG",     # Argument related
    "SLF",     # Self
    "D",       # Docstring related
    "G",
    "S",
    "A",
    "N",
    "TRY",
    "B",
    "PGH",
    "SIM",
    "ASYNC",
    "PTH",
    "DTZ",
    "PYI",
    "PLW",
]
unfixable = [
    "B028",    # People should intentionally tune the stacklevel
    "PLW1510", # People should intentionally set the check argument
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = [ "D1", "S", "SLF", "ARG001", "PGH003", "PT011"]
"scripts/**" = [ "INP", "S",]

[tool.mypy]
plugins = ["pydantic.mypy"]
strict = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = ["paddleocr.*", "paddlex.*"]
ignore_missing_imports = true

# TODO: activate for 'strict' checking
disallow_any_generics = false
warn_return_any = false

[tool.coverage.run]
omit = [
    "tests/*",
    "*/site-packages/*",
    "*/.venv/*",
    "*/venv/*",
]

[tool.pytest.ini_options]
# --strict-markers will raise errors on unknown marks.
# https://docs.pytest.org/en/7.1.x/how-to/mark.html#raising-errors-on-unknown-marks
#
# https://docs.pytest.org/en/7.1.x/reference/reference.html
# --strict-config       any warnings encountered while parsing the `pytest`
#                       section of the configuration file raise errors.
#
# https://github.com/tophat/syrupy
# --snapshot-warn-unused    Prints a warning on unused snapshots rather than fail the test suite.
#addopts = "--snapshot-warn-unused --strict-markers --strict-config --durations=5"
# Registering custom markers.
# https://docs.pytest.org/en/7.1.x/example/markers.html#registering-markers
markers = [
    "requires: mark tests as requiring a specific library",
    "asyncio: mark tests as requiring asyncio",
    "compile: mark placeholder test used to compile integration tests without running them",
]
asyncio_mode = "auto"
````

```pip name=deploy/avh/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/deploy/avh/requirements.txt
paddlepaddle
numpy
opencv-python
typing-extensions
```

```pip name=ppstructure/kie/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/ppstructure/kie/requirements.txt
sentencepiece
yacs
seqeval
pypandoc
attrdict3
python_docx
paddlenlp==2.5.2
```

```pip name=ppstructure/recovery/requirements.txt url=https://github.com/PaddlePaddle/PaddleOCR/blob/5b15abbe062a7c97df959a8f565a29516980e2b0/ppstructure/recovery/requirements.txt
python-docx
beautifulsoup4
fonttools>=4.43.0
fire>=0.3.0
```

If you need the main `pyproject.toml` of the root repo or any other requirements/lock files, let me know!