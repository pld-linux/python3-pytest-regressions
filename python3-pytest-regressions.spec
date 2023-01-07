#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Easy to use fixtures to write regression tests
Summary(pl.UTF-8):	Łatwe w użyciu wyposażenie do tworzenia testów regresji
Name:		python3-pytest-regressions
Version:	2.4.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-regressions/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-regressions/pytest-regressions-%{version}.tar.gz
# Source0-md5:	2e82a7d4701656b2fc35f8d08069543f
URL:		https://pypi.org/project/pytest-regressions/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-pandas
BuildRequires:	python3-pytest >= 3.5.0
BuildRequires:	python3-pytest-datadir >= 1.2.0
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
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

# fail because of numpy DeprecationWarnings
%{__mv} tests/test_dataframe_regression.py tests/disabled_dataframe_regression.py
%{__mv} tests/test_num_regression.py tests/disabled_num_regression.py
%{__mv} tests/test_filenames.py tests/disabled_filenames.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_datadir.plugin,pytest_regressions.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_common_case'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_regressions
%{py3_sitescriptdir}/pytest_regressions-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
