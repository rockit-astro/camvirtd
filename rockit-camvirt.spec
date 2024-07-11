Name:      rockit-camvirt
Version:   %{_version}
Release:   1
Summary:   Data pipeline
Url:       https://github.com/rockit-astro/camvirtd
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/camvirtd/

%{__install} %{_sourcedir}/camvirtd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/camvirtd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/camvirt %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/camvirt %{buildroot}/etc/bash_completion.d/camvirt

%{__install} %{_sourcedir}/config/clasp_das.json %{buildroot}%{_sysconfdir}/camvirtd
%{__install} %{_sourcedir}/config/clasp_tcs.json %{buildroot}%{_sysconfdir}/camvirtd
%{__install} %{_sourcedir}/config/sting_das1.json %{buildroot}%{_sysconfdir}/camvirtd
%{__install} %{_sourcedir}/config/sting_das2.json %{buildroot}%{_sysconfdir}/camvirtd

%package server
Summary:  Camera VM management server
Group:    Unspecified
Requires: python3-rockit-camvirt python3-libvirt python3-astropy

%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/camvirtd
%defattr(0644,root,root,-)
%{_unitdir}/camvirtd@.service

%package client
Summary:  Camera VM management client
Group:    Unspecified
Requires: python3-rockit-camvirt

%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/camvirt
/etc/bash_completion.d/camvirt

%package data-clasp
Summary: Camera VM configuration for CLASP telescope.
Group:   Unspecified
%description data-clasp

%files data-clasp
%defattr(0644,root,root,-)
%{_sysconfdir}/camvirtd/clasp_das.json
%{_sysconfdir}/camvirtd/clasp_tcs.json

%package data-sting
Summary: Camera VM configuration for the STING telescope.
Group:   Unspecified
%description data-sting

%files data-sting
%defattr(0644,root,root,-)
%{_sysconfdir}/camvirtd/sting_das1.json
%{_sysconfdir}/camvirtd/sting_das2.json

%changelog
