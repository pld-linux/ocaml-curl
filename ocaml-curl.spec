#
# Conditional build:
%bcond_with	opt		# build opt

%define debug_package %{nil}
%define	pkgname	curl
Summary:	OCaml Curl library (ocurl)
Name:		ocaml-%{pkgname}
Version:	0.6.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://forge.ocamlcore.org/frs/download.php/1374/ocurl-%{version}.tar.gz
# Source0-md5:	637336f41eb047b246e30a4c3caddc94
URL:		http://ocurl.forge.ocamlcore.org/
BuildRequires:	curl-devel >= 7.12.0
BuildRequires:	gawk
BuildRequires:	ocaml >= 3.10.0-7
BuildRequires:	ocaml-findlib-devel
# Explicitly require Curl (fixes RHBZ#711261). Since ocaml-curl uses
# -custom rather than ocamlmklib, automatic detection is infeasible.
Requires:	curl-devel >= 7.12.0
ExcludeArch:	sparc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Ocaml Curl Library (Ocurl) is an interface library for the
programming language Ocaml to the networking library libcurl.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocurl-%{version}

%build
%configure
%{__make} -j1 all \
%if %{with opt}
	OCBYTE="ocamlc.opt -g" \
	OCOPT="ocamlopt.opt -g"
%endif

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Install curl.mli
cp -p curl.mli $OCAMLFIND_DESTDIR/curl

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/curl
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/curl/META <<EOF
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
%{_libdir}/ocaml/curl
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcurl-helper.so
%{_libdir}/ocaml/stublibs/dllcurl-helper.so.owner
%if %{with opt}
%exclude %{_libdir}/ocaml/curl/*.a
%exclude %{_libdir}/ocaml/curl/*.o
%exclude %{_libdir}/ocaml/curl/*.cmx
%exclude %{_libdir}/ocaml/curl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/curl/*.mli

%files devel
%defattr(644,root,root,755)
%doc examples/*
%if %{with opt}
%{_libdir}/ocaml/curl/*.a
%{_libdir}/ocaml/curl/*.o
%{_libdir}/ocaml/curl/*.cmx
%{_libdir}/ocaml/curl/*.cmxa
%endif
%{_libdir}/ocaml/curl/*.mli
%{_libdir}/ocaml/site-lib/curl
