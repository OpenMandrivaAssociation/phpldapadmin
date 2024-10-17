# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

%define rname	phpLDAPAdmin

Summary:	A web-based LDAP administration tool
Name:		phpldapadmin
Version:	1.2.3
Release:	5
License:	GPLv2+
Group:		System/Servers
URL:		https://phpldapadmin.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/phpldapadmin/%{name}-%{version}.tgz
Source1:	rosaDSPerson.xml
Source2:	phpldapadmin-16x16.png
Source3:	phpldapadmin-32x32.png
Source4:	phpldapadmin-48x48.png
Patch0:		phpldapadmin-1.2.0.4-default-config.patch
# http://sourceforge.net/u/nihilisticz/phpldapadmin/ci/7e53dab990748c546b79f0610c3a7a58431e9ebc/
Patch1:     0001-Fixed-two-issues-to-get-phpLdapAdmin-to-work-under-P.patch
Requires:	apache-mod_php
Requires:	php-ldap
Requires:	php-xml
Requires:	php-mcrypt
Requires:	php-gettext
BuildArch:	noarch

%description
phpldapadmin is a web-based LDAP administration tool, written in PHP. You can
browse your LDAP tree, create, delete, edit, and copy entries, perform
searches, and view your server's schema. You can even copy objects between two
LDAP servers and recursively delete or copy entire trees. All this from the
comfort of your web browser.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

cp %{SOURCE1} templates/creation/

%build

%install

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

install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
    Require local granted
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"
</Directory>
EOF

# ROSA Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0644 %{SOURCE2} %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{SOURCE3} %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{SOURCE4} %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{rname}
Name[ru]=%{rname}
Comment=%{rname} is a web adminstration GUI for OpenLDAP
Comment[ru]=%{rname} - Web-интерфейс для администрирования OpenLDAP
Exec=%{_bindir}/www-browser https://localhost/%{name}/
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Databases;
EOF

# cleanup
rm -rf doc/certs
chmod 644 doc/*

%files
%doc INSTALL LICENSE doc/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%{_datadir}/%{name}
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
