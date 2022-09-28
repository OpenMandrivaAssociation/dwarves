%define soname 1
%define libname %mklibname dwarves

Name: dwarves
Version: 1.24
Release: 1
License: GPLv2
Summary: Dwarf Tools
Group: Development/Other
URL: http://oops.ghostprotocols.net:81/blog
Source: http://fedorapeople.org/~acme/dwarves/dwarves-%{version}.tar.bz2
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: elfutils-static-devel

%description
dwarves is a set of tools that use the DWARF debugging information inserted in
ELF binaries by compilers such as GCC, used by well known debuggers such as
GDB, and more recent ones such as systemtap.

Utilities in the dwarves suite include pahole, that can be used to find
alignment holes in structs and classes in languages such as C, C++, but not
limited to these, and other information such as CPU cacheline alignment,
helping pack those structures to achieve more cache hits, codiff, a diff like
tool to compare the effects changes in source code generate on the resulting
binaries, pfunct, that can be used to find all sorts of information about
functions, inlines, decisions made by the compiler about inlining, etc.

%package -n %{libname}
Summary: DWARF processing library
Group: System/Libraries

%description -n %{libname}
DWARF processing library.

%package -n %{libname}-devel
Summary: DWARF processing library development files
Group: Development/C
Provides: dwarves-devel = %{version}-%{release}
Provides: libdwarves-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description -n %{libname}-devel
DWARF processing library development files.

%prep
%autosetup -p1
%cmake \
	-D__LIB=%{_lib} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%defattr(0644,root,root,0755)
%doc README.ctracer
%defattr(0755,root,root,0755)
%{_bindir}/btfdiff
%{_bindir}/codiff
%{_bindir}/ctracer
%{_bindir}/dtagnames
%{_bindir}/fullcircle
%{_bindir}/ostra-cg
%{_bindir}/pahole
%{_bindir}/pdwtags
%{_bindir}/pfunct
%{_bindir}/pglobal
%{_bindir}/prefcnt
%{_bindir}/scncopy
%{_bindir}/syscse
%dir %{_datadir}/dwarves
%dir %{_datadir}/dwarves/runtime
%dir %{_datadir}/dwarves/runtime/python
%defattr(0644,root,root,0755)
%{_datadir}/dwarves/runtime/Makefile
%{_datadir}/dwarves/runtime/ctracer_relay.c
%{_datadir}/dwarves/runtime/ctracer_relay.h
%{_datadir}/dwarves/runtime/linux.blacklist.cu
%attr(0755,root,root) %{_datadir}/dwarves/runtime/python/ostra.py*
%{_mandir}/man1/pahole.1*

%files -n %{libname}
%defattr(0644,root,root,0755)
%{_libdir}/lib%{name}.so.%{soname}*
%{_libdir}/lib%{name}_emit.so.%{soname}*
%{_libdir}/lib%{name}_reorganize.so.%{soname}*

%files -n %{libname}-devel
%defattr(0644,root,root,0755)
%doc MANIFEST README
%{_includedir}/dwarves
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_emit.so
%{_libdir}/lib%{name}_reorganize.so
