import os
import argparse
import ee
from datetime import timedelta
#
# CONFIG
#
USER_ROOT=os.path.expanduser('~')
EE_CONFIG_PATH='{}/.config/earthengine'.format(USER_ROOT)
PEM_PATH='{}/.config/secret/privatekey.pem'.format(USER_ROOT)
NOISY=True
STATUS_PROPS=['description','state','id']
ALL='all'
OPENTASKS='opentasks'
FINISHED='finished'
CANCELLABLE=['READY','RUNNING','UNSUBMITTED']
COMPLETED=['COMPLETED','FAILED','CANCELLED','CANCEL_REQUESTED']


#
# INITIALIZATION/USERS
#
def init(user=None):
    sa=os.environ.get('SERVICE_ACCOUNT')
    if sa:
        _out('init','SERVICE_ACCOUNT ({})'.format(sa))
        ee.Initialize(ee.ServiceAccountCredentials(sa,PEM_PATH))
    else:
        if user: user_str='({})'.format(user)
        else: user_str=''
        _out('init','USER_ACCOUNT {}'.format(user_str))
        ee.Initialize()


def current_user(state='CURRENT'):
    os.system("echo 'gee.{}_USER:'".format(state))
    os.system("cat {}/current_user.txt".format(EE_CONFIG_PATH)) 


def switch_user(user_name):
    current_user('PREVIOUS') 
    os.system("rm {}/credentials-last".format(EE_CONFIG_PATH))
    os.system("mv {path}/credentials {path}/credentials-last".format(path=EE_CONFIG_PATH))
    os.system("cp {path}/{user}/credentials {path}/credentials".format(path=EE_CONFIG_PATH,user=user_name))
    os.system("echo '{}' > {}/current_user.txt".format(user_name,EE_CONFIG_PATH))
    current_user('NEW')



#
# TASKS
#
def summary(task_id,detailed=True,props=None):
    task_dict=get_status(task_id)
    print "\t{}".format(_task_report(task_dict,props))
    if detailed:
        error_message=task_dict.get('error_message')
        if error_message: print "\terror: {}".format(error_message)
        tupdate = task_dict.get('update_timestamp_ms')
        tstart = task_dict.get('start_timestamp_ms')
        tcreate = task_dict.get('creation_timestamp_ms')
        if tupdate:
            if tstart: run_time = timedelta(milliseconds=tupdate-tstart)
            else: run_time = "NOT RUNNING"
            if tcreate: total_time = timedelta(milliseconds=tupdate-tcreate)
            else: total_time = "NOT CREATED"
        else:
            run_time = "NO DATA"
            total_time = "NO DATA"
        print "\trun_time: {}".format(run_time)
        print "\ttotal_time: {}".format(total_time)


def cancel(task_id=None,description=None,states=None,opentasks=False):
    if task_id or description or states or opentasks:
        task_list=get_tasks(description=description,task_id=task_id,states=states,opentasks=opentasks)
        for task_dict in task_list: 
            task_id=task_dict.get('id')
            ee.data.cancelTask(task_id)
            _out('cancel',task_id)
    else: _out('cancel','EMPTY REQUEST')


def tasks(n=25,task_id=None,description=None,states=None,opentasks=False,props=None,return_list=False,print_tasks=True):
    task_list=get_tasks(description=description,task_id=task_id,states=states,opentasks=opentasks)
    task_reports=[]
    for task_dict in task_list[:n]: 
        task_report=_task_report(task_dict,props)
        if print_tasks: print task_report
        task_reports.append(task_report)
    if return_list: return task_reports


#
# HELPERS
# 
def get_status(task_id):
    return ee.data.getTaskStatus(task_id)[0]


def get_tasks(task_id=None,description=None,states=None,opentasks=False):
    if opentasks: states=CANCELLABLE
    tasks=ee.data.getTaskList()
    if states:
        states=_get_states(states)
        tasks=filter(lambda s: s['state'] in states,tasks)
    if task_id:
        tasks=filter(lambda s: task_id in s['id'],tasks)
    if description:
        tasks=filter(lambda s: description in s['description'],tasks)
    return tasks


#
#  INTERNAL
#
def _get_states(states):
    if type(states) is str:
        if states!=ALL:
            if states==OPENTASKS:
                states=CANCELLABLE
            elif states==FINISHED:
                states=COMPLETED
            else:
                states=states.split(',')
    return states


def _out(trace_info,data):
    if NOISY: print "gee.{}: {}".format(trace_info,data)


def _task_report(task_dict,props):
    if not props: props=STATUS_PROPS
    return "  |  ".join(map(lambda prop: str(task_dict.get(prop)),props))


#
# MAIN
#
def main():
    parser=argparse.ArgumentParser(description='GEE HELPER')
    subparsers=parser.add_subparsers()
    # status
    parser_status=subparsers.add_parser('status', help='GEE Task Status (consider using gee.summary)')
    parser_status.add_argument('task_id',help='gee-task-id')
    parser_status.set_defaults(func=_status)    
    # summary
    parser_summary=subparsers.add_parser('summary', help='GEE Task Summary')
    parser_summary.add_argument('task_id',help='gee-task-id')
    parser_summary.add_argument('-d','--detailed',default='True',help='include details')
    parser_summary.add_argument('-p','--props',help='comma seperated string of properties')
    parser_summary.set_defaults(func=_summary)    
    # cancel
    parser_cancel=subparsers.add_parser('cancel', help='Cancel Tasks')
    parser_cancel.add_argument('-t','--task_id',help='any portion of gee-task-id')
    parser_cancel.add_argument('-d','--description',help='any portion of gee-task-description')
    parser_cancel.add_argument('-s','--states',help='commas seperated state names or one of all|opentasks')
    parser_cancel.set_defaults(func=_cancel) 
    # tasks
    parser_tasks=subparsers.add_parser('tasks', help='Prints summary of recent tasks')
    parser_tasks.add_argument('-n','--num',default='50',help='number of tasks to print')
    parser_tasks.add_argument('-t','--task_id',help='any portion of gee-task-id')
    parser_tasks.add_argument('-d','--description',help='any portion of gee-task-description')
    parser_tasks.add_argument('-s','--states',help='commas seperated state names or one of all|opentasks|finished')
    parser_tasks.add_argument('-p','--props',help='commas seperated property names to display')
    parser_tasks.set_defaults(func=_tasks)
    # user
    parser_user=subparsers.add_parser('user', help='User Info')
    parser_user.add_argument('-n','--new',help='new username')
    parser_user.set_defaults(func=_user)
    # run
    args=parser.parse_args()
    if (args.func.__name__)!='_user': init()
    args.func(args)


def _status(args):
    print get_status(args.task_id)


def _summary(args):
    detailed=args.detailed.lower()=='true'
    if args.props: props=args.props.split(',')
    else: props=None
    summary(args.task_id,detailed,props)


def _cancel(args):
    cancel(args.task_id,args.description,args.states,False)


def _tasks(args):
    if args.props: props=args.props.split(',')
    else: props=None
    tasks(int(args.num),args.task_id,args.description,args.states,False,props)


def _user(args):
    if args.new: switch_user(args.new)
    else: current_user()


if __name__ == "__main__": 
    main()
