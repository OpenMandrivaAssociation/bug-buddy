%define major 0
%define libname %mklibname breakpad %major
%define libnamegnome %mklibname gnomebreakpad
%define breakpadarch %ix86

Summary:	Utility to ease the reporting of bugs within the GNOME Desktop Environment
Name:		bug-buddy
Version:        2.28.0
Release:	%mkrel 3
License:	GPLv2+
Group:		Graphical desktop/GNOME
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

URL:		http://www.gnome.org/
BuildRequires:	libgnome-menu-devel
BuildRequires:	libbonobo2_x-devel
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	evolution-data-server-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	libelfutils-devel
BuildRequires:	libsoup-devel >= 2.2.94
#gw libtool dep
BuildRequires:	dbus-glib-devel
BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	popt-devel
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

%ifarch %breakpadarch
%package -n %libname
Summary: Crash dump library
Group: System/Libraries

%description -n %libname
Breakpad is a set of client and server components which implement a
crash-reporting system.
%endif

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

%build

CFLAGS="`echo %optflags |sed -e 's/-fomit-frame-pointer//'`" CXXFLAGS="`echo %optflags |sed -e 's/-fomit-frame-pointer//'`" %configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
%find_lang %name

#gw not needed at the moment
rm -rf %buildroot%_libdir/{%name/libbreakpad{.so,.a,.la},gtk-2.0/modules/libgnomebreakpad*a} %buildroot%_datadir/doc/breakpad*


%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%post
%post_install_gconf_schemas %name
%update_icon_cache hicolor
%update_icon_cache HighContrastLargePrint

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_icon_cache hicolor
%clean_icon_cache HighContrastLargePrint

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%_datadir/icons/hicolor/*/apps/%{name}*
%_datadir/icons/HighContrastLargePrint/*/apps/bug-buddy*
%{_datadir}/bug-buddy
%_mandir/man1/bug*

%ifarch %breakpadarch
%files -n %libname
%defattr(-, root, root)
%doc google-breakpad/README google-breakpad/AUTHORS
%_libdir/%name/libbreakpad.so.%{major}*
%endif

%files -n %libnamegnome
%defattr(-, root, root)
%_libdir/gtk-2.0/modules/libgnomebreakpad.so*
