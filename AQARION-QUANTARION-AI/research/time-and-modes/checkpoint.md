# Time and Modes — Hosted Computational Checkpoint

## Status

**COMPUTATIONAL_CHECKPOINT_PASS**

This record verifies that the repository’s supplied checks and timing-model
sweeps completed successfully in a hosted GitHub Actions environment.

It does **not** establish physical validation, scientific novelty, historical
priority, formal proof, or reproduction of any externally reported experiment.

## Tested revision

- Repository: `quantarion369-arch/AQARION`
- Branch: `main`
- Tested commit: `71b45894ca5f6ba6bbae9b71e848f65bac3446ce`
- Workflow: `.github/workflows/time-and-modes-check.yml`
- Workflow run: Time and Modes Check #4
- Run ID: `38320884906`
- Artifact ID: `11779142554`
- Artifact ZIP SHA-256: `df286741401af8744ba69e526842ae758d898c99959276873a79b88534cb811b`

## Environment

- Runner operating system: Ubuntu 24.04
- Python: 3.12.15
- NumPy: 2.5.4
- SciPy: 1.18.1
- Dependency source: `requirements.txt`

## Commands executed

The workflow executed the repository’s `run.sh` unchanged:

```bash
python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py
python -m unittest -v test_causal_estimator
python timing_models.py

Skip to content
AQARION
Repository navigation
Code
Issues
Pull requests
1
 (1)
Time and Modes Check
Time and Modes Check #4
Annotations
1 warning
check
succeeded 12 minutes ago in 48s
2s
Current runner version: '2.337.0'
Runner Image Provisioner
Operating System
Runner Image
GITHUB_TOKEN Permissions
Secret source: Actions
Cache mode: write
Prepare workflow directory
Prepare all required actions
Getting action download info
Download action repository 'actions/checkout@v4' (SHA:11d5960a326750d5838078e36cf38b85af677262)
Download action repository 'actions/setup-python@v5' (SHA:a26af69be951a213d495a4c3e4e4022e16d87065)
Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
Complete job name: check
2s
2s
9s
0s
27s
1s
2s
0s
0s

---

sha256:df286741401af8744ba69e526842ae758d898c99959276873a79b88534cb811b


https://productionresultssa16.blob.core.windows.net/actions-results/cf2031b3-f5e7-4ab9-bcd2-b3db9e232ccc/workflow-job-run-39abf7d8-ef4f-5311-9646-8dd648f443d9/logs/job/job-logs.txt?rsct=text%2Fplain&se=2026-10-12T23%3A34%3A14Z&sig=39Bbu82jBaRJwlCbyR613uyY%2BvqEB81XRpYhuH1XfLk%3D&ske=2026-10-13T01%3A20%3A38Z&skoid=ca7593d4-ee42-46cd-af88-8b886a2f84eb&sks=b&skt=2026-10-12T21%3A20%3A38Z&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skv=2025-11-05&sp=r&spr=https&sr=b&st=2026-10-12T23%3A24%3A09Z&sv=2025-11-05


2026-10-12T23:12:22.2800094Z Current runner version: '2.337.0'
2026-10-12T23:12:22.2823163Z ##[group]Runner Image Provisioner
2026-10-12T23:12:22.2823870Z Hosted Compute Agent
2026-10-12T23:12:22.2824334Z Version: 20261002.596
2026-10-12T23:12:22.2824942Z Commit: c3d12f3313a95f25162a1503be624f3b0617f8c0
2026-10-12T23:12:22.2825536Z Build Date: 2026-10-02T22:28:27Z
2026-10-12T23:12:22.2826172Z Worker ID: {13b5927f-3377-4201-893c-40aec0eed885}
2026-10-12T23:12:22.2826747Z Region: westus3
2026-10-12T23:12:22.2827196Z Cloud: Azure
2026-10-12T23:12:22.2827717Z ##[endgroup]
2026-10-12T23:12:22.2828819Z ##[group]Operating System
2026-10-12T23:12:22.2829358Z Ubuntu
2026-10-12T23:12:22.2829948Z 24.04.5
2026-10-12T23:12:22.2830377Z LTS
2026-10-12T23:12:22.2830877Z ##[endgroup]
2026-10-12T23:12:22.2831332Z ##[group]Runner Image
2026-10-12T23:12:22.2831888Z Image: ubuntu-24.04
2026-10-12T23:12:22.2832368Z Version: 20261004.327.1
2026-10-12T23:12:22.2833460Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md
2026-10-12T23:12:22.2834689Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20261004.327
2026-10-12T23:12:22.2835492Z ##[endgroup]
2026-10-12T23:12:22.2836395Z ##[group]GITHUB_TOKEN Permissions
2026-10-12T23:12:22.2838567Z Contents: read
2026-10-12T23:12:22.2839074Z Metadata: read
2026-10-12T23:12:22.2839725Z ##[endgroup]
2026-10-12T23:12:22.2841609Z Secret source: Actions
2026-10-12T23:12:22.2842407Z Cache mode: write
2026-10-12T23:12:22.2843078Z Prepare workflow directory
2026-10-12T23:12:22.3191204Z Prepare all required actions
2026-10-12T23:12:22.3232172Z Getting action download info
2026-10-12T23:12:22.6305647Z Download action repository 'actions/checkout@v4' (SHA:11d5960a326750d5838078e36cf38b85af677262)
2026-10-12T23:12:22.9378685Z Download action repository 'actions/setup-python@v5' (SHA:a26af69be951a213d495a4c3e4e4022e16d87065)
2026-10-12T23:12:23.5552449Z Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
2026-10-12T23:12:24.2584761Z Complete job name: check
2026-10-12T23:12:24.3484549Z ##[group]Run actions/checkout@v4
2026-10-12T23:12:24.3485581Z with:
2026-10-12T23:12:24.3486224Z   persist-credentials: false
2026-10-12T23:12:24.3487031Z   repository: quantarion369-arch/AQARION
2026-10-12T23:12:24.3493711Z   token: ***
2026-10-12T23:12:24.3494510Z   ssh-strict: true
2026-10-12T23:12:24.3495390Z   ssh-user: git
2026-10-12T23:12:24.3496018Z   clean: true
2026-10-12T23:12:24.3496677Z   sparse-checkout-cone-mode: true
2026-10-12T23:12:24.3497468Z   fetch-depth: 1
2026-10-12T23:12:24.3498101Z   fetch-tags: false
2026-10-12T23:12:24.3498747Z   show-progress: true
2026-10-12T23:12:24.3499416Z   lfs: false
2026-10-12T23:12:24.3500140Z   submodules: false
2026-10-12T23:12:24.3500798Z   set-safe-directory: true
2026-10-12T23:12:24.3501562Z   allow-unsafe-pr-checkout: false
2026-10-12T23:12:24.3502630Z ##[endgroup]
2026-10-12T23:12:24.4413558Z Syncing repository: quantarion369-arch/AQARION
2026-10-12T23:12:24.4415993Z ##[group]Getting Git version info
2026-10-12T23:12:24.4417056Z Working directory is '/home/runner/work/AQARION/AQARION'
2026-10-12T23:12:24.4418515Z [command]/usr/bin/git version
2026-10-12T23:12:24.4587981Z git version 2.55.0
2026-10-12T23:12:24.4605593Z ##[endgroup]
2026-10-12T23:12:24.4620407Z Temporarily overriding HOME='/home/runner/work/_temp/0de90f53-48fb-4899-a1d4-2a3a01c88522' before making global git config changes
2026-10-12T23:12:24.4623625Z Adding repository directory to the temporary git global config as a safe directory
2026-10-12T23:12:24.4626160Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/AQARION/AQARION
2026-10-12T23:12:24.4960742Z Deleting the contents of '/home/runner/work/AQARION/AQARION'
2026-10-12T23:12:24.4963471Z ##[group]Initializing the repository
2026-10-12T23:12:24.4965080Z [command]/usr/bin/git init /home/runner/work/AQARION/AQARION
2026-10-12T23:12:24.7193564Z hint: Using 'master' as the name for the initial branch. This default branch name
2026-10-12T23:12:24.7201865Z hint: will change to "main" in Git 3.0. To configure the initial branch name
2026-10-12T23:12:24.7202677Z hint: to use in all of your new repositories, which will suppress this warning,
2026-10-12T23:12:24.7203264Z hint: call:
2026-10-12T23:12:24.7203551Z hint:
2026-10-12T23:12:24.7203941Z hint: 	git config --global init.defaultBranch <name>
2026-10-12T23:12:24.7204242Z hint:
2026-10-12T23:12:24.7204525Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2026-10-12T23:12:24.7204958Z hint: 'development'. The just-created branch can be renamed via this command:
2026-10-12T23:12:24.7205291Z hint:
2026-10-12T23:12:24.7205493Z hint: 	git branch -m <name>
2026-10-12T23:12:24.7205717Z hint:
2026-10-12T23:12:24.7206009Z hint: Disable this message with "git config set advice.defaultBranchName false"
2026-10-12T23:12:24.7206450Z Initialized empty Git repository in /home/runner/work/AQARION/AQARION/.git/
2026-10-12T23:12:24.7207922Z [command]/usr/bin/git remote add origin https://github.com/quantarion369-arch/AQARION
2026-10-12T23:12:24.7542040Z ##[endgroup]
2026-10-12T23:12:24.7542542Z ##[group]Disabling automatic garbage collection
2026-10-12T23:12:24.7545610Z [command]/usr/bin/git config --local gc.auto 0
2026-10-12T23:12:24.8133760Z ##[endgroup]
2026-10-12T23:12:24.8134387Z ##[group]Setting up auth
2026-10-12T23:12:24.8141236Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-12T23:12:24.8176275Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-12T23:12:24.8538181Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-12T23:12:24.8570048Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-12T23:12:24.8775480Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-12T23:12:24.8810662Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-12T23:12:24.9025716Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-10-12T23:12:25.0593249Z ##[endgroup]
2026-10-12T23:12:25.0603802Z ##[group]Fetching the repository
2026-10-12T23:12:25.0605336Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +71b45894ca5f6ba6bbae9b71e848f65bac3446ce:refs/remotes/origin/main
2026-10-12T23:12:26.4956673Z From https://github.com/quantarion369-arch/AQARION
2026-10-12T23:12:26.4957220Z  * [new ref]         71b45894ca5f6ba6bbae9b71e848f65bac3446ce -> origin/main
2026-10-12T23:12:26.4996304Z ##[endgroup]
2026-10-12T23:12:26.4996919Z ##[group]Determining the checkout info
2026-10-12T23:12:26.4997482Z ##[endgroup]
2026-10-12T23:12:26.4997814Z [command]/usr/bin/git sparse-checkout disable
2026-10-12T23:12:26.6249108Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2026-10-12T23:12:26.6282602Z ##[group]Checking out the ref
2026-10-12T23:12:26.6286716Z [command]/usr/bin/git checkout --progress --force -B main refs/remotes/origin/main
2026-10-12T23:12:26.6714909Z Switched to a new branch 'main'
2026-10-12T23:12:26.6717195Z branch 'main' set up to track 'origin/main'.
2026-10-12T23:12:26.6726433Z ##[endgroup]
2026-10-12T23:12:26.6771118Z [command]/usr/bin/git log -1 --format=%H
2026-10-12T23:12:26.6797680Z 71b45894ca5f6ba6bbae9b71e848f65bac3446ce
2026-10-12T23:12:26.6806503Z ##[group]Removing auth
2026-10-12T23:12:26.6810582Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-12T23:12:26.6843160Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-12T23:12:26.7047338Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-12T23:12:26.7074550Z http.https://github.com/.extraheader
2026-10-12T23:12:26.7082128Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2026-10-12T23:12:26.7116066Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-12T23:12:26.7322827Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-12T23:12:26.7355309Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-12T23:12:26.7571139Z ##[endgroup]
2026-10-12T23:12:26.7794156Z ##[group]Run actions/setup-python@v5
2026-10-12T23:12:26.7794437Z with:
2026-10-12T23:12:26.7794604Z   python-version: 3.12
2026-10-12T23:12:26.7794782Z   cache: pip
2026-10-12T23:12:26.7795097Z   cache-dependency-path: AQARION-QUANTARION-AI/research/time-and-modes/requirements.txt
2026-10-12T23:12:26.7795472Z   check-latest: false
2026-10-12T23:12:26.7797335Z   token: ***
2026-10-12T23:12:26.7797512Z   update-environment: true
2026-10-12T23:12:26.7797710Z   allow-prereleases: false
2026-10-12T23:12:26.7797898Z   freethreaded: false
2026-10-12T23:12:26.7798076Z ##[endgroup]
2026-10-12T23:12:26.9058092Z ##[group]Installed versions
2026-10-12T23:12:26.9130432Z (node:2187) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-12T23:12:26.9147816Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-12T23:12:26.9148191Z Successfully set up CPython (3.12.15)
2026-10-12T23:12:26.9148813Z ##[endgroup]
2026-10-12T23:12:27.0796903Z [command]/opt/hostedtoolcache/Python/3.12.15/x64/bin/pip cache dir
2026-10-12T23:12:27.8354568Z /home/runner/.cache/pip
2026-10-12T23:12:28.1976784Z pip cache is not found
2026-10-12T23:12:28.2105507Z ##[group]Run set -eu
2026-10-12T23:12:28.2105782Z [36;1mset -eu[0m
2026-10-12T23:12:28.2106027Z [36;1mpython -m pip install --upgrade pip[0m
2026-10-12T23:12:28.2106321Z [36;1mpython -m pip install -r requirements.txt[0m
2026-10-12T23:12:28.2106745Z [36;1mpython -c 'import numpy, scipy; print("NumPy", numpy.__version__); print("SciPy", scipy.__version__)'[0m
2026-10-12T23:12:28.2928673Z shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0}
2026-10-12T23:12:28.2928990Z env:
2026-10-12T23:12:28.2929244Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:28.2929794Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib/pkgconfig
2026-10-12T23:12:28.2930141Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:28.2930445Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:28.2930782Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:28.2931154Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib
2026-10-12T23:12:28.2931412Z ##[endgroup]
2026-10-12T23:12:29.1669348Z Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages (26.2.1)
2026-10-12T23:12:29.9367319Z Collecting numpy (from -r requirements.txt (line 1))
2026-10-12T23:12:29.9760993Z   Downloading numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
2026-10-12T23:12:30.1083247Z Collecting scipy (from -r requirements.txt (line 2))
2026-10-12T23:12:30.1119112Z   Downloading scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (62 kB)
2026-10-12T23:12:30.1384688Z Downloading numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
2026-10-12T23:12:30.3136385Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 97.5 MB/s  0:00:00
2026-10-12T23:12:30.3173953Z Downloading scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (35.3 MB)
2026-10-12T23:12:30.6041767Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35.3/35.3 MB 123.5 MB/s  0:00:00
2026-10-12T23:12:30.6933130Z Installing collected packages: numpy, scipy
2026-10-12T23:12:36.9297722Z 
2026-10-12T23:12:36.9307230Z Successfully installed numpy-2.5.4 scipy-1.18.1
2026-10-12T23:12:37.1180581Z NumPy 2.5.4
2026-10-12T23:12:37.1204416Z SciPy 1.18.1
2026-10-12T23:12:37.1355961Z ##[group]Run set -eu
2026-10-12T23:12:37.1356211Z [36;1mset -eu[0m
2026-10-12T23:12:37.1356560Z [36;1mfor file in run.sh requirements.txt causal_estimator.py test_causal_estimator.py timing_models.py[0m
2026-10-12T23:12:37.1356937Z [36;1mdo[0m
2026-10-12T23:12:37.1357165Z [36;1m  test -f "$file" || { echo "MISSING: $file"; exit 1; }[0m
2026-10-12T23:12:37.1357427Z [36;1m  echo "FOUND: $file"[0m
2026-10-12T23:12:37.1357617Z [36;1mdone[0m
2026-10-12T23:12:37.1416186Z shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0}
2026-10-12T23:12:37.1416494Z env:
2026-10-12T23:12:37.1416763Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1417094Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib/pkgconfig
2026-10-12T23:12:37.1417421Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1417717Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1418085Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1418380Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib
2026-10-12T23:12:37.1418637Z ##[endgroup]
2026-10-12T23:12:37.1503600Z FOUND: run.sh
2026-10-12T23:12:37.1503904Z FOUND: requirements.txt
2026-10-12T23:12:37.1504209Z FOUND: causal_estimator.py
2026-10-12T23:12:37.1504446Z FOUND: test_causal_estimator.py
2026-10-12T23:12:37.1504699Z FOUND: timing_models.py
2026-10-12T23:12:37.1532894Z ##[group]Run set -eu
2026-10-12T23:12:37.1533138Z [36;1mset -eu[0m
2026-10-12T23:12:37.1533367Z [36;1mLOG_DIR="$RUNNER_TEMP/time-and-modes-check"[0m
2026-10-12T23:12:37.1533643Z [36;1mmkdir -p "$LOG_DIR"[0m
2026-10-12T23:12:37.1533836Z [36;1m[0m
2026-10-12T23:12:37.1534015Z [36;1mcp run.sh "$LOG_DIR/run-script.txt"[0m
2026-10-12T23:12:37.1534436Z [36;1msha256sum run.sh causal_estimator.py test_causal_estimator.py timing_models.py > "$LOG_DIR/source-sha256.txt"[0m
2026-10-12T23:12:37.1534826Z [36;1m[0m
2026-10-12T23:12:37.1534978Z [36;1mset +e[0m
2026-10-12T23:12:37.1535212Z [36;1mbash -ex -o pipefail run.sh 2>&1 | tee "$LOG_DIR/run.log"[0m
2026-10-12T23:12:37.1535488Z [36;1mresult=${PIPESTATUS[0]}[0m
2026-10-12T23:12:37.1535837Z [36;1mset -e[0m
2026-10-12T23:12:37.1536064Z [36;1m[0m
2026-10-12T23:12:37.1536248Z [36;1mecho "$result" > "$LOG_DIR/exit-code.txt"[0m
2026-10-12T23:12:37.1536597Z [36;1mecho "Script exit code = $result" >> "$GITHUB_STEP_SUMMARY"[0m
2026-10-12T23:12:37.1536860Z [36;1m[0m
2026-10-12T23:12:37.1537014Z [36;1mexit "$result"[0m
2026-10-12T23:12:37.1596816Z shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0}
2026-10-12T23:12:37.1597106Z env:
2026-10-12T23:12:37.1597334Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1597699Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib/pkgconfig
2026-10-12T23:12:37.1598028Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1598322Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1598617Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:12:37.1598910Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib
2026-10-12T23:12:37.1599168Z ##[endgroup]
2026-10-12T23:12:37.1739981Z + python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py
2026-10-12T23:12:37.2121914Z + python -m unittest -v test_causal_estimator
2026-10-12T23:12:37.3740365Z test_future_spike_and_centered_negative_control (test_causal_estimator.TestBackwardSlope.test_future_spike_and_centered_negative_control) ... ok
2026-10-12T23:12:37.3790120Z test_insufficient_history (test_causal_estimator.TestBackwardSlope.test_insufficient_history) ... ok
2026-10-12T23:12:37.3799875Z test_invalid_inputs (test_causal_estimator.TestBackwardSlope.test_invalid_inputs) ... ok
2026-10-12T23:12:37.3830010Z test_linear_irregular_sampling (test_causal_estimator.TestBackwardSlope.test_linear_irregular_sampling) ... ok
2026-10-12T23:12:37.3850068Z test_prefix_consistency (test_causal_estimator.TestBackwardSlope.test_prefix_consistency) ... ok
2026-10-12T23:12:37.3850806Z test_window_boundary (test_causal_estimator.TestBackwardSlope.test_window_boundary) ... ok
2026-10-12T23:12:37.3910154Z test_feature_time_and_future_replacement (test_causal_estimator.TestGeometryFeatures.test_feature_time_and_future_replacement) ... ok
2026-10-12T23:12:37.3980194Z test_geometry_and_units (test_causal_estimator.TestGeometryFeatures.test_geometry_and_units) ... ok
2026-10-12T23:12:37.4001231Z test_missing_history_and_stale_frame (test_causal_estimator.TestGeometryFeatures.test_missing_history_and_stale_frame) ... ok
2026-10-12T23:12:37.4040477Z test_nonpositive_radius (test_causal_estimator.TestGeometryFeatures.test_nonpositive_radius) ... ok
2026-10-12T23:12:37.4040979Z 
2026-10-12T23:12:37.4041155Z ----------------------------------------------------------------------
2026-10-12T23:12:37.4041470Z Ran 10 tests in 0.059s
2026-10-12T23:12:37.4041592Z 
2026-10-12T23:12:37.4041661Z OK
2026-10-12T23:12:37.4229781Z + python timing_models.py
2026-10-12T23:13:04.5062722Z {
2026-10-12T23:13:04.5063070Z   "mechanical_displacement": {
2026-10-12T23:13:04.5063336Z     "observable_unit": "model units",
2026-10-12T23:13:04.5063570Z     "sampled_peak": {
2026-10-12T23:13:04.5063853Z       "frequency_ratio": 1.0,
2026-10-12T23:13:04.5064164Z       "omega_d_rad_s": 6.283185307179586,
2026-10-12T23:13:04.5064827Z       "measured_amplitude": 0.2533029524200644,
2026-10-12T23:13:04.5065208Z       "analytic_amplitude": 0.25330295910584444,
2026-10-12T23:13:04.5065595Z       "relative_error": 2.6394401664298073e-08
2026-10-12T23:13:04.5065921Z     },
2026-10-12T23:13:04.5066197Z     "maximum_relative_error": 3.028898799961599e-05,
2026-10-12T23:13:04.5066576Z     "acceptance_threshold": 0.001,
2026-10-12T23:13:04.5066897Z     "comparison_pass": true
2026-10-12T23:13:04.5067176Z   },
2026-10-12T23:13:04.5067400Z   "rlc_current": {
2026-10-12T23:13:04.5067662Z     "observable_unit": "A",
2026-10-12T23:13:04.5067904Z     "sampled_peak": {
2026-10-12T23:13:04.5068086Z       "frequency_ratio": 1.0,
2026-10-12T23:13:04.5068289Z       "omega_d_rad_s": 6.283185307179586,
2026-10-12T23:13:04.5068519Z       "measured_amplitude": 1.5915493889021943,
2026-10-12T23:13:04.5068754Z       "analytic_amplitude": 1.5915494309189535,
2026-10-12T23:13:04.5068978Z       "relative_error": 2.6399908370500214e-08
2026-10-12T23:13:04.5069185Z     },
2026-10-12T23:13:04.5069382Z     "maximum_relative_error": 3.028899702672838e-05,
2026-10-12T23:13:04.5069768Z     "acceptance_threshold": 0.001,
2026-10-12T23:13:04.5069979Z     "comparison_pass": true
2026-10-12T23:13:04.5070173Z   }
2026-10-12T23:13:04.5070318Z }
2026-10-12T23:13:04.5070707Z Output directory: /home/runner/work/AQARION/AQARION/AQARION-QUANTARION-AI/research/time-and-modes/timing-models-r2fh7v5g
2026-10-12T23:13:04.5071181Z Status: MODEL_COMPARISON_PASS
2026-10-12T23:13:04.6023430Z ##[group]Run actions/upload-artifact@v4
2026-10-12T23:13:04.6023696Z with:
2026-10-12T23:13:04.6023916Z   name: time-and-modes-check-38320884906-1
2026-10-12T23:13:04.6024295Z   path: /home/runner/work/_temp/time-and-modes-check/
2026-10-12T23:13:04.6024638Z   if-no-files-found: warn
2026-10-12T23:13:04.6024871Z   retention-days: 30
2026-10-12T23:13:04.6025084Z   compression-level: 6
2026-10-12T23:13:04.6025296Z   overwrite: false
2026-10-12T23:13:04.6025857Z   include-hidden-files: false
2026-10-12T23:13:04.6026668Z env:
2026-10-12T23:13:04.6026894Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:13:04.6028314Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib/pkgconfig
2026-10-12T23:13:04.6028929Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:13:04.6029905Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:13:04.6030464Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.15/x64
2026-10-12T23:13:04.6031565Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.15/x64/lib
2026-10-12T23:13:04.6032039Z ##[endgroup]
2026-10-12T23:13:04.7622997Z (node:2296) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-12T23:13:04.7623692Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-12T23:13:04.7700574Z With the provided path, there will be 4 files uploaded
2026-10-12T23:13:04.7701240Z Artifact name is valid!
2026-10-12T23:13:04.7701554Z Root directory input is valid!
2026-10-12T23:13:05.1094422Z Beginning upload of artifact content to blob storage
2026-10-12T23:13:05.1290939Z (node:2296) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-12T23:13:05.3484977Z Uploaded bytes 1563
2026-10-12T23:13:05.4060550Z Finished uploading artifact content to blob storage!
2026-10-12T23:13:05.4061069Z SHA256 digest of uploaded artifact zip is df286741401af8744ba69e526842ae758d898c99959276873a79b88534cb811b
2026-10-12T23:13:05.4062237Z Finalizing artifact upload
2026-10-12T23:13:05.6530712Z Artifact time-and-modes-check-38320884906-1.zip successfully finalized. Artifact ID 11779142554
2026-10-12T23:13:05.6531845Z Artifact time-and-modes-check-38320884906-1 has been successfully uploaded! Final size is 1563 bytes. Artifact ID is 11779142554
2026-10-12T23:13:05.6537609Z Artifact download URL: https://github.com/quantarion369-arch/AQARION/actions/runs/38320884906/artifacts/11779142554
2026-10-12T23:13:05.6716722Z Post job cleanup.
2026-10-12T23:13:05.7772023Z (node:2309) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-12T23:13:05.7772700Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-12T23:13:05.7936632Z [command]/usr/bin/tar --posix -cf cache.tzst --exclude cache.tzst -P -C /home/runner/work/AQARION/AQARION --files-from manifest.txt --use-compress-program zstdmt
2026-10-12T23:13:06.1736946Z (node:2309) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-12T23:13:07.1657147Z Sent 38797312 of 52451718 (74.0%), 37.0 MBs/sec
2026-10-12T23:13:07.4338863Z Sent 52451718 of 52451718 (100.0%), 39.4 MBs/sec
2026-10-12T23:13:07.6781166Z Cache saved with the key: setup-python-Linux-x64-24.04-Ubuntu-python-3.12.15-pip-a1f58ed6e4aebab99649f4572e5a64145686858f72bcbce28d197f7def919fe6
2026-10-12T23:13:07.6933268Z Post job cleanup.
2026-10-12T23:13:07.7685329Z [command]/usr/bin/git version
2026-10-12T23:13:07.7724293Z git version 2.55.0
2026-10-12T23:13:07.7758193Z Temporarily overriding HOME='/home/runner/work/_temp/c3c86f0b-7a38-474b-914a-c4a23c1e1363' before making global git config changes
2026-10-12T23:13:07.7759219Z Adding repository directory to the temporary git global config as a safe directory
2026-10-12T23:13:07.7763680Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/AQARION/AQARION
2026-10-12T23:13:07.7803931Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-12T23:13:07.7848264Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-12T23:13:07.8079270Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-12T23:13:07.8114623Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-12T23:13:07.8348663Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-12T23:13:07.8383671Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-12T23:13:07.8732319Z Cleaning up orphan processes
2026-10-12T23:13:07.8988552Z ##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/

Excellent—this is the complete hosted evidence. We can now record the checkpoint precisely.

## Verified hosted result

**Repository:** `quantarion369-arch/AQARION`  
**Branch:** `main`  
**Tested commit:** `71b45894ca5f6ba6bbae9b71e848f65bac3446ce`  
**Workflow:** Time and Modes Check #4  
**Runner:** Ubuntu 24.04, Python 3.12.15  
**Dependencies:** NumPy 2.5.4, SciPy 1.18.1  
**Artifact ZIP SHA-256:** `df286741401af8744ba69e526842ae758d898c99959276873a79b88534cb811b`

## What passed

| Check | Result |
|---|---|
| Required files | All five found |
| Python syntax | Passed for all three Python files |
| Estimator tests | 10 tests, all OK |
| Mechanical displacement model | Passed |
| Series RLC current model | Passed |
| `run.sh` exit code | 0 |
| Model status | `MODEL_COMPARISON_PASS` |

## Numerical results

Both sweeps used a 0.001 maximum relative-error threshold.

- **Mechanical displacement:** maximum relative error `3.028898799961599e-05`, about 0.00303%.
- **RLC current:** maximum relative error `3.028899702672838e-05`, about 0.00303%.
- Both sampled peaks occurred at frequency ratio `1.0`.
- The mechanical sampled peak was `0.2533029524200644` versus analytic `0.25330295910584444`.
- The RLC sampled peak was `1.5915493889021943` A versus analytic `1.5915494309189535` A.

## Accurate claim status

You can now state:

> At commit `71b4589`, the hosted Time and Modes Check installed NumPy 2.5.4 and SciPy 1.18.1, passed 10 estimator tests, and completed both mechanical-displacement and series-RLC-current sweeps. Each sweep’s maximum sampled-amplitude relative error was below the 0.001 acceptance threshold.

You cannot yet state:

- That the water-ring or vortex hypothesis is physically validated.
- That the RLC-to-mechanical mapping describes a real physical system.
- That this establishes priority or novelty.
- That the separately reported 10 mH RLC result was independently reproduced.

----------------------------------------------------------------------                                      Ran 10 tests in 0.059s                                
OK                                                    + python timing_models.py                             {
  "mechanical_displacement": {                            "observable_unit": "model units",                     "sampled_peak": {                                       "frequency_ratio": 1.0,
      "omega_d_rad_s": 6.283185307179586,                   "measured_amplitude": 0.2533029524200644,             "analytic_amplitude": 0.25330295910584444,            "relative_error": 2.6394401664298073e-08
    },                                                    "maximum_relative_error": 3.028898799961599e-05,      "acceptance_threshold": 0.001,
    "comparison_pass": true                             },
  "rlc_current": {
    "observable_unit": "A",
    "sampled_peak": {
      "frequency_ratio": 1.0,                               "omega_d_rad_s": 6.283185307179586,
      "measured_amplitude": 1.5915493889021943,
      "analytic_amplitude": 1.5915494309189535,
      "relative_error": 2.6399908370500214e-08            },
    "maximum_relative_error": 3.028899702672838e-05,      "acceptance_threshold": 0.001,
    "comparison_pass": true                             }
}
Output directory: /home/runner/work/AQARION/AQARION/AQARION-QUANTARION-AI/research/time-and-modes/timing-models-r2fh7v5g                                          Status: MODEL_COMPARISON_PASS

===== run-script.txt =====
python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py
python -m unittest -v test_causal_estimator           python timing_models.py                                                                                     ~/pb-core-direct-enum-audit $

---

def rlc_rhs(t, state, L, R, C, V0, omega_d):
    q, current = state
    voltage = V0 * np.cos(omega_d * t)
    dq_dt = current
    di_dt = (voltage - R*current - q/C) / L
    return [dq_dt, di_dt]

https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/research/time-and-modes

For timing test — ideal series RLC driven by prescribed V_{in}(t), $L>0$, $C>0$, $R>0$:

Governing equation

Charge $q(t)$, current i(t)=\dot q(t), Kirchhoff voltage law:[
  {
    "ratio": 0.5,
    "amp": 0.03369868917724763,
    "expected": 0.03369892440492949,
    "rel_err": 6.980272694634415e-06
  },
  {
    "ratio": 0.525,
    "amp": 0.03487633507843102,
    "expected": 0.034877003270691195,
    "rel_err": 1.915853420630942e-05
  },
  {
    "ratio": 0.55,
    "amp": 0.03620345744186427,
    "expected": 0.03620345786350707,
    "rel_err": 1.1646478781379699e-08
  },
  {
    "ratio": 0.575,
    "amp": 0.03770189914900334,
    "expected": 0.03770286312317716,
    "rel_err": 2.5567664998504824e-05
  },
  {
    "ratio": 0.6,
    "amp": 0.03940578446606516,
    "expected": 0.039405796194980455,
    "rel_err": 2.976444185565086e-07
  },
  {
    "ratio": 0.625,
    "amp": 0.04134950015784676,
    "expected": 0.04135074167199976,
    "rel_err": 3.002398754647917e-05
  },
  {
    "ratio": 0.65,
    "amp": 0.04358666667240371,
    "expected": 0.04358676526129264,
    "rel_err": 2.2618996462497876e-06
  },
  {
    "ratio": 0.675,
    "amp": 0.04617721542318316,
    "expected": 0.04617733737565538,
    "rel_err": 2.6409593785192698e-06
  },
  {
    "ratio": 0.7,
    "amp": 0.04920530909375005,
    "expected": 0.04920591661455338,
    "rel_err": 1.2346499062121374e-05
  },
  {
    "ratio": 0.725,
    "amp": 0.05278351792912135,
    "expected": 0.052784293420873006,
    "rel_err": 1.4691714170900205e-05
  },
  {
    "ratio": 0.75,
    "amp": 0.05706512068152096,
    "expected": 0.05706537913252002,
    "rel_err": 4.529033241995606e-06
  },
  {
    "ratio": 0.775,
    "amp": 0.06226304572693454,
    "expected": 0.062263359722666584,
    "rel_err": 5.04302584114491e-06
  },
  {
    "ratio": 0.8,
    "amp": 0.06868635547623878,
    "expected": 0.06868640860706396,
    "rel_err": 7.735274890618982e-07
  },
  {
    "ratio": 0.825,
    "amp": 0.07679131353241048,
    "expected": 0.07679139593619372,
    "rel_err": 1.073086147718172e-06
  },
  {
    "ratio": 0.8500000000000001,
    "amp": 0.08727770476024914,
    "expected": 0.08727776983789115,
    "rel_err": 7.45638232158008e-07
  },
  {
    "ratio": 0.875,
    "amp": 0.10124921717315455,
    "expected": 0.10125001723462018,
    "rel_err": 7.901840290869266e-06
  },
  {
    "ratio": 0.9,
    "amp": 0.12048353821870089,
    "expected": 0.1204839309724496,
    "rel_err": 3.259801913291227e-06
  },
  {
    "ratio": 0.925,
    "amp": 0.14772692610149984,
    "expected": 0.14772830435156958,
    "rel_err": 9.329627628118509e-06
  },
  {
    "ratio": 0.95,
    "amp": 0.18607425611206552,
    "expected": 0.18607494777053013,
    "rel_err": 3.7170961104671107e-06
  },
  {
    "ratio": 0.9750000000000001,
    "amp": 0.2317722669440927,
    "expected": 0.23177298246088293,
    "rel_err": 3.0871449409053398e-06
  },
  {
    "ratio": 1.0,
    "amp": 0.2533029524200644,
    "expected": 0.25330295910584444,
    "rel_err": 2.6394401664298073e-08
  },
  {
    "ratio": 1.025,
    "amp": 0.2215717958434637,
    "expected": 0.2215729540199319,
    "rel_err": 5.227066061985752e-06
  },
  {
    "ratio": 1.05,
    "amp": 0.17262461625213266,
    "expected": 0.17262577505658816,
    "rel_err": 6.712812470333063e-06
  },
  {
    "ratio": 1.0750000000000002,
    "amp": 0.13391694523918932,
    "expected": 0.1339208111228173,
    "rel_err": 2.8866937077043353e-05
  },
  {
    "ratio": 1.1,
    "amp": 0.10684835358204342,
    "expected": 0.10684940435987444,
    "rel_err": 9.83419455935497e-06
  },
  {
    "ratio": 1.125,
    "amp": 0.08780753882772552,
    "expected": 0.08781019850977442,
    "rel_err": 3.028898799961599e-05
  },
  {
    "ratio": 1.15,
    "amp": 0.07398037936657031,
    "expected": 0.07398072199927071,
    "rel_err": 4.631378163533206e-06
  },
  {
    "ratio": 1.175,
    "amp": 0.06358822710366088,
    "expected": 0.06358825721125896,
    "rel_err": 4.734773274561732e-07
  },
  {
    "ratio": 1.2000000000000002,
    "amp": 0.055540330744075356,
    "expected": 0.055540347899495295,
    "rel_err": 3.0888211166590906e-07
  },
  {
    "ratio": 1.225,
    "amp": 0.04914691180727,
    "expected": 0.04914737886983462,
    "rel_err": 9.503305676838991e-06
  },
  {
    "ratio": 1.25,
    "amp": 0.04395926751168505,
    "expected": 0.04395930150852094,
    "rel_err": 7.733707024781822e-07
  },
  {
    "ratio": 1.275,
    "amp": 0.03967231138244817,
    "expected": 0.03967250956096833,
    "rel_err": 4.995361330806247e-06
  },
  {
    "ratio": 1.3,
    "amp": 0.036075775995684733,
    "expected": 0.036075869200555666,
    "rel_err": 2.583579356452148e-06
  },
  {
    "ratio": 1.3250000000000002,
    "amp": 0.03301851386870219,
    "expected": 0.033018524433691875,
    "rel_err": 3.1997158755903143e-07
  },
  {
    "ratio": 1.35,
    "amp": 0.030389603052908838,
    "expected": 0.030390080188959244,
    "rel_err": 1.5700388002914956e-05
  },
  {
    "ratio": 1.375,
    "amp": 0.028107814715074834,
    "expected": 0.028108028815533332,
    "rel_err": 7.617057030340213e-06
  },
  {
    "ratio": 1.4,
    "amp": 0.026109390467041266,
    "expected": 0.026109545024599664,
    "rel_err": 5.919580684077275e-06
  },
  {
    "ratio": 1.425,
    "amp": 0.024345800091084967,
    "expected": 0.024345992626690557,
    "rel_err": 7.908307890436284e-06
  },
  {
    "ratio": 1.4500000000000002,
    "amp": 0.022778863726585583,
    "expected": 0.022779160523274992,
    "rel_err": 1.3029307603606988e-05
  },
  {
    "ratio": 1.475,
    "amp": 0.02137862126680467,
    "expected": 0.021378628950883227,
    "rel_err": 3.5942803322530636e-07
  },
  {
    "ratio": 1.5,
    "amp": 0.020119500319849985,
    "expected": 0.020119891297311433,
    "rel_err": 1.943238438373296e-05
  }
]
1. First-order form for simulation

State $$:[q][i]
Initially unenergized:
Equivalent v_C = q/C form:
2. Frequency-sweep test

Fix R,L,C,V_0, vary only \omega_d:
Parameters:
\omega_0 undamped natural frequency, \alpha decay rate.

Observable — current amplitude:
Maximum at:
Reactances cancel at \omega_0.

Charge / v_C amplitude peaks at different frequency:
This is the same shift you saw in mechanical run — sampled peak $1.000$ vs theoretical displacement peak $0.9975 = \sqrt{1-2\zeta^2}$ for \zeta=0.05.

Mechanical ↔ electrical: m\leftrightarrow L, b\leftrightarrow R, k\leftrightarrow 1/C, x\leftrightarrow q.

3. Two-pulse timing test

Smooth finite pulse:
Input:
Simulate:
Hold T_p,V_p,R,L,C fixed, sweep \Delta only. This matches your "change delay between two inputs" design.

Possible responses: peak current in fixed window after 2nd pulse, stored energy after 2nd pulse, energy dissipated after 2nd pulse.

4. Energy balance — safeguard
V_{in}i source power in
Ri^2 resistive dissipation
Source off → $E$ cannot increase in ideal passive model

Fixed V_p,T_p does not guarantee equal delivered energy — current during 2nd pulse depends on state left by 1st. Record:
Minimal RHS for your previous sweep code
def rlc_rhs(t, state, L, R, C, V0, omega_d):
    q, current = state
    voltage = V0 * np.cos(omega_d * t)
    dq_dt = current
    di_dt = (voltage - R*current - q/C) / L
    return [dq_dt, di_dt]
Next check: run same frequency sweep you ran for mechanical oscillator, compare numerical I_{amp} vs analytic V_0/\sqrt{R^2+(\omega_d L-1/(\omega_d C))^2}, largest relative error should be O(10^{-5}) with your $rtol=1e-8$ settings — same $0.003\%$ level you already achieved.

Your plot and JSON show the mechanical displacement sweep—not yet an RLC current sweep. I have now run the separate **RLC** simulation and compared its current amplitude with the analytical prediction.

## What your plot establishes

The blue numerical curve closely follows the theoretical displacement response. The sampled maximum is at $$\omega_d/\omega_0=1.000$$, while the theoretical displacement maximum for $$\zeta=0.05$$ is at

$$
\frac{\omega_{\mathrm{peak}}}{\omega_0}
=\sqrt{1-2\zeta^2}
\approx0.997497.
$$

Your frequency grid has spacing 0.025, so it does not resolve that small shift. There is no contradiction between the sampled and theoretical peaks.

The title and legend also have missing Greek characters. Fix those before publication, and give the vertical-axis units—or explicitly call them model units.

## New RLC simulation: actual result

I chose parameters that reproduce the same oscillator equation for charge:

$$
L=1\ \mathrm H,\qquad
C=\frac{1}{(2\pi)^2}\ \mathrm F
\approx0.0253303\ \mathrm F,
$$

$$
R=0.6283185\ \Omega,\qquad V_0=1\ \mathrm V.
$$

These give $$f_0=1$$ Hz and $$\zeta=0.05$$. They are illustrative simulation parameters, not a hardware recommendation.

I swept 41 frequency ratios from 0.5 to 1.5, simulated 100 driving cycles per setting, and measured current amplitude over the final ten cycles.

| Check | Computed result |
|---|---:|
| Sampled current-peak frequency ratio | 1.000 |
| Numerical peak current amplitude | 1.591549389 A |
| Analytical peak current amplitude | 1.591549431 A |
| Largest relative discrepancy across the sweep | 0.0030289% |

The analytical comparison was

$$
I_{\mathrm{amp}}(\omega_d)
=
\frac{V_0}{
\sqrt{R^2+\left(\omega_dL-\frac{1}{\omega_dC}\right)^2}
}.
$$

For an ideal series RLC, current peaks at $$\omega_0=1/\sqrt{LC}$$, where the reactances cancel. [1027][1030]

The new current-sweep CSV is attached.

## The important distinction

The mechanical/electrical mapping is:

$$
x\leftrightarrow q,
\qquad
\dot x\leftrightarrow i.
$$

Therefore:

- Mechanical displacement corresponds to electrical charge.
- Mechanical velocity corresponds to electrical current.
- The charge/displacement peak is slightly shifted by damping.
- The series-current peak is at $$\omega_0$$. [1029]

Do not compare a displacement plot directly with a current formula and call them the same observable.

## What we can put in the report

> A numerical series-RLC frequency sweep agreed with the analytical current response to a maximum relative discrepancy of approximately 0.00303% over the tested grid. The result validates this numerical implementation of a known linear model; it does not establish new resonance physics or validate vortex-ring dynamics.

One final correction: setting `rtol=1e-8` does not guarantee a particular amplitude error. The reported discrepancy also depends on integration settings, transient duration, and sampled peak extraction. We measured the agreement rather than assuming it.

This is now a genuine second model execution—but because the RLC equations were deliberately mapped to the mechanical oscillator, it is a structural consistency check, not independent physical confirmation.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/179686421/4e955d56-6a36-416d-acc0-d4d229be14a4/1000031202.jpg
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/179686421/b7e812c4-2651-4b76-a2af-bfef1bfebc40/1000031225.jpg
[3] RLC Circuit: Series and Parallel, Applied circuits https://techweb.rohm.com/product/circuit-design/electric-circuit-design/23194/
[4] 6.3: The RLC Circuit - Mathematics LibreTexts https://math.libretexts.org/Bookshelves/Differential_Equations/Elementary_Differential_Equations_with_Boundary_Value_Problems_(Trench)/06:_Applications_of_Linear_Second_Order_Equations/6.03:_The_RLC_Circuit
[5] Series RLC Circuit Analysis - Electronics Tutorials https://www.electronics-tutorials.ws/accircuits/series-circuit.html
[6] 1000031369.jpeg https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/179686421/4583919a-49d4-4498-ace9-6e30f52c38d5/1000031369.jpeg
Run complete — resonance sweep verified
Sampled peak frequency ratio: 1.000
Sampled peak amplitude: 0.253303
Peak / half-frequency amplitude: 7.5167
Largest relative numerical error: 0.003029%

Theoretical displacement peak: 0.99750 = sqrt(1-2*zeta^2)
zeta=0.05, Q-factor ~ 10.0
What this proves:

Solver solve_ivp with rtol=1e-8, atol=1e-10, max_step=period/30 after 100 periods transient decay → final 10 cycles measurement = steady state
Measured amp = ptp(displacement)/2 matches analytic:
Error $0.003\%$ max across 41 points $0.5\le \omega_d/\omega_0 \le 1.5$ — numerical integration reproduces theory
Peak at sampled grid $1.000$ vs theoretical $0.9975$ — difference is grid resolution (step 0.025), not physics. Velocity resonance exactly at $1.0$, displacement resonance slightly below due to sqrt(1-2\zeta^2)
Amplification $7.5\times$ vs half-frequency drive — classic Q\approx 1/(2\zeta)=10 behavior

This is the clean inverse of the leapfrog predictor: there you used causal backward slope to avoid future leak, here you use long transient to isolate steady-state, both are about removing contamination from outside the measurement window.

Plot — blue measured vs orange theory, dashed lines at \omega_d=\omega_0 and theoretical peak $0.9975$:
Files:
📎 resonance_sweep.json
— 41 points ratio/amp/expected/rel_err
📎 resonance_curve.png
This is now a verified bounded verifier artifact you can drop into EVIDENCE/RESONANCE/ same pattern as Burnside M3 — JSON + recompute script + validation.md + hashes.{
  "parameters": {
    "L_h": 0.01,
    "C_f": 0.0001,
    "R_ohm": 2.0,
    "source_peak_v": 1.0,
    "initial_charge_c": 0,
    "initial_current_a": 0
  },
  "natural_frequency_hz": 159.15494309189535,
  "damping_ratio": 0.1,
  "sampled_peak": {
    "frequency_ratio": 1.0,
    "frequency_hz": 159.15494309189535,
    "numerical_peak_current_a": 0.49999999848905785,
    "analytic_peak_current_a": 0.5,
    "relative_error": 3.0218842983487093e-09,
    "mean_input_power_w": 0.24999999924453775,
    "mean_resistive_power_w": 0.24999999848907561,
    "charge_amplitude_c": 0.0004999999984515123
  },
  "max_relative_current_error": 3.0782224629048974e-09,
  "selected_rows": [
    {
      "frequency_ratio": 0.5,
      "frequency_hz": 79.57747154594767,
      "numerical_peak_current_a": 0.06608186004825806,
      "analytic_peak_current_a": 0.06608186004550898,
      "relative_error": 4.16011102068307e-11,
      "mean_input_power_w": 0.004366812247174282,
      "mean_resistive_power_w": 0.004366812227437046,
      "charge_amplitude_c": 0.00013216372008826205
    },
    {
      "frequency_ratio": 0.8,
      "frequency_hz": 127.32395447351627,
      "numerical_peak_current_a": 0.2030692329613287,
      "analytic_peak_current_a": 0.20306923302672383,
      "relative_error": 3.2203368662933906e-10,
      "mean_input_power_w": 0.041237113545372246,
      "mean_resistive_power_w": 0.04123711337549773,
      "charge_amplitude_c": 0.0002538365411792046
    },
    {
      "frequency_ratio": 1.0,
      "frequency_hz": 159.15494309189535,
      "numerical_peak_current_a": 0.49999999848905785,
      "analytic_peak_current_a": 0.5,
      "relative_error": 3.0218842983487093e-09,
      "mean_input_power_w": 0.24999999924453775,
      "mean_resistive_power_w": 0.24999999848907561,
      "charge_amplitude_c": 0.0004999999984515123
    },
    {
      "frequency_ratio": 1.2,
      "frequency_hz": 190.9859317102744,
      "numerical_peak_current_a": 0.2394260650105131,
      "analytic_peak_current_a": 0.2394260653402866,
      "relative_error": 1.377349979950821e-09,
      "mean_input_power_w": 0.05732484083940304,
      "mean_resistive_power_w": 0.05732484060641646,
      "charge_amplitude_c": 0.00019952172081717188
    },
    {
      "frequency_ratio": 1.5,
      "frequency_hz": 238.73241463784302,
      "numerical_peak_current_a": 0.11668647616277074,
      "analytic_peak_current_a": 0.11668647623766212,
      "relative_error": 6.418171768922084e-10,
      "mean_input_power_w": 0.013615733793854685,
      "mean_resistive_power_w": 0.013615733719286415,
      "charge_amplitude_c": 7.77909840918124e-05
    },
    {
      "frequency_ratio": 2.0,
      "frequency_hz": 318.3098861837907,
      "numerical_peak_current_a": 0.06608186002772712,
      "analytic_peak_current_a": 0.06608186004550898,
      "relative_error": 2.690883595904726e-10,
      "mean_input_power_w": 0.004366812253387159,
      "mean_resistive_power_w": 0.004366812224729343,
      "charge_amplitude_c": 3.304093000419105e-05
    }
  ],
  "scope": "Ideal linear lumped series RLC simulation; not hardware measurements."
}Write out the RLC differential equations for this test

For our timing test, use an ideal **series** RLC circuit driven by a prescribed voltage $$V_{\mathrm{in}}(t)$$, with $$L>0$$, $$C>0$$, and $$R>0$$.

The governing equation is

$$
\boxed{
L\ddot q+R\dot q+\frac{q}{C}=V_{\mathrm{in}}(t)
}
$$

where $$q(t)$$ is capacitor charge and $$i(t)=\dot q(t)$$ is the shared series current. This follows from Kirchhoff’s voltage law. [1029]

## 1. First-order equations for simulation

Using charge and current as the state variables:

$$
\boxed{
\begin{aligned}
\dot q &= i,\\
\dot i &= \frac{V_{\mathrm{in}}(t)-Ri-q/C}{L}.
\end{aligned}
}
$$

For an initially unenergized circuit, choose

$$
q(0)=0,\qquad i(0)=0.
$$

An equivalent formulation uses capacitor voltage $$v_C=q/C$$:

$$
\boxed{
\begin{aligned}
\dot v_C &= \frac{i}{C},\\
\dot i &= \frac{V_{\mathrm{in}}(t)-Ri-v_C}{L}.
\end{aligned}
}
$$

These are convenient state-space forms of the same circuit model. [1026][1029]

## 2. Frequency-sweep test

Keep $$R,L,C$$, and the source’s peak voltage $$V_0$$ fixed. Change only the driving angular frequency $$\omega_d$$:

$$
V_{\mathrm{in}}(t)=V_0\cos(\omega_dt).
$$

Then

$$
\boxed{
\ddot q+\frac RL\dot q+\frac{1}{LC}q
=
\frac{V_0}{L}\cos(\omega_dt).
}
$$

The oscillator parameters are

$$
\omega_0=\frac{1}{\sqrt{LC}},
\qquad
\alpha=\frac{R}{2L},
\qquad
\zeta=\frac{R}{2}\sqrt{\frac CL}.
$$

Here $$\omega_0$$ is the undamped natural angular frequency and $$\alpha$$ is the decay-rate parameter. [1027][1028]

### Observable and analytical prediction

Measure steady-state current amplitude:

$$
\boxed{
I_{\mathrm{amp}}(\omega_d)=
\frac{V_0}{
\sqrt{
R^2+
\left(\omega_dL-\frac{1}{\omega_dC}\right)^2
}
}.
}
$$

For this ideal series circuit, current amplitude reaches its maximum at

$$
\omega_d=\omega_0,\qquad
I_{\mathrm{amp,max}}=\frac{V_0}{R}.
$$

The inductive and capacitive reactances cancel at that frequency. [1029][1030]

Keep the observable explicit: charge or capacitor-voltage amplitude does not generally peak at exactly the same frequency as current. From the charge-response denominator, its nonzero-frequency maximum occurs at

$$
\omega_{\mathrm{charge,peak}}
=
\omega_0\sqrt{1-2\zeta^2},
$$

when $$\zeta<1/\sqrt2$$. This is the damped-displacement distinction in the mechanical analogy. [1029]

## 3. Two-pulse timing test

To match our “change the delay between two inputs” idea more closely, define two identical, nonoverlapping voltage pulses.

A smooth finite-duration pulse can be

$$
p(t)=
\begin{cases}
\sin^2\!\left(\dfrac{\pi t}{T_p}\right),
&0\leq t\leq T_p,\\
0,&\text{otherwise}.
\end{cases}
$$

Use

$$
\boxed{
V_{\mathrm{in}}(t;\Delta)
=
V_p\,[p(t)+p(t-\Delta)],
\qquad \Delta\geq T_p.
}
$$

Then simulate

$$
\boxed{
\begin{aligned}
\dot q &= i,\\
\dot i &=
\frac{
V_p[p(t)+p(t-\Delta)]-Ri-q/C
}{L}.
\end{aligned}
}
$$

This is our proposed test input, not a new circuit law. Hold pulse shape, duration $$T_p$$, amplitude $$V_p$$, and circuit parameters fixed; sweep the pulse-start separation $$\Delta$$.

Possible response measurements include:

- Peak current in a fixed window after the second pulse.
- Stored energy immediately after the second pulse.
- Energy dissipated after the second pulse.

## 4. Energy balance—the safeguard against overclaiming

Stored electrical energy is

$$
E(t)=\frac12Li^2+\frac{q^2}{2C}.
$$

Differentiating and substituting the governing equations gives

$$
\boxed{
\frac{dE}{dt}
=
V_{\mathrm{in}}(t)i(t)-Ri(t)^2.
}
$$

Thus:

- $$V_{\mathrm{in}}i$$ is instantaneous source power delivered to the circuit.
- $$Ri^2$$ is resistive dissipation.
- With the source off, stored energy cannot increase in this ideal passive model.

This balance follows directly from the RLC voltage law and element relations. [1029]

Fixed pulse amplitude and duration do not guarantee equal delivered energy: the current during the second pulse depends on the state left by the first. Record

$$
W_{\mathrm{in}}=\int V_{\mathrm{in}}(t)i(t)\,dt
$$

alongside the response.

## Minimal Python right-hand side

For the sinusoidal sweep:

```python
import numpy as np

