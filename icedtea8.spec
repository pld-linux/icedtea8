#
# IMPORTANT:
#	when upgrading remember to redownload all sources from the upstream
#	URLs and update MD5 sums, as there is no change in the file names
#	and distfiles would provide outdated files
#

# TODO:
# - install .ttf fonts (same as in sun-java-base-jre-X11 package) or configure
#   it to use system fonts (is it possible?).
# - desktop files, icons, etc. Some of these are included in the source root dir
# - maybe build Shark VM, at least on i486, as the zero-assembly VM is very slow
# - pass %{rpmcflags} to build

%bcond_with	bootstrap	# build a bootstrap version, using icedtea6
%bcond_without	nss		# don't use NSS
%bcond_without	cacerts		# don't include the default CA certificates
%bcond_without	systemtap	# build without systemtap

%if %{with bootstrap}
%define		use_jdk	openjdk8
%else
%define		use_jdk	icedtea8
%endif

%ifarch %{ix86} %{x8664} sparc ppc64 ppc64le %{arm} aarch64
%define		with_jfr	1
%endif

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 52.0
# JDK/JRE version, as returned with `java -version`, '_' replaced with '.'
%define		_jdkversion 1.8.0.292

Summary:	OpenJDK and GNU Classpath code
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath
Name:		icedtea8
Version:	3.19.0
Release:	1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	http://icedtea.wildebeest.org/download/source/icedtea-%{version}.tar.gz
# Source0-md5:	196e08948558322e7dd5c0b54b6d08a6
Source1:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/openjdk.tar.xz
# Source1-md5:	31e8f9aa1359a7bbf28b7c4b5046a472
Source2:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/corba.tar.xz
# Source2-md5:	1d7446a502305da6f5340858dd49b76f
Source3:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/jaxp.tar.xz
# Source3-md5:	5e77415af4a088bc643456f7e01ae013
Source4:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/jaxws.tar.xz
# Source4-md5:	e020b567a60b0302bc9da4a4e7245b5e
Source5:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/jdk.tar.xz
# Source5-md5:	02ed69e9f862ff30e540296aaab28799
Source6:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/langtools.tar.xz
# Source6-md5:	86a49394f091e4ae6bc7eac8e02a2f83
Source7:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/hotspot.tar.xz
# Source7-md5:	aaddd1cc1af543542318933d1d47d57e
Source8:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/aarch32.tar.xz
# Source8-md5:	8cc9496816d9b752e7dcc64aefd8a385
Source9:	http://icedtea.wildebeest.org/download/drops/icedtea8/%{version}/nashorn.tar.xz
# Source9-md5:	0c449d68b6cafcfec6099770f95c6347
Source10:	make-cacerts.sh
# 0-99 patches for the IcedTea files
Patch0:		%{name}-x32-ac.patch
Patch1:		%{name}-heimdal.patch
# 100-... patches applied to the extracted sources
Patch100:	%{name}-libpath.patch
Patch101:	%{name}-x32.patch
Patch102:	openjdk-heimdal.patch
Patch103:	atomic.patch
URL:		http://icedtea.classpath.org/wiki/Main_Page
BuildRequires:	alsa-lib-devel
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	bash
%{?with_cacerts:BuildRequires:	ca-certificates-update}
BuildRequires:	cups-devel
BuildRequires:	/usr/bin/jar
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.3
BuildRequires:	gawk
BuildRequires:	giflib-devel >= 5.1
BuildRequires:	glib2-devel
BuildRequires:	glibc-misc
BuildRequires:	gtk+2-devel
BuildRequires:	heimdal-devel
BuildRequires:	java-rhino
BuildRequires:	java-xalan
%buildrequires_jdk
BuildRequires:	lcms2-devel
%ifarch %{arm}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libffi-devel
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel
BuildRequires:	libsctp-devel
BuildRequires:	libstdc++-static
BuildRequires:	lsb-release
%{?with_nss:BuildRequires:	nss-devel >= 1:3.17.2-5}
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel >= 3.2}
BuildRequires:	tar >= 1:1.22
BuildRequires:	unzip
BuildRequires:	util-linux
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	xz
BuildRequires:	zip
BuildRequires:	zlib-devel
Requires:	%{name}-appletviewer = %{version}-%{release}
Requires:	%{name}-jdk = %{version}-%{release}
Suggests:	%{name}-jre-X11
Suggests:	icedtea-web
Obsoletes:	icedtea6
Obsoletes:	icedtea7
Obsoletes:	java5-sun
Obsoletes:	java5-sun-jre
Obsoletes:	java5-sun-jre-jdbc
Obsoletes:	java5-sun-jre-X11
Obsoletes:	java5-sun-tools
Obsoletes:	java-gcj-compat
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java-sun-demos
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-alsa
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	java-sun-jre-X11
Obsoletes:	java-sun-tools
Obsoletes:	openjdk8
Obsoletes:	oracle-java7
Obsoletes:	oracle-java7-jre
Obsoletes:	oracle-java7-jre-alsa
Obsoletes:	oracle-java7-jre-jdbc
Obsoletes:	oracle-java7-jre-X11
Obsoletes:	oracle-java7-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dstreldir	%{name}-%{version}
%define		dstdir		%{_jvmdir}/%{dstreldir}
%define		jrereldir	%{dstreldir}/jre
%define		jredir		%{_jvmdir}/%{jrereldir}
%define		jvmjardir	%{_jvmjardir}/%{name}-%{version}

