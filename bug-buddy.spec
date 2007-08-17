%define major 0
%define libname %mklibname breakpad %major
%define libnamegnome %mklibname gnomebreakpad
%define breakpadarch %ix86

Summary:	Utility to ease the reporting of bugs within the GNOME Desktop Environment
Name:		bug-buddy
Version:        2.19.0
Release:	%mkrel 1
License:	GPL
Group:		Graphical desktop/GNOME
Source: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
#gw adapted from svn, allow build on non-i586 by disabling breakpad there
Patch: bug-buddy-2.19.0-disable-breakpad-on-unsupported-architectures.patch
URL:		http://www.gnome.org/
BuildRequires:	libgnome-menu-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:  libxslt-proc
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	evolution-data-server-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	libelfutils-devel
BuildRequires:	libsoup-devel >= 2.2.94
BuildRequires:	perl-XML-Parser
BuildRequires:	intltool gnome-common
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	gdb
Requires: %libnamegnome = %version
#gw it does a dlopen on libplds4.so
Requires: %mklibname nspr 4
Requires: %mklibname nss 3

%description
bug-buddy is a druid based tool which steps you through the GNOME bug
submission process.  It can automatically obtain stack traces from core
files or crashed applications.  Debian and KDE bug tracking systems are
also supported.

%package -n %libname
Summary: Crash dump library
Group: System/Libraries

%description -n %libname
Breakpad is a set of client and server components which implement a
crash-reporting system.

%package -n %libnamegnome
Summary: GTK+ module for loading the crash dump library
Group: System/Libraries
%ifarch %breakpadarch
Requires: %libname = %version
%endif

%description -n %libnamegnome
Breakpad is a set of client and server components which implement a
crash-reporting system. This is a module for GTK+ to automatically load the
breakpad library.

%prep
%setup -q
%patch -p1 -b .breakpad
intltoolize --force
aclocal
autoconf
automake

%build
%configure2_5x --disable-scrollkeeper

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
%find_lang %name

#gw not needed at the moment
rm -rf %buildroot%_libdir/{libbreakpad{.so,.a,.la},gtk-2.0/modules/libgnomebreakpad*a} %buildroot%_datadir/doc/breakpad*


%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%post
%post_install_gconf_schemas %name
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_icon_cache hicolor

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%_datadir/icons/hicolor/*/apps/%{name}*
%{_datadir}/bug-buddy

%ifarch %breakpadarch
%files -n %libname
%defattr(-, root, root)
%doc google-breakpad/README google-breakpad/AUTHORS
%_libdir/libbreakpad.so.%{major}*
%endif

%files -n %libnamegnome
%defattr(-, root, root)
%_libdir/gtk-2.0/modules/libgnomebreakpad.so*
