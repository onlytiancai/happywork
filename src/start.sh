#. /home/huhao/.monitor/bin/activate
curdir=$(cd "$(dirname $0)"; pwd)
setsid python ${curdir}/run.py > ${curdir}/log/log.log 2>&1 &
