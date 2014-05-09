# Init module
. /usr/local/packages/Modules/default/init/bash
# Set MODULEPATH
MODULEPATH=/usr/local/packages/Modules/modulefiles
export MODULEPATH
# Load easybuild
module load EasyBuild/1.11.1
# 
PATH=$PATH:/usr/local/packages/Modules/default/bin
export PATH
# Set easybuild configuration file
EASYBUILD_CONFIGFILES=/usr/local/packages/easybuild/1.11.1/etc/config.py
export EASYBUILD_CONFIGFILES
