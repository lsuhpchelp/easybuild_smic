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
EasyBuild support for building SOAPdenovo-Trans, implemented as an easyblock

@author: Le Yan
"""
import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake


class EB_soapdenovotrans(ConfigureMake):
    """
    Support for building SOAPdenovo-Trans.
    """

    def __init__(self, *args, **kwargs):
        """Define lists of files to install."""
        super(EB_soapdenovotrans, self).__init__(*args, **kwargs)

        self.bin_suffixes = ["31mer", "63mer", "127mer"]

    def configure_step(self):
        """
	    Skip the configure as not part of this build process
        """
        pass

    def build_step(self):
        """
        Start the actual build
        """
	#srcdir = os.path.join(self.cfg['start_dir'],'src')
	#try:
	#    for suff in self.bin_suffixes:
	#	os.chdir(srcdir)
	#        cmd = "%s %s make %s" % ("%s = 1" % suff, self.cfg['prebuildopts'], self.cfg['makeopts'])
	#        (out, _) = run_cmd(cmd, log_all=True, simple=False, log_output=verbose)
	#except OSError, err:
	#    self.log.error("Build failed")
	cmd = "./make.sh"
	os.system("chmod u+x %s" % cmd)
	try:
		os.system(cmd)
	except err:
		self.log.error("Build failed")

    def install_step(self):
        """
        Install by copying files to install dir
        """
        srcdir = self.cfg['start_dir']
        destdir = os.path.join(self.installdir, 'bin')
        srcfile = None
        try:
            os.makedirs(destdir)
            for suff in self.bin_suffixes:
                srcfile = os.path.join(srcdir, "SOAPdenovo-Trans-%s" % suff)
                shutil.copy2(srcfile, destdir)
        except OSError, err:
            self.log.error("Copying %s to installation dir %s failed: %s" % (srcfile, destdir, err))

    def sanity_check_step(self):
        """Custom sanity check for SOAPdenovo-Trans."""

        custom_paths = {
                        'files': ['bin/SOAPdenovo-Trans-%s' % x for x in self.bin_suffixes],
                        'dirs': []
                       }

        super(EB_soapdenovotrans, self).sanity_check_step(custom_paths=custom_paths)
