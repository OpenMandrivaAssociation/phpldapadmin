# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

%define rname	phpLDAPAdmin

Summary:	A web-based LDAP administration tool
Name:		phpldapadmin
Version:	1.0.2
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://phpldapadmin.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/phpldapadmin/%{name}-%{version}.tar.gz
Patch0:		phpldapadmin-1.0.1-mdv_conf.diff
Requires(pre):  apache-mod_php php-ldap php-xml php-mcrypt php-gettext
Requires:       apache-mod_php php-ldap php-xml php-mcrypt php-gettext
Requires(post):	ccp >= 0.4.0
BuildRequires:	apache-base >= 2.0.54
BuildRequires:	ImageMagick
BuildArch:	noarch
Obsoletes:	phpLDAPAdmin
Conflicts:	phpLDAPAdmin
BuildRoot:	%{_tmppath}/%{name}-buildroot

# Macro for generating an environment variable (%1) with %2 random characters
%define randstr() %1=`perl -e 'for ($i = 0, $bit = "!", $key = ""; $i < %2; $i++) {while ($bit !~ /^[0-9A-Za-z]$/) { $bit = chr(rand(90) + 32); } $key .= $bit; $bit = "!"; } print "$key";'`

%description
phpldapadmin is a web-based LDAP administration tool, written in PHP. You can
browse your LDAP tree, create, delete, edit, and copy entries, perform
searches, and view your server's schema. You can even copy objects between two
LDAP servers and recursively delete or copy entire trees. All this from the
comfort of your web browser. 

On the server it is installed on, this should be accessible at
http://localhost/%{name}

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# fix dir perms
find . -type d | xargs chmod 755
    
# fix file perms
find . -type f | xargs chmod 644

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}/var/www/%{name}
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_localstatedir}/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

mv %{buildroot}/var/www/%{name}/config/config.php.example %{buildroot}%{_sysconfdir}/%{name}/config.php
rm -rf %{buildroot}/var/www/%{name}/config %{buildroot}/var/www/%{name}/tools/po

rm -f %{buildroot}/var/www/%{name}/{INSTALL,LICENSE,config.php.example}
rm -Rf %{buildroot}/var/www/%{name}/doc

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory "/var/www/%{name}">
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>

# Uncomment the following lines to force a redirect to a working 
# SSL aware apache server. This serves as an example.
# 
#<IfModule mod_ssl.c>
#    <LocationMatch /%{name}>
#        Options FollowSymLinks
#        RewriteEngine on
#        RewriteCond %{SERVER_PORT} !^443$
#        RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
#    </LocationMatch>
#</IfModule>

EOF

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert htdocs/images/logo.jpg -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert htdocs/images/logo.jpg -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert htdocs/images/logo.jpg -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

# install menu entry.
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}): \
needs=X11 \
section="More Applications/Databases" \
title="%{rname}" \
longtitle="%{rname} is a web adminstration GUI for OpenLDAP" \
command="%{_bindir}/www-browser http://localhost/%{name}/" \
icon="%{name}.png" \
xdg=true
EOF

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

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt config_version --oldfile %{_sysconfdir}/%{name}/config.php --newfile %{_sysconfdir}/%{name}/config.php.rpmnew

%randstr BLOWFISH 8

BLOWFISH=`echo -n $BLOWFISH | md5sum | awk '{print $1}'`
perl -pi -e "s|_BLOWFISH_SECRET_|$BLOWFISH|g" %{_sysconfdir}/%{name}/config.php

%_post_webapp
%update_menus

%postun
%_postun_webapp
%clean_menus

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
/var/www/%{name}
%attr(0755,apache,apache) %dir %{_localstatedir}/%{name}
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
