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
EasyBuild support for PETSc, implemented as an easyblock

@author: Kenneth Hoste (Ghent University)
"""
import os
import re
from distutils.version import LooseVersion

import easybuild.tools.environment as env
import easybuild.tools.toolchain as toolchain
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.framework.easyconfig import BUILD, CUSTOM
from easybuild.tools.filetools import run_cmd
from easybuild.tools.modules import get_software_root
from easybuild.tools.systemtools import get_shared_lib_ext


class EB_PETSc(ConfigureMake):
    """Support for building and installing PETSc"""

    def __init__(self, *args, **kwargs):
        """Initialize PETSc specific variables."""
        super(EB_PETSc, self).__init__(*args, **kwargs)

        self.petsc_arch = ""
        self.petsc_subdir = ""

    @staticmethod
    def extra_options():
        """Add extra config options specific to PETSc."""
        extra_vars = [
                      ('sourceinstall', [False, "Indicates whether a source installation should be performed (default: False)", CUSTOM]),
                      ('shared_libs', [False, "Build shared libraries (default: False)", CUSTOM]),
                      ('with_papi', [False, "Enable PAPI support (default: False)", CUSTOM]),
                      ('papi_inc', ['/usr/include', "Path for PAPI include files (default: /usr/include)", CUSTOM]),
                      ('papi_lib', ['/usr/lib64/libpapi.so', "Path for PAPI library (default: '/usr/lib64/libpapi.so')", CUSTOM]),
                      ('runtest', ['test', "Make target to test build (default: test)", BUILD])
                     ]
        return ConfigureMake.extra_options(extra_vars)

    def make_builddir(self):
        """Decide whether or not to build in install dir before creating build dir."""

        if self.cfg['sourceinstall']:
            self.build_in_installdir = True

        super(EB_PETSc, self).make_builddir()

    def configure_step(self):
        """
        Configure PETSc by setting configure options and running configure script.

        Configure procedure is much more concise for older versions (< v3).
        """

        if LooseVersion(self.version) >= LooseVersion("3"):

            # compilers, shaohao 04-2014
            #self.cfg.update('configopts', '--with-cc="%s"' % os.getenv('CC'))
            #self.cfg.update('configopts', '--with-cxx="%s" --with-c++-support' % os.getenv('CXX'))
            #self.cfg.update('configopts', '--with-fc="%s"' % os.getenv('F90'))

            # compiler flags
            cflag = os.getenv('CFLAGS')
            cxxflag = os.getenv('CXXFLAGS')
            f90flag = os.getenv('F90FLAGS')
            print cflag
            print cxxflag
            print f90flag
            self.cfg.update('configopts', '--with-cflags="%s"' % cflag)
            self.cfg.update('configopts', '--with-cxxflags="%s"' % cxxflag)
            self.cfg.update('configopts', '--with-fcflags="%s"' % f90flag)

            #if not self.toolchain.comp_family() == toolchain.GCC:  #@UndefinedVariable
            #    self.cfg.update('configopts', '--with-gnu-compilers=0')

            # MPI, shaohao 04-2014
            if self.toolchain.options.get('usempi', None):
                self.cfg.update('configopts', '--with-mpi=1')

            #mpi_path = os.getenv('MPI_DIR')
            #print mpi_path
            #self.cfg.update('configopts', '--with-mpi-dir="%s"' % mpi_path) # compiler also is specified here
            mpi_cc = os.getenv('MPI_CC')
            mpi_cxx = os.getenv('MPI_CXX')
            mpi_f90 = os.getenv('MPI_F90')
            mpi_exec = os.getenv('MPI_EXEC')
            print mpi_cc
            print mpi_cxx
            print mpi_f90
            print mpi_exec
            self.cfg.update('configopts', '--with-cc="%s"' % mpi_cc )
            self.cfg.update('configopts', '--with-cxx="%s" --with-c++-support' % mpi_cxx )
            self.cfg.update('configopts', '--with-mpi-f90="%s"' % mpi_f90 )
            self.cfg.update('configopts', '--with-mpiexec="%s"' % mpi_exec )

            # build options
            #self.cfg.update('configopts', '--with-build-step-np=%s' % self.cfg['parallel'])
            #self.cfg.update('configopts', '--with-shared-libraries=%d' % self.cfg['shared_libs'])
            #self.cfg.update('configopts', '--with-debugging=%d' % self.toolchain.options['debug'])
            #self.cfg.update('configopts', '--with-pic=%d' % self.toolchain.options['pic'])
            #self.cfg.update('configopts', '--with-x=0 --with-windows-graphics=0')

            # PAPI support
            #if self.cfg['with_papi']:
            #    papi_inc = self.cfg['papi_inc']
            #    papi_inc_file = os.path.join(papi_inc, "papi.h")
            #    papi_lib = self.cfg['papi_lib']
            #    if os.path.isfile(papi_inc_file) and os.path.isfile(papi_lib):
            #        self.cfg.update('configopts', '--with-papi=1')
            #        self.cfg.update('configopts', '--with-papi-include=%s' % papi_inc)
            #        self.cfg.update('configopts', '--with-papi-lib=%s' % papi_lib)
            #    else:
            #        self.log.error("PAPI header (%s) and/or lib (%s) not found, " % (papi_inc_file,
            #                                                                         papi_lib) + \
            #                       "can not enable PAPI support?")

            # Python extensions_step
            #if get_software_root('Python'):
            #    self.cfg.update('configopts', '--with-numpy=1')
            #    if self.cfg['shared_libs']:
            #        self.cfg.update('configopts', '--with-mpi4py=1')

            # BLACS, FFTW, ScaLAPACK
            #for dep in ["BLACS", "FFTW", "ScaLAPACK"]:
            #    inc = os.getenv('%s_INC_DIR' % dep.upper())
            #    libdir = os.getenv('%s_LIB_DIR' % dep.upper())
            #    libs = os.getenv('%s_STATIC_LIBS' % dep.upper())
            #    if inc and libdir and libs:
            #        with_arg = "--with-%s" % dep.lower()
            #        self.cfg.update('configopts', '%s=1' % with_arg)
            #        self.cfg.update('configopts', '%s-include=%s' % (with_arg, inc))
            #        self.cfg.update('configopts', '%s-lib=[%s/%s]' % (with_arg, libdir, libs))
            #    else:
            #        self.log.info("Missing inc/lib info, so not enabling %s support." % dep)

            # BLAS, LAPACK libraries # shaohao 04-2014
            la_bl_libdir = os.getenv('LAPACK_BLAS_LIB_DIR')
            la_libs = os.getenv('LAPACK_LIBS')
            bl_libs = os.getenv('BLAS_LIBS')
            print la_bl_libdir 
            print la_libs
            print bl_libs
            if la_bl_libdir and bl_libs and la_libs:
                #self.cfg.update('configopts', '--with-blas-lapack-lib=[%s/%s]' % (bl_libdir, bl_libs))
                self.cfg.update('configopts', '--with-lapack-lib=[%s/%s]' % (la_bl_libdir, la_libs))
                self.cfg.update('configopts', '--with-blas-lib=[%s/%s]' % (la_bl_libdir, bl_libs))
            else:
                    self.log.error("One or more environment variables for BLAS/LAPACK not defined?")

            # additional dependencies
            # filter out deps handled seperately
            depfilter = self.cfg.builddependencies() + ["BLACS", "BLAS", "FFTW", "LAPACK", "numpy",
                                                        "mpi4py", "papi", "ScaLAPACK", "SuiteSparse"]
            deps = [dep['name'] for dep in self.cfg.dependencies() if not dep['name'] in depfilter]
            for dep in deps:
                if type(dep) == str:
                    dep = (dep, dep)
                deproot = get_software_root(dep[0])
                if deproot:
                    withdep = "--with-%s" % dep[1].lower()
                    self.cfg.update('configopts', '%s=1 %s-dir=%s' % (withdep, withdep, deproot))

            # CHOLMOD and UMFPACK are part of SuiteSparse
            suitesparse = get_software_root('SuiteSparse')
            if suitesparse:
                withdep = "--with-umfpack"
                # specified order of libs matters!
                umfpack_libs = [os.path.join(suitesparse, l, "Lib", "lib%s.a" % l.lower())
                                for l in ["UMFPACK", "CHOLMOD", "COLAMD", "AMD"]]

                self.cfg.update('configopts', ' '.join([(withdep+x) for x in [
                                                                             "=1",
                                                                             "-include=%s" % os.path.join(suitesparse, "UMFPACK", "Include"),
                                                                            "-lib=[%s]" % ','.join(umfpack_libs)
                                                                           ]
                                                      ])
                              )

            ## set PETSC_DIR for configure (env) and build_step
            env.setvar('PETSC_DIR', self.cfg['start_dir'])
            self.cfg.update('makeopts', 'PETSC_DIR=%s' % self.cfg['start_dir'])

            if self.cfg['sourceinstall']:
                # run configure without --prefix (required)
                cmd = "%s ./configure %s" % (self.cfg['preconfigopts'], self.cfg['configopts'])
                (out, _) = run_cmd(cmd, log_all=True, simple=False)
            else:
                out = super(EB_PETSc, self).configure_step()

            # check for errors in configure
            error_regexp = re.compile("ERROR")
            if error_regexp.search(out):
                self.log.error("Error(s) detected in configure output!")

            if self.cfg['sourceinstall']:
                #figure out PETSC_ARCH setting
                petsc_arch_regex = re.compile("^\s*PETSC_ARCH:\s*(\S+)$", re.M)
                res = petsc_arch_regex.search(out)
                if res:
                    self.petsc_arch = res.group(1)
                    self.cfg.update('makeopts', 'PETSC_ARCH=%s' % self.petsc_arch)
                else:
                    self.log.error("Failed to determine PETSC_ARCH setting.")

            self.petsc_subdir = '%s-%s' % (self.name.lower(), self.version)

        else:  # old versions (< 3.x)

            self.cfg.update('configopts', '--prefix=%s' % self.installdir)
            self.cfg.update('configopts', '--with-shared=1')

            # additional dependencies
            for dep in ["SCOTCH"]:
                deproot = get_software_root(dep)
                if deproot:
                    withdep = "--with-%s" % dep.lower()
                    self.cfg.update('configopts', '%s=1 %s-dir=%s' % (withdep, withdep, deproot))

            cmd = "./config/configure.py %s" % self.get_cfg('configopts')
            run_cmd(cmd, log_all=True, simple=True)

    # default make should be fine

    def install_step(self):
        """
        Install using make install (for non-source installations), 
        or by symlinking files (old versions, < 3).
        """
        if LooseVersion(self.version) >= LooseVersion("3"):
            if not self.cfg['sourceinstall']:
                super(EB_PETSc, self).install_step()

        else:  # old versions (< 3.x)

            try:
                for f in ['petscconf.h', 'petscconfiginfo.h', 'petscfix.h', 'petscmachineinfo.h']:
                    includedir = os.path.join(self.installdir, 'include')
                    bmakedir = os.path.join(self.installdir, 'bmake', 'linux-gnu-c-opt')
                    os.symlink(os.path.join(bmakedir, f), os.path.join(includedir, f))
            except Exception, err:
                self.log.error("Something went wrong during symlink creation of file %s: %s" % (f, err))

    def make_module_req_guess(self):
        """Specify PETSc custom values for PATH, CPATH and LD_LIBRARY_PATH."""

        guesses = super(EB_PETSc, self).make_module_req_guess()

        prefix1 = ""
        prefix2 = ""
        if self.cfg['sourceinstall']:
            prefix1 = self.petsc_subdir
            prefix2 = os.path.join(self.petsc_subdir, self.petsc_arch)

        guesses.update({
                        'PATH': [os.path.join(prefix1, "bin")],
                        'CPATH': [os.path.join(prefix2, "include"),
                                  os.path.join(prefix1, "include")],
                        'LD_LIBRARY_PATH': [os.path.join(prefix2, "lib")]
                        })

        return guesses

    def make_module_extra(self):
        """Set PETSc specific environment variables (PETSC_DIR, PETSC_ARCH)."""
        txt = super(EB_PETSc, self).make_module_extra()

        if self.cfg['sourceinstall']:
            txt += self.moduleGenerator.set_environment('PETSC_DIR', '$root/%s' % self.petsc_subdir)
            txt += self.moduleGenerator.set_environment('PETSC_ARCH', self.petsc_arch)

        else:
            txt += self.moduleGenerator.set_environment('PETSC_DIR', '$root')

        return txt

    def sanity_check_step(self):
        """Custom sanity check for PETSc"""

        prefix1 = ""
        prefix2 = ""
        if self.cfg['sourceinstall']:
            prefix1 = self.petsc_subdir
            prefix2 = os.path.join(self.petsc_subdir, self.petsc_arch)

        if self.cfg['shared_libs']:
            libext = get_shared_lib_ext()
        else:
            libext = "a"

        custom_paths = {
                        'files': [os.path.join(prefix2, "lib", "libpetsc.%s" % libext)],
                        'dirs': [os.path.join(prefix1, "bin"), os.path.join(prefix2, "conf"),
                                 os.path.join(prefix1, "include"), os.path.join(prefix2, "include")]
                       }

        super(EB_PETSc, self).sanity_check_step(custom_paths=custom_paths)