%ifarch %{x8664}
%define		jre_arch	amd64
%endif
%ifarch %{ix86}
%define		jre_arch	i386
%endif
%ifarch x32
%define		jre_arch	x32
%endif
%ifarch aarch64
%define		jre_arch	aarch64
%endif
%ifarch %{arm}
%define		jre_arch	aarch32
%endif

%ifarch %{arm}
%define		jvm_type	client
%else
%define		jvm_type	server
%endif

# to break artificial subpackage dependency loops
%define		_noautoreq	'libmawt.so' java\\\\(ClassDataVersion\\\\)

%description
The IcedTea project provides a harness to build the source code from
http://openjdk.java.net/ using Free Software build tools and provides
replacements libraries for the binary plugs with code from the GNU
Classpath project.

This is a meta-package which provides, by its dependencies, all the
IcedTea6 components including the OpenJDK, Java 6 developement kit and
runtime environment.

%description -l pl.UTF-8
Projekt IcedTea daje możliwość kompilacji kodu źródłowego z
http://openjdk.java.net/ przy użyciu wolnodostępnych narzędzi oraz
dostarcza zamienniki biblioteczne binarnych wtyczek pochodzące z
projektu GNU Classpath.

To jest meta-pakiet, który, za pośrednictwem zależności, dostarcza
wszystkie komponenty IcedTea7, w tym środowisko programistyczne
(OpenJDK) i uruchomieniowe (JRE).

%package jdk
Summary:	OpenJDK and GNU Classpath code - software development kit
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jar = %{version}-%{release}
Requires:	%{name}-jdk-base = %{version}-%{release}
Requires:	%{name}-jre = %{version}-%{release}
Provides:	j2sdk = %{_jdkversion}
Provides:	jdk = %{_jdkversion}
Obsoletes:	blackdown-java-sdk
Obsoletes:	ibm-java
Obsoletes:	icedtea6-jdk
Obsoletes:	icedtea7-jdk
Obsoletes:	java-blackdown
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java5-sun
Obsoletes:	openjdk8-jdk
Obsoletes:	oracle-java7
Obsoletes:	jdk
Obsoletes:	kaffe

%description jdk
This package symlinks OpenJDK development tools provided by
%{name}-jdk-base to system-wide directories like %{_bindir}, making
IcedTea6 default JDK.

%description jdk -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do narzędzi programistycznych
OpenJDK, dostarczanych przez pakiet %{name}-jdk-base, w standardowych
systemowych ścieżkach takich jak %{_bindir}, sprawiając tym samym, że
IcedTea6 staje się domyślnym JDK w systemie.

%package jdk-base
Summary:	OpenJDK and GNU Classpath code - software development kit
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	jpackage-utils >= 0:1.7.5-4
Provides:	jdk(%{name})

%description jdk-base
OpenJDK development tools built using free software only.

%description jdk-base -l pl.UTF-8
OpenJDK skompilowane wyłącznie przy użyciu wolnego oprogramowania.

