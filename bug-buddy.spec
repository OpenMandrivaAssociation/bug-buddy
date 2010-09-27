%define major 0
%define libnamegnome %mklibname gnomebreakpad

Summary:	Utility to ease the reporting of bugs within the GNOME Desktop Environment
Name:		bug-buddy
Version:        2.32.0
Release:	%mkrel 1
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

%package -n %libnamegnome
Summary: GTK+ module for loading the crash dump library
Group: System/Libraries

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
rm -rf %buildroot%_libdir/gtk-2.0/modules/libgnomesegvhandler*a


%clean
rm -rf $RPM_BUILD_ROOT

%post
#gw gnomebreakpad was replaced by gnomesegvhandler
%{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/gnome_settings_daemon/gtk-modules/gnomebreakpad false > /dev/null || :

%preun
%preun_uninstall_gconf_schemas %name

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

%files -n %libnamegnome
%defattr(-, root, root)
%_libdir/gtk-2.0/modules/libgnomesegvhandler.so
