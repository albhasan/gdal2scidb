#!/bin/bash
# HDF5 guide http://www.hdfgroup.org/ftp/HDF5/current/src/unpacked/release_docs/INSTALL
function DEBUG()
{
  [ "$_DEBUG" == "on" ] && $@
}
echo "*****************************"
echo "INSTALL GDAL WITH HDF SUPPORT"
echo "*****************************"
cd ~
rm -rf install-gdal
mkdir install-gdal
cd install-gdal
echo "************** Installing additional stuff... ***************"
yes | sudo apt-get install wget
yes | sudo apt-get install zlibc
yes | sudo apt-get install zlib1g
yes | sudo apt-get install zlib1g-dev
yes | sudo apt-get install hdf4-tools
yes | sudo apt-get install hdf5-tools
yes | sudo apt-get install libproj-dev
yes | sudo apt-get install python
yes | sudo apt-get install python-gdal
yes | sudo apt-get remove libhdf4-dev package
yes | sudo apt-get install libhdf4-alt-dev
yes | sudo apt-get install gdal-bin
echo "************** Downloading files ... ************************"
wget www.hdfgroup.org/ftp/lib-external/szip/2.1/src/szip-2.1.tar.gz
wget www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.12.tar.gz
wget download.osgeo.org/gdal/1.10.1/gdal-1.10.1.tar.gz
wget https://github.com/Unidata/netcdf-cxx4/archive/v4.2.1.tar.gz
tar xvzf szip-2.1.tar.gz
tar xvzf hdf5-1.8.12.tar.gz
tar xvzf gdal-1.10.1.tar.gz
tar xvzf v4.2.1.tar.gz
echo "************** Processing SZIP... ***************************"
cd ~/install-gdal/szip-2.1/
./configure
make
sudo make install
cd szip/lib
tar cvf - . | (cd /usr/local/lib/ : sudo tar xvf -)
cd ../include
tar cvf - . | (cd /usr/local/include ; sudo tar xvf -)
echo "************** Processing HDF... ****************************"
cd ~/install-gdal/hdf5-1.8.12
./configure --prefix=/usr/local/hdf5 --enable-cxx --with-szlib=/usr/lib/libsz.a
if ["$DEBUG" == "on"]; then
  echo "Press ENTER to continue..."
  read
fi
make
sudo make install
cd /usr/local/hdf5/lib
tar cvf - . | (cd /usr/local/lib/ : sudo tar xvf -)
cd ../include
tar cvf - . | (cd /usr/local/include ; sudo tar xvf -)
echo "************** NETCDF... **************************************"
cd ~/install-gdal/netcdf-cxx4-4.2.1
./configure --prefix=/usr/local
make
sudo make install
make check
echo "************** GDAL... **************************************"
cd ~/install-gdal/gdal-1.10.1
#--with-netcdf=/usr/local
./configure --with-hdf5=/usr/local/hdf5 --disable-netcdf --disable-fortran --with-python
if ["$_DEBUG" == "on"]; then
  echo "Press ENTER to continue..."
  read
fi
make
sudo make install
echo "************** CLEANING... **************************************"
rm -rf ~/install-gdal
echo "************** TEST... **************************************"
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
gdalinfo
