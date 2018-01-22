%global pypi_name cursive
%if 0%{?fedora}
%global with_python3 1
%endif
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Cursive implements OpenStack-specific validation of digital signatures. \
\
The cursive project contains code extracted from various OpenStack \
projects for verifying digital signatures. Additional capabilities will be \
added to this project in support of various security features.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack-specific validation of digital signatures

License:        ASL 2.0
URL:            https://github.com/openstack/cursive
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-hacking
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  python-pbr >= 1.8
BuildRequires:  python-setuptools
BuildRequires:  python-subunit >= 0.0.18
BuildRequires:  python-testrepository >= 0.0.18
BuildRequires:  python-testscenarios >= 0.4
BuildRequires:  python-testtools >= 1.4.0
# Required for documentation
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-reno
BuildRequires:  python-sphinx
# Required for tests
BuildRequires: python-castellan
BuildRequires: python-cryptography
BuildRequires: python-oslo-log
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-utils
%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Cursive implements OpenStack-specific validation of digital signatures
%{?python_provide:%python_provide python2-%{pypi_name}}
Requires:       python-castellan >= 0.4.0
Requires:       python-cryptography
Requires:       python-lxml >= 2.3
Requires:       python-netifaces >= 0.10.4
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.16.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-six >= 1.9.0
Requires:       python-pbr

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Cursive implements OpenStack-specific validation of digital signatures
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-setuptools
BuildRequires:  python3-subunit >= 0.0.18
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testscenarios >= 0.4
BuildRequires:  python3-testtools >= 1.4.0
# Required for documentation
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-reno
BuildRequires:  python3-sphinx
# Required for tests
BuildRequires:  python3-castellan
BuildRequires:  python3-cryptography
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-utils

Requires:       python3-castellan >= 0.4.0
Requires:       python3-cryptography
Requires:       python3-lxml >= 2.3
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-oslo-log >= 1.14.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.16.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-six >= 1.9.0
Requires:       python3-pbr

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%package -n python-%{pypi_name}-doc
Summary:        cursive documentation
%description -n python-%{pypi_name}-doc
Documentation for cursive

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%changelog
