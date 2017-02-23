from os.path import expanduser
#
# `gee_config.py` should be in the root directory of your project
#
""" 
    BASE PATH FOR EE-CONFIG 
"""  
USER_ROOT=expanduser('~')
EE_CONFIG_PATH='{}/.config/earthengine'.format(USER_ROOT)

"""
    USER CONFIG
"""
NOISY=True
STATUS_PROPS=['description','state','id']

