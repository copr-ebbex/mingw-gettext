# Windows on ARM64, clang/lld based.  Must precede %%mingw_package_header.
%global mingw_build_ucrtarm64 1
# win32/win64: C builds with the clang supplement drivers, so libintl-8.dll
# (the one DLL the qemu-ga MSI ships) carries no GNU runtime imports.  The
# C++ parts (woe32dll/c++*.cc, autosprintf.cc) stay on g++ and libstdc++:
# there is no libc++ for these targets, and none of those DLLs are shipped
# in the MSI.
%global mingw_toolchain_win32 clang
%global mingw_toolchain_win64 clang
%{?mingw_package_header}

Name:      mingw-gettext
Version:   1.0
Release:   2.2%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPL-2.0-or-later AND LGPL-2.0-or-later
URL:       http://www.gnu.org/software/gettext/
Source0:   https://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz

BuildArch: noarch

BuildRequires: make
# The win32/win64 clang columns dispatch to the supplement drivers only from
# 152-1.9 on.  gcc-c++ stays: the C++ parts build with g++ (see the toolchain
# comment above), and GNU windres finds its <triplet>-gcc preprocessor again.
BuildRequires: mingw32-filesystem >= 152-1.9
BuildRequires: mingw32-clang
BuildRequires: mingw32-compiler-rt >= 22.1.8
BuildRequires: mingw32-libunwind >= 22.1.8
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-win-iconv
BuildRequires: mingw32-termcap

BuildRequires: mingw64-filesystem >= 152-1.9
BuildRequires: mingw64-clang
BuildRequires: mingw64-compiler-rt >= 22.1.8
BuildRequires: mingw64-libunwind >= 22.1.8
BuildRequires: mingw64-gcc
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-binutils
BuildRequires: mingw64-win-iconv
BuildRequires: mingw64-termcap

# No gcc for this target: the toolchain is clang, lld and the llvm-* tools.
# Headers and CRT must be named; the other targets get them through gcc.
BuildRequires: ucrtarm64-filesystem >= 152
BuildRequires: ucrtarm64-clang
BuildRequires: ucrtarm64-llvm-tools
BuildRequires: ucrtarm64-headers
BuildRequires: ucrtarm64-crt
# The drivers always link -rtlib=compiler-rt (__chkstk lives there) and
# -unwindlib=libunwind; libunwind only arrives through ucrtarm64-clang's
# Recommends chain, and mock installs no weak dependencies.
BuildRequires: ucrtarm64-compiler-rt >= 22.1.8
BuildRequires: ucrtarm64-libunwind >= 22.1.8
# gettext compiles real C++ on Windows targets (woe32dll/c++*.cc,
# autosprintf.cc); clang++ always passes -stdlib=libc++, which is only a
# Recommends of ucrtarm64-clang.
BuildRequires: ucrtarm64-libcxx >= 22.1.8
# gnulib's threadlib puts -pthread on the libgettextlib link line even with
# --enable-threads=win32.
BuildRequires: ucrtarm64-winpthreads
# win-iconv ships no pkg-config file; gnulib's AM_ICONV finds it by link
# probe out of the sysroot, as for mingw32/mingw64.
BuildRequires: ucrtarm64-win-iconv
# No ucrtarm64-termcap: there is no termcap/ncurses port for this target.
# libtextstyle's terminfo probe is allowed to fail; no installed file changes.

# Possible extra BRs.  These are used if available, but
# not required just for building.
#BuildRequires: mingw32-dlfcn
#BuildRequires: mingw32-libxml2
#BuildRequires: mingw32-expat
#BuildRequires: mingw32-glib2


%description
MinGW Windows Gettext library


# Win32
%package -n mingw32-gettext-libs
Summary:         Runtime libintl for the win32 target

%description -n mingw32-gettext-libs
The gettext runtime DLL (libintl-8.dll) for the win32 target, split out so
that a package whose DLLs only need libintl does not drag in the gettext
tools and their GNU runtime dependencies (the Fedora native gettext-libs
precedent).

%package -n mingw32-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages
Requires:        mingw32-gettext-libs = %{version}-%{release}

%description -n mingw32-gettext
MinGW Windows Gettext library

%package -n mingw32-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       mingw32-gettext = %{version}-%{release}

