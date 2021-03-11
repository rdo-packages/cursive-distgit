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
Version:        XXX
Release:        XXX
Summary:        OpenStack-specific validation of digital signatures

License:        ASL 2.0
URL:            https://github.com/openstack/cursive
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-setuptools
BuildRequires:  python3-subunit >= 0.0.18
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testscenarios >= 0.4
BuildRequires:  python3-testtools >= 1.4.0
# Required for tests
BuildRequires: python3-castellan
BuildRequires: python3-cryptography
BuildRequires: python3-mock
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-serialization
BuildRequires: python3-oslo-utils
%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Cursive implements OpenStack-specific validation of digital signatures
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:       python3-castellan >= 0.4.0
Requires:       python3-cryptography
Requires:       python3-oslo-log >= 1.14.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.16.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-pbr

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        cursive documentation
# Required for documentation
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
%description -n python-%{pypi_name}-doc
Documentation for cursive
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{py3_build}

%if 0%{?with_doc}
# generate docs
python3 setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{py3_install}

%check
export PYTHON=python3
python3 setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
