Summary:	Blitz++ - a C++ class library for scientific computing
Summary(pl.UTF-8):	Blitz++ - biblioteka klas C++ do obliczeń naukowych
Name:		blitz
Version:	0.9
Release:	0.1
License:	GPL or Blitz artistic license
Group:		Libraries
Source0:	http://dl.sourceforge.net/blitz/%{name}-%{version}.tar.gz
# Source0-md5:	031df2816c73e2d3bd6d667bbac19eca
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-compiler_specific_header.patch
Patch2:		%{name}-infopage.patch
URL:		http://www.oonumerics.org/blitz/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	fonts-TTF-bitstream-vera
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
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
#%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared
%{__make} lib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_docdir}/%{name}-doc-%{version}/doxygen,%{_examplesdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -af examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
%{__sed} -i -e 's/(blitz++)\./(blitz)./' %{_infodir}/dir

%postun devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog ChangeLog.1 LEGAL LICENSE NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_pkgconfigdir}/blitz-uninstalled.pc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/blitz
%{_includedir}/random
%{_pkgconfigdir}/blitz.pc
%{_infodir}/*.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc-%{version}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
