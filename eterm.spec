%define oname	Eterm
%define version 0.9.5
%define release %mkrel 16

# this situation is similar to Berkeley DB
%define major	%{version}
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Terminal emulator
Name:		eterm
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Terminals
URL:		http://eterm.sourceforge.net/
Source0:	http://www.eterm.org/download/%{oname}-%{version}.tar.gz
Source5:	http://www.eterm.org/download/%{oname}-bg-%{version}.tar.gz

BuildRequires:	imlib2-devel
BuildRequires:	libast-devel >= 0.5
BuildRequires:	utempter-devel
BuildRequires:	libx11-devel twin-devel
BuildRequires:	libxres-devel
BuildRequires:	libxext-devel
BuildRequires:	libxmu-devel
BuildRequires:  groff-for-man man
BuildRequires:	gdb
Requires(pre):	ncurses
# needed by Etbg_update_list script
Requires(post):	diffutils
Conflicts:	ncurses-extraterms
Provides:	%{oname} = %{version}-%{release}
Obsoletes:	%{oname} < 0.9.5-13

%description
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any window manager/desktop environment, although it is designed
to work and integrate best with Enlightenment.

%package -n %{libname}
Summary:	Library from Eterm (Enlightened Terminal Emulator)
Group:		Terminals
Obsoletes:	%{mklibname Eterm 0.9.5} < 0.9.5-13
Provides:	%{mklibname Eterm 0.9.5} = %{version}-%{release}

%description -n	%{libname}
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any window manager/desktop environment, although it is designed
to work and integrate best with Enlightenment.

This library is essential for Eterm to work.

%package -n %{devname}
Summary:	Devel files for Eterm
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{oname}-devel < 0.9.5-13
Obsoletes:	%{mklibname -d -s Eterm} < 0.9.5-13
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{devname}
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any window manager/desktop environment, although it is designed
to work and integrate best with Enlightenment.

This package provides the necessary development libraries and include files
to allow you to develop or compile programs that needs Eterm, though no such
program has existed so far.

%prep
%setup -q -a5 -n %{oname}-%{version}

# patch1 also sets $TERM = xterm for all themes,
# do that here since patch1 is not applied
find themes/ -name 'theme.cfg.in' -print0 | xargs -0 -r perl -pi -e 's/term_name Eterm/term_name xterm/'

%build
%configure2_5x \
  --enable-etwin \
  --enable-escreen-fx \
  --enable-profile \
  --enable-trans \
  --with-backspace=bs \
  --enable-mmx \
  --enable-utmp \
  --with-delete=execute \
  --enable-auto-encoding \
  --enable-multi-charset \
  --enable-xim \
  --enable-greek \
  --disable-static

%make

%install
rm -fr %{buildroot}
%makeinstall_std

# Install menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{_real_vendor}-%{name}.desktop << EOF
[Desktop Entry]
Name=Eterm
Comment=Enlightened Terminal Emulator
Exec=%{name}
Icon=terminals_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Terminals;System;TerminalEmulator;
EOF

mkdir -p %{buildroot}%{_datadir}/terminfo/E
tic -o %{buildroot}%{_datadir}/terminfo doc/Eterm.ti

#we don't want these
rm -rf %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post
update-alternatives --install /usr/bin/xvt xvt /usr/bin/Eterm 15
%{_bindir}/Etbg_update_list

%postun
[ "$1" = "0" ]&& update-alternatives --remove xvt /usr/bin/Eterm

%files
%defattr(-, root, root)
%doc ChangeLog README ReleaseNotes doc/Eterm_reference.html doc/README.Escreen
%{_bindir}/*
%dir %{_datadir}/Eterm
%config(noreplace) %{_datadir}/Eterm/themes
%{_datadir}/Eterm/pix
%{_mandir}/man1/Eterm.1.*
%{_datadir}/applications/mandriva-%name.desktop
%{_datadir}/%{oname}/gdb.scr
/%{_datadir}/terminfo/E/*

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib%{oname}-%{major}.so

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/lib%{oname}.so