%description -n mingw32-gettext-static
Static version of the MinGW Windows Gettext library.

# Win64
%package -n mingw64-gettext-libs
Summary:         Runtime libintl for the win64 target

%description -n mingw64-gettext-libs
The gettext runtime DLL (libintl-8.dll) for the win64 target, split out so
that a package whose DLLs only need libintl does not drag in the gettext
tools and their GNU runtime dependencies (the Fedora native gettext-libs
precedent).

%package -n mingw64-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages
Requires:        mingw64-gettext-libs = %{version}-%{release}

%description -n mingw64-gettext
MinGW Windows Gettext library

%package -n mingw64-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       mingw64-gettext = %{version}-%{release}

%description -n mingw64-gettext-static
Static version of the MinGW Windows Gettext library.

# Windows on ARM64
%package -n ucrtarm64-gettext-libs
Summary:         Runtime libintl for the Windows on ARM64 target

%description -n ucrtarm64-gettext-libs
The gettext runtime DLL (libintl-8.dll) for the aarch64-w64-mingw32 target,
split out so that a package whose DLLs only need libintl does not drag in
the gettext tools (the Fedora native gettext-libs precedent).

%package -n ucrtarm64-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages
Requires:        ucrtarm64-gettext-libs = %{version}-%{release}

%description -n ucrtarm64-gettext
MinGW Windows Gettext library for the Windows on ARM64 target.

%package -n ucrtarm64-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       ucrtarm64-gettext = %{version}-%{release}

%description -n ucrtarm64-gettext-static
Static version of the MinGW Windows Gettext library for the Windows on ARM64
target.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n gettext-%{version}

%build
# pass_all for ucrtarm64 only: libtool's func_win32_libid file-magic test
# predates AArch64 PE, rejects every import library, and with -no-undefined
# silently degrades all the DLLs to static-only.  A plain argument reaches
# the sub-configures through ac_configure_args; %%check asserts the result.
UCRTARM64_CONFIGURE_ARGS="lt_cv_deplibs_check_method=pass_all"
# The clang columns supply CC; C++ stays on g++ with the gcc-flavoured
# flags (the clang cflags carry -Qunused-arguments, which g++ rejects).
MINGW32_CXX=i686-w64-mingw32-g++
MINGW64_CXX=x86_64-w64-mingw32-g++
MINGW32_CXXFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions --param=ssp-buffer-size=4"
MINGW64_CXXFLAGS="$MINGW32_CXXFLAGS"
%mingw_configure            \
    --disable-java          \
    --disable-native-java   \
    --disable-csharp        \
    --enable-static         \
    --enable-threads=win32  \
    --without-emacs         \
    --disable-openmp
%mingw_make_build


%install
%mingw_make_install

rm -f %{buildroot}%{mingw32_datadir}/locale/locale.alias
rm -f %{buildroot}%{mingw32_libdir}/charset.alias

rm -f %{buildroot}%{mingw64_datadir}/locale/locale.alias
rm -f %{buildroot}%{mingw64_libdir}/charset.alias

rm -f %{buildroot}%{ucrtarm64_datadir}/locale/locale.alias
rm -f %{buildroot}%{ucrtarm64_libdir}/charset.alias

# Remove documentation - already available in base gettext-devel.
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw32_docdir}
rm -rf %{buildroot}%{mingw32_infodir}

rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{mingw64_docdir}
rm -rf %{buildroot}%{mingw64_infodir}

rm -rf %{buildroot}%{ucrtarm64_mandir}
rm -rf %{buildroot}%{ucrtarm64_docdir}
rm -rf %{buildroot}%{ucrtarm64_infodir}

# Drop some useless tools
rm -rf %{buildroot}%{mingw32_libdir}/gettext
rm -rf %{buildroot}%{mingw64_libdir}/gettext
rm -rf %{buildroot}%{ucrtarm64_libdir}/gettext

# Drop all .la files and .a files
find %{buildroot} -name "*.la" -delete
rm %{buildroot}%{mingw32_libdir}/libgettextlib.a
rm %{buildroot}%{mingw32_libdir}/libgettextsrc.a
rm %{buildroot}%{mingw64_libdir}/libgettextlib.a
rm %{buildroot}%{mingw64_libdir}/libgettextsrc.a
rm %{buildroot}%{ucrtarm64_libdir}/libgettextlib.a
rm %{buildroot}%{ucrtarm64_libdir}/libgettextsrc.a

