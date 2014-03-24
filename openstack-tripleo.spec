%global commit d305ad25f2538d829465092146de5cdfb4a803d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global alphatag 20140220git
%global repo_name tripleo-incubator

Name:			openstack-tripleo
Version:		0.0.2
Release:		4.%{alphatag}%{?dist}
Summary:		OpenStack TripleO

Group:			Applications/System
License:		ASL 2.0
URL:			https://wiki.openstack.org/wiki/TripleO
Source0:		https://github.com/openstack/%{repo_name}/archive/%{commit}.tar.gz
Source1:		tripleo

# Upstream patch: https://review.openstack.org/#/c/74452/
Patch0001:		0001-Add-shebang.patch
# Upstream switched to oslosphinx in https://review.openstack.org/#/c/73353/,
# but that does not yet exist in Fedora.
Patch0002:		0002-Switch-back-to-oslo.sphinx.patch
Patch0003:		0003-Use-packaged-template-directory.patch
Patch0004:		0004-Default-devtest_variables.sh.patch

BuildArch:		noarch

BuildRequires:		python-sphinx
BuildRequires:		python-oslo-sphinx

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
%setup -q -n %{repo_name}-%{commit}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1

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

# libvirt templates
install -d -m 755 %{buildroot}/%{_datadir}/tripleo/libvirt-templates
install -p -m 644 -t %{buildroot}/%{_datadir}/tripleo/libvirt-templates libvirt-templates/*

# documentation
sphinx-build -b html doc/source doc/build/html
install -d -m 755 %{buildroot}%{_datadir}/doc/tripleo/html
cp -r doc/build/html/* %{buildroot}%{_datadir}/doc/tripleo/html

%files
%doc LICENSE README.md
%{_bindir}/*
%{_libexecdir}/%{name}
# These config files are *not* noreplace. They aren't meant to be edited by
# users.
%config %{_sysconfdir}/tripleo
%{_datadir}/tripleo

%files doc
%doc LICENSE README.md
%{_datadir}/doc/tripleo

%changelog
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
