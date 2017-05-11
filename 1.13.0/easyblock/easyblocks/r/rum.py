##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for RUM, implemented as an easyblock

@author: Jens Timmerman (Ghent University)
@author: Kenneth Hoste (Ghent University)
"""
import os

from easybuild.easyblocks.generic.perlmodule import PerlModule
from easybuild.tools.filetools import run_cmd
from easybuild.easyblocks.generic.configuremake import ConfigureMake

class EB_rum(PerlModule):
    """Builds and installs RUM as a Perl module."""

    def install_perl_module(self):
        """Install procedure for Perl modules: using either Makefile.Pl or Build.PL."""
        # Perl modules have two possible installation procedures: using Makefile.PL and Build.PL
        # configure, build, test, install
        if os.path.exists('Makefile.PL'):
            run_cmd('perl Makefile.PL PREFIX=%s' % self.installdir)
            ConfigureMake.build_step(self)
#            ConfigureMake.test_step(self)
            ConfigureMake.install_step(self)
        elif os.path.exists('Build.PL'):
            run_cmd('perl Build.PL --prefix %s' % self.installdir)
            run_cmd('perl Build build')
#            run_cmd('perl Build test')
            run_cmd('perl Build install')

    def sanity_check_step(self, *args, **kwargs):
        """
        Custom sanity check for Perl modules
        """
#        return ExtensionEasyBlock.sanity_check_step(self, EXTS_FILTER_PERL_MODULES, *args, **kwargs)
	pass
