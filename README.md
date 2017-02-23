##### gee_toolbox ( _this is a work in progress_ )
___
 
`gee_toolbox` is convenience module and command line tool for GEE.  Note if you have earthengine installed you already have access to the [earthengine CLI](https://developers.google.com/earth-engine/command_line]). In most respects the [earthengine CLI](https://developers.google.com/earth-engine/command_line]) is better and more complete.  Use cases for this module/cli are:

* Making task management both pretty and easy
* An `init` method (when used as a module) that uses service accounts (when an ENV var is present)
* User mangement (which you probably shouldn't use)

##### INSTALL

```bash
# pip (testpypi)
pip install -U -i https://testpypi.python.org/pypi  gee_toolbox

# github
$ git https://github.com/wri/gee_toolbox
$ cd gee_toolbox/
$ pip install . 
```

___
##### COMMAND LINE

```bash
$ gee -h
usage: gee.py [-h] {status,summary,cancel,tasks,user} ...

GEE HELPER

positional arguments:
  {status,summary,cancel,tasks,user}
    status              GEE Task Status (consider using gee.summary)
    summary             GEE Task Summary
    cancel              Cancel Tasks
    tasks               Prints summary of recent tasks
    user                User Info

optional arguments:
  -h, --help            show this help message and exit
```
____



```bash
$ gee summary -h
usage: gee.py summary [-h] [-d DETAILED] [-p PROPS] task_id

positional arguments:
  task_id               gee-task-id

optional arguments:
  -d DETAILED, --detailed DETAILED
                        include details
  -p PROPS, --props PROPS
                        comma seperated string of properties

```
____



```bash
$ gee tasks -h
usage: gee.py tasks [-h] [-n NUM] [-t TASK_ID] [-d DESCRIPTION] [-s STATES]
                    [-p PROPS]

optional arguments:
  -n NUM, --num NUM     number of tasks to print
  -t TASK_ID, --task_id TASK_ID
                        any portion of gee-task-id
  -d DESCRIPTION, --description DESCRIPTION
                        any portion of gee-task-description
  -s STATES, --states STATES
                        commas seperated state names or one of
                        all|opentasks|finished
  -p PROPS, --props PROPS
                        commas seperated property names to display
```
____



```bash
$ gee cancel -h
usage: gee.py cancel [-h] [-t TASK_ID] [-d DESCRIPTION] [-s STATES]

optional arguments:
  -t TASK_ID, --task_id TASK_ID
                        any portion of gee-task-id
  -d DESCRIPTION, --description DESCRIPTION
                        any portion of gee-task-description
  -s STATES, --states STATES
                        commas seperated state names or one of
                        all|opentasks|finished
```

___
##### SERVICE_ACCOUNT

Simply set a `SERVICE_ACCOUNT` environment variable 

```bash
$ export SERVICE_ACCOUNT=yourserviceaccount@project_id.iam.gserviceaccount.com
```

and `gee.init()` will use the account to initialize earthengine.

___
##### USERS
This module contains methods for (the potentially unsafe but convenient practice of) handling multiple GEE accounts on the same computer. For this to work simply create a sub-directories in your `.config/earthengine` for each user containing their crediential file. The system will then create a `current_user.txt` file and `credentials-last` (backup) file. Your `.config/earthengine` directory will look like this:

```bash
$ tree <USER_HOME>/.config/earthengine
<USER_HOME>/.config/earthengine
├── username1
│   └── credentials
├── username2
│   └── credentials
├── client_secrets.json
├── credentials
├── credentials-last
├── current_user.txt
├── username3
│   └── credentials
```

```bash
$ gee user -h
usage: gee.py user [-h] [-n NEW]

optional arguments:
  -n NEW, --new NEW  new username
```