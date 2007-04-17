Summary:	Utility to ease the reporting of bugs within the GNOME Desktop Environment
Name:		bug-buddy
Version:        2.18.1
Release:	%mkrel 1
License:	GPL
Group:		Graphical desktop/GNOME
Source: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	libgnome-menu-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:  libxslt-proc
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	evolution-data-server-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	libsoup-devel >= 2.2.94
BuildRequires:	perl-XML-Parser
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	gdb
#gw it does a dlopen on libplds4.so
Requires: %mklibname nspr 4
Requires: %mklibname nss 3

%description
bug-buddy is a druid based tool which steps you through the GNOME bug
submission process.  It can automatically obtain stack traces from core
files or crashed applications.  Debian and KDE bug tracking systems are
also supported.

%prep
%setup -q

%build
%configure2_5x --disable-scrollkeeper

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT


%post
%post_install_gconf_schemas %name
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_icon_cache hicolor

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%_datadir/icons/hicolor/*/apps/%{name}*
%{_datadir}/bug-buddy
