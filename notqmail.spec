%undefine _missing_build_ids_terminate_build
%global _unpackaged_files_terminate_build 1

%define nq_docdir          %{_docdir}/%{name}
%if %{defined _project}
# define build_on_obs if building on openSUSE build service
%global build_on_obs       1
%else
%define _project           local
%global build_on_obs       0
%global _hardened_build    1
%endif
%global qmaildir           /var/qmail
#log directory if we use multilog in supervise scripts
%global logdir             /var/log/svc
%global see_base           For a description of notqmail visit https://notqmail.org/

Name: notqmail
Version: 1.08
Release: 1.1%{?dist}
Summary: A community driven fork of qmail
License: CC-PDDC
URL: https://notqmail.org
Source0: https://github.com/notqmail/notqmail/releases/download/notqmail-1.08/notqmail-1.08.tar.xz
%if 0%{?suse_version} >= 1120
Source1: %{name}-permissions.easy
Source2: %{name}-permissions.secure
Source3: %{name}-permissions.paranoid
%endif
Group: System Environment/Base
#Group: Productivity/Networking/Email/Servers
BuildRequires: rpm gcc make coreutils
BuildRequires: glibc glibc-devel

%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version}
Requires(pre): shadow-utils
Requires(postun): shadow-utils
%endif
%if 0%{?suse_version} || 0%{?sles_version}
Requires(pre): pwdutils
Requires(postun): pwdutils
%endif

%if %build_on_obs == 1
BuildRequires: -post-build-checks
%endif

Requires: /usr/sbin/useradd /usr/sbin/userdel /usr/sbin/groupadd /usr/sbin/groupdel
Requires: /sbin/chkconfig procps
Requires: coreutils /bin/sh glibc
%if "%{?_unitdir}" == ""
Requires: initscripts
%endif
%if 0%{?suse_version} >= 1120
PreReq: permissions
%endif

Provides: user(alias)       > 999
Provides: user(qmaild)      > 999
Provides: user(qmaill)      > 999
Provides: user(qmailp)      > 999
Provides: user(qmailq)      > 999
Provides: user(qmailr)      > 999
Provides: user(qmails)      > 999
Provides: group(nofiles)    > 999
Provides: group(qmail)      > 999
Provides: smtp_daemon

%if %build_on_obs == 1
BuildRoot: %{_tmppath}/%{name}-%{version}-build
%endif

%description
notqmail is a community-driven fork of qmail, beginning where netqmail
left off: providing stable, compatible, small releases to which existing
qmail users can safely update.
notqmail also aims higher: developing an extensible, easily packaged, and
increasingly useful modern mail server.

%package doc
Summary: Documentations for the %{name} package
%if %{undefined suse_version} && %{undefined sles_version}
Group: System Environment/Base
%else
Group: Productivity/Networking/Email/Servers
%endif
Requires: notqmail
BuildArch: noarch

%description doc
notqmail is a community-driven fork of qmail, beginning where netqmail
left off: providing stable, compatible, small releases to which existing
qmail users can safely update.
notqmail also aims higher: developing an extensible, easily packaged, and
increasingly useful modern mail server.
This package contains the documentation for %{name}

%{see_base}

%prep
%setup
yum install systemd -y
%build

conf_cc=`head -1 conf-cc`
echo "$conf_cc -g -fPIC" > conf-cc
echo "cc -fPIE -pie"     > conf-ld
make it man NROFF=true

