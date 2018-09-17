##
# Copyright 2012-2014 Ghent University
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
EasyBuild support for intel-180-MVAPICH2 compiler toolchain (includes Intel compilers (icc, ifort) and MVAPICH2).

@author: Stijn De Weirdt (Ghent University)
@author: Kenneth Hoste (Ghent University)
"""

from easybuild.toolchains.compiler.inteliccifort import IntelIccIfort
from easybuild.toolchains.mpi.mvapich2 import Mvapich2
from easybuild.toolchains.linalg.intelmkl import IntelMKL


class INTEL_180_MVAPICH2(IntelIccIfort, Mvapich2, IntelMKL):
    """
    Compiler toolchain with Intel compilers (icc/ifort) and MPICH.
    """
    NAME = 'INTEL-180-MVAPICH2'
