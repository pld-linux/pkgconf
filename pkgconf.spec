#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Package compiler and linker metadata toolkit
Name:		pkgconf
Version:	1.3.5
Release:	0.1
License:	ISC
Source0:	https://distfiles.dereferenced.org/pkgconf/%{name}-%{version}.tar.xz
# Source0-md5:	cd3f3b2328996eb7eac4ab24f58989ba
Group:		Development/Tools
URL:		http://pkgconf.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:	libtool
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with tests}
BuildRequires:	%{_bindir}/kyua
BuildRequires:	atf-tests
%endif
Requires:	libpkgconf = %{version}-%{release}
# This is defined within pkgconf code as a virtual pc (just like in pkgconfig)
Provides:	pkgconfig(pkgconf) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pkgconf is a program which helps to configure compiler and linker
flags for development frameworks. It is similar to pkg-config from
freedesktop.org and handles .pc files in a similar manner as
pkg-config.

%package -n libpkgconf
Summary:	Backend library for %{name}

%description -n libpkgconf
This package provides libraries for applications to use the
functionality of %{name}.

%package -n libpkgconf-devel
Summary:	Development files for lib%{name}
Requires:	lib%{name} = %{version}-%{release}

%description -n libpkgconf-devel
This package provides files necessary for developing applications to
use functionality provided by %{name}.

%prep
%setup -q

%build
%{__aclocal}
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-pkg-config-dir=%{_pkgconfigdir}:%{_npkgconfigdir} \
	--with-system-includedir=%{_includedir} \
	--with-system-libdir=%{_libdir}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/libpkgconf.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libpkgconf -p /sbin/ldconfig
%postun	-n libpkgconf -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS NEWS
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_aclocaldir}/pkg.m4

%files -n libpkgconf
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libpkgconf.so.*.*.*
%ghost %{_libdir}/libpkgconf.so.2

%files -n libpkgconf-devel
%defattr(644,root,root,755)
%{_libdir}/libpkgconf.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libpkgconf.pc
