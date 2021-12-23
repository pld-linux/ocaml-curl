#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define debug_package %{nil}
%define	pkgname	curl
Summary:	OCaml Curl library (ocurl)
Summary(pl.UTF-8):	Biblioteka Curl dla OCamla (ocurl)
Name:		ocaml-%{pkgname}
Version:	0.9.1
Release:	4
License:	MIT
Group:		Libraries
Source0:	https://github.com/ygrek/ocurl/releases/download/%{version}/ocurl-%{version}.tar.gz
# Source0-md5:	1ff6b12803fa0c6e9a4358dd29b83910
Patch0:		ocaml_opt.patch
URL:		http://ocurl.forge.ocamlcore.org/
BuildRequires:	curl-devel >= 7.12.0
BuildRequires:	gawk
BuildRequires:	ocaml >= 3.10.0-7
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-lwt-devel
BuildRequires:	ocaml-lwt-ppx-devel
# Explicitly require Curl (fixes RHBZ#711261). Since ocaml-curl uses
# -custom rather than ocamlmklib, automatic detection is infeasible.
Requires:	curl-devel >= 7.12.0
%requires_eq	ocaml-runtime
ExcludeArch:	sparc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Ocaml Curl Library (Ocurl) is an interface library for the
programming language Ocaml to the networking library libcurl.

%description -l pl.UTF-8
Biblioteka Ocaml Curl (Ocurl) to biblioteka interfejsu języka
programowania Ocaml do biblioteki sieciowe libcurl.

%package devel
Summary:	OCaml Curl library (ocurl) - development part
Summary(pl.UTF-8):	Biblioteka Curl dla OCamla (ocurl) - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and signature files for developing
applications that use OCaml Curl library.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
z użyciem biblioteki OCamla Curl.

%prep
%setup -q -n ocurl-%{version}
%patch0 -p1

%build
%configure
%{__make} -j1 all

%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Install curl.mli
cp -p curl.mli $OCAMLFIND_DESTDIR/curl

cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/curl/META <<EOF
requires = ""
version = "%{version}"
directory = "+curl"
archive(byte) = "curl.cma"
archive(native) = "curl.cmxa"
linkopts = ""
EOF

# Make clean in the examples dir so our docs don't contain binaries.
%{__make} -C examples clean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%dir %{_libdir}/ocaml/curl
%{_libdir}/ocaml/curl/META
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcurl-helper.so
%{_libdir}/ocaml/stublibs/dllcurl-helper.so.owner
%{_libdir}/ocaml/curl/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/curl/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc examples/*
%{_libdir}/ocaml/curl/*.a
%{_libdir}/ocaml/curl/*.cmi
%{_libdir}/ocaml/curl/*.cmo
%{_libdir}/ocaml/curl/*.cmt
%{_libdir}/ocaml/curl/*.cmti
%if %{with ocaml_opt}
%{_libdir}/ocaml/curl/*.cmx
%{_libdir}/ocaml/curl/*.cmxa
%endif
%{_libdir}/ocaml/curl/*.mli
