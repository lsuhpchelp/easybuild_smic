##
# This file is an EasyBuild reciPY as per https://github.com/hpcugent/easybuild
#
# Copyright:: Copyright 2012-2013 University of Luxembourg/Luxembourg Centre for Systems Biomedicine
# Authors::   Cedric Laczny <cedric.laczny@uni.lu>, Fotis Georgatos <fotis.georgatos@uni.lu>, Kenneth Hoste
# License::   MIT/GPL
# $Id$
#
# This work implements a part of the HPCBIOS project and is a component of the policy:
# http://hpcbios.readthedocs.org/en/latest/HPCBIOS_2012-94.html
##
"""
EasyBuild support for building LAST, implemented as an easyblock

@author: Le Yan
"""
import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake


class EB_last(ConfigureMake):
    """
    Support for building SOAPdenovo-Trans.
    """

    def __init__(self, *args, **kwargs):
        """Define lists of files to install."""
        super(EB_last, self).__init__(*args, **kwargs)

        self.binaries = ["lastal", "lastdb", "last-split", "last-merge-batches", "last-pair-probs"]

    def configure_step(self):
        """
	    Skip the configure as not part of this build process.
        """
        pass

    def install_step(self):
        """
        Install by copying files to install dir
        """
        srcdir = self.cfg['start_dir']
        destdir = os.path.join(self.installdir, 'bin')
        srcfile = None
        try:
            os.makedirs(destdir)
            for suff in self.binaries:
                srcfile = os.path.join(srcdir, "src/%s" % suff)
                shutil.copy2(srcfile, destdir)
        except OSError, err:
            self.log.error("Copying %s to installation dir %s failed: %s" % (srcfile, destdir, err))

	destdir = os.path.join(self.installdir, 'scripts')
        scripts = os.path.join(srcdir, "scripts")
	try:
	    shutil.copytree(scripts, destdir)
	except OSError, err:
	    self.log.error("Copying %s to installation dir %s failed: %s" % (scripts, destdir, err))
	

#    def sanity_check_step(self):
#        """Custom sanity check for LAST."""
#
#        custom_paths = {
#                        'files': ['bin/SOAPdenovo-Trans-%s' % x for x in self.bin_suffixes],
#                        'dirs': []
#                       }
#
#        super(EB_last, self).sanity_check_step(custom_paths=custom_paths)
