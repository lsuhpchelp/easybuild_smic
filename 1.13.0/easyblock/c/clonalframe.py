"""
EasyBuild support for ClonalFram, implemented as an easyblock

@authors: Le Yan(LSU)
"""
import os
import shutil

from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.filetools import run_cmd


class EB_clonalframe(EasyBlock):
    """Support for building and installing ClonalFrame."""

    def configure_step(self):
        """No configure step for ClonalFrame."""
        pass

    def build_step(self):
        """No build step for ClonalFrame."""
        pass

    def install_step(self):
        """Custom install procedure for ClonalFrame."""

        srcdir = os.path.join(self.cfg['start_dir'],'src')
        destdir = os.path.join(self.installdir, 'bin')

	bin = "ClonalFrame"
	tup = (os.getenv('CXX'),"ClonalFrame",self.cfg['buildopts'])
	cmd = '%s *.cpp -o %s %s' % tup

	try:
	    os.chdir(srcdir)
	    run_cmd(cmd, log_all=True, simple=True)
	except OSError, err:
	    self.log.error("Failed to build ClonalFrame: %s" % err)

	# copy the executable over
	try:
	    os.makedirs(destdir)
	    shutil.copy(os.path.join(srcdir,bin),destdir)
        except OSError, err:
            self.log.error("Failed to install ClonalFrame: %s" % err)

	
