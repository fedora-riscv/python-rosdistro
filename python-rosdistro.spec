%{?!_without_python2:%global with_python2 0%{?_with_python2:1} || !(0%{?fedora} >= 32 || 0%{?rhel} >= 8)}
%{?!_without_python3:%global with_python3 0%{?_with_python3:1} || !0%{?rhel} || 0%{?rhel} >= 7}

%global srcname rosdistro

Name:           python-%{srcname}
Version:        0.9.0
Release:        1%{?dist}
Summary:        File format for managing ROS Distributions

License:        BSD and MIT
URL:            http://www.ros.org/wiki/rosdistro
Source0:        https://github.com/ros-infrastructure/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

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


%package doc
Summary:        HTML documentation for '%{name}'
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-catkin-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx

%description doc
HTML documentation for the '%{srcname}' python module


%if 0%{?with_python2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-catkin_pkg
BuildRequires:  python2-mock
BuildRequires:  python2-pytest
BuildRequires:  python2-pyyaml
BuildRequires:  python2-rospkg
BuildRequires:  python2-setuptools
%{?python_provide:%python_provide python2-%{srcname}}

%if %{undefined __pythondist_requires}
Requires:       python2-catkin_pkg
Requires:       python2-pyyaml
Requires:       python2-rospkg
Requires:       python2-setuptools
%endif

%if !0%{?rhel} || 0%{?rhel} >= 8
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description -n python2-%{srcname}
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


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  git
BuildRequires:  python%{python3_pkgversion}-catkin_pkg
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-PyYAML
BuildRequires:  python%{python3_pkgversion}-rospkg
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%if %{undefined __pythondist_requires}
Requires:       python%{python3_pkgversion}-catkin_pkg
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-rospkg
Requires:       python%{python3_pkgversion}-setuptools
%endif

%if !0%{?rhel} || 0%{?rhel} >= 8
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-%{srcname}
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
%autosetup -p1 -n %{srcname}-%{version}

# Drop unsupported syntax in older setuptools
sed -i "s/mock; python_version < '3.3'//" setup.py


%build
%if 0%{?with_python2}
%py2_build
%endif

%if 0%{?with_python3}
%py3_build
pushd build/scripts-%{python3_version}
for f in *; do mv $f python%{python3_pkgversion}-$f; done
popd
%endif

PYTHONPATH=$PWD/src \
  %make_build -C doc html SPHINXBUILD=sphinx-build-%{python3_version} SPHINXAPIDOC=sphinx-apidoc-%{python3_version}
rm doc/_build/html/.buildinfo


%install
%if 0%{?with_python2}
%py2_install
%endif

%if 0%{?with_python3}
%py3_install
%endif


%check
%if 0%{?with_python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{__python2} -m pytest \
  -k 'not test_manifest_providers' \
  test
%endif

%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{__python3} -m pytest \
  -k 'not test_manifest_providers' \
  test
%endif


%files doc
%license LICENSE.txt
%doc doc/_build/html

%if 0%{?with_python2}
%files -n python2-%{srcname}
%license LICENSE.txt
%doc README.md
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info/
%{_bindir}/rosdistro_build_cache
%{_bindir}/rosdistro_freeze_source
%{_bindir}/rosdistro_migrate_to_rep_141
%{_bindir}/rosdistro_migrate_to_rep_143
%{_bindir}/rosdistro_reformat
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{_bindir}/python%{python3_pkgversion}-rosdistro_build_cache
%{_bindir}/python%{python3_pkgversion}-rosdistro_freeze_source
%{_bindir}/python%{python3_pkgversion}-rosdistro_migrate_to_rep_141
%{_bindir}/python%{python3_pkgversion}-rosdistro_migrate_to_rep_143
%{_bindir}/python%{python3_pkgversion}-rosdistro_reformat
%endif


%changelog
* Fri Jun 10 2022 Scott K Logan <logans@cottsay.net> - 0.9.0-1
- Update to 0.9.0 (rhbz#2095797)
- Re-enable test_get_index_from_http_with_query_parameters

* Wed Sep 30 2020 Scott K Logan <logans@cottsay.net> - 0.8.3-1
- Update to 0.8.3 (rhbz#1883374)

* Fri May 29 2020 Scott K Logan <logans@cottsay.net> - 0.8.2-1
- Update to 0.8.2 (rhbz#1838293)

* Sat May 09 2020 Scott K Logan <logans@cottsay.net> - 0.8.1-1
- Update to 0.8.1 (rhbz#1824379)

* Wed Apr 15 2020 Scott K Logan <logans@cottsay.net> - 0.8.0-1
- Update to 0.8.0 (rhbz#1782354)

* Fri Oct 11 2019 Scott K Logan <logans@cottsay.net> - 0.7.5-1
- Update to 0.7.5 (rhbz#1761003)

* Wed Jul 17 2019 Scott K Logan <logans@cottsay.net> - 0.7.4-1
- Update to 0.7.4 (rhbz#1702421)

* Wed Mar 27 2019 Scott K Logan <logans@cottsay.net> - 0.7.3-1
- Update to 0.7.3 (rhbz#1693483)
- Switch to Python 3 Sphinx
- Handle automatic dependency generation (f30+)
- Make doc subpackage a weaker dependency

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
