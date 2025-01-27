# Please handle this spec with care, As this a custom spec file created
# for podman so it should be manually upgraded when required. Because
# it has specific files from multiple repos as mention in spec comment
# section itself. Also whenever upgrading podman please check the
# compaitable version of containers-common and upgrade this by picking
# the required files like below.
# Clone containers sub repo common, image, shortnames, skopeo and storage
# Checkout to specific tag for all sub repo & pick the files as per requirment
# Move those files into directory & create tarball
#
# For example:
# git clone git@github.com:containers/common.git
# cd common && git checkout -b v1.0.1 tags/v1.0.1
# cp pkg/config/containers.conf pkg/seccomp/seccomp.json pkg/subscriptions/mounts.conf ../containers-common-2/
#
# git clone git@github.com:containers/image.git
# cd image && git checkout -b v5.23.1 tags/v5.23.1
# cp registries.conf ../containers-common-2/
#
# git clone git@github.com:containers/shortnames.git
# cd shortnames && git checkout -b v2022.02.08 tags/v2022.02.08
# cp shortnames.conf ../containers-common-2/
#
# git clone git@github.com:containers/skopeo.git
# cd skopeo && git checkout -b v1.10.0 tags/v1.10.0
# cp default.yaml default-policy.json ../containers-common-2/
#
# git clone git@github.com:containers/storage.git
# cd storage && git checkout -b v1.44.0 tags/v1.44.0
# cp storage.conf ../containers-common-2/
#
# cd .. && tar czf containers-common-2.tar.gz containers-common-2

Summary:        Common configuration and documentation for containers
Name:           containers-common
Version:        3
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/containers
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=74c42f76794998e27b015bb1fe3123df7aa626628753efa003916fedbd6da8a12df52fa420c035555cd4fc4d3e76eae529c2c2092b87ca99646c572c4df345ee
Group:          Tools/Podman
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Requires:       fuse-overlayfs
Requires:       selinux-policy
Requires:       cni

%description
This package contains common configuration files and documentation for container
tools ecosystem, such as Podman, Buildah and Skopeo.It is required because the most
of configuration files and docs come from projects which are vendored into Podman,
Buildah, Skopeo, etc. but they are not packaged separately.

%prep
%autosetup -n %{name}-%{version}
cp shortnames.conf  000-shortnames.conf
cp default-policy.json policy.json

%install
# install config and policy files for registries
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d}
install -dp %{buildroot}%{_sharedstatedir}/containers/sigstore
install -Dp -m0644 default.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d
install -Dp -m0644 storage.conf -t %{buildroot}%{_datadir}/containers
install -Dp -m0644 registries.conf -t %{buildroot}%{_sysconfdir}/containers
install -Dp -m0644 000-shortnames.conf -t %{buildroot}%{_sysconfdir}/containers/registries.conf.d
install -Dp -m0644 policy.json -t %{buildroot}%{_sysconfdir}/containers

# install config files for mounts, containers and seccomp
install -m0644 mounts.conf %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 seccomp.json %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 containers.conf %{buildroot}%{_datadir}/containers/containers.conf

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%dir %{_sysconfdir}/containers/registries.d
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%ghost %{_sysconfdir}/containers/storage.conf
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%dir %{_datadir}/containers
%{_datadir}/containers/storage.conf
%{_datadir}/containers/containers.conf
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%changelog
* Sun Feb 12 2023 Piyush Gupta <gpiyush@vmware.com> 3-1
- Version upgrade to v3
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 2-1
- Version upgrade to v2
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1-2
- Bump version as a part of cni upgrade
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1-1
- Initial version
