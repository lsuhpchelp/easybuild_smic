export MPI_DIR=/usr/local/packages/MPICH/3.0.3/intelcomp-14.0.2
export MPI_CC=$MPI_DIR/bin/mipcc
export MPI_CXX=$MPI_DIR/bin/mipcxx
export MPI_F90=$MPI_DIR/bin/mipf90
export MPI_EXEC=$MPI_DIR/bin/mpiexec
export CFLAGS=O2
export CXXFLAGS=O2
export F90FLAGS=O2

export LAPACK_BLAS_LIB_DIR=/usr/local/packages/LAPACK/3.5.0-intel-14-mpich-3.0.3/lib
export LAPACK_LIBS=liblapack.a
export BLAS_LIBS=librefblas.a