# Drop javaversion.class since it's a binary blob (RHBZ#2294881)
rm %{buildroot}%{mingw32_datadir}/gettext/javaversion.class
rm %{buildroot}%{mingw64_datadir}/gettext/javaversion.class
rm %{buildroot}%{ucrtarm64_datadir}/gettext/javaversion.class

%mingw_find_lang %{name} --all-name


%check
# Verify the ucrtarm64 output with the llvm-* tools only: GNU nm/ar/objdump
# silently mis-read AArch64 PE/COFF.  %%check runs after the BRP passes.

# 1. libtool exports through a generated .def on every Windows host, so
#    lld's missing --version-script never comes up; assert that positively
#    and negatively on every generated libtool.  with_gnu_ld is yes here
#    (ld.lld announces GNU compatibility), so the guard is not vacuous.
#    The pass_all override from %%build is a configure cache variable, and a
#    sub-configure that did not inherit it would fail silently; assert it in
#    each script too.
lts=$(find build_ucrtarm64 -name libtool -type f | sort)
echo "ucrtarm64 libtool scripts:"; echo "$lts"
test -n "$lts"
for lt in $lts ; do
    # Variables are quoted and repeated per language tag: strip the quotes,
    # require that some copy says yes and none says no.
    gnuld=$(sed -n 's/^with_gnu_ld=//p' "$lt" | tr -d '"')
    echo "$lt: with_gnu_ld=[$gnuld]"
    echo "$gnuld" | grep -qx yes
    ! echo "$gnuld" | grep -qx no
    grep -q 'soname\.def' "$lt"
    ! grep -q 'version-script' "$lt"
    dcm=$(sed -n 's/^deplibs_check_method=//p' "$lt" | tr -d '"')
    echo "$lt: deplibs_check_method=[$dcm]"
    echo "$dcm" | grep -qx pass_all
    ! echo "$dcm" | grep -q file_magic
done
# ... and a GNU-ld target's libtool matches the same positive pattern, which is
# what proves the greps above cannot pass on a renamed or missing variable.
gnult=$(find build_win64 -name libtool -type f | sort | head -n 1)
echo "GNU-ld reference libtool: $gnult"
test -n "$gnult"
grep -q 'soname\.def' "$gnult"
# The mingw64 target keeps stock libtool's file-magic check -- proof both that
# the pass_all greps above are not matching some string every libtool contains,
# and that the override stayed confined to this one target.
grep -q '^deplibs_check_method=.*file_magic' "$gnult"

# 2. Every PE this target ships is a Windows ARM64 one, and the DLL set is the
#    same set the mingw32/mingw64 subpackages ship.  A missing DLL here would
#    otherwise only surface as an unresolvable dependency in glib2's build.
for d in libasprintf-0.dll libgettextlib-1-0.dll libgettextpo-0.dll \
         libgettextsrc-1-0.dll libintl-8.dll libtextstyle-0.dll ; do
    test -f %{buildroot}%{ucrtarm64_bindir}/$d