%package jre
Summary:	OpenJDK and GNU Classpath code - runtime environment
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	nss >= 1:3.13.4
# Require zoneinfo data provided by java-tzdata subpackage.
Requires:	java-tzdata
Provides:	java
Provides:	java(ClassDataVersion) = %{_classdataversion}
Provides:	java(jaas) = %{version}
Provides:	java(jaf) = 1.1.1
Provides:	java(jaxp) = 1.3
Provides:	java(jaxp_parser_impl)
Provides:	java(jce) = %{version}
Provides:	java(jdbc-stdext) = %{version}
Provides:	java(jdbc-stdext) = 3.0
Provides:	java(jmx) = 1.4
Provides:	java(jndi) = %{version}
Provides:	java(jsse) = %{version}
Provides:	java1.4
Provides:	jre = %{_jdkversion}
Obsoletes:	icedtea6-jre
Obsoletes:	icedtea7-jre
Obsoletes:	jaas
Obsoletes:	jaf
Obsoletes:	java-gcj-compat
Obsoletes:	java-jaxp
Obsoletes:	java-jdbc-stdext
Obsoletes:	java-sun-jre
Obsoletes:	java5-sun-jre
Obsoletes:	jce
Obsoletes:	jdbc-stdext
Obsoletes:	jmx
Obsoletes:	jndi
Obsoletes:	jre
Obsoletes:	jsse
Obsoletes:	openjdk8-jre
Obsoletes:	oracle-java7-jre

%description jre
This package symlinks OpenJDK runtime environment tools provided by
%{name}-jre-base to system-wide directories like %{_bindir}, making
IcedTea6 default JRE.

%description jre -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do środowiska
uruchomieniowego OpenJDK, dostarczanych przez pakiet %{name}-jre-base,
w standardowych systemowych ścieżkach takich jak %{_bindir},
sprawiając tym samym, że IcedTea7 staje się domyślnym JRE w systemie.

%package jre-X11
Summary:	IcedTea7 OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	IcedTea7 OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
Requires:	%{name}-jre-base-X11 = %{version}-%{release}
Provides:	jre-X11 = %{_jdkversion}
Obsoletes:	icedtea6-jre-X11
Obsoletes:	java-sun-jre-X11
Obsoletes:	openjdk8-jre-X11
Obsoletes:	oracle-java7-jre-X11

%description jre-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base
Summary:	OpenJDK and GNU Classpath code - runtime environment
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	jpackage-utils >= 0:1.7.5-4
Provides:	jre(%{name})
Provides:	jre-base = %{_jdkversion}

%description jre-base
OpenJDK runtime environment built using free software only.

%description jre-base -l pl.UTF-8
Środowisko uruchomieniowe OpenJDK zbudowany wyłącznie przy użyciu
wolnego oprogramowania.

%package jre-base-X11
Summary:	IcedTea7 OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	IcedTea7 OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}
Requires:	%{name}-jre-base-freetype = %{version}-%{release}
Provides:	jre-base-X11 = %{_jdkversion}

%description jre-base-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-base-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base-alsa
Summary:	IcedTea7 OpenJDK - runtime environment - ALSA support
Summary(pl.UTF-8):	IcedTea7 OpenJDK - środowisko uruchomieniowe - obsługa ALSA
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-alsa
ALSA sound support for OpenJDK runtime environment build using free
software only.

%description jre-base-alsa -l pl.UTF-8
Biblioteki ALSA rozszerzające środowisko OpenJDK o obsługę dźwięku
zbudowane przy uzyciu wyłącznie wolnego oprogramowania.

%package jre-base-freetype
Summary:	IcedTea7 OpenJDK - runtime environment - font support
Summary(pl.UTF-8):	IcedTea7 OpenJDK - środowisko uruchomieniowe - obsługa fontów
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-freetype
Font handling library for OpenJDK runtime environment built using free
software only.

%description jre-base-freetype -l pl.UTF-8
Biblioteki obsługi czcionek dla OpenJDK zbudowane wyłącznie przy
użyciu wolnego oprogramowania.

%package jre-base-gtk
Summary:	IcedTea7 OpenJDK - runtime environment - GTK support
Summary(pl.UTF-8):	IcedTea7 OpenJDK - środowisko uruchomieniowe - obsługa GTK
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{version}-%{release}

%description jre-base-gtk
GTK support for OpenJDK runtime environment.

%description jre-base-gtk -l pl.UTF-8
Biblioteki GTK dla OpenJDK.

%package jar
Summary:	OpenJDK and GNU Classpath code - JAR tool
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - narzędzie JAR
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{version}-%{release}
Provides:	jar
Obsoletes:	fastjar
Obsoletes:	icedtea6-jar
Obsoletes:	icedtea7-jar
Obsoletes:	openjdk8-jar
Obsoletes:	jar

%description jar
JAR tool from OpenJDK built using free software only.

JAR is an archiver used to merge Java classes into a single library.

