#!/bin/sh
# chkconfig: 2345 99 10
# description: enable celery to manage tasks
. /etc/init.d/functions

# Change these 6 variables for different configurations
RUN_USER="kettle_data_transfer"
CD_DIR="/home/${RUN_USER}/dt-regression-api/"
NODES="1"
LOG_FILE="/home/${RUN_USER}/dt-regression-api/%n.log"
PID_FILE="/home/${RUN_USER}/dt-regression-api/%n.pid"
WORKER_NAME="dt_regression_api"


if [[ `dirname $0` == /etc/rc*.d ]]; then
    target="$(readlink $0)"
else
    target=$0
fi

prog="$(basename $target)"

CELERYD_PID_DIR=`dirname $PID_FILE`

fstart() {
	su - ${RUN_USER} -c "cd ${CD_DIR}; venv/bin/celery multi start ${NODES} -A ${WORKER_NAME}.tasks --pidfile=${PID_FILE} --logfile=${LOG_FILE} -n ${WORKER_NAME}"
}

fstop() {
	su - ${RUN_USER} -c "cd ${CD_DIR}; venv/bin/celery multi stop ${NODES} --pidfile=${PID_FILE}"
}

frestart() {
    su - ${RUN_USER} -c "cd ${CD_DIR}; venv/bin/celery multi restart ${NODES} -A ${WORKER_NAME}.tasks --pidfile=${PID_FILE} --logfile=${LOG_FILE} -n ${WORKER_NAME}"
}

_get_pid_files() {
    [[ ! -d "$CELERYD_PID_DIR" ]] && return
    echo $(ls -1 "$CELERYD_PID_DIR"/*.pid 2> /dev/null)
}

fstatus() {
    local pid_files=$(_get_pid_files)
    [[ -z "$pid_files" ]] && echo "$prog is stopped" && return 1
    for pid_file in $pid_files; do
        local node=$(basename "$pid_file" .pid)
        echo Worker $node PID $(cat "$pid_file") is running
    done
    return 0
}

ARG=$1

[ -z "$ARG" ] && ARG=usage

case $ARG in

        start)
		        fstart
        ;;

        stop)
                fstop
        ;;

        restart)
                echo "Restarting ..."
                frestart
        ;;

        status)
                fstatus
        ;;

        *)
                echo "Usage:$0 (start|stop|status|restart)"
        ;;
esac

exit 0