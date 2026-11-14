#!/bin/bash
# usage: tools/deploy4.sh NAME   (NAME = netlify site name = surge subdomain). Uses logged-in netlify / surge CLIs.
set -e
R=$(cd "$(dirname "$0")/.." && pwd); N=$1; D=/tmp/dist-$N
rm -rf $D && mkdir -p $D
(cd $R && tar --exclude=.git --exclude=__pycache__ --exclude=_shots --exclude=.netlify --exclude=tools --exclude=node_modules --exclude='*.py' --exclude=data --exclude=.netrc --exclude=.env --exclude=CNAME --exclude='*.secret' -cf - .) | (cd $D && tar xf -)
SID=$(netlify sites:list --json 2>/dev/null | python3 -c "import json,sys;n=sys.argv[1];print(next((s['id'] for s in json.load(sys.stdin) if s['name']==n),''))" $N)
if [ -z "$SID" ]; then echo "creating netlify site $N"; netlify sites:create --name $N --disable-linking >/dev/null 2>&1 || true
  SID=$(netlify sites:list --json 2>/dev/null | python3 -c "import json,sys;n=sys.argv[1];print(next((s['id'] for s in json.load(sys.stdin) if s['name']==n),''))" $N); fi
[ -n "$SID" ] || { echo "no netlify site id"; exit 1; }
netlify deploy --prod --dir $D --site $SID --message "$N $(date '+%F %T %Z')" 2>&1 | grep -Ei "deployed|url|error" | head -5
surge $D $N.surge.sh 2>&1 | grep -Ei "success|published|error|domain" | head -3
