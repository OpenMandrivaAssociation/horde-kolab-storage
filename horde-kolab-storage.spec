%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary:	A package for handling Kolab data stored on an IMAP server
Name: 		horde-kolab-storage
Version:	0.5.0
Release:	6
License:	LGPLv2.1+
Group:		Networking/Mail
Url: 		http://pear.horde.org/package/Kolab_Storage
Source0:	http://pear.horde.org/get/Kolab_Storage-%{version}.tgz
BuildRequires:	php-pear >= 1.4.7
BuildRequires: 	php-pear-channel-horde
Requires:	php-pear-Net_IMAP >= 1.1.0
Requires:	php-pear-Mail_mimeDecode
Requires:	php-pear-HTTP_Request
Requires:	horde-kolab-format
Requires:	horde-kolab-server
Requires:	php-pear-Auth >= 0.1.1
Requires:	horde-cache
Requires:	horde-group
Requires:	horde-history
Requires:	horde-ldap
Requires:	horde-perms
Requires:	horde-sessionobjects
Requires:	horde-mime
Requires:	horde-nls
Requires:	horde-util
Requires:	php-pear >= 1.4.0b1
Requires: 	php-pear-channel-horde
BuildArch:	noarch

%description
Storing user data in an IMAP account belonging to the user is one of the Kolab
server core concepts. This package provides  all the necessary means to deal
with this type of data storage effectively.

%files
%doc docs/Kolab_Storage/*
%{peardir}/*
%{xmldir}/Kolab_Storage.xml

%post
pear install --nodeps --soft --force --register-only %{xmldir}/Kolab_Storage.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/Kolab_Storage
fi

#----------------------------------------------------------------------------

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}

# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock

mv %{buildroot}/docs .

# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/Kolab_Storage.xml

