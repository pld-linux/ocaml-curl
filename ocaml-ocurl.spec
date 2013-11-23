#
# Conditional build:
%bcond_without	opt		# build opt

%define debug_package %{nil}
Summary:	OCaml Curl library (ocurl)
Name:		ocaml-curl
Version:	0.5.3
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ocurl/ocurl-%{version}.tgz
Patch1:		ocurl-0.5.3-include-o-cmx.patch
URL:		http://sourceforge.net/projects/ocurl
BuildRequires:	curl-devel >= 7.12.0
BuildRequires:	gawk
BuildRequires:	ocaml >= 3.10.0-7
BuildRequires:	ocaml-findlib-devel
ExcludeArch:	sparc64 s390 s390x
# Explicitly require Curl (fixes #711261). Since ocaml-curl uses
# -custom rather than ocamlmklib, automatic detection is infeasible.
Requires:	curl-devel >= 7.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Ocaml Curl Library (Ocurl) is an interface library for the
programming language Ocaml to the networking library libcurl.

%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -qc
mv ocurl/* .
%patch1 -p1

# Files in the archive have spurious +x mode.
find -type f | xargs chmod 0644
chmod 0755 configure install-sh

%build
%configure \
	--with-findlib

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

# Make clean in the examples dir so our docs don't contain binaries.
%{__make} -C examples clean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%{_libdir}/ocaml/curl
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
