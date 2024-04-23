#
# Conditional build:
%bcond_without	apidocs	# Doxygen API documentation
%bcond_with	tbb	# Intel Threading Building Blocks atomic types

Summary:	Blitz++ - a C++ class library for scientific computing
Summary(pl.UTF-8):	Blitz++ - biblioteka klas C++ do obliczeń naukowych
Name:		blitz
Version:	1.0.2
Release:	1
License:	Artistic v2.0, BSD or LGPL v3
Group:		Libraries
#Source0Download: https://github.com/blitzpp/blitz/releases
Source0:	https://github.com/blitzpp/blitz/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	195873ba25ae4c10b9cd374bf42c67c2
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-doc.patch
Patch2:		%{name}-infopage.patch
URL:		https://github.com/blitzpp/blitz/wiki/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	blas-devel
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	fonts-TTF-bitstream-vera
BuildRequires:	gcc-fortran
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_tbb:BuildRequires:	tbb-devel}
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blitz++ is a C++ class library for scientific computing which provides
performance on par with Fortran 77/90. It uses template techniques to
achieve high performance. The current versions provide dense arrays
and vectors, random number generators, and small vectors and matrices.

%description -l pl.UTF-8
Blitz++ jest biblioteką klas C++ do obliczeń naukowych o wydajności
dorównującej Fortranowi 77/90. Do osiągnięcia dużej wydajności używa
rozwiązań opartych na szablonach. Dostarcza gęstych tablic i wektorów,
generatorów liczb losowych oraz małych wektorów i macierzy.

%package devel
Summary:	Header files for Blitz++ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Blitz++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Blitz++ library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Blitz++.

%package static
Summary:	Static Blitz++ library
Summary(pl.UTF-8):	Statyczna biblioteka Blitz++
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Blitz++ library.

%description static -l pl.UTF-8
Statyczna biblioteka Blitz++.

%package doc
Summary:	Documentation for Blitz++ library
Summary(pl.UTF-8):	Dokumentacja Blitz++
Group:		Documentation

%description doc
Documentation for Blitz++ library.

%description doc -l pl.UTF-8
Dokumentacja biblioteki Blitz++.

%package examples
Summary:	Examples for Blitz++ library
Summary(pl.UTF-8):	Przykłady Blitz++
Group:		Documentation

%description examples
Examples for Blitz++ library.

%description examples -l pl.UTF-8
Przykłady Blitz++.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# here papi is ptools-perfapi library, not the one from papi.spec
%configure \
	ac_cv_lib_papi_main=no \
	%{?with_apidocs:--enable-doxygen --enable-html-docs} \
	--enable-serialization \
	--enable-shared \
	--with-boost-libdir=%{_libdir} \
	%{?with_tbb:--with-tbb}

%{__make}

%{__make} -j1 info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install install-info \
	DESTDIR=$RPM_BUILD_ROOT

cp -af examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-doc-%{version}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libblitz.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT ChangeLog* LEGAL NEWS README.md
%attr(755,root,root) %{_libdir}/libblitz.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblitz.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblitz.so
%{_includedir}/blitz
%{_includedir}/random
%{_pkgconfigdir}/blitz.pc
%{_infodir}/blitz.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libblitz.a

%if %{with apidocs}
%files doc
%defattr(644,root,root,755)
%doc doc/doxygen/html/{search,*.css,*.html,*.js,*.png}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
