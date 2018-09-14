%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global srcname rosdistro

Name:           python-%{srcname}
Version:        0.6.9
Release:        1%{?dist}
Summary:        File format for managing ROS Distributions

License:        BSD and MIT
URL:            http://www.ros.org/wiki/rosdistro
Source0:        https://github.com/ros-infrastructure/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-pyyaml
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-catkin_pkg
BuildRequires:  python2-catkin-sphinx
BuildRequires:  python2-rospkg
BuildRequires:  python2-setuptools
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  python-nose1.1
BuildRequires:  python-sphinx10
%else
BuildRequires:  python2-nose
BuildRequires:  python2-sphinx
%endif

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

%package -n python2-%{srcname}
Summary: %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
Requires:       python2-pyyaml
Requires:       python2-catkin_pkg
Requires:       python2-rospkg
Requires:       python2-setuptools

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


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        File format for managing ROS Distributions
%{?python_provide:%python_provide python3-%{srcname}}
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

%description -n python3-%{srcname}
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
%setup -qn %{srcname}-%{version}
sed -i 's|#!/usr/bin/env python||' \
  src/rosdistro/external/appdirs.py \
  src/rosdistro/freeze_source.py

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
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests1.1 -w test -e test_get_index_from_http_with_query_parameters -e test_manifest_providers*
%else
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests -w test -e test_get_index_from_http_with_query_parameters -e test_manifest_providers*
%endif

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} nosetests-%{python3_version} -w test -e test_get_index_from_http_with_query_parameters -e test_manifest_providers*
popd
%endif

%files -n python2-%{srcname}
%doc README.md LICENSE.txt doc/_build/html
%{_bindir}/rosdistro_build_cache
%{_bindir}/rosdistro_reformat
%{_bindir}/rosdistro_migrate_to_rep_141
%{_bindir}/rosdistro_migrate_to_rep_143
%{_bindir}/rosdistro_freeze_source
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.md LICENSE.txt doc/_build/html
%{_bindir}/python3-rosdistro_build_cache
%{_bindir}/python3-rosdistro_reformat
%{_bindir}/python3-rosdistro_migrate_to_rep_141
%{_bindir}/python3-rosdistro_migrate_to_rep_143
%{_bindir}/python3-rosdistro_freeze_source
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%endif

%changelog
* Fri Sep 14 2018 Scott K Logan <logans@cottsay.net> - 0.6.9-1
- Update to 0.6.9 (rhbz#1525745)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.2-5
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.6.2-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 09 2017 Rich Mattes <richmattes@gmail.com> - 0.6.2-1
- Update to release 0.6.2 (rhbz#1425644)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Rich Mattes <richmattes@gmail.com> - 0.5.0-1
- Update to release 0.5.0 (rhbz#1388280)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.7-4
- Rebuild for Python 3.6

* Tue Sep 27 2016 Rich Mattes <richmattes@gmail.com> - 0.4.7-3
- Remove python-argparse requirement

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Apr 03 2016 Rich Mattes <richmattes@gmail.com> - 0.4.7-1
- Update to release 0.4.7 (rhbz#1304921)

* Wed Feb 10 2016 Rich Mattes <richmattes@gmail.com> - 0.4.4-1
- Update to release 0.4.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
