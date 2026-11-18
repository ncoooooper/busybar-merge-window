"""Read pull request review and checks through the official GitHub CLI."""
import json,subprocess
from serve import page
INTERVAL=60
def read_pr(o):
    p=subprocess.run(["gh","pr","view",str(int(o["pr"])),"--repo",o["repo"],"--json","state,isDraft,reviewDecision,mergeStateStatus,statusCheckRollup"],text=True,capture_output=True,timeout=15)
    if p.returncode:raise ValueError("GitHub CLI cannot read the selected PR")
    return json.loads(p.stdout)
def snapshot(o,m):
    data=read_pr(o);checks=data.get("statusCheckRollup") or []
    def outcome(c):
        return str(c.get("conclusion") or c.get("state") or c.get("status") or "UNKNOWN").upper()
    passed=sum(outcome(c) in ("SUCCESS","NEUTRAL","SKIPPED") for c in checks)
    failed=sum(outcome(c) in ("FAILURE","ERROR","CANCELLED","TIMED_OUT","ACTION_REQUIRED","STARTUP_FAILURE") for c in checks)
    pending=len(checks)-passed-failed;review=data.get("reviewDecision") or "UNSPECIFIED"
    state=data["state"].upper();merge=str(data.get("mergeStateStatus","UNKNOWN")).upper()
    if state!="OPEN":verdict=state.title()
    elif data.get("isDraft"):verdict="Draft"
    elif failed:verdict="Checks fail"
    elif pending:verdict="Checking"
    elif review=="CHANGES_REQUESTED":verdict="Changes"
    elif review=="REVIEW_REQUIRED" or (o.get("require_review",True) and review!="APPROVED"):verdict="Need review"
    elif merge!="CLEAN":verdict=merge.title()
    else:verdict="Ready"
    return dict(state="GitHub PR "+str(o["pr"]),key=verdict,alert=verdict=="Ready",pages=[
        page("MERGE WINDOW",verdict,review.replace("_"," ")[:25],str(passed)+" checks passed",fraction=passed/max(1,len(checks))),
        page("CHECKS",f"{passed}/{len(checks)}",f"{pending} pending / {failed} failed","Merge state "+merge)])
