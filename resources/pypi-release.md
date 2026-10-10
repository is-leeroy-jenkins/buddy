# PyPI release

Distribution: **buddy-py**. Import: **buddy**. Initial version: **0.1.0**.

## First publication — complete these steps in order

1. Merge the PyPI packaging pull request into `main`.
2. Open GitHub **Settings → Environments**, create an environment named `pypi`.
3. Sign in to [PyPI Publishing](https://pypi.org/manage/account/publishing/) and add a pending GitHub publisher using these exact values:

   | Field | Value |
   |---|---|
   | PyPI project name | `buddy-py` |
   | Owner | `is-leeroy-jenkins` |
   | Repository | `buddy` |
   | Workflow filename | `publish-to-pypi.yml` |
   | Environment | `pypi` |

4. After the publisher is registered, open GitHub **Actions → Publish to PyPI → Run workflow**, select `main`, and run it.
5. Confirm both **build** and **publish** succeed. Check [the project page](https://pypi.org/project/buddy-py/) and install in a fresh virtual environment:

   ```powershell
   python -m pip install buddy-py
   buddy
   ```

A pending publisher does not reserve the package name. The first successful upload creates the project. No API token is needed with Trusted Publishing. Do not create a GitHub release before configuring the publisher. A release is optional for the first upload because the workflow supports manual publication.

## Launch commands

`buddy` opens the tabless Windows window. `buddy-browser` opens the standard browser UI.

```powershell
python -m pip install buddy-py
buddy
```

The desktop command requires Windows and Edge WebView2. The standalone Setup executable remains a separate build documented in [installation.md](installation.md).

## Subsequent releases

Update `pyproject.toml` and `__version__` in `__init__.py` to the same new version. Merge the changes, then publish a GitHub release with a matching tag, for example `v0.1.1`. The release triggers **Publish to PyPI**. PyPI versions cannot be overwritten; a failed upload after partial publication may require a new version.

## Package contents

The wheel contains the application modules, PNG/ICO interface assets, and Streamlit theme configuration. Runtime dependencies are read from `requirements-runtime.txt`. Documentation/build dependencies  are excluded from the base dependency list. Development databases, logs, secrets, GIF demos, and local model weights are excluded.

Application data uses `%LOCALAPPDATA%\Buddy` on Windows and `~/AppData/Local/Buddy` when `LOCALAPPDATA` is absent. Existing user resources are preserved. Provider credentials, external loader services, downloaded models require their normal configuration.

Avoid installing the unrelated `buddy` distribution alongside `buddy-py`; both use the `buddy` import namespace.
