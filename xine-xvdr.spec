
%define oname	vdr-plugin-xineliboutput
%define plugin	xineliboutput
%define name	xine-xvdr
# manually created tarball from CVS tag
%define version	1.0.5
%define snapshot 0
%define prever	0
%define rel	2

%if %snapshot
%if %prever
%define release	%mkrel 0.%prever.%snapshot.%rel
%else
%define release %mkrel 0.%snapshot.%rel
%endif
%else
%if %prever
%define release %mkrel 0.%prever.%rel
%else
%define release %mkrel %rel
%endif
%endif

%define xineplugindir	%(xine-config --plugindir 2>/dev/null || echo 0)
# Does not always match rpm version, reports 1.1.9 on 1.1.9.1, so use rpmver directly instead.
#define xineversion	%(xine-config --version 2>/dev/null || echo 0)
%define xineversion	%(rpm -qf --qf '%%{version}' %{_bindir}/xine-config 2>/dev/null || echo 0)
%define xineapi		%(A=%xineplugindir; echo ${A##*/})

Summary:	Xine frontend for the xineliboutput VDR plugin
Name:		%name
Version:	%version
Release:	%release
Group:		Video
License:	GPLv2+
URL:		http://sourceforge.net/projects/xineliboutput/
%if %snapshot
Source:		vdr-%plugin-%snapshot.tar.bz2
%else
%if %prever
Source:		http://prdownloads.sourceforge.net/xineliboutput/vdr-%plugin-%{version}%{prever}.tar.bz2
%else
Source:		http://prdownloads.sourceforge.net/xineliboutput/vdr-%plugin-%version.tar.bz2
%endif
%endif
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	libx11-devel
BuildRequires:	libxv-devel
BuildRequires:	libxine-devel
BuildRequires:	jpeg-devel
BuildRequires:	libextractor-devel
BuildRequires:	libxrender-devel
BuildRequires:	libxinerama-devel
BuildRequires:	dbus-glib-devel
Requires:	xine-plugin-api >= %xineapi
Obsoletes:	vdr-plugin-xineliboutput-frontend-xine xineliboutput-fe-xine

%description
With this package you can connect to your VDR xineliboutput plugin
with xine with an MRL like below:
xvdr://127.0.0.1#nocache;demux:mpeg_block

Frontend packages:
- xine-xvdr: Xine frontend
- xine1.2-xvdr: Xine1.2 frontend
- xineliboutput-sxfe: Standalone X11 frontend
- xineliboutput-fbfe: Standalone FB frontend
- xineliboutput-local-sxfe: Local X11 frontend
- xineliboutput-local-fbfe: Local FB frontend

%prep
%if %snapshot
%setup -q -n vdr-%plugin
%else
%if %prever
%setup -q -n %plugin-%version%prever
%else
%setup -q -n %plugin-%version
%endif
%endif

find -name CVS -type d | while read i; do rm -r "$i" || exit 1; done

%build
%setup_compile_flags
CFLAGS="$CFLAGS -fPIC"
%make XINELIBOUTPUT_VDRPLUGIN=0 XINELIBOUTPUT_X11=0 XINELIBOUTPUT_FB=0 LOCALEDIR=.

%install
rm -rf %{buildroot}
install -d -m755 %buildroot%xineplugindir/post %buildroot%_bindir
%makeinstall XINELIBOUTPUT_VDRPLUGIN=0 XINELIBOUTPUT_X11=0 XINELIBOUTPUT_FB=0 LOCALEDIR=. \
	XINEPLUGINDIR=%buildroot%xineplugindir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
# xine-plugins maybe upgraded without new xine-xvdr (while everything still
# works). Therefore we have to include the plugindir as well.
%dir %{xineplugindir}
%{xineplugindir}/*.so
%{xineplugindir}/post/*.so
