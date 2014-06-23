##
# Copyright 2013-2014 Ghent University
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
Implementation of (default) EasyBuild module naming scheme.

@author: Kenneth Hoste (Ghent University)
"""

import os

from easybuild.tools.module_naming_scheme import ModuleNamingScheme
from easybuild.tools.module_naming_scheme.utilities import det_full_ec_version
from easybuild.tools.toolchain import DUMMY_TOOLCHAIN_NAME

class SuperMicModuleNamingScheme(ModuleNamingScheme):
    """Class implementing the default EasyBuild module naming scheme."""

    def det_full_module_name(self, ec):
        """
        Determine full module name from given easyconfig, according to the EasyBuild module naming scheme.

        @param ec: dict-like object with easyconfig parameter values (e.g. 'name', 'version', etc.)

        @return: string with full module name <name>/<installversion>, e.g.: 'gzip/1.5-goolf-1.4.10'
        """
	
	name = ec['name']
	version = ec['version']
	tc_name = ec['toolchain']['name']
	tc_ver = ec['toolchain']['version']

	if tc_name == DUMMY_TOOLCHAIN_NAME:
		return os.path.join(name, version)
	else:
		tcver = "%s-%s" % (tc_name, tc_ver)
		#append version suffix
		tcver = ''.join([x for x in [tcver, ec['versionsuffix']] if x])
		return os.path.join(name, version, tcver)