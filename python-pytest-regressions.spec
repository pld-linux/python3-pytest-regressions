#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Easy to use fixtures to write regression tests
Summary(pl.UTF-8):	Łatwe w użyciu wyposażenie do tworzenia testów regresji
Name:		python-pytest-regressions
# keep 1.x here for python2 support
Version:	1.0.6
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-regressions/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-regressions/pytest-regressions-%{version}.tar.gz
# Source0-md5:	52cf60a43ff9aa0a89f98f8da0e2dc5a
URL:		https://pypi.org/project/pytest-regressions/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML
BuildRequires:	python-pandas
BuildRequires:	python-pathlib2
BuildRequires:	python-pytest >= 3.5.0
BuildRequires:	python-pytest-datadir >= 1.2.0
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-pandas
BuildRequires:	python3-pytest >= 3.5.0
BuildRequires:	python3-pytest-datadir >= 1.2.0
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin makes it simple to test general data, images, files, and
numeric tables by saving expected data in a data directory (courtesy
of pytest-datadir) that can be used to verify that future runs produce
the same data.

%description -l pl.UTF-8
Ta wtyczka ułatwia testowanie ogólnych danych, obrazów, plików i
tablic liczbowych poprzez zapisanie oczekiwanych danych w katalogu z
danymi (dzięki pytest-datadir), które mogą być użyte do
zweryfikowania, że przyszłe uruchomienia dadzą te same dane.

%package -n python3-pytest-regressions
Summary:	Easy to use fixtures to write regression tests
Summary(pl.UTF-8):	Łatwe w użyciu wyposażenie do tworzenia testów regresji
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-pytest-regressions
This plugin makes it simple to test general data, images, files, and
numeric tables by saving expected data in a data directory (courtesy
of pytest-datadir) that can be used to verify that future runs produce
the same data.

%description -n python3-pytest-regressions -l pl.UTF-8
Ta wtyczka ułatwia testowanie ogólnych danych, obrazów, plików i
tablic liczbowych poprzez zapisanie oczekiwanych danych w katalogu z
danymi (dzięki pytest-datadir), które mogą być użyte do
zweryfikowania, że przyszłe uruchomienia dadzą te same dane.

%package apidocs
Summary:	API documentation for Python pytest-regressions module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-regressions
Group:		Documentation

%description apidocs
API documentation for Python pytest-regressions module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-regressions.

%prep
%setup -q -n pytest-regressions-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_datadir.plugin,pytest_regressions.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# fails because of numpy DeprecationWarnings
%{__mv} tests/test_num_regression.py tests/disabled_num_regression.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_datadir.plugin,pytest_regressions.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -W ignore::DeprecationWarning -m pytest tests
%{__mv} tests/disabled_num_regression.py tests/test_num_regression.py
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/pytest_regressions
%{py_sitescriptdir}/pytest_regressions-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-regressions
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_regressions
%{py3_sitescriptdir}/pytest_regressions-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
