#!/usr/bin/env bash
me=$(realpath ${BASH_SOURCE})
here=${me%/*}


problem=${1:?expecting problem name}
problem_path=${here}/${problem}

[[ -d ${problem_path} ]] && { echo "directory ${problem_path} already exists." 1>&2 ; exit 1; }

echo -n "description:"
description="$(</dev/stdin)"

# copy the template of a python coding problem solution into ${problem} and
#   do some housekeeping afterwards.
mkdir -pv ${problem_path}
env problem=${problem} description="${description}" envsubst < ${here}/__template__/__template__.py > ${problem_path}/${problem}.py
env problem=${problem} description="${description}" envsubst < ${here}/__template__/README.md > ${problem_path}/README.md

git add ${problem_path}
git commit -m "${problem} initialized and commited by ${me##*/}"

# TODO mike@carif.io: abstract away the ide using alternatives?
[[ -n "$2" ]] && ( set -x ; env -C ${problem_path} pycharm-professional . & )

