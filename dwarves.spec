%define soname 1
%define libname %mklibname dwarves %{soname}

Name: dwarves
Version: 1.7
Release: %mkrel 2
License: GPLv2
Summary: Dwarf Tools
Group: Development/Other
URL: http://oops.ghostprotocols.net:81/blog
Source: http://fedorapeople.org/~acme/dwarves/dwarves-%{version}.tar.bz2
BuildRequires: cmake
BuildRequires: elfutils-static-devel
BuildRoot: %{_tmppath}/%{name}-buildroot

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
%setup -q -c -n %{name}-%{version}

%build
cmake \
	-D__LIB=%{_lib} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE="MinSizeRel" .
%make

%install
rm -Rf %{buildroot}

make DESTDIR=%{buildroot} install

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README.ctracer
%defattr(0755,root,root,0755)
%{_bindir}/codiff
%{_bindir}/ctracer
%{_bindir}/dtagnames
%{_bindir}/ostra-cg
%{_bindir}/pahole
%{_bindir}/pdwtags
%{_bindir}/pfunct
%{_bindir}/pglobal
%{_bindir}/prefcnt
%{_bindir}/syscse
%dir %{_datadir}/dwarves/runtime/
%dir %{_datadir}/dwarves/runtime/python/
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
%{_includedir}/dwarves.h
%{_includedir}/dwarves_emit.h
%{_includedir}/dwarves_reorganize.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_emit.so
%{_libdir}/lib%{name}_reorganize.so
