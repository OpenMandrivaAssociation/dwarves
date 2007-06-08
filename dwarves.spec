%define libname libdwarves
%define libver 1

Name: dwarves
Version: 1.0
Release: 1
License: GPL
Summary: Dwarf Tools
Group: Development/Tools
URL: http://oops.ghostprotocols.net:81/blog
Source: http://http://userweb.kernel.org/~acme/dwarves/%{name}-%{version}.tar.bz2
BuildRequires: cmake
BuildRequires: elfutils-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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

%package -n %{libname}%{libver}
Summary: DWARF processing library
Group: Development/Libraries

%description -n %{libname}%{libver}
DWARF processing library

%package -n %{libname}%{libver}-devel
Summary: DWARF processing library development files
Group: Development/Libraries
Requires: %{libname}%{libver} = %{version}-%{release}

%description -n %{libname}%{libver}-devel
DWARF processing library development files

%prep
%setup -q -c -n %{name}-%{version}

%build
cmake -D__LIB=%{_lib} -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE="MinSizeRel" .
make %{?_smp_mflags}

%install
rm -Rf %{buildroot}

make DESTDIR=%{buildroot} install

%post -n %{libname}%{libver} -p /sbin/ldconfig

%postun -n %{libname}%{libver} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README.ctracer
%defattr(0755,root,root,0755)
%{_bindir}/codiff
%{_bindir}/ctracer
%{_bindir}/dtagnames
%{_bindir}/pahole
%{_bindir}/pdwtags
%{_bindir}/pfunct
%{_bindir}/pglobal
%{_bindir}/prefcnt
%{_bindir}/ostra-cg
%dir %{_datadir}/dwarves/runtime/
%dir %{_datadir}/dwarves/runtime/python/
%defattr(0644,root,root,0755)
%{_datadir}/dwarves/runtime/Makefile
%{_datadir}/dwarves/runtime/ctracer_jprobe.c
%{_datadir}/dwarves/runtime/ctracer_relay.c
%{_datadir}/dwarves/runtime/ctracer_relay.h
%attr(0755,root,root) %{_datadir}/dwarves/runtime/python/ostra.py*

%files -n %{libname}%{libver}
%defattr(0644,root,root,0755)
%{_libdir}/%{libname}.so.*
%{_libdir}/%{libname}_emit.so.*
%{_libdir}/%{libname}_reorganize.so.*

%files -n %{libname}%{libver}-devel
%defattr(0644,root,root,0755)
%doc MANIFEST README
%{_includedir}/dwarves.h
%{_includedir}/dwarves_emit.h
%{_includedir}/dwarves_reorganize.h
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}_emit.so
%{_libdir}/%{libname}_reorganize.so
