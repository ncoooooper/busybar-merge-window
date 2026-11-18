# Merge Window

Count open GitLab merge requests, see who needs your review, and check branch divergence. GitHub mode follows one pull request and its checks.

## From “Ready” to the check count

1. Open Merge Window with your pull request selected in the companion config.
2. Read the front display. **Ready** means the PR is open, out of draft, meets the review setting, has no pending or failed checks, and GitHub reports a clean merge state.
3. Turn the wheel one notch forward. **CHECKS 1/1** means the one reported check passed. The back display gives the pending and failed counts separately.

![Turning the wheel from Ready to Checks 1/1 on the BUSY Bar](media/guide/inspect-checks.gif)

This recording used an approved PR response with one successful check. Both GIFs are excerpts from the emulator, enlarged pixel by pixel. The first and last frames are held so you can read them.

## Leave the verdict visible

1. From **CHECKS**, turn the wheel one notch back to the verdict.
2. Press **Start** to pin that page. Turning the wheel now keeps the verdict in place. Press **Start** again to unpin it.
3. Click the wheel to request a reading. The companion caches the GitHub response for 60 seconds. Press **Back** to exit.

![Returning from the check total to the Ready verdict](media/guide/return-to-verdict.gif)

A green check run can still be waiting for a reviewer. Merge Window puts **Need review** on the front in that case. A failed check, a requested change, a draft, and a merge conflict each have their own verdict. The companion only reads the PR. Merging stays in GitHub.

## Connect a pull request

On a computer with Python 3.10 or later and GitHub CLI installed, run `gh auth status` and confirm you can read the repository. From this app’s checkout:

```sh
cp companion/example.json config.json
```

Set `repo` to the owner and repository, and `pr` to the pull request number:

```json
{"repo": "your-org/your-repo", "pr": 42, "require_review": true}
```

Leave `require_review` on if you want the bar to wait for an approval even when reviews are optional in that repo. Set it to `false` to follow GitHub’s review decision.

```sh
python3 companion/serve.py --config config.json
```

In the emulator, set **Local companion URL** to `http://127.0.0.1:8770/reading` and allow that local port when prompted. For a physical bar, run the companion with `--host` set to the computer’s LAN address, and use that address in the URL. The GitHub login stays on the computer. If it becomes unavailable, the rear screen marks the last successful reading as offline.

## Run in the emulator

Open BUSY Bar Emulator and run this from the checkout:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

[Full control recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md)

## Additional source setup

Install Git on the companion host. In GitLab, create a token with `read_api` and set `GITLAB_TOKEN` in the companion’s environment. Use the project’s full namespace in `project`. Set `checkout` to the local clone, `branch` to the local branch, and `upstream` to the remote-tracking branch you intend to compare with. Run `git fetch origin` from the checkout when you want current origin refs. The companion reads both refs. It never runs rebase, merge, checkout or fetch.

From the repository root, copy the example and start the companion with Python 3.10 or newer.

```sh
cp companion/live-example.json config.json
# Edit config.json for your source before starting the server.
python3 companion/serve.py --config config.json
```

In the emulator, run `~/.busy-emulator/bin/busy-emulator allow-local 8770` and approve that port. Open **Apps → Merge Window → Setup**, set **Local companion URL** to `http://127.0.0.1:8770/reading`, save, then reopen the app. For a physical bar, start the companion with `--host YOUR_LAN_IP` and replace `127.0.0.1` with that address. Bind only to your trusted network. Open `/reading` on the host to inspect the current reading. Keep credentials in the host environment.

## Check the review queue

OPEN MRS counts all open merge requests in the selected GitLab project. Turn to MY REVIEW to see requests assigned to the signed-in token owner whose review is unreviewed or started. Completed reviews drop out.

![The wheel changes from seven open merge requests to two awaiting review.](media/guide/use-1.gif)

## Decide whether to update a branch

Turn to BEHIND, then BRANCH. Behind with zero commits ahead can fast-forward. Diverged means both sides have commits. Follow the project’s merge or rebase policy. The rear shows which local and remote-tracking refs were compared.

![The sample branch is three commits behind and has diverged.](media/guide/use-2.gif)

The recordings use example responses on emulator firmware. Each display pixel is enlarged to a 9 × 9 square.

[GitLab reviewer states](https://docs.gitlab.com/api/graphql/reference/enums/#mergerequestreviewstate) · [Git revision counts](https://git-scm.com/docs/git-rev-list).
