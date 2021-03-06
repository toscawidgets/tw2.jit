%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global modname tw2.jit

Name:           python-tw2-jit
Version:        2.0.3
Release:        3%{?dist}
Summary:        Javascript Infovis Toolkit (JIT) for ToscaWidgets2

Group:          Development/Languages
License:        MIT
URL:            http://toscawidgets.org
Source0:        http://pypi.python.org/packages/source/t/%{modname}/%{modname}-%{version}.tar.gz
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

%if %{?rhel}%{!?rhel:0} >= 6

# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"WebOb>=1.0\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py

%endif


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%files
%doc README.rst LICENSE-tw2-jit.txt LICENSE-jit.txt

%{python_sitelib}/tw2/jit
%{python_sitelib}/%{modname}-%{version}*


%changelog
* Fri May 11 2012 Ralph Bean <rbean@redhat.com> - 2.0.3-3
- Fixed typo in the files section.

* Fri May 11 2012 Ralph Bean <rbean@redhat.com> - 2.0.3-2
- Resolved directory ownership conflict.

* Wed May 02 2012 Ralph Bean <rbean@redhat.com> - 2.0.3-1
- New upstream release just to include LICENSE files.

* Wed May 02 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-2
- Removed clean section
- Removed defattr in files section
- Removed unnecessary references to buildroot

* Thu Apr 12 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-1
- Initial packaging for Fedora
