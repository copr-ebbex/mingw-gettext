%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define __debug_install_post %{_mingw32_debug_install_post}

Name:      mingw-gettext
Version:   0.18.1.1
Release:   6%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/gettext/
Source0:   http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz

# Fix compatibility with mingw-w64
Patch0:    gettext-0.18.1.1-tml.patch

BuildArch: noarch

BuildRequires: mingw32-filesystem >= 68
BuildRequires: mingw32-runtime >= 3.15.1
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-win-iconv
BuildRequires: mingw32-termcap >= 1.3.1-3

# Possible extra BRs.  These are used if available, but
# not required just for building.
#BuildRequires: mingw32-dlfcn
#BuildRequires: mingw32-libxml2
#BuildRequires: mingw32-expat
#BuildRequires: mingw32-glib2


%description
MinGW Windows Gettext library


%package -n mingw32-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages

%description -n mingw32-gettext
MinGW Windows Gettext library

%package -n mingw32-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       mingw32-gettext = %{version}-%{release}
Group:          Development/Libraries

%description -n mingw32-gettext-static
Static version of the MinGW Windows Gettext library.


%{?_mingw32_debug_package}


%prep
%setup -q -n gettext-%{version}
%patch0 -p0


%build
# Some build workarounds
export gl_cv_func_memchr_works="yes"
export ac_cv_func_strnlen_working="yes"
%{_mingw32_configure} \
  --disable-java \
  --disable-native-java \
  --disable-csharp \
  --enable-static \
  --enable-threads=win32 \
  --without-emacs
make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw32_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{_mingw32_libdir}/charset.alias

# Remove documentation - already available in base gettext-devel.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}/man1/
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}/man3/
rm -rf $RPM_BUILD_ROOT%{_mingw32_docdir}/gettext/
rm -rf $RPM_BUILD_ROOT%{_mingw32_docdir}/libasprintf/
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/info/

%find_lang %{name} --all-name


%files -n mingw32-gettext -f %{name}.lang
%doc COPYING
%{_mingw32_bindir}/autopoint
%{_mingw32_bindir}/envsubst.exe
%{_mingw32_bindir}/gettext.exe
%{_mingw32_bindir}/gettext.sh
%{_mingw32_bindir}/gettextize
%{_mingw32_bindir}/libasprintf-0.dll
%{_mingw32_bindir}/libgettextlib-0-18-1.dll
%{_mingw32_bindir}/libgettextpo-0.dll
%{_mingw32_bindir}/libgettextsrc-0-18-1.dll
%{_mingw32_bindir}/libintl-8.dll
%{_mingw32_bindir}/msg*.exe
%{_mingw32_bindir}/ngettext.exe
%{_mingw32_bindir}/recode-sr-latin.exe
%{_mingw32_bindir}/xgettext.exe

%{_mingw32_includedir}/autosprintf.h
%{_mingw32_includedir}/gettext-po.h
%{_mingw32_includedir}/libintl.h

%{_mingw32_libdir}/gettext

%{_mingw32_libdir}/libasprintf.dll.a
%{_mingw32_libdir}/libasprintf.la

%{_mingw32_libdir}/libgettextlib.dll.a
%{_mingw32_libdir}/libgettextlib.la

%{_mingw32_libdir}/libgettextpo.dll.a
%{_mingw32_libdir}/libgettextpo.la

%{_mingw32_libdir}/libgettextsrc.dll.a
%{_mingw32_libdir}/libgettextsrc.la

%{_mingw32_libdir}/libintl.dll.a
%{_mingw32_libdir}/libintl.la

%{_mingw32_datadir}/gettext/

%{_mingw32_datadir}/aclocal/*m4

%files -n mingw32-gettext-static
%{_mingw32_libdir}/libasprintf.a
%{_mingw32_libdir}/libgettextpo.a
%{_mingw32_libdir}/libintl.a


%changelog
* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-6
- Renamed the source package to mingw-gettext (RHBZ #xxxx)

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-5
- Rebuild against the mingw-w64 toolchain
- Added a patch to fix compatibility with mingw-w64

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-3
- Rebuild again to fix incomplete dependencies

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-2
- Rebuild against win-iconv

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 0.18.1.1-1
- Update to 0.18.1.1
- Spec cleanup
- Split debug symbols in -debuginfo subpackage

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 0.17-16
- Removed html documentation and info pages

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17.15
- Dropped the proxy-libintl pieces as the upstream gtk+ win32 maintainers
  also decided to drop it and it's causing more harm than good

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17-13
- Replaced the libintl import library with a small wrapper library in order
  to let other binaries have a soft-dependency on libintl-8.dll as proposed
  on the fedora-mingw mailing list

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17-11
- Added -static subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-9
- Rebuild for mingw32-gcc 4.4

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-8
- Use find_lang macro.

* Fri Jan 16 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-7
- Remove the manpages - already available in base Fedora gettext-devel.
- Use _smp_mflags for build.
- Added list of potential BRs.
- Added license file to doc section.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-6
- Add fix for undefined Gnulib symbols (Farkas Levente).
- Rebuild against mingw32-termcap / libtermcap.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-5
- Rename mingw -> mingw32.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-4
- Disable emacs lisp file install

* Thu Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-3
- Remove static libraries.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
