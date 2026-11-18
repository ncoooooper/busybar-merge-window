"""Inspect GitLab review assignments and compare local Git refs without changing them."""
import json,os,subprocess
from urllib.request import Request,urlopen
from serve import page
def reading(o,m):
    base=o.get("host","https://gitlab.com").rstrip("/")+"/api/v4"
    headers={"PRIVATE-TOKEN":os.environ["GITLAB_TOKEN"]}
    def get(path):
        with urlopen(Request(base+path,headers=headers),timeout=12) as r:return json.load(r),r.headers.get("X-Next-Page","")
    me=get("/user")[0]["username"]
    query="""query($path: ID!, $cursor: String) {
      project(fullPath: $path) { mergeRequests(state: opened, first: 25, after: $cursor) {
        pageInfo { endCursor hasNextPage }
        nodes { reviewers { nodes { username mergeRequestInteraction { reviewState } } } }
      } }
    }"""
    cursor=None;opened=waiting=0
    while True:
        body=json.dumps({"query":query,"variables":{"path":o["project"],"cursor":cursor}}).encode()
        req=Request(o.get("host","https://gitlab.com").rstrip("/")+"/api/graphql",data=body,
                    headers={**headers,"Content-Type":"application/json"})
        with urlopen(req,timeout=12) as r:result=json.load(r)
        if result.get("errors"):raise ValueError("GitLab could not read reviewer states")
        connection=result["data"]["project"]["mergeRequests"]
        for mr in connection["nodes"]:
            opened+=1
            for user in mr["reviewers"]["nodes"]:
                if user["username"]==me and (user.get("mergeRequestInteraction") or {}).get("reviewState") in ("UNREVIEWED","REVIEW_STARTED"):waiting+=1
        if not connection["pageInfo"]["hasNextPage"]:break
        cursor=connection["pageInfo"]["endCursor"]
    args=["git","-C",os.path.expanduser(o["checkout"]),"rev-list","--left-right","--count",
          "refs/heads/"+o["branch"]+"...refs/remotes/"+o.get("upstream","origin/main"),"--"]
    ahead,behind=map(int,subprocess.check_output(args,text=True,timeout=8).split())
    status="Diverged" if ahead and behind else "Behind" if behind else "Ahead" if ahead else "Current"
    return dict(state="GitLab / local refs",key=f"{opened}/{waiting}/{ahead}/{behind}",pages=[
        page("OPEN MRS",opened,o["project"]),page("MY REVIEW",waiting,me,"Requested or in progress"),
        page("BEHIND",behind,o["branch"],o.get("upstream","origin/main"),f"{ahead} commits ahead"),
        page("BRANCH",status,"Rebase or merge" if behind and ahead else "Fast-forward possible" if behind else "No update needed","Using last fetched refs")])
