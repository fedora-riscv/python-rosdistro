%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global commit 98c556080721f961bbcd0d7a6b70ec7d8ed33454
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global realname rosdistro

Name:           python-%{realname}
Version:        0.4.2
Release:        3%{?dist}
Summary:        File format for managing ROS Distributions

License:        BSD and MIT
URL:            http://www.ros.org/wiki/rosdistro
Source0:        https://github.com/ros-infrastructure/%{realname}/archive/%{commit}/%{realname}-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  PyYAML
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-catkin_pkg
BuildRequires:  python-catkin-sphinx
BuildRequires:  python-rospkg
BuildRequires:  python-setuptools
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  python-nose1.1
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-nose
BuildRequires:  python-sphinx
%endif
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

%if 0%{?with_python3}
%package -n python3-%{realname}
Summary:        File format for managing ROS Distributions
BuildRequires:  python3-PyYAML
BuildRequires:  python3-catkin_pkg
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-rospkg
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
Requires:       python3-PyYAML
Requires:       python3-catkin_pkg
Requires:       python3-rospkg
Requires:       python3-setuptools

%description -n python3-%{realname}
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
%endif

%prep
%setup -qn %{realname}-%{commit}
sed -i 's|#!/usr/bin/env python||' src/rosdistro/external/appdirs.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
%{__python2} setup.py build
%if 0%{?rhel} && 0%{?rhel} < 7
make -C doc html SPHINXBUILD=sphinx-1.0-build
%else
make -C doc html
%endif
rm -f doc/_build/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
# TODO: Disabled until python3-catkin-sphinx is built
#make -C doc html man SPHINXBUILD=sphinx-build-%{python3_version}
#rm -f doc/_build/html/.buildinfo
pushd build/scripts-%{python3_version}
for f in *; do mv $f python3-$f; done
popd
popd
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%check
%if 0%{?rhel} && 0%{?rhel} < 7
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests1.1 -w test
%else
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests -w test
%endif

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} nosetests-%{python3_version} -w test
popd
%endif
 
%files
%doc README.md LICENSE.txt doc/_build/html
%{_bindir}/rosdistro_build_cache
%{_bindir}/rosdistro_reformat
%{_bindir}/rosdistro_migrate_to_rep_141
%{_bindir}/rosdistro_migrate_to_rep_143
%{python2_sitelib}/%{realname}
%{python2_sitelib}/%{realname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{realname}
%doc README.md LICENSE.txt doc/_build/html
%{_bindir}/python3-rosdistro_build_cache
%{_bindir}/python3-rosdistro_reformat
%{_bindir}/python3-rosdistro_migrate_to_rep_141
%{_bindir}/python3-rosdistro_migrate_to_rep_143
%{python3_sitelib}/%{realname}
%{python3_sitelib}/%{realname}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Rich Mattes <richmattes@gmail.com> - 0.4.2-1
- Update to release 0.4.2 (#1207455)

* Wed Mar 04 2015 Rich Mattes <richmattes@gmail.com> - 0.4.1-1
- Update to release 0.4.1

* Mon Dec 15 2014 Scott K Logan <logans@cottsay.net> - 0.4.0-1
- Update to release 0.4.0

* Sat Oct 25 2014 Scott K Logan <logans@cottsay.net> - 0.3.7-1
- Update to release 0.3.7
- Remove argparse patch (fixed upstream)
- Fix sphinx dependency in el6
- Add check section
- Add python3 package

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
