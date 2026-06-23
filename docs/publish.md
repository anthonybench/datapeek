# Publishing

How to publish `sleepydatapeek` to PyPI with [Poetry](https://python-poetry.org/).

## Prerequisites

- Poetry installed (`uv tool install poetry`).
- A PyPI account with maintainer access to the `sleepydatapeek` project.
- A PyPI API token, configured once:

  ```sh
  poetry config pypi-token.pypi <your-token>
  ```

- The `[build-system]` in `pyproject.toml` uses Poetry's backend:

  ```toml
  [build-system]
  requires = ["poetry-core"]
  build-backend = "poetry.core.masonry.api"
  ```

## Release

1. Bump the version (PyPI rejects re-uploading an existing version):

   ```sh
   poetry version patch   # or: minor | major | <explicit-version>
   ```

2. Build the wheel and sdist into `dist/`:

   ```sh
   poetry build
   ```

3. (Optional) Smoke-test the artifacts before going live by publishing to TestPyPI:

   ```sh
   poetry config repositories.testpypi https://test.pypi.org/legacy/
   poetry publish -r testpypi
   ```

4. Publish to PyPI:

   ```sh
   poetry publish
   ```

   Steps 2 and 4 can be combined with `poetry publish --build`.

5. Verify the release:

   ```sh
   uv tool install --upgrade sleepydatapeek
   ```
