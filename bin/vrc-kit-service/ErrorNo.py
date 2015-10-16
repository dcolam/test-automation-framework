'''
Created on 26 juin 2014

@author: decottignies
'''


NONE = 0

INVALID_PARAMETER = 0x1
NO_EPPN = 0x2
UNABLE_TO_LOGIN = 0x3  #  "unable_to_login"   #  "Unable to login"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT_ID = 0x4  #  "no_account_id"   #  "Account ID data not found"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT_FIND = 0x5  #  "no_account"   #  "No account found for this ID"   #  "www.vade-retro.com/fr/")   # 
UNAUTHORIZED = 0x6  #  "unauthorized"   #  "Action not authorized for this account"   #  "www.vade-retro.com/fr/")   #
 
#
# gestion des comptes
#
NO_ACCOUNT_FIRSTNAME = 0x7  #  "no_account_first_name"   #  "Account First Name data not found"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT_LASTNAME = 0x8  #  "no_account_last_name"   #  "Account Last Name data not found"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT_COMPANY = 0x9  #  "no_account_company"   #  "Account Company data not found"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT_EMAIL = 0x10  #  "no_account_email"   #  "Account Email data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_FIRSTNAME = 0x11  #  "no_billing_first_name"   #  "Billing First Name data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_LASTNAME = 0x12  #  "no_billing_last_name"   #  "Billing Last Name data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_COMPANY = 0x13  #  "no_billing_company"   #  "Billing Company data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_LINE1 = 0x14  #  "no_billing_line1"   #  "Billing Line 1 data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_LINE2 = 0x15  #  "no_billing_line2"   #  "Billing Line 2 data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_CITY = 0x16  #  "no_billing_city"   #  "Billing City data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_ZIPCODE = 0x17  #  "no_billing_zipcode"   #  "Billing Zipcode data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_EMAIL = 0x18  #  "no_billing_email"   #  "Billing Email data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_PHONE = 0x19  #  "no_billing_phone"   #  "Billing Phone data not found"   #  "www.vade-retro.com/fr/")   # 
NO_BILLING_FAX = 0x20  #  "no_billing_fax"   #  "Billing Fax data not found"   #  "www.vade-retro.com/fr/")   # 
ALREADY_EXIST = 0x21  #  "account_already_exist"   #  "Account already exist"   #  "www.vade-retro.com/fr/")   # 
EPPN_ALREADY_USED = 0x22  #  "eppn_already_exist"   #  "EPPN already exist"   #  "www.vade-retro.com/fr/")   # 
INVALID_EPPN = 0x23  #  "invalid_eppn"   #  "Invalid EPPN"   #  "www.vade-retro.com/fr/")   # 
NO_USER_ACCOUNT_SELECTED = 0x24  #  "no_user_account_selected"   #  "No user account selected"   #  "www.vade-retro.com/fr/")   #

#
# Gestion des domaines
#
NO_DOMAIN_ID = 0x25  #  "no_domain_id"   #  "Domain ID data not found"   #  "www.vade-retro.com/fr/")   # 
NO_DOMAIN_FIND = 0x26  #  "no_domain_find"   #  "No domain found for this ID"   #  "www.vade-retro.com/fr/")   # 
UNABLE_TO_UPDATE_DOMAIN = 0x27  #  "unable_to_update_domain"   #  "Unable to update domain"   #  "www.vade-retro.com/fr/")   # 
NO_DOMAIN_NAME = 0x28  #  "no_domain_name"   #  "Domain Name data not found"   #  "www.vade-retro.com/fr/")   # 
NO_DOMAIN_CONTACT_ADDRESS = 0x29  #  "no_domain_contact_address"   #  "Domain Contact Address data not found"   #  "www.vade-retro.com/fr/")   # 
DOMAIN_ALREADY_EXIST = 0x30  #  "domain_already_exist"   #  "Domain already exist"   #  "www.vade-retro.com/fr/")   # 
NO_DOMAIN_RELAY = 0x31  #  "no_domain_relay"   #  "Domain relay data not found   #  domain relays are needed"   #  "www.vade-retro.com/fr/")   #

