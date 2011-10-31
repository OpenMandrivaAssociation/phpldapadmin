%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

%define rname	phpLDAPAdmin

Summary:	A web-based LDAP administration tool
Name:		phpldapadmin
Version:	1.2.2
Release:	%{release}
License:	GPLv2+
Group:		System/Servers
URL:		http://phpldapadmin.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/phpldapadmin/%{name}-%{version}.tgz
Source1:	mandrivaDSPerson.xml
Source2:	phpldapadmin-16x16.png
Source3:	phpldapadmin-32x32.png
Source4:	phpldapadmin-48x48.png
Patch0:		phpldapadmin-1.2.0.4-default-config.patch
Requires:	apache-mod_php
Requires:	php-ldap
Requires:	php-xml
Requires:	php-mcrypt
Requires:	php-gettext
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
phpldapadmin is a web-based LDAP administration tool, written in PHP. You can
browse your LDAP tree, create, delete, edit, and copy entries, perform
searches, and view your server's schema. You can even copy objects between two
LDAP servers and recursively delete or copy entire trees. All this from the
comfort of your web browser.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

cp %{SOURCE1} templates/creation/

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_localstatedir}/lib/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 644 index.php %{buildroot}%{_datadir}/%{name}
install -m 644 VERSION %{buildroot}%{_datadir}/%{name}
cp -pr hooks %{buildroot}%{_datadir}/%{name}
cp -pr htdocs %{buildroot}%{_datadir}/%{name}
cp -pr lib %{buildroot}%{_datadir}/%{name}
cp -pr locale %{buildroot}%{_datadir}/%{name}
cp -pr queries %{buildroot}%{_datadir}/%{name}
cp -pr templates %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/tools
install -m 644 tools/unserialize.php %{buildroot}%{_datadir}/%{name}/tools

install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 640 config/config.php.example \
    %{buildroot}%{_sysconfdir}/%{name}/config.php

install -d -m 755 %{buildroot}%{webappconfdir}
cat > %{buildroot}%{webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"
</Directory>
EOF

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0644 %{SOURCE2} %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{SOURCE3} %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{SOURCE4} %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{rname}
Comment=%{rname} is a web adminstration GUI for OpenLDAP
Exec=%{_bindir}/www-browser http://localhost/%{name}/
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Databases;
EOF

# cleanup
rm -rf doc/certs

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL LICENSE doc/*
%config(noreplace) %{webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%{_datadir}/%{name}
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
