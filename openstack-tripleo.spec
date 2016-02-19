%global commit c3fb309727671130a32b4c19de48ec22c8530aa1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global alphatag %commit
%global repo_name tripleo-incubator

Name:			openstack-tripleo
Version: XXX
Release: XXX
Summary:		OpenStack TripleO

Group:			Applications/System
License:		ASL 2.0
URL:			https://wiki.openstack.org/wiki/TripleO
Source0:		https://github.com/openstack/%{repo_name}/archive/%{commit}.tar.gz
Source1:		tripleo

Patch0001:             0001-Use-packaged-template-directory-path.patch

BuildArch:		noarch

BuildRequires:		python-sphinx
BuildRequires:		python-oslo-sphinx

Requires:		jq

#
# patches_base=c3fb309727671130a32b4c19de48ec22c8530aa1
#

%description
TripleO is a program aimed at installing, upgrading and operating OpenStack
clouds using OpenStack's own cloud facilities as the foundations - building on
nova, neutron and heat to automate fleet management at datacenter scale.

%package doc
Summary:		Documentation for OpenStack TripleO
Group:			Documentation

Requires:		%{name} = %{version}-%{release}

BuildArch:		noarch

BuildRequires:		python-sphinx

%description	doc
TripleO is a program aimed at installing, upgrading and operating OpenStack
clouds using OpenStack's own cloud facilities as the foundations - building on
nova, neutron and heat to automate fleet management at datacenter scale.

This package contains documentation files for TripleO.

%prep
%setup -q -n %{repo_name}-%{upstream_version}

%patch0001 -p1

%install
# scripts
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
install -p -m 755 -t %{buildroot}/%{_libexecdir}/%{name} scripts/* 
mkdir -p %{buildroot}/%{_bindir}
install -p -m 755 -t %{buildroot}/%{_bindir} %{SOURCE1}
# extract-docs.awk and extract-docs are only used for building docs, we don't
# need them installed
rm -f %{buildroot}/%{_libexecdir}/%{name}/extract-docs*

# rc files
install -d -m 755 %{buildroot}/%{_sysconfdir}/tripleo
install -p -m 644 -t %{buildroot}/%{_sysconfdir}/tripleo cloudprompt
install -p -m 644 -t %{buildroot}/%{_sysconfdir}/tripleo seedrc
install -p -m 644 -t %{buildroot}/%{_sysconfdir}/tripleo undercloudrc
install -p -m 644 -t %{buildroot}/%{_sysconfdir}/tripleo overcloudrc
install -p -m 644 -t %{buildroot}/%{_sysconfdir}/tripleo overcloudrc-user

# templates
install -d -m 755 %{buildroot}/%{_datadir}/tripleo/templates
install -p -m 644 -t %{buildroot}/%{_datadir}/tripleo/templates templates/*

# documentation
sphinx-build -b html doc/source doc/build/html
install -d -m 755 %{buildroot}%{_datadir}/doc/tripleo/html
cp -r doc/build/html/* %{buildroot}%{_datadir}/doc/tripleo/html

%files
%{_bindir}/*
%{_libexecdir}/%{name}
# These config files are *not* noreplace. They aren't meant to be edited by
# users.
%config %{_sysconfdir}/tripleo
%{_datadir}/tripleo

%files doc
%doc LICENSE README.rst
%{_datadir}/doc/tripleo

%changelog
* Wed Oct 08 2014 James Slagle <jslagle@redhat.com> 0.0.5-2c3fb309727671130a32b4c19de48ec22c8530aa1
- Remove check for $TRIPLEO_ROOT.

* Thu Oct 2 2014 James Slagle <jslagle@redhat.com> 0.0.5-1
- Update to c3fb309727671130a32b4c19de48ec22c8530aa1

* Mon Sep 29 2014 James Slagle <jslagle@redhat.com> 0.0.4-1
- Update to b51d5a1840b4e985b7daa334814a10590af00d53

* Mon Sep 15 2014 James Slagle <jslagle@redhat.com> 0.0.3-1
- Update to later version.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-7.icehouse
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 James Slagle <jslagle@redhat.com> 0.0.2-6.icehouse
- Build from upstream stable/icehouse branch
- Add Requires on jq

* Fri Apr 04 2014 James Slagle <jslagle@redhat.com> 0.0.2-5.20140220git
- Add patch 0005-Move-setup-clienttools-to-devtest_setup.sh.patch

* Wed Mar 19 2014 James Slagle <jslagle@redhat.com> 0.0.2-4.20140220git
- Add patch 0003-Use-packaged-template-directory.patch
- Add patch 0004-Default-devtest_variables.sh.patch

* Tue Mar 18 2014 James Slagle <jslagle@redhat.com> 0.0.2-3.20140220git
- Add LICENSE and README.md to -doc package

* Thu Mar 13 2014 James Slagle <jslagle@redhat.com> 0.0.2-2.20140220git
- Use _datadir macro instead of _datarootdir
- Correct permissions when creating /usr/bin/tripleo

* Thu Mar 13 2014 James Slagle <jslagle@redhat.com> 0.0.2-1.20140220git
- Move scripts under /usr/libexec/openstack-tripleo
- Add /usr/bin/tripleo wrapper

* Mon Feb 17 2014 James Slagle <jslagle@redhat.com> 0.0.1-1.20140220git
- Updates to spec file to match Fedora packaging guidelines.

* Mon Sep 23 2013 Ryan Brady <rbrady@redhat.com> 0.0.1-1
- Initial RPM build