done
for f in %{buildroot}%{ucrtarm64_bindir}/*.dll \
         %{buildroot}%{ucrtarm64_bindir}/*.exe \
         %{buildroot}%{ucrtarm64_libexecdir}/gettext/*.exe ; do
    %{ucrtarm64_objdump} -f "$f" | grep -q 'file format coff-arm64'
    # ... and the debug info really was split out; without
    # %%mingw_debug_package every DLL ships unstripped, silently.
    %{ucrtarm64_objdump} -h "$f" | grep -q 'gnu_debuglink'
    test -f %{buildroot}%{_prefix}/lib/debug"${f#%{buildroot}}".debug
done

# 3. Every shipped archive -- static and import alike -- still carries its ar
#    symbol index, and its members are ARM64 COFF.
for a in %{buildroot}%{ucrtarm64_libdir}/*.a ; do
    magic=$(od -A n -t x1 -N 10 "$a" | tr -d ' \n')
    n=$(%{ucrtarm64_nm} --print-armap "$a" | grep -c ' in ' || :)
    echo "archive $a: header $magic, $n indexed symbols"
    test "$magic" = "213c617263683e0a2f20"
    test "$n" -gt 0
    %{ucrtarm64_objdump} -f "$a" | grep -q 'file format coff-arm64'
    ! %{ucrtarm64_objdump} -f "$a" \
        | grep -E 'file format (coff-i386|coff-x86-64|elf)'
done
# ... and libintl in particular resolves the entry point everything downstream
# calls.  gettext renames the public API to libintl_* on Windows (libintl.h
# redirects gettext -> libintl_gettext), so that is the name that has to be in
# the index of both the static library and the import library.
for a in %{buildroot}%{ucrtarm64_libdir}/libintl.a \
         %{buildroot}%{ucrtarm64_libdir}/libintl.dll.a ; do
    %{ucrtarm64_nm} --print-armap "$a" \
        | awk '$1 == "libintl_gettext" && $2 == "in" { found = 1 } END { exit !found }'
done

# 4. Link test: a real libintl consumer -- which is what glib2 is -- has to
#    compile and link against exactly what is about to be packaged, both against
#    the import library and statically.  The executables cannot be run here, so
#    only the link, the resulting file format and the imports are checked.
armcheck=%{_builddir}/ucrtarm64-gettext-check
rm -rf $armcheck
mkdir -p $armcheck
cat > $armcheck/t.c <<'EOF'
#include <libintl.h>
#include <stdio.h>
#include <string.h>

int main (void)
{
  const char *s;

  if (bindtextdomain ("hello", ".") == NULL)
    return 1;
  if (textdomain ("hello") == NULL)
    return 1;
  s = gettext ("Hello, world!");
  printf ("%%s\n", s);
  return strcmp (s, "Hello, world!") == 0 ? 0 : 1;
}
EOF

# Shared: -lintl resolves to libintl.dll.a -> libintl-8.dll.
%{ucrtarm64_cc} -I%{buildroot}%{ucrtarm64_includedir} $armcheck/t.c \
    -L%{buildroot}%{ucrtarm64_libdir} -lintl -o $armcheck/t.exe
%{ucrtarm64_objdump} -f $armcheck/t.exe
%{ucrtarm64_objdump} -f $armcheck/t.exe | grep -q 'file format coff-arm64'
%{ucrtarm64_objdump} -p $armcheck/t.exe | grep -i 'libintl-8.dll'

# Static: the same program against ucrtarm64-gettext-static, which must not end
# up importing the DLL.  libintl.a pulls in iconv, which stays shared here.
%{ucrtarm64_cc} -I%{buildroot}%{ucrtarm64_includedir} $armcheck/t.c \
    -L%{buildroot}%{ucrtarm64_libdir} -Wl,-Bstatic -lintl -Wl,-Bdynamic \
    -liconv -o $armcheck/t-static.exe
%{ucrtarm64_objdump} -f $armcheck/t-static.exe
%{ucrtarm64_objdump} -f $armcheck/t-static.exe | grep -q 'file format coff-arm64'
! %{ucrtarm64_objdump} -p $armcheck/t-static.exe | grep -i 'libintl-8.dll'

# 5. libintl-8.dll is the one gettext DLL the qemu-ga MSI ships, from clang
#    toolchain sysroots where the GNU runtime DLLs do not exist: it must be
#    clang-linked and import no libgcc, libssp or libunwind.  The other x86
#    DLLs stay g++-linked (see %%build) and keep their libstdc++/libgcc
#    imports, which is why libintl lives in the -libs subpackage.  The same
#    consumer links through the clang drivers.
for t in i686-w64-mingw32 x86_64-w64-mingw32 ; do
  case $t in
    i686-*)
      wbin_rel=%{mingw32_bindir}
      wlibdir=%{buildroot}%{mingw32_libdir}
      wincdir=%{buildroot}%{mingw32_includedir}
      peformat=pei-i386
      ;;
    x86_64-*)
      wbin_rel=%{mingw64_bindir}
      wlibdir=%{buildroot}%{mingw64_libdir}
      wincdir=%{buildroot}%{mingw64_includedir}
      peformat=pei-x86-64
      ;;
  esac
  wbindir=%{buildroot}$wbin_rel

  $t-objdump -f $wbindir/libintl-8.dll | grep -q "file format $peformat"
  $t-objdump -h $wbindir/libintl-8.dll | grep -q '\.gnu_debuglink'
  test -f %{buildroot}%{_prefix}/lib/debug$wbin_rel/libintl-8.dll.debug
  imports=$($t-objdump -p $wbindir/libintl-8.dll | grep 'DLL Name' || :)
  echo "$t libintl-8.dll imports: $imports"
  if echo "$imports" | grep -qiE 'libgcc|libssp|libunwind|libstdc'; then
    echo "ERROR: $t libintl-8.dll imports a GNU runtime or unwinder DLL" >&2
    exit 1
  fi

  $t-clang -I$wincdir $armcheck/t.c -L$wlibdir -lintl -o $armcheck/t-$t.exe
  $t-objdump -f $armcheck/t-$t.exe | grep -q "file format $peformat"
  $t-objdump -p $armcheck/t-$t.exe | grep -i 'libintl-8.dll'
done

rm -rf $armcheck


# Win32
%files -n mingw32-gettext-libs
%license COPYING
%{mingw32_bindir}/libintl-8.dll

%files -n mingw32-gettext -f mingw32-%{name}.lang
%license COPYING
%{mingw32_bindir}/autopoint
%{mingw32_bindir}/envsubst.exe
%{mingw32_bindir}/gettext.exe
%{mingw32_bindir}/gettext.sh
%{mingw32_bindir}/gettextize
%{mingw32_bindir}/libasprintf-0.dll
%{mingw32_bindir}/libgettextlib-1-0.dll
%{mingw32_bindir}/libgettextpo-0.dll
%{mingw32_bindir}/libgettextsrc-1-0.dll
%{mingw32_bindir}/libtextstyle-0.dll
%{mingw32_bindir}/msg*.exe
%{mingw32_bindir}/ngettext.exe
%{mingw32_bindir}/po-fetch
%{mingw32_bindir}/printf_gettext.exe
%{mingw32_bindir}/printf_ngettext.exe
%{mingw32_bindir}/recode-sr-latin.exe
%{mingw32_bindir}/spit
%{mingw32_bindir}/xgettext.exe
%{mingw32_includedir}/autosprintf.h
%{mingw32_includedir}/gettext-po.h
%{mingw32_includedir}/libintl.h
%{mingw32_includedir}/textstyle.h
%{mingw32_includedir}/textstyle/version.h
%{mingw32_includedir}/textstyle/woe32dll.h
%{mingw32_libdir}/libasprintf.dll.a
%{mingw32_libdir}/libgettextlib.dll.a
%{mingw32_libdir}/libgettextpo.dll.a
%{mingw32_libdir}/libgettextsrc.dll.a
%{mingw32_libdir}/libintl.dll.a
%{mingw32_libdir}/libtextstyle.dll.a
%dir %{mingw32_libexecdir}/gettext/
%{mingw32_libexecdir}/gettext/cldr-plurals.exe
%{mingw32_libexecdir}/gettext/hostname.exe
%{mingw32_libexecdir}/gettext/project-id
%{mingw32_libexecdir}/gettext/urlget.exe
%{mingw32_libexecdir}/gettext/user-email
%{mingw32_datadir}/gettext/
%{mingw32_datadir}/gettext-%{version}/
%{mingw32_datadir}/aclocal/nls.m4

%files -n mingw32-gettext-static
%{mingw32_libdir}/libasprintf.a
%{mingw32_libdir}/libgettextpo.a
%{mingw32_libdir}/libintl.a
%{mingw32_libdir}/libtextstyle.a

# Win64
%files -n mingw64-gettext-libs
%license COPYING
%{mingw64_bindir}/libintl-8.dll

%files -n mingw64-gettext -f mingw64-%{name}.lang
%license COPYING
%{mingw64_bindir}/autopoint
%{mingw64_bindir}/envsubst.exe
%{mingw64_bindir}/gettext.exe
%{mingw64_bindir}/gettext.sh
%{mingw64_bindir}/gettextize
%{mingw64_bindir}/libasprintf-0.dll
%{mingw64_bindir}/libgettextlib-1-0.dll
%{mingw64_bindir}/libgettextpo-0.dll
%{mingw64_bindir}/libgettextsrc-1-0.dll
%{mingw64_bindir}/libtextstyle-0.dll
%{mingw64_bindir}/msg*.exe
%{mingw64_bindir}/ngettext.exe
%{mingw64_bindir}/po-fetch
%{mingw64_bindir}/printf_gettext.exe
%{mingw64_bindir}/printf_ngettext.exe
%{mingw64_bindir}/recode-sr-latin.exe
%{mingw64_bindir}/spit
%{mingw64_bindir}/xgettext.exe
%{mingw64_includedir}/autosprintf.h
%{mingw64_includedir}/gettext-po.h
%{mingw64_includedir}/libintl.h
%{mingw64_includedir}/textstyle.h
%{mingw64_includedir}/textstyle/version.h
%{mingw64_includedir}/textstyle/woe32dll.h
%{mingw64_libdir}/libasprintf.dll.a
%{mingw64_libdir}/libgettextlib.dll.a
%{mingw64_libdir}/libgettextpo.dll.a
%{mingw64_libdir}/libgettextsrc.dll.a
%{mingw64_libdir}/libintl.dll.a
%{mingw64_libdir}/libtextstyle.dll.a
%dir %{mingw64_libexecdir}/gettext/
%{mingw64_libexecdir}/gettext/cldr-plurals.exe
%{mingw64_libexecdir}/gettext/hostname.exe
%{mingw64_libexecdir}/gettext/project-id
%{mingw64_libexecdir}/gettext/urlget.exe
%{mingw64_libexecdir}/gettext/user-email
%{mingw64_datadir}/gettext/
%{mingw64_datadir}/gettext-%{version}/
%{mingw64_datadir}/aclocal/nls.m4

%files -n mingw64-gettext-static
%{mingw64_libdir}/libasprintf.a
%{mingw64_libdir}/libgettextpo.a
%{mingw64_libdir}/libintl.a
%{mingw64_libdir}/libtextstyle.a

# Windows on ARM64
%files -n ucrtarm64-gettext-libs
%license COPYING
%{ucrtarm64_bindir}/libintl-8.dll

%files -n ucrtarm64-gettext -f ucrtarm64-%{name}.lang
%license COPYING
%{ucrtarm64_bindir}/autopoint
%{ucrtarm64_bindir}/envsubst.exe
%{ucrtarm64_bindir}/gettext.exe
%{ucrtarm64_bindir}/gettext.sh
%{ucrtarm64_bindir}/gettextize
%{ucrtarm64_bindir}/libasprintf-0.dll
%{ucrtarm64_bindir}/libgettextlib-1-0.dll
%{ucrtarm64_bindir}/libgettextpo-0.dll
%{ucrtarm64_bindir}/libgettextsrc-1-0.dll
%{ucrtarm64_bindir}/libtextstyle-0.dll
%{ucrtarm64_bindir}/msg*.exe
%{ucrtarm64_bindir}/ngettext.exe
%{ucrtarm64_bindir}/po-fetch
%{ucrtarm64_bindir}/printf_gettext.exe
%{ucrtarm64_bindir}/printf_ngettext.exe
%{ucrtarm64_bindir}/recode-sr-latin.exe
%{ucrtarm64_bindir}/spit
%{ucrtarm64_bindir}/xgettext.exe
%{ucrtarm64_includedir}/autosprintf.h
%{ucrtarm64_includedir}/gettext-po.h
%{ucrtarm64_includedir}/libintl.h
%{ucrtarm64_includedir}/textstyle.h
%{ucrtarm64_includedir}/textstyle/version.h
%{ucrtarm64_includedir}/textstyle/woe32dll.h
%{ucrtarm64_libdir}/libasprintf.dll.a
%{ucrtarm64_libdir}/libgettextlib.dll.a
%{ucrtarm64_libdir}/libgettextpo.dll.a
%{ucrtarm64_libdir}/libgettextsrc.dll.a
%{ucrtarm64_libdir}/libintl.dll.a
%{ucrtarm64_libdir}/libtextstyle.dll.a
%dir %{ucrtarm64_libexecdir}/gettext/
%{ucrtarm64_libexecdir}/gettext/cldr-plurals.exe
%{ucrtarm64_libexecdir}/gettext/hostname.exe
%{ucrtarm64_libexecdir}/gettext/project-id
%{ucrtarm64_libexecdir}/gettext/urlget.exe
%{ucrtarm64_libexecdir}/gettext/user-email
%{ucrtarm64_datadir}/gettext/
%{ucrtarm64_datadir}/gettext-%{version}/
%{ucrtarm64_datadir}/aclocal/nls.m4

%files -n ucrtarm64-gettext-static
%{ucrtarm64_libdir}/libasprintf.a
%{ucrtarm64_libdir}/libgettextpo.a
%{ucrtarm64_libdir}/libintl.a
%{ucrtarm64_libdir}/libtextstyle.a


%changelog
* Mon Aug 24 2026 Erik Berg <fedora@slipsprogrammor.no> - 1.0-2.2
- Build the win32/win64 C halves with the clang supplement drivers, so
  libintl-8.dll (the one gettext DLL the qemu-ga MSI ships) carries no
  GNU runtime imports; the C++ parts stay on g++ and libstdc++, as no
  libc++ is packaged for these targets
- Split libintl-8.dll into per-target -libs subpackages (the Fedora
  native gettext-libs precedent): the tools DLLs import libgcc, so a
  package whose DLLs only need libintl no longer drags mingw-gcc into
  its install closure

* Thu Aug 06 2026 Erik Berg <fedora@slipsprogrammor.no> - 1.0-2.1
- Add gettext for the Windows on ARM64 target

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Sun Apr 12 2026 Sandro Mani <manisandro@gmail.com> - 1.0-1
- Update to 1.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Aug 27 2025 Sandro Mani <manisandro@gmail.com> - 0.26-1
- Update to 0.26

* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 0.25.1-1
- Update to 0.25.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 16 2025 Sandro Mani <manisandro@gmail.com> - 0.25-1
- Update to 0.25

* Tue Mar 11 2025 Sandro Mani <manisandro@gmail.com> - 0.24-1
- Update to 0.24

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Sandro Mani <manisandro@gmail.com> - 0.23.1-1
- Update to 0.23.1

* Wed Dec 18 2024 Sandro Mani <manisandro@gmail.com> - 0.23-1
- Update to 0.23

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Richard W.M. Jones <rjones@redhat.com> - 0.22.5-2
- Drop javaversion.class files (RHBZ#2294881)

* Mon Mar 04 2024 Sandro Mani <manisandro@gmail.com> - 0.22.5-1
- Update to 0.22.5

* Thu Feb 15 2024 Sandro Mani <manisandro@gmail.com> - 0.22.4-1
- Update to 0.22.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Sandro Mani <manisandro@gmail.com> - 0.22-1
- Update to 0.22

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 20 2022 Sandro Mani <manisandro@gmail.com> - 0.21.1-1
- Update to 0.21.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.21-5
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Sandro Mani <manisandro@gmail.com> - 0.21.0-1
- Update to 0.21.0

* Tue Jul 28 2020 Sandro Mani <manisandro@gmail.com> - 0.20.2-3
- Add gettext-printf_collision.patch

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Sandro Mani <manisandro@gmail.com> - 0.20.2-1
- Update to 0.20.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0.20.1-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 0.20.1-1
- Update the sources accordingly to its native counter part, rhbz#1740721

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 0.19.7-1
- Update to 0.19.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.19.4-1
- Update to 0.19.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 0.18.3.2-1
- Update to 0.18.3.2

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.3.1-1
- Update to 0.18.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.3-1
- Update to 0.18.3
- Dropped upstreamed patch

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-3
- Fix FTBFS due to invalid use of cdecl

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Sat May  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-1
- Update to 0.18.2.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2-1
- Update to 0.18.2
- Removed all hacks as they're not needed any more

* Thu Dec  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-11
- Fix the build on RHEL6 (too old libtool)
- Minor cleanup

* Sun Jul 22 2012 Kalev Lember <kalevlember@gmail.com> - 0.18.1.1-10
- Fix message catalog split to subpackages (#842166)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-8
- Added win64 support

* Thu Mar 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-7
- Dropped .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-6
- Renamed the source package to mingw-gettext (RHBZ #800387)
- Use mingw macros without leading underscore

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

* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-3
- Remove static libraries.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
