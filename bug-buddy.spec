%define major 0
%define libnamegnome %mklibname gnomebreakpad

Summary:	Utility to ease the reporting of bugs within the GNOME Desktop Environment
Name:		bug-buddy
Version:        2.32.0
Release:	8
License:	GPLv2+
Group:		Graphical desktop/GNOME
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	gnome-menus-devel
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	evolution-data-server-devel
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	elfutils-devel
BuildRequires:	libsoup-devel >= 2.2.94
#gw libtool dep
BuildRequires:	dbus-glib-devel
BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	popt-devel
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
%apply_patches

%build

CFLAGS="`echo %optflags |sed -e 's/-fomit-frame-pointer//'`"
CXXFLAGS="`echo %optflags |sed -e 's/-fomit-frame-pointer//'`"
%configure2_5x

%make LIBS='-lgmodule-2.0 -lelf'

%install
%makeinstall_std
%find_lang %name

#gw not needed at the moment
rm -rf %buildroot%_libdir/gtk-2.0/modules/libgnomesegvhandler*a

%post
#gw gnomebreakpad was replaced by gnomesegvhandler
%{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/gnome_settings_daemon/gtk-modules/gnomebreakpad false > /dev/null || :

%preun
%preun_uninstall_gconf_schemas %name

%files -f %name.lang
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%_datadir/icons/hicolor/*/apps/%{name}*
%_datadir/icons/HighContrastLargePrint/*/apps/bug-buddy*
%{_datadir}/bug-buddy
%_mandir/man1/bug*

%files -n %libnamegnome
%_libdir/gtk-2.0/modules/libgnomesegvhandler.so


%changelog
* Mon Sep 03 2012 Vladimir Testov <vladimir.testov@rosalab.ru> 2.32.0-4
- adopted for ROSA

* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 2.32.0-3mdv2011.0
+ Revision: 677067
- rebuild to add gconf2 as req

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.32.0-2
+ Revision: 663341
- mass rebuild

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581419
- update to new version 2.32.0

* Mon Sep 13 2010 Götz Waschk <waschk@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 577935
- update to new version 2.31.92

* Mon Aug 16 2010 Götz Waschk <waschk@mandriva.org> 2.31.3-3mdv2011.0
+ Revision: 570454
- disable gnomebreakpad gtk module loading (bug #60670)

* Mon Aug 09 2010 Götz Waschk <waschk@mandriva.org> 2.31.3-2mdv2011.0
+ Revision: 568220
- rebuild for new e-d-s

* Fri Jul 30 2010 Götz Waschk <waschk@mandriva.org> 2.31.3-1mdv2011.0
+ Revision: 563392
- new version
- remove libbreakpad
- update file list

* Mon Mar 29 2010 Götz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528752
- update to new version 2.30.0

* Thu Mar 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2.28.0-3mdv2010.1
+ Revision: 527388
- rebuilt against nss-3.12.6

* Tue Mar 16 2010 Funda Wang <fwang@mandriva.org> 2.28.0-2mdv2010.1
+ Revision: 522514
- fix typo
- BR popt
  set libpackage correctly

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for 2010.1

* Mon Sep 21 2009 Götz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446529
- update to new version 2.28.0

* Thu Sep 10 2009 Götz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 437418
- update to new version 2.27.92

* Mon May 11 2009 Götz Waschk <waschk@mandriva.org> 2.27.1-1mdv2010.0
+ Revision: 374179
- new version

* Tue Mar 17 2009 Funda Wang <fwang@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 356456
- New version 2.26.0

* Mon Feb 16 2009 Götz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 340898
- update to new version 2.25.91

* Tue Dec 02 2008 Götz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 309007
- fix build deps
- update to new version 2.25.2

* Sat Nov 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2.25.1-2mdv2009.1
+ Revision: 301008
- rebuilt against new libxcb

  + Götz Waschk <waschk@mandriva.org>
    - update build deps

* Tue Nov 04 2008 Götz Waschk <waschk@mandriva.org> 2.25.1-1mdv2009.1
+ Revision: 299718
- update to new version 2.25.1

* Sun Oct 19 2008 Götz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 295229
- update to new version 2.24.1

* Mon Sep 22 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 286613
- new version

* Mon Sep 01 2008 Götz Waschk <waschk@mandriva.org> 2.23.91.1-1mdv2009.0
+ Revision: 278365
- new version

* Mon Sep 01 2008 Götz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278074
- new version

* Mon Aug 18 2008 Götz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 273384
- new version

* Thu Aug 07 2008 Götz Waschk <waschk@mandriva.org> 2.23.6-2mdv2009.0
+ Revision: 265949
- handle icon cache

* Mon Aug 04 2008 Götz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 263080
- new version
- update file list

* Tue Jul 22 2008 Götz Waschk <waschk@mandriva.org> 2.23.5.1-1mdv2009.0
+ Revision: 240006
- new version

* Mon Jul 21 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 239467
- new version
- drop patch

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue May 27 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-2mdv2009.0
+ Revision: 211747
- Patch0: fix underlinking

* Tue Mar 11 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 184999
- new version

* Tue Feb 12 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-2mdv2008.1
+ Revision: 166149
- libsoup rebuild

* Wed Jan 30 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 160393
- new version

* Tue Jan 22 2008 Funda Wang <fwang@mandriva.org> 2.20.1-2mdv2008.1
+ Revision: 156327
- rebuild against latest gnutls

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 08 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.1-1mdv2008.1
+ Revision: 95695
- Don't compile with omit-frame-pointer, it creates useless minidump

  + Götz Waschk <waschk@mandriva.org>
    - new version
    - drop patch

* Wed Sep 26 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-2mdv2008.0
+ Revision: 93038
- Patch0 (SVN): various bug fixes

* Tue Sep 18 2007 Götz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 89464
- new version
- update file list

* Tue Aug 28 2007 Götz Waschk <waschk@mandriva.org> 2.19.91-1mdv2008.0
+ Revision: 72766
- new version
- drop patch

* Fri Aug 17 2007 Götz Waschk <waschk@mandriva.org> 2.19.0-1mdv2008.0
+ Revision: 65121
- fix buildrequires
- fix package split
- fix build with a patch from svn
- fix buildrequires
- new version
- add breakpad library

* Tue Apr 17 2007 Götz Waschk <waschk@mandriva.org> 2.18.1-1mdv2008.0
+ Revision: 13872
- new version
- drop patches


* Tue Apr 03 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0-2mdv2007.1
+ Revision: 150296
- Patch1: fix other-binaries search

  + Götz Waschk <waschk@mandriva.org>
    - fix crash on exit (b.g.o #425245)

* Tue Mar 13 2007 Götz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 142143
- new version

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.4-3mdv2007.1
+ Revision: 126176
- bump
- this release bump is presented to you by ...
- new version

* Mon Jan 08 2007 Götz Waschk <waschk@mandriva.org> 2.17.3-4mdv2007.1
+ Revision: 105905
- add more missing deps

* Mon Jan 08 2007 Götz Waschk <waschk@mandriva.org> 2.17.3-3mdv2007.1
+ Revision: 105469
- really fix deps

* Mon Jan 08 2007 Götz Waschk <waschk@mandriva.org> 2.17.3-2mdv2007.1
+ Revision: 105452
- fix deps

* Mon Dec 18 2006 Götz Waschk <waschk@mandriva.org> 2.17.3-1mdv2007.1
+ Revision: 98391
- new version

* Mon Dec 04 2006 Götz Waschk <waschk@mandriva.org> 2.17.2-1mdv2007.1
+ Revision: 90318
- new version

* Wed Nov 29 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-3mdv2007.1
+ Revision: 88304
- Import bug-buddy

* Wed Nov 29 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-3mdv2007.1
- Rebuild

* Tue Sep 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2.16.0-2mdv2007.0
- Remove source4 and 5, since we now ships debug package

* Wed Sep 06 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- drop scrollkeeper stuff
- update file list
- New version 2.16.0

* Wed Aug 23 2006 Götz Waschk <waschk@mandriva.org> 2.15.92-1mdv2007.0
- New release 2.15.92

* Wed Jul 26 2006 Götz Waschk <waschk@mandriva.org> 2.15.90-1mdv2007.0
- rebuild for new e-d-s

* Wed Jul 26 2006 Götz Waschk <waschk@mandriva.org> 2.15.90-1mdv2007.0
- update file list
- New release 2.15.90

* Fri Jun 30 2006 Götz Waschk <waschk@mandriva.org> 2.15.0-3mdv2007.0
- don't make profile.d scripts executable
- new macros
- remove menu entry

* Thu Jun 15 2006 Götz Waschk <waschk@mandriva.org> 2.15.0-2mdv2007.0
- fix buildrequires

* Wed Jun 14 2006 Götz Waschk <waschk@mandriva.org> 2.15.0-1mdv2007.0
- fix rpmlint warning about scripts without shell-bang
- update file list
- update deps
- drop patch
- New release 2.15.0

* Wed Apr 19 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-1mdk
- Release 2.14.0

* Wed Oct 19 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-4mdk
- Fix Buildrequires

* Sun Oct 09 2005 Götz Waschk <waschk@mandriva.org> 2.12.1-3mdk
- fix buildrequires
- use /usr/lib/sendmail by default

* Sat Oct 08 2005 Götz Waschk <waschk@mandriva.org> 2.12.1-2mdk
- fix buildrequires

* Fri Oct 07 2005 Götz Waschk <waschk@mandriva.org> 2.12.1-1mdk
- fix buildrequires
- New release 2.12.1

* Fri Oct 07 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.0-1mdk
- Release 2.12.0

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.8.0-3mdk
- fix rpmlint errors (PreReq)

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.8.0-2mdk
- fix rpmlint errors (PreReq)

* Wed Oct 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.0-1mdk
- New release 2.8.0

* Sat Aug 28 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.1-2mdk
- Fix menu

* Wed Apr 21 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.1-1mdk
- New release 2.6.1

* Sun Apr 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.6.0-2mdk
- buildrequires
- minor cosmetics

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- New release 2.6.0