%description jar -l pl.UTF-8
Narzędzie jar z OpenJDK zbudowane przy uzyciu wyłącznie wolnego
oprogramowania.

JAR jest narzędziem pozwalającym wykonywać podstawowe operacje na
archiwach javy .jar takie jak na przykład tworzenie lub rozpakowywanie
archiwów.

%package appletviewer
Summary:	OpenJDK and GNU Classpath code - appletviewer tool
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - narzędzie appletviewer
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{version}-%{release}
Requires:	%{name}-jre-X11 = %{version}-%{release}
Obsoletes:	icedtea6-appletviewer
Obsoletes:	icedtea7-appletviewer
Obsoletes:	java-sun-appletviewer
Obsoletes:	openjdk8-appletviewer
Obsoletes:	oracle-java7-appletviewer

%description appletviewer
Appletviewer from OpenJDK build using free software only.

%description appletviewer -l pl.UTF-8
Appletviewer pozwala uruchamiać aplety javy niezależnie od
przeglądarki www. Ten appletviewer pochodzi z zestawu narzędzi OpenJDK
i został zbudowany wyłącznie przy użyciu wolnego oprogramowania.

%package jdk-sources
Summary:	OpenJDK and GNU Classpath code - sources
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - kod źródłowy
Group:		Documentation
BuildArch:	noarch

%description jdk-sources
Source code for the OpenJDK development kit and Java standard library.

%description jdk-sources -l pl.UTF-8
Kod źródłowy narzędzi programistycznych OpenJDK oraz standardowej
biblioteki Javy.

%package examples
Summary:	OpenJDK and GNU Classpath code - examples
Summary(pl.UTF-8):	Kod OpenJDK i GNU Classpath - przykłady
Group:		Documentation
BuildArch:	noarch

%description examples
Code examples for OpenJDK.

%description examples -l pl.UTF-8
Przykłady dla OpenJDK.

%prep
%setup -qn icedtea-%{version}
%patch0 -p1
%patch1 -p1

# patches to applied to the extracted sources
install -d pld-patches
cp -p %{PATCH100} pld-patches
%ifarch x32
cp -p %{PATCH101} pld-patches
%endif
cp -p %{PATCH102} pld-patches
cp -p %{PATCH103} pld-patches

# let the build system extract the sources where it wants them
install -d drops
ln -s %{SOURCE1} openjdk.tar.xz
ln -s %{SOURCE2} corba.tar.xz
ln -s %{SOURCE3} jaxp.tar.xz
ln -s %{SOURCE4} jaxws.tar.xz
ln -s %{SOURCE5} jdk.tar.xz
ln -s %{SOURCE6} langtools.tar.xz
%ifarch %{arm}
ln -s %{SOURCE8} hotspot.tar.xz
%else
ln -s %{SOURCE7} hotspot.tar.xz
%endif
ln -s %{SOURCE9} nashorn.tar.xz

%build
# Make sure we have /proc mounted - otherwise idlc will fail later.
if [ ! -f /proc/self/stat ]; then
	echo "You need to have /proc mounted in order to build this package!"
	exit 1
fi

unset JAVA_HOME

mkdir -p build-bin
export PATH="$(pwd)/build-bin:$PATH"

# our /usr/bin/ant is quite broken and won't run properly
# in the bootstrap JDK environment prepared by IcedTea build process
cat >>build-bin/ant <<'EOF'
#!/bin/sh

exec java \
	-classpath /usr/share/java/ant-launcher.jar \
	-Dant.home=/usr/share/ant \
	-Dant.lib=/usr/share/ant/lib \
	org.apache.tools.ant.launch.Launcher \
	"$@"
EOF
chmod a+x build-bin/ant

%{__aclocal}
%{__autoconf}
%{__automake}

# NOTE: the weird '--disable-bootstrap' is how it is supposed to be
# http://icedtea.classpath.org/wiki/CommonIssues#IcedTea7_building_on_systems_with_JDK_5_or_JDK_6
%configure \
	WGET=%{_bindir}/wget \
%ifarch x32
	--enable-zero \
%endif
	--disable-downloading \
	--with-jdk-home=%{java_home} \
	--disable-bootstrap \
	--enable-improved-font-rendering \
	%{__enable_disable jfr} \
	--enable-system-kerberos \
	--enable-system-pcsc \
	--enable-system-sctp \
	--%{!?with_nss:dis}%{?with_nss:en}able-nss

%{__make} extract \
	SHELL=/bin/bash \
	DISTRIBUTION_PATCHES="$(echo pld-patches/*.patch)"

