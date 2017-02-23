#### gee
_This is a work in progress_

A convenience module and command line tool for GEE.

### INSTALL

```bash
$ git clone https://github.com/wri/gee.git
```

----------------------------------------------------------
### COMMAND LINE

```bash
$ python gee.py -h
usage: gee.py [-h] {status,summary,cancel,tasks,user} ...

GEE HELPER

positional arguments:
  {status,summary,cancel,tasks,user}
    status              GEE Task Status (consider using gee.summary)
    summary             GEE Task Summary
    cancel              Cancel Task (consider using gee.status_n)
    tasks               Prints summary of recent tasks
    user                User Info

optional arguments:
  -h, --help            show this help message and exit
```
____



```bash
$ python gee.py summary -h
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
$ python gee.py tasks -h
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
$ python gee.py cancel -h
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

----------------------------------------------------------
### USERS
This module contains methods for (the potentially unsafe but convenient practice of) handling multiple GEE accounts on the same computer. For this to work simply create a sub-directories in you `.config/earthengine` for each user containing their crediential file. The system will then create a `current_user.txt` file and `credentials-last` (backup) file. Your `.config/earthengine` directory will look like this:

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
$ python gee.py user -h
usage: gee.py user [-h] [-n NEW]

optional arguments:
  -n NEW, --new NEW  new username
```