def rlc_rhs(t, state, L, R, C, V0, omega_d):
    q, current = state
    voltage = V0 * np.cos(omega_d * t)

    dq_dt = current
    di_dt = (voltage - R * current - q / C) / L

    return [dq_dt, di_dt]
```

This specifies the computational model. It has not yet been run here as an RLC experiment; the next check is to compare numerical steady-state current amplitudes with the analytical formula above.

Citations:
[1] [PDF] RLC Circuit Response and Analysis (Using State Space Method) http://www.science.smith.edu/~jcardell/Courses/EGR326/RLC_SSModelIEEE.pdf
[2] RLC Circuit: Series and Parallel, Applied circuits https://techweb.rohm.com/product/circuit-design/electric-circuit-design/23194/
[3] RLC circuit - Wikipedia https://en.wikipedia.org/wiki/RLC_circuit
[4] 6.3: The RLC Circuit - Mathematics LibreTexts https://math.libretexts.org/Bookshelves/Differential_Equations/Elementary_Differential_Equations_with_Boundary_Value_Problems_(Trench)/06:_Applications_of_Linear_Second_Order_Equations/6.03:_The_RLC_Circuit
[5] Series RLC Circuit Analysis - Electronics Tutorials https://www.electronics-tutorials.ws/accircuits/series-circuit.html
[6] RLC natural response - derivation (article) | Khan Academy https://www.khanacademy.org/a/ee-rlc-natural-response-derivation
[7] RLC Circuit State-Space Representation | PDF | Capacitor - Scribd https://www.scribd.com/document/882386841/The-state-space-representation-in-RLC-circuits
[8] [PDF] ELECTRICAL CIRCUIT ANALYSIS Lecture Notes Prepared By S ... https://mrcet.com/downloads/digital_notes/EEE/31082020/Electrical%20Circuit%20Analysis.pdf
[9] series RLC circuit - All About Circuits Forum https://forum.allaboutcircuits.com/threads/series-rlc-circuit.50885/
[10] Need help with modelling a RLC Circuit into State Space Model https://www.reddit.com/r/ControlTheory/comments/180ijsa/need_help_with_modelling_a_rlc_circuit_into_state/

---

https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/research/time-and-modes
