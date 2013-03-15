%if %mandriva_branch == Cooker
# Cooker
%define release 5
%else
# Old distros
%define subrel 2
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
Patch1:		phpldapadmin-1.2.2-CVE-2012-0834.diff
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
    Require host 127.0.0.1
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



%clean

%files
%defattr(-,root,root)
%doc INSTALL LICENSE doc/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%{_datadir}/%{name}
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-3mdv2012.0
+ Revision: 772583
- P1: security fix for CVE-2012-0834

* Mon Jan 30 2012 Glen Ogilvie <nelg@mandriva.org> 1.2.2-2
+ Revision: 769762
- SILNET: fixed mandrivaDSPerson.xml to prevert errors being displayed
- fixed mandrivaDSPerson.xml to prevert errors being displayed

* Mon Oct 31 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1
+ Revision: 708042
- 1.2.2 (fixes CVE-2011-4074, CVE-2011-4075)
- cleanup

* Sat Oct 30 2010 Glen Ogilvie <nelg@mandriva.org> 1.2.0.5-3mdv2011.0
+ Revision: 590344
- fixed bug #61192, configuration file patch should not remove <

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.5-2mdv2010.1
+ Revision: 501775
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.5-1mdv2010.1
+ Revision: 501718
- update to new version 1.2.0.5

* Thu Dec 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-6mdv2010.1
+ Revision: 479751
- no need to enforce a specific version of php-ldap
- install VERSION file, otherwise phpldapadmin think he is a devel version :(
- add missing doc files

* Thu Dec 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-5mdv2010.1
+ Revision: 479737
- fix path to config file

* Sun Dec 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-4mdv2010.1
+ Revision: 478259
- fix apache configuration to allow localhost access
- drop reference to application URL in package description, this is true for all our packages

* Fri Dec 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-3mdv2010.1
+ Revision: 473476
- better apache configuration

* Mon Nov 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-2mdv2010.1
+ Revision: 472076
- restrict default access permissions to localhost only, as per new policy

* Mon Nov 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0.4-1mdv2010.1
+ Revision: 471747
- install files under %%{_docdir}, rather than %%{_localstatedir}/www
- no default access restriction, let user decide
- new version
- drop php5.3 patch
- rediff config patch
- don't generate blowfish secret, as cookie are not used by default

* Sun Nov 08 2009 Glen Ogilvie <nelg@mandriva.org> 1.1.0.7-2mdv2010.1
+ Revision: 462884
- patch fixes bug: 54261
- added patch for php 5.3.  This hides some errors and changes the code to fix other errors.

* Tue May 19 2009 Glen Ogilvie <nelg@mandriva.org> 1.1.0.7-1mdv2010.0
+ Revision: 377528
- New release: 1.1.0.7, fixing a few minor bugs. Also, a minor improvement to mandrivaDSPerson template, making gidNumber a dropdown list

* Tue Jan 20 2009 Jérôme Soyer <saispo@mandriva.org> 1.1.0.6-1mdv2009.1
+ Revision: 331574
- Add patch for Boost

* Fri Jul 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.0.5-3mdv2009.0
+ Revision: 231663
- hardcode %%{_localstatedir}
- don't package the certs

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sat May 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.0.5-2mdv2009.0
+ Revision: 213592
- added S1 to support the Mandriva Directory Server

* Wed Feb 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0.5-1mdv2008.1
+ Revision: 163038
- new version
  rediff config patch

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0.4-1mdv2008.1
+ Revision: 158641
- update to new version 1.1.0.4

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

* Sun Jan 06 2008 Funda Wang <fwang@mandriva.org> 1.1.0.3-1mdv2008.1
+ Revision: 145962
- New version 1.1.0.3
- rediff patch0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2008.1
+ Revision: 96997
- drop the quotes in the Exec= line (blino)

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2008.0
+ Revision: 54974
- 1.0.2
- fix deps
- added apache access restrictions to 127.0.0.1 only


* Fri Mar 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3mdv2007.1
+ Revision: 145081
- fix xdg menu
- adjust the patch

  + Jérôme Soyer <saispo@mandriva.org>
    - Add Obsoletes and Conflicts
    - Lowercase

* Sun Feb 18 2007 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.1-1mdv2007.1
+ Revision: 122573
- Fix typo found by berthy

  + Jérôme Soyer <saispo@mandriva.org>
    - Import phpLDAPAdmin

