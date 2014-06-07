%global commit 1eb929bb2f715bd6cabf49bad165a31da5f5a589
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global realname rosdistro

Name:           python-rosdistro
Version:        0.3.5
Release:        2%{?dist}
Summary:        File format for managing ROS Distributions

License:        BSD and MIT
URL:            http://www.ros.org/wiki/rosdistro
Source0:        https://github.com/ros-infrastructure/%{realname}/archive/%{commit}/%{realname}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{realname}-0.3.5-argparse.patch

BuildArch:      noarch

BuildRequires:  PyYAML
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-catkin-sphinx
Requires:       PyYAML
Requires:       python-argparse
Requires:       python-catkin_pkg
Requires:       python-rospkg
Requires:       python-setuptools

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
%patch0 -p1
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
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Scott K Logan <logans@cottsay.net> - 0.3.5-1
- Update to release 0.3.5
- Remove argparse from python dependency list
- Added missing install requirements
- Remove patch for setuptools (merged upstream)

* Tue Apr 08 2014 Rich Mattes <richmattes@gmail.com> - 0.3.4-2
- Depend on setuptools instead of distribute

* Sat Feb 08 2014 Rich Mattes <richmattes@gmail.com> - 0.3.4-1
- Update to release 0.3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-3.20130602git6e83551
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Rich Mattes <richmattes@gmail.com> - 0.2.8-2.20130602git6e83551
- Update BuildRequires to python2-devel
- Remove cleanup of buildroot in install

* Sun Jun 02 2013 Rich Mattes <richmattes@gmail.com> - 0.2.8-1.20130602git6e83551
- Initial package