%{__make} patch \
	SHELL=/bin/bash \
	DISTRIBUTION_PATCHES="$(echo pld-patches/*.patch)"

# break here to prepare openjdk patches
#exit 1

cd openjdk/common/autoconf
sh autogen.sh
cd ../../..

%{__make} -j1 \
	SHELL=/bin/bash \
	DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
	DISTRIBUTION_PATCHES="$(echo pld-patches/*.patch)" \
	PRINTF=/bin/printf \
	MAX_VM_MEMORY=1024

# smoke test
openjdk.build/jdk/bin/java -version

%{?with_cacerts:%{__sh} %{SOURCE10}}

# _jdkversion check
JDKVER=$(openjdk.build/jdk/bin/java -version 2>&1 | gawk -F'"' '/openjdk version/ { s=$2; gsub("_", ".", s); print s; } ')
if [ "$JDKVER" != "%{_jdkversion}" ]; then
	echo "Please update _jdkversion macro to $JDKVER" >&2
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{dstdir},%{_mandir}/ja} \
	$RPM_BUILD_ROOT{%{jvmjardir},%{_examplesdir}/%{name}-%{version},%{_javasrcdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# install the 'JDK image', it contains the JRE too
cp -a openjdk.build/images/j2sdk-image/* $RPM_BUILD_ROOT%{dstdir}

# convenience symlinks without version number
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}
ln -s %{jrereldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}-jre

ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/java

# move JDK sources and demo to /usr/src
mv $RPM_BUILD_ROOT%{dstdir}/demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{dstdir}/sample $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{dstdir}/src.zip $RPM_BUILD_ROOT%{_javasrcdir}/%{name}-jdk.zip

# move manual pages to its place
mv $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8/man1 $RPM_BUILD_ROOT%{_mandir}/ja/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8
rm $RPM_BUILD_ROOT%{dstdir}/man/ja
mv $RPM_BUILD_ROOT%{dstdir}/man/man1 $RPM_BUILD_ROOT%{_mandir}/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man

# replace duplicates with symlinks, link to %{_bindir}
for path in $RPM_BUILD_ROOT%{dstdir}/bin/*; do
	filename=$(basename $path)
	if diff -q "$path" "$RPM_BUILD_ROOT%{jredir}/bin/$filename" > /dev/null; then
		ln -sf "../jre/bin/$filename" "$path"
		ln -sf "%{jredir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
	else
		ln -sf "%{dstdir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
	fi
done
ln -sf ../jre/lib/jexec $RPM_BUILD_ROOT%{dstdir}/lib/jexec

# keep configuration in /etc (not all *.properties go there)
for config in management security content-types.properties \
		logging.properties net.properties sound.properties; do

	mv $RPM_BUILD_ROOT%{jredir}/lib/$config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
	ln -s %{_sysconfdir}/%{name}/$config $RPM_BUILD_ROOT%{jredir}/lib/$config
done

ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jsse.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jcert.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jnet.jar
ln -sf %{jredir}/lib/jce.jar $RPM_BUILD_ROOT%{jvmjardir}/jce.jar
for f in jndi jndi-ldap jndi-cos jndi-rmi jaas jdbc-stdext jdbc-stdext-3.0 \
	sasl jaxp_parser_impl jaxp_transform_impl jaxp jmx activation xml-commons-apis \
	jndi-dns jndi-rmi; do
	ln -sf %{jredir}/lib/rt.jar $RPM_BUILD_ROOT%{jvmjardir}/$f.jar
done

# some apps (like opera) looks for it in different place
ln -s %{jvm_type}/libjvm.so $RPM_BUILD_ROOT%{jredir}/lib/%{jre_arch}/libjvm.so

%{__rm} $RPM_BUILD_ROOT%{dstdir}/{,jre/}{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README}

%{?with_cacerts:install cacerts $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/security}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README

%files jdk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/extcheck
%attr(755,root,root) %{_bindir}/idlj
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/java-rmi.cgi
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/javap
%attr(755,root,root) %{_bindir}/jcmd
%attr(755,root,root) %{_bindir}/jconsole
%attr(755,root,root) %{_bindir}/jdb
%attr(755,root,root) %{_bindir}/jdeps
%attr(755,root,root) %{_bindir}/jhat
%attr(755,root,root) %{_bindir}/jinfo
%attr(755,root,root) %{_bindir}/jjs
%attr(755,root,root) %{_bindir}/jmap
%attr(755,root,root) %{_bindir}/jps
%attr(755,root,root) %{_bindir}/jrunscript
%attr(755,root,root) %{_bindir}/jsadebugd
%attr(755,root,root) %{_bindir}/jstack
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jstatd
%attr(755,root,root) %{_bindir}/native2ascii
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_bindir}/schemagen
%attr(755,root,root) %{_bindir}/serialver
%attr(755,root,root) %{_bindir}/wsgen
%attr(755,root,root) %{_bindir}/wsimport
%attr(755,root,root) %{_bindir}/xjc
%{_mandir}/man1/extcheck.1*
%{_mandir}/man1/idlj.1*
%{_mandir}/man1/jarsigner.1*
%{_mandir}/man1/javac.1*
%{_mandir}/man1/javadoc.1*
%{_mandir}/man1/javah.1*
%{_mandir}/man1/javap.1*
%{_mandir}/man1/jcmd.1*
%{_mandir}/man1/jconsole.1*
%{_mandir}/man1/jdb.1*
%{_mandir}/man1/jdeps.1*
%{_mandir}/man1/jhat.1*
%{_mandir}/man1/jinfo.1*
%{_mandir}/man1/jjs.1*
%{_mandir}/man1/jmap.1*
%{_mandir}/man1/jps.1*
%{_mandir}/man1/jrunscript.1*
%{_mandir}/man1/jsadebugd.1*
%{_mandir}/man1/jstack.1*
%{_mandir}/man1/jstat.1*
%{_mandir}/man1/jstatd.1*
%{_mandir}/man1/native2ascii.1*
%{_mandir}/man1/schemagen.1*
%{_mandir}/man1/serialver.1*
%{_mandir}/man1/rmic.1*
%{_mandir}/man1/wsgen.1*
%{_mandir}/man1/wsimport.1*
%{_mandir}/man1/xjc.1*
%lang(ja) %{_mandir}/ja/man1/extcheck.1*
%lang(ja) %{_mandir}/ja/man1/idlj.1*
%lang(ja) %{_mandir}/ja/man1/jarsigner.1*
%lang(ja) %{_mandir}/ja/man1/javac.1*
%lang(ja) %{_mandir}/ja/man1/javadoc.1*
%lang(ja) %{_mandir}/ja/man1/javah.1*
%lang(ja) %{_mandir}/ja/man1/javap.1*
%lang(ja) %{_mandir}/ja/man1/jcmd.1*
%lang(ja) %{_mandir}/ja/man1/jconsole.1*
%lang(ja) %{_mandir}/ja/man1/jdb.1*
%lang(ja) %{_mandir}/ja/man1/jdeps.1*
%lang(ja) %{_mandir}/ja/man1/jhat.1*
%lang(ja) %{_mandir}/ja/man1/jinfo.1*
%lang(ja) %{_mandir}/ja/man1/jjs.1*
%lang(ja) %{_mandir}/ja/man1/jmap.1*
%lang(ja) %{_mandir}/ja/man1/jps.1*
%lang(ja) %{_mandir}/ja/man1/jrunscript.1*
%lang(ja) %{_mandir}/ja/man1/jsadebugd.1*
%lang(ja) %{_mandir}/ja/man1/jstack.1*
%lang(ja) %{_mandir}/ja/man1/jstat.1*
%lang(ja) %{_mandir}/ja/man1/jstatd.1*
%lang(ja) %{_mandir}/ja/man1/native2ascii.1*
%lang(ja) %{_mandir}/ja/man1/schemagen.1*
%lang(ja) %{_mandir}/ja/man1/serialver.1*
%lang(ja) %{_mandir}/ja/man1/rmic.1*
%lang(ja) %{_mandir}/ja/man1/wsgen.1*
%lang(ja) %{_mandir}/ja/man1/wsimport.1*
%lang(ja) %{_mandir}/ja/man1/xjc.1*

%files jdk-base
%defattr(644,root,root,755)
%doc openjdk.build/images/j2sdk-image/THIRD_PARTY_README
%doc openjdk.build/images/j2sdk-image/ASSEMBLY_EXCEPTION
%dir %{dstdir}
%{_jvmdir}/%{name}
%dir %{dstdir}/bin
%attr(755,root,root) %{dstdir}/bin/appletviewer
%attr(755,root,root) %{dstdir}/bin/extcheck
%attr(755,root,root) %{dstdir}/bin/idlj
%attr(755,root,root) %{dstdir}/bin/jar
%attr(755,root,root) %{dstdir}/bin/jarsigner
%attr(755,root,root) %{dstdir}/bin/java-rmi.cgi
%attr(755,root,root) %{dstdir}/bin/javac
%attr(755,root,root) %{dstdir}/bin/javadoc
%attr(755,root,root) %{dstdir}/bin/javah
%attr(755,root,root) %{dstdir}/bin/javap
%attr(755,root,root) %{dstdir}/bin/jconsole
%attr(755,root,root) %{dstdir}/bin/jcmd
%attr(755,root,root) %{dstdir}/bin/jdb
%attr(755,root,root) %{dstdir}/bin/jdeps
%attr(755,root,root) %{dstdir}/bin/jhat
%attr(755,root,root) %{dstdir}/bin/jinfo
%attr(755,root,root) %{dstdir}/bin/jmap
%attr(755,root,root) %{dstdir}/bin/jps
%attr(755,root,root) %{dstdir}/bin/jrunscript
%attr(755,root,root) %{dstdir}/bin/jsadebugd
%attr(755,root,root) %{dstdir}/bin/jstack
%attr(755,root,root) %{dstdir}/bin/jstat
%attr(755,root,root) %{dstdir}/bin/jstatd
%attr(755,root,root) %{dstdir}/bin/native2ascii
%attr(755,root,root) %{dstdir}/bin/rmic
%attr(755,root,root) %{dstdir}/bin/schemagen
%attr(755,root,root) %{dstdir}/bin/serialver
%attr(755,root,root) %{dstdir}/bin/wsgen
%attr(755,root,root) %{dstdir}/bin/wsimport
%attr(755,root,root) %{dstdir}/bin/xjc
%{dstdir}/include
%dir %{dstdir}/lib
%{dstdir}/lib/ct.sym
%{dstdir}/lib/dt.jar
%{dstdir}/lib/ir.idl
%{dstdir}/lib/jconsole.jar
%attr(755,root,root) %{dstdir}/lib/jexec
%{dstdir}/lib/orb.idl
%ifnarch %{arm} x32
%{dstdir}/lib/sa-jdi.jar
%endif
%{dstdir}/lib/tools.jar
%dir %{dstdir}/lib/%{jre_arch}
%dir %{dstdir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/jli/*.so
%{?with_systemtap:%{dstdir}/tapset}

%files jre
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/clhsdb
%attr(755,root,root) %{_bindir}/java
%{?with_jfr:%attr(755,root,root) %{_bindir}/jfr}
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/orbd
%attr(755,root,root) %{_bindir}/pack200
%attr(755,root,root) %{_bindir}/rmid
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/tnameserv
%attr(755,root,root) %{_bindir}/unpack200
%{_mandir}/man1/java.1*
%{_mandir}/man1/keytool.1*
%{_mandir}/man1/orbd.1*
%{_mandir}/man1/pack200.1*
%{_mandir}/man1/rmid.1*
%{_mandir}/man1/rmiregistry.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/tnameserv.1*
%{_mandir}/man1/unpack200.1*
%lang(ja) %{_mandir}/ja/man1/java.1*
%lang(ja) %{_mandir}/ja/man1/keytool.1*
%lang(ja) %{_mandir}/ja/man1/orbd.1*
%lang(ja) %{_mandir}/ja/man1/pack200.1*
%lang(ja) %{_mandir}/ja/man1/rmid.1*
%lang(ja) %{_mandir}/ja/man1/rmiregistry.1*
%lang(ja) %{_mandir}/ja/man1/servertool.1*
%lang(ja) %{_mandir}/ja/man1/tnameserv.1*
%lang(ja) %{_mandir}/ja/man1/unpack200.1*
%{_jvmdir}/java

%files jre-base
%defattr(644,root,root,755)
%doc openjdk.build/images/j2sdk-image/THIRD_PARTY_README
%doc openjdk.build/images/j2sdk-image/ASSEMBLY_EXCEPTION
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%dir %{dstdir}
%{dstdir}/release
%dir %{jredir}
%{_jvmdir}/%{name}-jre
%dir %{jredir}/bin
%dir %{dstdir}/bin
%attr(755,root,root) %{dstdir}/bin/clhsdb
%attr(755,root,root) %{jredir}/bin/java
%attr(755,root,root) %{dstdir}/bin/java
%{?with_jfr:%attr(755,root,root) %{dstdir}/bin/jfr}
%attr(755,root,root) %{jredir}/bin/jjs
%attr(755,root,root) %{dstdir}/bin/jjs
%attr(755,root,root) %{jredir}/bin/keytool
%attr(755,root,root) %{dstdir}/bin/keytool
%attr(755,root,root) %{jredir}/bin/orbd
%attr(755,root,root) %{dstdir}/bin/orbd
%attr(755,root,root) %{jredir}/bin/pack200
%attr(755,root,root) %{dstdir}/bin/pack200
%attr(755,root,root) %{jredir}/bin/rmid
%attr(755,root,root) %{dstdir}/bin/rmid
%attr(755,root,root) %{jredir}/bin/rmiregistry
%attr(755,root,root) %{dstdir}/bin/rmiregistry
%attr(755,root,root) %{jredir}/bin/servertool
%attr(755,root,root) %{dstdir}/bin/servertool
%attr(755,root,root) %{jredir}/bin/tnameserv
%attr(755,root,root) %{dstdir}/bin/tnameserv
%attr(755,root,root) %{jredir}/bin/unpack200
%attr(755,root,root) %{dstdir}/bin/unpack200
%dir %{jredir}/lib
%dir %{jredir}/lib/applet
%{jredir}/lib/cmm
%{jredir}/lib/ext
%if %{with jfr}
%{jredir}/lib/jfr.jar
%dir %{jredir}/lib/jfr
%{jredir}/lib/jfr/*.jfc
%endif
%dir %{jredir}/lib/%{jre_arch}
%dir %{jredir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/jli/*.so
%dir %{jredir}/lib/%{jre_arch}/%{jvm_type}
%{jredir}/lib/%{jre_arch}/%{jvm_type}/Xusage.txt
%ifnarch x32
%{jredir}/lib/%{jre_arch}/%{jvm_type}/classes.jsa
%endif
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/%{jvm_type}/*.so
%{jredir}/lib/%{jre_arch}/jvm.cfg
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libattach.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_headless.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libdt_socket.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libhprof.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libinstrument.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2gss.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2krb5.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pcsc.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pkcs11.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2sctp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjaas_unix.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjavajpeg.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjavalcms.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava_crw_demo.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjdwp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsdt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsig.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsound.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjvm.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmanagement.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmlib_image.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnet.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnio.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnpt.so
%ifnarch %{arm} x32
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsaproc.so
%endif
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsunec.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libunpack.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libverify.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libzip.so
%{jredir}/lib/images
%{jredir}/lib/management
%{jredir}/lib/security
%{jredir}/lib/hijrah-config-umalqura.properties
%{jredir}/lib/tzdb.dat
%{jredir}/lib/tz.properties

%if %{with webstart}
%{jredir}/lib/about.jar
%{jredir}/lib/about.jnlp
%endif
%{jredir}/lib/calendars.properties
%{jredir}/lib/charsets.jar
%{jredir}/lib/classlist
%{jredir}/lib/content-types.properties
%{jredir}/lib/currency.data
%{jredir}/lib/flavormap.properties
%{jredir}/lib/jce.jar
%attr(755, root, root) %{jredir}/lib/jexec
%{jredir}/lib/jsse.jar
%{jredir}/lib/jvm.hprof.txt
%{jredir}/lib/logging.properties
%{jredir}/lib/management-agent.jar
%{jredir}/lib/meta-index
%{jredir}/lib/net.properties
%{jredir}/lib/psfont.properties.ja
%{jredir}/lib/psfontj2d.properties
%{jredir}/lib/resources.jar
%{jredir}/lib/rt.jar
%{jredir}/lib/sound.properties
%{jvmjardir}

%files jre-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hsdb
%attr(755,root,root) %{_bindir}/policytool
%{_mandir}/man1/policytool.1*
%lang(ja) %{_mandir}/ja/man1/policytool.1*

%files jre-base-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/bin/hsdb
%attr(755,root,root) %{jredir}/bin/policytool
%attr(755,root,root) %{dstdir}/bin/policytool
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_xawt.so
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/libjawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsplashscreen.so

%files jre-base-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsoundalsa.so

%files jre-base-freetype
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libfontmanager.so

%files jre-base-gtk
%defattr(644,root,root,755)

%files jar
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jar
%{_mandir}/man1/jar.1*
%lang(ja) %{_mandir}/ja/man1/jar.1*

%files appletviewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/appletviewer
%{_mandir}/man1/appletviewer.1*
%lang(ja) %{_mandir}/ja/man1/appletviewer.1*

%files jdk-sources
%defattr(644,root,root,755)
%{_javasrcdir}/%{name}-jdk.zip

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
