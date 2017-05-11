"""
EasyBuild support for building SOAPdenovo-Trans, implemented as an easyblock

@author: Le Yan
"""
import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.filetools import run_cmd

class EB_clonalorigin(ConfigureMake):
    """
    Support for building ClonalOrigin
    """

    def configure_step(self, cmd_prefix=''):
        """
	need to run autogen.sh first
        """

	os.chdir(os.path.join(self.cfg['start_dir'],"warg"))
	cmd = "./autogen.sh"
	try:
		run_cmd(cmd, log_all=True, simple=True)	
	except OSError, err:
		self.log.error("Error running %s." % cmd)

        if self.cfg['configure_cmd_prefix']:
            if cmd_prefix:
                tup = (cmd_prefix, self.cfg['configure_cmd_prefix'])
                self.log.debug("Specified cmd_prefix '%s' is overruled by configure_cmd_prefix '%s'" % tup)
            cmd_prefix = self.cfg['configure_cmd_prefix']

        if self.cfg['tar_config_opts']:
            # setting am_cv_prog_tar_ustar avoids that configure tries to figure out
            # which command should be used for tarring/untarring
            # am__tar and am__untar should be set to something decent (tar should work)
            tar_vars = {
                        'am__tar': 'tar chf - "$$tardir"',
                        'am__untar': 'tar xf -',
                        'am_cv_prog_tar_ustar': 'easybuild_avoid_ustar_testing'
                       }
            for (key, val) in tar_vars.items():
                self.cfg.update('preconfigopts', "%s='%s'" % (key, val))

        cmd = "%(preconfigopts)s %(cmd_prefix)s./configure %(prefix_opt)s%(installdir)s %(configopts)s" % {
            'preconfigopts': self.cfg['preconfigopts'],
            'cmd_prefix': cmd_prefix,
            'prefix_opt': self.cfg['prefix_opt'],
            'installdir': self.installdir,
            'configopts': self.cfg['configopts'],
        }

        (out, _) = run_cmd(cmd, log_all=True, simple=False)

        return out




