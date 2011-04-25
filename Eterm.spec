%define version 0.9.5
%define release %mkrel 12

# this situation is similar to Berkeley DB
%define libname %mklibname Eterm %{version}
%define staticlibname %mklibname -d -s Eterm

Summary:	Terminal emulator
Name:		Eterm
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Terminals
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://eterm.sourceforge.net/

Source0:	http://www.eterm.org/download/%{name}-%{version}.tar.bz2
Source5:	http://www.eterm.org/download/%{name}-bg-0.9.3.tar.bz2
Patch1:		Eterm-0.9.1-themefix.patch.bz2
Patch2:		Eterm-0.9.2-muttandirc-themes.patch.bz2
Patch3:		Eterm-0.9.3-no-freetype1.patch.bz2
Patch4:		Eterm-0.9.3-no-rpath.patch.bz2
Patch5:		Eterm-0.9.3-gcc4.patch.bz2
Patch6:		eterm_0.9.5_utf8_hack.patch	

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

%description
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any windowmanager/desktop environment, although it is designed
to work and integrate best with Enlightenment.


%package -n	%{libname}
Summary:	Library from Eterm (Enlightened Terminal Emulator)
Group:		Terminals

%description -n	%{libname}
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any windowmanager/desktop environment, although it is designed
to work and integrate best with Enlightenment.

This library is essential for Eterm to work.

%package -n %{staticlibname}
Summary:	Static Library from Eterm (Enlightened Terminal Emulator)
Group:		Terminals

%description -n	%{staticlibname}
Static Library from Eterm (Enlightened Terminal Emulator)

%package	devel
Summary:	Devel files for Eterm
Group:		Development/Other
Requires:	%{name} = %{version}

%description	devel
Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.
It is designed with a Freedom of Choice philosophy, leaving as much power,
flexibility, and freedom as possible in the hands of the user.

It is designed to look good and work well, but takes a feature-rich approach
rather than one of minimalism while still maintaining speed and efficiency.

It works on any windowmanager/desktop environment, although it is designed
to work and integrate best with Enlightenment.

This package provides the necessary development libraries and include files
to allow you to develop or compile programs that needs Eterm, though no such
program has existed so far.

%prep
%setup -q -a5
#patch1 -p1 
#%patch2 -p1
#%patch3 -p1 -b .no-ttf
#%patch4 -p1 -b .no-rpath
#%patch5 -p1 -b .gcc4
#%patch6 -p1

# need to regen all auto* stuff, for patches
#%__libtoolize -c -f
#AUTOMAKE=automake-1.9 ACLOCAL=aclocal-1.9 FORCE_AUTOCONF_2_5=1 autoreconf --force --install

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
  --enable-greek

%make


%install
rm -fr %buildroot
%makeinstall_std

# Install menu

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Eterm
Comment=Enlightened Terminal Emulator
Exec=%{name}
Icon=terminals_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;;
EOF

mkdir -p %buildroot/%{_datadir}/terminfo/E
tic -o %buildroot/%{_datadir}/terminfo doc/Eterm.ti

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%{update_menus}
%endif
update-alternatives --install /usr/bin/xvt xvt /usr/bin/Eterm 15
%{_bindir}/Etbg_update_list

%postun
%if %mdkversion < 200900
%{clean_menus}	
%endif
[ "$1" = "0" ]&& update-alternatives --remove xvt /usr/bin/Eterm

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-, root, root,0755)
%doc ChangeLog README ReleaseNotes doc/Eterm_reference.html doc/README.Escreen doc/escreen.cfg doc/gen-menus
%{_bindir}/*
%dir %{_datadir}/Eterm
%config(noreplace) %{_datadir}/Eterm/themes
%{_datadir}/Eterm/pix
%{_mandir}/man1/Eterm.1.*
%{_datadir}/applications/mandriva-%name.desktop
%{_datadir}/%name/gdb.scr
/%{_datadir}/terminfo/E/*

%files -n %{libname}
%defattr(-, root, root,0755)
%{_libdir}/libEterm-*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.la
%{_libdir}/libEterm.so

%files -n %{staticlibname}
%defattr(-,root,root,-)
%{_libdir}/*.a
