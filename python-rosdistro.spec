%global commit dce80f72ae9c6a7372b798f354068de5496f66e2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global realname rosdistro

Name:           python-rosdistro
Version:        0.3.4
Release:        1%{?dist}
Summary:        File format for managing ROS Distributions

License:        BSD and MIT
URL:            http://www.ros.org/wiki/rosdistro
Source0:        https://github.com/ros-infrastructure/%{realname}/archive/%{commit}/%{realname}-%{version}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  PyYAML
BuildRequires:  python2-devel
BuildRequires:  python-catkin-sphinx
BuildRequires:  git

%description
The rosdistro tool allows you to get access to the full dependency tree and 
the version control system information of all packages and repositories. To 
increase performance, the rosdistro tool will automatically look for a cache 
file on your local disk. If no cache file is found locally, it will try to 
download the latest cache file from the server. The cache files are only used 
to improve performance, and are not needed to get correct results. rosdistro 
will automatically go to Github to find any dependencies that are not part 
of the cache file. Note that operation without a cache file can be very slow, 
depending on your own internet connection and the response times of Github. 
The rosdistro tool will always write the latest dependency information to a 
local cache file, to speed up performance for the next query. 

%prep
%setup -qn %{realname}-%{commit}
sed -i 's|#!/usr/bin/env python||' src/rosdistro/external/appdirs.py

%build
%{__python} setup.py build
pushd doc
make html
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -f doc/_build/html/.buildinfo

 
%files
%doc README.md LICENSE.txt doc/_build/html
%{_bindir}/rosdistro_build_cache
%{_bindir}/rosdistro_reformat
%{_bindir}/rosdistro_migrate_to_rep_141
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-py?.?.egg-info

%changelog
* Sat Feb 08 2014 Rich Mattes <richmattes@gmail.com> - 0.3.4-1
- Update to release 0.3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-3.20130602git6e83551
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Rich Mattes <richmattes@gmail.com> - 0.2.8-2.20130602git6e83551
- Update BuildRequires to python2-devel
- Remove cleanup of buildroot in install

* Sun Jun 02 2013 Rich Mattes <richmattes@gmail.com> - 0.2.8-1.20130602git6e83551
- Initial package