# 
# Gestion des souscriptions
#
UNABLE_TO_ADD_SUBSCRIPTION = 0x32  #  "unable_to_add_subscription"   #  "Unable to add subscription"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_ID = 0x33  #  "subscription_no_id"   #  "Subscription ID data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_REFERENCE = 0x34  #  "subscription_no_reference"   #  "Reference data not found"   #  "www.vade-retro.com/fr/")   # 
NO_ADDRESS = 0x35  #  "subscription_no_address"   #  "Address data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_MAX_DOMAIN = 0x36  #  "subscription_no_max_domain"   #  "Max Domain data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_MAX_ADDRESS = 0x37  #  "subscription_no_max_address"   #  "Max Address data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_DURATION_MODE = 0x38  #  "subscription_no_duration_mode"   #  "Duration Mode data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_DURATION_UNITS = 0x39  #  "subscription_no_duration_units"   #  "Duration Unit data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_HEURISTIC_ANTIVIRUS = 0x40  #  "subscription_no_heuristic_antivirus"   #  "Heuristic Antivirus data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_EXTERNAL_ANTIVIRUS = 0x41  #  "subscription_no_external_antivirus"   #  "External Antivirus data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_ADVERTISING_FILTERING = 0x42  #  "subscription_no_avertising_filtering"   #  "Advertising Filtering data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_OUTBOUND_FILTERING = 0x43  #  "subscription_no_outbound_filtering"   #  "Outbound filtering data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NOT_FOUND = 0x44  #  "subscription_not_found"   #  "Subscription not found for this ID"   #  "www.vade-retro.com/fr/")   # 
ONLY_SYSTEM_ACCOUNT = 0x45  #  "only_system_account"   #  "Only system account can add/update this data"   #  "www.vade-retro.com/fr/")   # 
UNABLE_TO_UPDATE_SUBSCRIPTION = 0x46  #  "unable_to_update_subscription"   #  "Unable to update subscription"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_MISSING = 0x47  #  "subscription_missing"   #  "Subscription Data not found"   #  "www.vade-retro.com/fr/")   # 
SUBSCRIPTION_NO_TEMPLATE_ID = 0x48  #  "subscription_no_template_id"   #  "Template ID of Subscription Data not found"   #  "www.vade-retro.com/fr/")   # 
UNABLE_TO_ADD_DOMAIN = 0x49  #  "unable_to_add_domain"   #  "Unable to add domain"   #  "www.vade-retro.com/fr/")   # 
NO_ACCOUNT = 0x50  #  "no_account"   #  "Account data not found"   #  "www.vade-retro.com/fr/")   # 
UNABLE_TO_UPDATE_ACCOUNT = 0x51  #  "unable_to_update_account"   #  "Unable to update account"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_DESCRIPTION = 0x52  #  "ldap_no_description"   #  "No description for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_SERVERNAME = 0x53  #  "ldap_no_servername"   #  "No servername for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_PORT = 0x54  #  "ldap_no_port"   #  "No port for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_SEARCHBASE = 0x55  #  "ldap_no_searchbase"   #  "No Searchbase for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_LOGIN = 0x56  #  "ldap_no_login"   #  "No Login for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_PASSWORD = 0x57  #  "ldap_no_password"   #  "No Password for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_RESULTATTRIBUTE = 0x58  #  "ldap_no_resultattribute"   #  "No Resultattribute for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_TIMEOUT = 0x59  #  "ldap_no_timeout"   #  "No Timeout for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_OTHERS = 0x60  #  "ldap_no_others"   #  "No Others for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_WEIGHT = 0x61  #  "ldap_no_weight"   #  "No Weight for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_SEARCHFILTER = 0x62  #  "ldap_no_searchfilter"   #  "No SearchFilter for LDAP"   #  "www.vade-retro.com/fr/")   # 
LDAP_NO_ID = 0x63  #  "ldap_no_id"   #  "No ID for LDAP"   #  "www.vade-retro.com/fr/")   # 
NO_LDAP = 0x64  #  "no_ldap"   #  "LDAP not found"   #  "www.vade-retro.com/fr/")   # 

#
#  server error
#
NOT_YET_IMPLEMENTED = 0x100  # "no_method"   #  "method not yet implemented"   #  "www.vade-retro.com/fr/")   # 
INTERNAL_ERROR = 0x101  # "internal_error"   #  "internal_error"   #  "www.vade-retro.com/fr/");
