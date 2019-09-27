#!/usr/bin/env bash
me=$(realpath ${BASH_SOURCE})
here=${me%/*}

problem=${1:?expecting problem name}
py=${problem}.py
problem_path=${here}/${problem}

[[ -d ${problem_path} ]] && { echo "directory ${problem_path} already exists." 1>&2 ; exit 1; }
mkdir -pv ${problem_path}
cp -v ${here}/__template__.py ${problem_path}/${py}
cat<<EOF ${problem_path}/README.md

# get user id info for current id
user_id_info=$(getent passwd $(id -u)|cut -f5 -d':'|cut -f1 -d',')
long_email_address="${user_id_info:-tbs} <${EMAIL:-tbs}>"

# ${problem}

Todo ${long_email_address}:

* Adds problem description to `${py}`.

* Solve the problem.

* Write commentary (below).

* `git add . && git push`

* Convert commentary to blog post.

* Blog dat sh*t.

* Publish blog post.

* Tweet dat sh*t. 

EOF
