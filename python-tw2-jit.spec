%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global modname tw2.jit

Name:           python-tw2-jit
Version:        2.0.2
Release:        1%{?dist}
Summary:        Javascript Infovis Toolkit (JIT) for ToscaWidgets2

Group:          Development/Languages
License:        MIT
URL:            http://toscawidgets.org
Source0:        http://pypi.python.org/packages/source/t/%{modname}/%{modname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# For building
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-tw2-core
BuildRequires:  python-tw2-jquery
BuildRequires:  python-tw2-sqla
BuildRequires:  python-sqlalchemy
BuildRequires:  python-BeautifulSoup
BuildRequires:  python-genshi
BuildRequires:  python-mako

# Runtime requirements
Requires:  python-tw2-core
Requires:  python-tw2-jquery
Requires:  python-tw2-sqla
Requires:  python-sqlalchemy
Requires:  python-BeautifulSoup
Requires:  python-genshi
Requires:  python-mako

%description
toscawidgets2 (tw2) aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

The JavaScript InfoVis Toolkit (thejit) is a javascript library that
provides web standard based tools to create interactive data visualizations
for the Web.  It is pretty, interactive, and fast.

This module, tw2.jit, provides toscawidgets2 (tw2) widgets that render
thejit data visualizations.

%prep
%setup -q -n %{modname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{python_sitelib}/*

%changelog
* Thu Apr 12 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-1
- Initial packaging for Fedora
