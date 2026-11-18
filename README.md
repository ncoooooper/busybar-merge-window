# Merge Window

Keep one pull request on your desk while its checks run. The front display gives you the verdict. Turn the wheel once to see how many checks have finished and whether any failed.

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
