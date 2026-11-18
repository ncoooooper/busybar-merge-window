# Merge Window

Identify the remaining review, failing check or merge-state condition on one GitHub pull request.

Configure repo and pr. Install and sign in to GitHub CLI with read access to that repository. It reads gh pr view fields from your selected PR and never merges or writes. By default an approving review is required by this dashboard even in a repository with optional reviews. Set require_review to false to defer to GitHub's review decision.

## Connect the bar

Copy companion/example.json to a private config.json and adjust it for your source. From the project folder run `python3 companion/serve.py --config config.json`. Use Python 3.10+. Set Local companion URL to `http://127.0.0.1:8770/reading` on the emulator and allow local port 8770. On hardware, bind the companion to a trusted LAN interface and set its reachable address. The wheel browses pages. Click refreshes. Start pins or unpins the current page. The last good reading is labeled offline after a source error.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)
