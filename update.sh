OPTION="$1 --update -avz"

SRC=/usr/local/packages/easybuild/1.13.0
DEST=/project/lyan1/projects/easybuild_smic/1.13.0

# Config files
rsync $OPTION $SRC/configs/* $DEST/configs/

# etc files
rsync $OPTION $SRC/etc/* $DEST/etc/

# Easybuild framework
rsync $OPTION --include '*.py' --exclude '*.pyc'  $SRC/lib/python2.6/site-packages/easybuild_framework-1.13.0-py2.6.egg/easybuild/* $DEST/easybuild/

# Easyblock files
rsync $OPTION --include '*.py' --exclude '*.pyc' $SRC/lib/python2.6/site-packages/easybuild_easyblocks-1.13.0-py2.6.egg/easybuild/* $DEST/easyblock/
