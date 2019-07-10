%global __requires_exclude perl\\(.*\\)
Summary:        Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.
Name:           net-snmp
Version:        5.7.3
Release:        11%{?dist}
License:        BSD (like)
URL:            http://net-snmp.sourceforge.net/
Group:          Productivity/Networking/Other
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 net-snmp=97dc25077257680815de44e34128d365c76bd839
Source1:        snmpd.service
Source2:        snmptrapd.service
Patch1:         net-snmp-5.7.2-systemd.patch
Patch2:         net-snmp-remove-u64-typedef.patch
Patch3:         net-snmp-fix-perl-module-compilation.patch
Patch4:         net-snmp-CVE-2018-1000116.patch
Patch5:         net-snmp-CVE-2018-18065.patch
BuildRequires:  openssl-devel perl systemd
Requires:       perl systemd
%description
 Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.

%package devel
Group: Development/Libraries
Summary: The includes and static libraries from the Net-SNMP package.
Requires: net-snmp = %{version}

%description devel
The net-snmp-devel package contains headers and libraries for building SNMP applications.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
./configure --prefix=%{_prefix} \
                --host=ia64-linux \
                --build=i686 \
                --target=ia64-linux \
                --sbindir=/sbin \
                --sysconfdir=%{_sysconfdir} \
                --with-sys-location="unknown" \
                --with-logfile=/var/log/net-snmpd.log \
                --with-persistent-directory=/var/lib/net-snmp \
                --with-sys-contact="root@localhost" \
                --with-defaults \
                --with-systemd \
                --disable-static \
                --with-x=no \
                --enable-as-needed
make

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
install -m 0644 %{SOURCE1} %{buildroot}/lib/systemd/system/snmpd.service
install -m 0644 %{SOURCE2} %{buildroot}/lib/systemd/system/snmptrapd.service

%check
make %{?_smp_mflags} test

%post
if [ $1 == 2 ]; then
  # Upgrading net-snmp, preserve the existing config in /usr/etc/snmp
  if [ -d /usr/etc/snmp -a ! -e %{_sysconfdir}/snmp ]; then
    ln -sf /usr/etc/snmp %{_sysconfdir}/snmp
  fi
fi
/sbin/ldconfig
%systemd_post snmpd.service
%systemd_post snmptrapd.service

%preun
%systemd_preun snmpd.service
%systemd_preun snmptrapd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart snmpd.service
%systemd_postun_with_restart snmptrapd.service

%clean
rm -rf %{buildroot}/*
 
%files
%doc COPYING NEWS README ChangeLog
%defattr(-,root,root)
/lib/systemd/system/snmpd.service
/lib/systemd/system/snmptrapd.service
%{_bindir}
%{_libdir}/*.so.*
/sbin/*  
%ghost %config(noreplace) %{_sysconfdir}/snmp/*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.la
%{_libdir}/perl5
%{_libdir}/*.so
%{_datadir}
%exclude /usr/lib/perl5/5.22.1/*/perllocal.pod
%exclude /usr/lib/perl5/5.24.1/*/perllocal.pod

%changelog
*   Wed Feb 20 2019 Dweep Advani <dadvani@vmware.com> 5.7.3-11
-   Fixed snmpd.conf path
*   Mon Dec 31 2018 Ankit Jain <ankitja@vmware.com> 5.7.3-10
-   Fix for CVE-2018-18065
*   Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> 5.7.3-9
-   Excluded perllocal.pod for aarch64
*   Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.3-8
-   Apply patch for CVE-2018-1000116
*   Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.7.3-7
-   Make service file a different source
*   Tue Apr 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.7.3-6
-   Patch to remove U64 typedef
*   Tue Oct 04 2016 ChangLee <changLee@vmware.com> 5.7.3-5
-   Modified %check
*   Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-4
-   Excluded the perllocal.pod log.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.7.3-3
-   GA - Bump release of all rpms
*   Wed May 04 2016 Nick Shi <nshi@vmware.com> 5.7.3-2
-   Add snmpd and snmptrapd to systemd service.
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-1
-   Initial build.  First version
