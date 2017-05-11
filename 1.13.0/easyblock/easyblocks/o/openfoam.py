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
EasyBuild support for building and installing openfoam, implemented as an easyblock

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
"""
import os
import stat
from distutils.version import LooseVersion

import easybuild.tools.environment as env
import easybuild.tools.toolchain as toolchain
from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.filetools import run_cmd, adjust_permissions
from easybuild.tools.modules import get_software_root


class EB_openfoam(EasyBlock):
    """Support for building and installing openfoam."""

    def __init__(self,*args,**kwargs):
        """Specify that openfoam should be built in install dir."""

        super(EB_openfoam, self).__init__(*args, **kwargs)

        self.build_in_installdir = True

        self.wm_compiler= None
        self.wm_mplib = None
        self.mpipath = None
        self.thrdpartydir = None

    def configure_step(self):
        """Configure openfoam build by setting appropriate environment variables."""

        # installation directory
        env.setvar("FOAM_INST_DIR", self.installdir)

        # third party directory
        self.thrdpartydir = "ThirdParty-%s" % self.version
        # only if third party stuff is actually installed
        if os.path.exists(self.thrdpartydir):
            os.symlink(os.path.join("..", self.thrdpartydir), self.thrdpartydir)
            env.setvar("WM_THIRD_PARTY_DIR", os.path.join(self.installdir, self.thrdpartydir))

        # compiler
        comp_fam = self.toolchain.comp_family()

        if comp_fam == toolchain.GCC:  #@UndefinedVariable
            self.wm_compiler="Gcc"

        elif comp_fam == toolchain.INTELCOMP:  #@UndefinedVariable
            self.wm_compiler="Icc"

            # make sure -no-prec-div is used with Intel compilers
            self.cfg.update('premakeopts', 'CFLAGS="$CFLAGS -no-prec-div" CXXFLAGS="$CXXFLAGS -no-prec-div"')

        else:
            self.log.error("Unknown compiler family, don't know how to set WM_COMPILER")

        env.setvar("WM_COMPILER",self.wm_compiler)

        # type of MPI
        mpi_type = self.toolchain.mpi_family()
        
        if mpi_type == toolchain.INTELMPI:  #@UndefinedVariable
            self.mpipath = os.path.join(get_software_root('IMPI'),'intel64')
            self.wm_mplib = "IMPI"

        elif mpi_type == toolchain.QLOGICMPI:  #@UndefinedVariable
            self.mpipath = get_software_root('QLogicMPI')
            self.wm_mplib = "MPICH"

        elif mpi_type == toolchain.OPENMPI:  #@UndefinedVariable
            self.mpipath = get_software_root('OpenMPI')
            self.wm_mplib = "MPI-MVAPICH2"

        else:
            self.mpipath = "/usr/local/packages/mvapich2/2.0/INTEL-14.0.2/bin/"
            self.wm_mplib = "MVAPICH2"
            print self.mpipath 
            print self.wm_mplib 
            #self.log.error("Unknown MPI, don't know how to set MPI_ARCH_PATH, WM_MPLIB or FOAM_MPI_LIBBIN")

        env.setvar("WM_MPLIB", self.wm_mplib)
        env.setvar("MPI_ARCH_PATH", self.mpipath)
        env.setvar("FOAM_MPI_LIBBIN", self.mpipath)

        # parallel build spec
        env.setvar("WM_NCOMPPROCS", str(self.cfg['parallel']))

    def build_step(self):
        """Build openfoam using make after sourcing script to set environment."""

        #nameversion = "%s-%s"%(self.name, self.version)
        nameversion = "%s-%s"%("OpenFOAM", self.version)

        precmd = "source %s" % os.path.join(self.builddir, nameversion, "etc", "bashrc")

	print "nameversion", nameversion
        print precmd

        # make directly in install directory
        cmd="%(precmd)s && %(premakeopts)s %(makecmd)s"%{'precmd':precmd,
                                                         'premakeopts':self.cfg['premakeopts'],
                                                         'makecmd':os.path.join(self.builddir, nameversion, "Allwmake")}
        print cmd
        run_cmd(cmd,log_all=True,simple=True,log_output=True)

    def install_step(self):
        """Building was performed in install dir, so just fix permissions."""

        # fix permissions of openfoam dir
        #fullpath = os.path.join(self.installdir, "%s-%s" % (self.name, self.version))
        fullpath = os.path.join(self.installdir, "%s-%s" % ("OpenFOAM", self.version))
        adjust_permissions(fullpath, stat.S_IROTH, add=True, recursive=True)
        adjust_permissions(fullpath, stat.S_IXOTH, add=True, recursive=True, onlydirs=True)

        # fix permissions of ThirdParty dir and subdirs (also for 2.x)
        # if the thirdparty tarball is installed
        fullpath = os.path.join(self.installdir, self.thrdpartydir)
        if os.path.exists(fullpath):
            adjust_permissions(fullpath, stat.S_IROTH, add=True, recursive=True)
            adjust_permissions(fullpath, stat.S_IXOTH, add=True, recursive=True, onlydirs=True)

    def sanity_check_step(self):
        """Custom sanity check for openfoam"""

        #odir = "%s-%s" % (self.name, self.version)
        odir = "%s-%s" % ("OpenFOAM", self.version)

        psubdir = "linux64%sDPOpt" % self.wm_compiler

        if LooseVersion(self.version) < LooseVersion("2"):
            toolsdir = os.path.join(odir, "applications", "bin", psubdir)

        else:
            toolsdir = os.path.join(odir, "platforms", psubdir, "bin")

        pdirs = []
        if LooseVersion(self.version) >= LooseVersion("2"):
            pdirs = [toolsdir, os.path.join(odir, "platforms", psubdir, "lib")]

        # some randomly selected binaries
        # if one of these is missing, it's very likely something went wrong
        bins = [os.path.join(odir, "bin", x) for x in ["foamExec", "paraFoam"]] + \
               [os.path.join(toolsdir, "buoyant%sSimpleFoam" % x) for x in ["", "Boussinesq"]] + \
               [os.path.join(toolsdir, "%sFoam" % x) for x in ["boundary", "engine", "sonic"]] + \
               [os.path.join(toolsdir, x) for x in ["deformedGeom", "engineSwirl", "modifyMesh",
                                                    "refineMesh", "vorticity"]]

        custom_paths = {
                        'files':["%s/etc/%s" % (odir, x) for x in ["bashrc", "cshrc"]] + bins,
                        'dirs':pdirs
                       }

        super(EB_openfoam, self).sanity_check_step(custom_paths=custom_paths)

    def make_module_extra(self):
        """Define extra environment variables required by openfoam"""

        txt = super(EB_openfoam, self).make_module_extra()

        env_vars = [("WM_PROJECT_VERSION", self.version),
                    ("FOAM_INST_DIR", "$root"),
                    ("WM_COMPILER", self.wm_compiler),
                    ("WM_MPLIB", self.wm_mplib),
                    ("MPI_ARCH_PATH", self.mpipath),
                    ("FOAM_BASH", "$root/%s-%s/etc/bashrc" % (self.name, self.version)),
                    ("FOAM_CSH", "$root/%s-%s/etc/cshrc" % (self.name, self.version)),
                    ]

        for env_var in env_vars:
            txt += "setenv\t%s\t%s\n" % env_var

        #txt += "\n. $FOAM_BASH"

        return txt
        custom_paths = {
                        'files':["%s/etc/%s" % (odir, x) for x in ["bashrc", "cshrc"]] + bins,
                        'dirs':pdirs
                       }

        super(EB_openfoam, self).sanity_check_step(custom_paths=custom_paths)

    def make_module_extra(self):
        """Define extra environment variables required by openfoam"""

        txt = super(EB_openfoam, self).make_module_extra()

        env_vars = [("WM_PROJECT_VERSION", self.version),
                    ("FOAM_INST_DIR", "$root"),
                    ("WM_COMPILER", self.wm_compiler),
                    ("WM_MPLIB", self.wm_mplib),
                    ("MPI_ARCH_PATH", self.mpipath),
                    ("FOAM_BASH", "$root/%s-%s/etc/bashrc" % (self.name, self.version)),
                    ("FOAM_CSH", "$root/%s-%s/etc/cshrc" % (self.name, self.version)),
                    ]

        for env_var in env_vars:
            txt += "setenv\t%s\t%s\n" % env_var

        #txt += "\n. $FOAM_BASH"

        return txt
