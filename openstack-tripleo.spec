%global commit d81bd6d00683870af9add7a45e54a47598563ccd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global alphatag .%{shortcommit}git
%global project tripleo-incubator

Name:             openstack-tripleo
Version:          0.0.8
Release:          0.1%{alphatag}%{?dist}
Summary:          OpenStack TripleO

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/TripleO
Source0:          https://github.com/openstack/%{project}/archive/%{commit}.tar.gz#/%{project}-%{commit}.tar.gz
Source1:          tripleo
Patch0001:        0001-Use-packaged-template-directory-path.patch

BuildArch:        noarch

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
Requires:         jq

#
# patches_base=c3fb309727671130a32b4c19de48ec22c8530aa1
#

%description
TripleO is a program aimed at installing, upgrading and operating OpenStack
clouds using OpenStack's own cloud facilities as the foundations - building on
nova, neutron and heat to automate fleet management at datacenter scale.

%package doc
Summary:          Documentation for OpenStack TripleO
BuildRequires:    python-sphinx
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch


%description    doc
TripleO is a program aimed at installing, upgrading and operating OpenStack
clouds using OpenStack's own cloud facilities as the foundations - building on
nova, neutron and heat to automate fleet management at datacenter scale.

This package contains documentation files for TripleO.

%prep
%setup -q -n %{project}-%{commit}

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
%license LICENSE
%doc README.rst
%{_bindir}/*
%{_libexecdir}/%{name}
# These config files are *not* noreplace. They aren't meant to be edited by
# users.
%config %{_sysconfdir}/tripleo
%{_datadir}/tripleo

%files doc
%{_datadir}/doc/tripleo

%changelog
* Fri Apr  1 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.0.8-0.1.d81bd6dgit
- Upstream Mitaka RC1