%install
env DESTDIR=%{buildroot} ./instpackage
%{__rm} -rf %{buildroot}%{qmaildir}/man/man3 %{buildroot}%{qmaildir}/man/cat*
%{__mkdir_p} %{buildroot}%{_mandir}
%{__mkdir_p} %{buildroot}%{nq_docdir}
mv %{buildroot}%{qmaildir}/man/man? %{buildroot}%{_mandir}
mv %{buildroot}%{qmaildir}/doc/* %{buildroot}%{nq_docdir}
%{__cp} COPYRIGHT %{buildroot}%{nq_docdir}
rmdir --ignore-fail-on-non-empty %{buildroot}%{qmaildir}/doc
rmdir --ignore-fail-on-non-empty %{buildroot}%{qmaildir}/man
%if 0%{?suse_version} >= 1120
  %{__mkdir_p} %{buildroot}%{_sysconfdir}/permissions.d/
  install -m 644 %{S:1} %{buildroot}%{_sysconfdir}/permissions.d/%{name}-permissions
  install -m 644 %{S:2} %{buildroot}%{_sysconfdir}/permissions.d/%{name}-permissions.secure
%endif
%if "%{?_unitdir}" != ""
  make qmail-send.service
  %{__mkdir_p} %{buildroot}%{_unitdir}
  install -m 644 qmail-send.service %{buildroot}%{_unitdir}/%{name}.service
%endif
rm -f %{buildroot}%{qmaildir}/bin/{qail,elq,pinq,maildirwatch,qsmhook}

%files
%defattr(-, root, root,-)
%dir %attr(755,root,qmail)        %{qmaildir}
%dir %attr(755,root,qmail)        %{qmaildir}/bin
%dir %attr(755,root,qmail)        %{qmaildir}/boot
%dir %attr(755,root,qmail)        %{qmaildir}/control
%dir %attr(755,root,qmail)        %{qmaildir}/users
%dir %attr(2755,alias,qmail)      %{qmaildir}/alias
%dir %attr(750,qmailq,qmail)      %{qmaildir}/queue
%dir %attr(700,qmails,qmail)      %{qmaildir}/queue/bounce
     %attr(700,qmails,qmail)      %{qmaildir}/queue/info
%dir %attr(700,qmailq,qmail)      %{qmaildir}/queue/intd
     %attr(700,qmails,qmail)      %{qmaildir}/queue/local
%dir %attr(750,qmailq,qmail)      %{qmaildir}/queue/lock
%attr(600,qmails,qmail)           %{qmaildir}/queue/lock/sendmutex
%attr(644,qmailr,qmail)           %{qmaildir}/queue/lock/tcpto
%attr(622,qmails,qmail)           %{qmaildir}/queue/lock/trigger
     %attr(750,qmailq,qmail)      %{qmaildir}/queue/mess
%dir %attr(700,qmailq,qmail)      %{qmaildir}/queue/pid
     %attr(700,qmails,qmail)      %{qmaildir}/queue/remote
%dir %attr(750,qmailq,qmail)      %{qmaildir}/queue/todo
%attr(0700,root,qmail)            %{qmaildir}/bin/qmail-lspawn
%attr(0711,root,qmail)            %{qmaildir}/bin/splogger
%attr(0755,root,qmail)            %{qmaildir}/bin/preline
%attr(0700,root,qmail)            %{qmaildir}/bin/qmail-newu
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-popup
%attr(0755,root,qmail)            %{qmaildir}/bin/qreceipt
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-showctl
%attr(0755,root,qmail)            %{qmaildir}/bin/maildir2mbox
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-qread
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-getpw
%attr(0755,root,qmail)            %{qmaildir}/bin/bouncesaying
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-smtpd
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-inject
%attr(0755,root,qmail)            %{qmaildir}/bin/sendmail
%attr(0755,root,qmail)            %{qmaildir}/bin/except
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-pop3d
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-clean
%attr(0755,root,qmail)            %{qmaildir}/bin/qbiff
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-qstat
%attr(0755,root,qmail)            %{qmaildir}/bin/mailsubj
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-tcpok
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-tcpto
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-qmtpd
%attr(0700,root,qmail)            %{qmaildir}/bin/qmail-start
%attr(0755,root,qmail)            %{qmaildir}/bin/maildirmake
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-qmqpd
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-pw2u
%attr(0755,root,qmail)            %{qmaildir}/bin/datemail
%attr(0700,root,qmail)            %{qmaildir}/bin/qmail-newmrh
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-local
%attr(0755,root,qmail)            %{qmaildir}/bin/predate
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-send
%attr(0755,root,qmail)            %{qmaildir}/bin/forward
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-rspawn
%attr(0755,root,qmail)            %{qmaildir}/bin/qmail-qmqpc
%attr(0755,root,qmail)            %{qmaildir}/bin/condredirect
%attr(0755,root,qmail)            %{qmaildir}/bin/tcp-env
%attr(0711,root,qmail)            %{qmaildir}/bin/qmail-remote

%attr(0755,root,qmail)            %{qmaildir}/boot/proc+df
%attr(0755,root,qmail)            %{qmaildir}/boot/proc
%attr(0755,root,qmail)            %{qmaildir}/boot/home
%attr(0755,root,qmail)            %{qmaildir}/boot/binm2+df
%attr(0755,root,qmail)            %{qmaildir}/boot/binm3
%attr(0755,root,qmail)            %{qmaildir}/boot/home+df
%attr(0755,root,qmail)            %{qmaildir}/boot/binm1
%attr(0755,root,qmail)            %{qmaildir}/boot/binm2
%attr(0755,root,qmail)            %{qmaildir}/boot/binm1+df
%attr(0755,root,qmail)            %{qmaildir}/boot/binm3+df
%if "%{?_unitdir}" != ""
                                  %{_unitdir}/%{name}.service
%endif

%if 0%{?suse_version} >= 1120
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/permissions.d/%{name}-permissions
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/permissions.d/%{name}-permissions.secure
%verify (not user group mode caps) %attr(4711, qmailq, qmail)   %{qmaildir}/bin/qmail-queue
%else
%attr(4711,qmailq,qmail)           %{qmaildir}/bin/qmail-queue
%endif

%files doc
%defattr(-, root, root,-)
%dir %attr(0755,root,root) %{nq_docdir}
     %attr(0644,root,root) %{nq_docdir}/*
%attr(0644,root,root) %{_mandir}/man?/*%{?ext_man}

### SCRIPTLETS ###############################################################################
%verifyscript
%if 0%{?suse_version} >= 1120
  %verify_permissions -e %{qmaildir}/bin/qmail-queue
  %verify_permissions -e %{qmaildir}/alias/
  %verify_permissions -e %{qmaildir}/queue/lock/trigger
%endif

%pretrans
argv1=$1
if test -f %{_sysconfdir}/systemd/system/multi-user.target.wants/%{name}.service
then
  echo "Giving %{name} exactly 5 seconds to exit nicely"
  /bin/systemctl stop %{name} > /dev/null 2>&1
fi
sleep 5

%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?suse_version} < 1500 || 0%{?sles_version} < 15
%pre
  /usr/bin/getent group nofiles   > /dev/null || /usr/sbin/groupadd nofiles
  /usr/bin/getent group qmail     > /dev/null || /usr/sbin/groupadd qmail
  /usr/bin/getent passwd alias    > /dev/null || /usr/sbin/useradd -M -g nofiles  -d %{qmaildir}/alias  -s /sbin/nologin alias
  /usr/bin/getent passwd qmaild   > /dev/null || /usr/sbin/useradd -M -g nofiles  -d %{qmaildir}        -s /sbin/nologin qmaild
  /usr/bin/getent passwd qmaill   > /dev/null || /usr/sbin/useradd -M -g nofiles  -d %{logdir}          -s /sbin/nologin qmaill
  /usr/bin/getent passwd qmailp   > /dev/null || /usr/sbin/useradd -M -g nofiles  -d %{qmaildir}        -s /sbin/nologin qmailp
  /usr/bin/getent passwd qmailq   > /dev/null || /usr/sbin/useradd -M -g qmail    -d %{qmaildir}        -s /sbin/nologin qmailq
  /usr/bin/getent passwd qmailr   > /dev/null || /usr/sbin/useradd -M -g qmail    -d %{qmaildir}        -s /sbin/nologin qmailr
  /usr/bin/getent passwd qmails   > /dev/null || /usr/sbin/useradd -M -g qmail    -d %{qmaildir}        -s /sbin/nologin qmails
for i in alias qmaild qmaill qmailp qmailq qmailr qmails
do
  %{__rm} -f /var/spool/mail/$i
done
%else
%pre -f notqmail.pre
%endif
%if 0%{?suse_version} || 0%{?sles_version}
  %service_add_pre %{name}.service
%endif

### SCRIPTLET ###############################################################################
%post
%if 0%{?suse_version} >= 1120
%if 0%{?set_permissions:1} > 0
  %set_permissions %{qmaildir}/bin/qmail-queue
  %set_permissions %{qmaildir}/alias/
%else
  %run_permissions
%endif
%endif
%if 0%{?suse_version} || 0%{?sles_version}
  %service_add_post %{name}.service
%endif

if [ ! -f %{qmaildir}/control/me ] ; then
	uname -n > %{qmaildir}/control/me
fi

# setup notqmail as alternative mta
alternatives --install /usr/sbin/sendmail mta %{qmaildir}/bin/sendmail 120 \
  --slave /usr/lib/sendmail mta-sendmail %{qmaildir}/bin/sendmail

# Create aliases if they do not exist
%{__mkdir_p}  %{qmaildir}/alias/Maildir/new
%{__mkdir_p}  %{qmaildir}/alias/Maildir/cur
%{__mkdir_p}  %{qmaildir}/alias/Maildir/tmp
chown -R alias:qmail %{qmaildir}/alias/Maildir
for i in postmaster mailer-daemon root
do
  if [ ! -f %{qmaildir}/alias/.qmail-"$i" ] ; then
    echo "%{qmaildir}/alias/Maildir/" > %{qmaildir}/alias/.qmail-"$i"
  fi
done

### SCRIPTLET ###############################################################################
%preun
argv1=$1
if [ -z "$argv1" ] ; then
  argv1=0
fi
# we are doing upgrade
if [ $argv1 -eq 1 ] ; then
  exit 0
fi
%if 0%{?suse_version} || 0%{?sles_version}
  %service_del_preun %{name}.service
%endif

### SCRIPTLET ###############################################################################
%postun
argv1=$1
if [ -z "$argv1" ] ; then
  argv1=0
fi
# we are doing upgrade
if [ $argv1 -eq 1 ] ; then
  exit 0
fi
%if 0%{?suse_version} || 0%{?sles_version}
  %service_del_postun %{name}.service
%endif
alternatives --remove mta %{qmaildir}/bin/sendmail
alternatives --auto mta
# remove users / groups
for i in alias qmaild qmaill qmailp qmailq qmailr qmails
do
  echo "Removing user $i"
  /usr/bin/getent passwd $i > /dev/null && /usr/sbin/userdel $i >/dev/null || true
done
for i in nofiles qmail
do
  echo "Removing group $i"
  /usr/bin/getent group $i > /dev/null && /usr/sbin/groupdel $i  >/dev/null || true
done

for i in postmaster mailer-daemon root
do
  %{__rm} -f %{qmaildir}/alias/.qmail-"$i"
done
%{__rm} -rf %{qmaildir}/alias/Maildir

### SCRIPTLET ###############################################################################
%posttrans
argv1=$1
