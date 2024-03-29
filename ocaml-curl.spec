#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define debug_package %{nil}

Summary:	OCaml Curl library (ocurl)
Summary(pl.UTF-8):	Biblioteka Curl dla OCamla (ocurl)
Name:		ocaml-curl
Version:	0.9.1
Release:	5
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ygrek/ocurl/releases
Source0:	https://github.com/ygrek/ocurl/releases/download/%{version}/ocurl-%{version}.tar.gz
# Source0-md5:	1ff6b12803fa0c6e9a4358dd29b83910
Patch0:		ocaml_opt.patch
Patch1:		%{name}-sh.patch
URL:		https://ygrek.org/p/ocurl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	curl-devel >= 7.28.0
BuildRequires:	gawk
BuildRequires:	ocaml >= 3.10.0-7
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-lwt-devel
BuildRequires:	ocaml-lwt-ppx-devel
BuildRequires:	pkgconfig
# Explicitly require Curl (fixes RHBZ#711261). Since ocaml-curl uses
# -custom rather than ocamlmklib, automatic detection is infeasible.
Requires:	curl-devel >= 7.28.0
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

%package lwt
Summary:	Lwt support for OCaml Curl library
Summary(pl.UTF-8):	Obsługa Lwt do biblioteki OCamla Curl
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-lwt

%description lwt
Lwt support for OCaml Curl library.

%description lwt -l pl.UTF-8
Obsługa Lwt do biblioteki OCamla Curl.

%package lwt-devel
Summary:	Lwt support for OCaml Curl library - development part
Summary(pl.UTF-8):	Obsługa Lwt do biblioteki OCamla Curl - część programistyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-lwt = %{version}-%{release}
Requires:	ocaml-lwt-devel

%description lwt-devel
This package contains libraries and signature files for developing
applications that use OCaml curl-lwt library.

%description lwt-devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
z użyciem biblioteki OCamla curl-lwt.

%prep
%setup -q -n ocurl-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure
%{__make} -j1 all

%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# useless in rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so.owner

# Make clean in the examples dir so our docs don't contain binaries.
%{__make} -C examples clean
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%dir %{_libdir}/ocaml/curl
%{_libdir}/ocaml/curl/META
%{_libdir}/ocaml/curl/curl.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/curl/curl.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcurl-helper.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/curl/libcurl-helper.a
%{_libdir}/ocaml/curl/curl.cmi
%{_libdir}/ocaml/curl/curl.cmt
%{_libdir}/ocaml/curl/curl.cmti
%{_libdir}/ocaml/curl/curl.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/curl/curl.a
%{_libdir}/ocaml/curl/curl.cmx
%{_libdir}/ocaml/curl/curl.cmxa
%endif
%{_examplesdir}/%{name}-%{version}

%files lwt
%defattr(644,root,root,755)
# without ocaml_opt: just stub package to collect dependencies
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/curl/curl_lwt.cmxs
%endif

%files lwt-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/curl/curl_lwt.cmi
%{_libdir}/ocaml/curl/curl_lwt.cmo
%{_libdir}/ocaml/curl/curl_lwt.cmt
%{_libdir}/ocaml/curl/curl_lwt.cmti
%{_libdir}/ocaml/curl/curl_lwt.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/curl/curl_lwt.cmx
%{_libdir}/ocaml/curl/curl_lwt.o
%endif
