[MAIN]
# Enable debug log mode (def False)
#debug=
# Enable info log mode (def False)
#info=
# Enable info quiet/warning mode (def False)
#quiet=

[basic]
# Print build overview incl. dependencies (full paths) (def False)
#dry-run=
# Print build overview incl. dependencies (short paths) (def False)
#dry-run-short=
# Force to rebuild software even if it's already installed (i.e. if it can be found as module) (def False)
#force=
# Submit the build as a job (def False)
#job=
# Redirect main log to stdout (def False)
#logtostdout=
# Only build listed blocks (type comma-separated list)
#only-blocks=
# Path(s) to search for easyconfigs for missing dependencies (colon-separated) (def /usr/local/packages/easybuild/1.13.0/lib/python2.6/site-packages/easybuild_easyconfigs-1.13.0-py2.6.egg/easybuild/easyconfigs)
robot=/usr/local/packages/easybuild/1.13.0/configs
# Skip existing software (useful for installing additional packages) (def False)
#skip=
# Stop the installation after certain step (type choice; def source) (choices: fetch, ready, source, patch, prepare, configure, build, test, install, extensions, package, postproc, sanitycheck, cleanup, module, testcases)
#stop=
# Set strictness level (type choice; def warn) (choices: ignore, warn, error)
#strict=

[config]
# Show all supported module naming schemes (def False)
#avail-module-naming-schemes=
# Show all supported module tools (def False)
#avail-modules-tools=
# Show all repository types (incl. non-usable) (def False)
#avail-repositories=
# Temporary build path (def /root/.local/easybuild/build)
buildpath=/usr/local/packages/sources/eb_packages/build
# Path to EasyBuild config file (def /home/packages/easybuild/1.13.0/lib/python2.6/site-packages/easybuild_framework-1.13.0-py2.6.egg/easybuild/easybuild_config.py)
#config=
# Directory names to ignore when searching for files/dirs (type comma-separated list; def .git,.svn)
#ignore-dirs=
# Install path for software and modules (def /root/.local/easybuild)
installpath=/usr/local/packages
# Directory name and format of the log file (type comma-separated list; def easybuild,easybuild-%(name)s-%(version)s-%(date)s.%(time)s.log)
#logfile-format=
# Module naming scheme (type choice; def EasyBuildModuleNamingScheme) (choices: EasyBuildModuleNamingScheme)
module-naming-scheme=SuperMicModuleNamingScheme
# Extend supported module classes (For more info on the default classes, use --show-default-moduleclasses) (type comma-separated list; def base,bio,cae,chem,compiler,data,debugger,devel,geo,ide,lang,lib,math,mpi,numlib,perf,phys,system,toolchain,tools,vis)
#moduleclasses=
# Path to file containing footer to be added to all generated module files
#modules-footer=
# Modules tool to use (type choice; def EnvironmentModulesC) (choices: EnvironmentModulesC, EnvironmentModulesTcl, Lmod)
#modules-tool=
# Change prefix for buildpath, installpath, sourcepath and repositorypath (repositorypath prefix is only relevant in case of FileRepository repository) (used prefix for defaults /root/.local/easybuild)
#prefix=
# Enable generating of modules that unload recursively. (def False)
#recursive-module-unload=
# Repository type, using repositorypath (type choice; def FileRepository) (choices: FileRepository)
#repository=
# Repository path, used by repository (is passed as list of arguments to create the repository instance). For more info, use --avail-repositories. (type comma-separated list; def /root/.local/easybuild/ebfiles_repo)
repositorypath=/usr/local/packages/sources/eb_packages/ebfiles_repo
# Show default module classes with description (def False)
#show-default-moduleclasses=
# Path(s) to where sources should be downloaded (string, colon-separated) (def /root/.local/easybuild/sources)
sourcepath=/usr/local/packages/sources/eb_packages/sources
# Installpath subdir for modules (def modules)
subdir-modules=Modules/modulefiles/apps
# Installpath subdir for software (def software)
subdir-software=.
# Path to where a job should place the output (to be set within jobscript)
#testoutput=
# Log directory where temporary log files are stored (def /tmp)
#tmp-logdir=
# Directory to use for temporary storage
#tmpdir=

[informative]
# Show all constants that can be used in easyconfigs (def False)
#avail-easyconfig-constants=
# Show all license constants that can be used in easyconfigs (def False)
#avail-easyconfig-licenses=
# Show all easyconfig parameters (include easyblock-specific ones by using -e) (def False)
#avail-easyconfig-params=
# Show all template names and template constants that can be used in easyconfigs (def False)
#avail-easyconfig-templates=
# Create dependency graph
#dep-graph=
# Show list of available easyblocks (type choice; def simple) (choices: simple, detailed)
#list-easyblocks=
# Show list of known toolchains (def False)
#list-toolchains=
# Search for easyconfig files in the robot directory, print full paths
#search=
# Search for easyconfig files in the robot directory, print short paths
#search-short=

[override]
# Run pretending to be (future) version, to test removal of deprecated code.
#deprecated=
# easyblock to use for processing the spec file or dumping the options
#easyblock=
# Allow experimental code (with behaviour that can be changed or removed at any given time). (def False)
#experimental=
# Ignore any listed OS dependencies (def False)
#ignore-osdeps=
# Look for and use the oldstyle configuration file. (def True)
#oldstyleconfig=
# Does the build/installation in a test directory located in $HOME/easybuildinstall (def False)
#pretend=
# Skip running test cases (def False)
skip-test-cases=True

[regtest]
# Collect all the xmls inside the given directory and generate a single file
#aggregate-regtest=
# Enable regression test mode (def False)
#regtest=
# Enable online regression test mode (def False)
#regtest-online=
# Set output directory for test-run
#regtest-output-dir=
# Specify this option if you want to prevent parallel build (def False)
#sequential=

[software]
# Specify additional search and build parameters (can be used multiple times); for example: versionprefix=foo or patches=one.patch,two.patch)
#amend=
# Search and build software with name
#software-name=
# Search and build software with version
#software-version=
# Search and build with toolchain (name and version) (type comma-separated list)
toolchain=INTEL,14.0.2
# Search and build with toolchain name
#toolchain-name=
# Search and build with toolchain version
#toolchain-version=
# Try to specify additional search and build parameters (can be used multiple times); for example: versionprefix=foo or patches=one.patch,two.patch) (USE WITH CARE!)
#try-amend=
# Try to search and build software with name (USE WITH CARE!)
#try-software-name=
# Try to search and build software with version (USE WITH CARE!)
#try-software-version=
# Try to search and build with toolchain (name and version) (USE WITH CARE!) (type comma-separated list)
#try-toolchain=
# Try to search and build with toolchain name (USE WITH CARE!)
#try-toolchain-name=
# Try to search and build with toolchain version (USE WITH CARE!)
#try-toolchain-version=

[unittest]
# Log to this file in unittest mode
#unittest-file=

