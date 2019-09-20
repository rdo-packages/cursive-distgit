# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name cursive
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global common_desc \
Cursive implements OpenStack-specific validation of digital signatures. \
\
The cursive project contains code extracted from various OpenStack \
projects for verifying digital signatures. Additional capabilities will be \
added to this project in support of various security features.

Name:           python-%{pypi_name}
Version:        0.2.2
Release:        1%{?dist}
Summary:        OpenStack-specific validation of digital signatures

License:        ASL 2.0
URL:            https://github.com/openstack/cursive
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-oslotest >= 1.10.0
BuildRequires:  python%{pyver}-pbr >= 1.8
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-subunit >= 0.0.18
BuildRequires:  python%{pyver}-testrepository >= 0.0.18
BuildRequires:  python%{pyver}-testscenarios >= 0.4
BuildRequires:  python%{pyver}-testtools >= 1.4.0
# Required for tests
BuildRequires: python%{pyver}-castellan
BuildRequires: python%{pyver}-cryptography
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-utils
%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Cursive implements OpenStack-specific validation of digital signatures
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
Requires:       python%{pyver}-castellan >= 0.4.0
Requires:       python%{pyver}-cryptography
Requires:       python%{pyver}-oslo-log >= 1.14.0
Requires:       python%{pyver}-oslo-serialization >= 1.10.0
Requires:       python%{pyver}-oslo-utils >= 3.16.0
Requires:       python%{pyver}-oslo-i18n >= 2.1.0
Requires:       python%{pyver}-pbr

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        cursive documentation
# Required for documentation
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx
%description -n python-%{pypi_name}-doc
Documentation for cursive
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{pyver_build}

%if 0%{?with_doc}
# generate docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{pyver_install}

%check
export PYTHON=%{pyver_bin}
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Sep 20 2019 RDO <dev@lists.rdoproject.org> 0.2.2-1
- Update to 0.2.2

