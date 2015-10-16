#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-#
#
# VRC - VadeRetro Technology - Copyright 2013
#
# Python sample using the VadeRetro Cloud Rest Client API
# Json in/out entities
# 
# $LastChangedDate:$
# $Rev:$
#
import io
import json
import pickle
import jsonpickle

def strbool(s):
    if str(s).lower() == 'true':
        return True
    return False

class Error(object):
    def __init__(self, data=None):
        self.setDefault()         
        self.explore(data)
        
    def setDefault(self):
        self.errno = 0
        self.message = ''
        self.parameter = ''
        self.url = ''
                
    def explore(self, data):
        if data is None:
            return
        self.errno = int(data['errno'])
        self.message = str(data['message'])
        self.parameter = str(data['parameter'])
        self.url = str(data['url'])

    def getErrorNo(self):
        return self.errno
    
    def getMessage(self):
        return self.message
    
    def getParameter(self):
        return self.message
    
    def getDocumentationUrl(self):
        return self.url
    def __str__(self):
        return "error %d: %s (parameter: %s)" % (self.errno, str(self.message), str(self.parameter))
        
        
#
# ADDRESS
# 
class Address:
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
    
    def getFirstName(self):
        return self.account_first_name
      
    def setFirstName(self, value):
        self.account_first_name = value
    
    def setLastName(self, value):
        self.account_last_name = value
        
    def getLastName(self):
        return self.account_last_name
    
    def getCompany(self):
        return self.account_company    

    def setCompany(self, value):
        self.account_company = value

    def getAccountEmail(self):
        return self.account_email

    def setAccountEmail(self, value):
        self.account_email = value

    def getBillingPhone(self):
        return self.billing_phone 

    def setBillingPhone(self, value):
        self.billing_phone = value

    def getBillingEmail(self):
        return self.billing_email

    def setBillingEmail(self, value):
        self.billing_email = value
    
    def getBillingZipCode(self):
        return self.billing_zipcode

    def setBillingZipCode(self, value):
        self.billing_zipcode = value

    def getBillingCity(self):
        return self.billing_city

    def setBillingCity(self, value):
        self.billing_city = value

    def getBillingCountry(self):
        return self.billing_city

    def setBillingCoountry(self, value):
        self.billing_city = value

    def getBillingAddr1(self):        
        return self.billing_line1

    def setBillingAddr1(self, value):
        self.billing_line1 = value

    def getBillingAddr2(self):        
        return self.billing_line2

    def setBillingAddr2(self, value):
        self.billing_line2 = value

    def getBillingCompany(self):        
        return self.billing_company

    def setBillingCompany(self, value):
        self.billing_company = value 

    def getBillingFirstName(self):        
        return self.billing_first_name

    def setBillingFirstName(self, value):
        self.billing_first_name = value 

    def getBillingLastName(self):        
        return self.billing_last_name

    def setBillingLastName(self, value):
        self.billing_last_name = value 

    def setDefault(self):        
        self.account_first_name = ''
        self.account_last_name = ''        
        self.account_company = ''
        self.account_email = ''
        self.address_line1 = ''                
        self.address_line2 = ''                
        self.address_line3 = ''                
        self.address_line4 = ''
        self.address_city = ''
        self.address_zipcode = ''
        self.address_country = ''
        self.address_phone = ''
        self.address_fax = ''
        self.billing_first_name = ''
        self.billing_last_name = '' 
        self.billing_company = ''
        self.billing_line1 = ''   
        self.billing_line2 = ''   
        self.billing_city = ''    
        self.billing_zipcode = '' 
        self.billing_country = '' 
        self.billing_email = ''  
        self.billing_phone = ''  
        self.billing_fax = ''

    def explore(self, data):
        if data is None:
            return        
        if 'account_first_name' in data:                
           self.account_first_name = str(data['account_first_name'])

        if 'account_last_name' in data:
           self.account_last_name = str(data['account_last_name'])
      
        if 'account_company' in data: 
           self.account_company = str(data['account_company'])
        
        if 'account_email' in data: 
           self.account_email = str(data['account_email'])
        
        if 'address_line1' in data:        
            self.address_line1 = str(data['address_line1'])
            
        if 'address_line2' in data:                
            self.address_line2 = str(data['address_line2'])
            
        if 'address_line3' in data:                                    
            self.address_line3 = str(data['address_line3'])
            
        if 'address_line4' in data:            
            self.address_line4 = str(data['address_line4'])

        if 'address_city' in data:            
            self.address_city = str(data['address_city'])
            
        if 'address_zipcode' in data:
            self.address_zipcode = str(data['address_zipcode'])
        
        if 'address_country' in data:    
            self.address_country = str(data['address_country'])
            
        if 'address_phone' in data:
            self.address_phone = str(data['address_phone'])
                    
        if 'address_fax' in data:
            self.address_fax = str(data['address_fax'])
            
        if 'billing_first_name' in data:
            self.billing_first_name = str(data['billing_first_name'])
            
        if 'billing_last_name' in data:
            self.billing_last_name = str(data['billing_last_name'])
             
        if 'billing_company' in data:
            self.billing_company = str(data['billing_company'])
            
        if 'billing_line1' in data:
            self.billing_line1 = str(data['billing_line1'])
               
        if 'billing_line2' in data:
            self.billing_line2 = str(data['billing_line2'])
            
        if 'billing_city' in data:   
            self.billing_city = str(data['billing_city'])
                
        if 'billing_zipcode' in data:
            self.billing_zipcode = str(data['billing_zipcode'])
    
        if 'billing_country' in data:
            self.billing_country = str(data['billing_country'])
             
        if 'billing_email' in data:
            self.billing_email = str(data['billing_email'])
              
        if 'billing_phone' in data:
            self.billing_phone = str(data['billing_phone'])
          
        if 'billing_fax' in data:
            self.billing_fax = str(data['billing_fax'])
    
    def __repr__(self):
        return """
        first name: %s\n
        last name: %s\n
        """ % (str(self.account_first_name), str(self.account_last_name))
    

#
# SUBSCRIPTION
#       
class Subscription:
    
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):                
        self.subscription_id = 0
        self.reference = ''        
        self.duration_units = 15
        self.duration_mode = 'YEARS'
        self.heuristic_antivirus_subscribed = True
        self.external_antivirus_subscribed = True
        self.outbound_filtering_subscribed = True       
        self.max_address_count = 500000
        self.max_domain_count = 3000        
        self.subscription_date = '06-06-2013 01:00:00'
        self.expiration_datee = '06-06-2036 01:00:00'
        self.template_id = 1

    def getReference(self):
        return self.reference
   
    def setReference(self, value):
        self.reference = str(value)
        
    def explore(self, data):
        if data is None:
            return        
        self.subscription_id = int(data['subscription_id'])
        if 'duration_units' in data:
            self.duration_units = int(data['duration_units'])
        if 'self.duration_mode' in data: 
            self.duration_mode = data['duration_mode']
        if 'subscription_date' in data:
            self.subscription_date = data['subscription_date']
        if 'expiration_date' in data:
            self.expiration_date = data['expiration_date']          
        if 'heuristic_antivirus_subscribed' in data:
            self.heuristic_antivirus_subscribed = bool(data['heuristic_antivirus_subscribed'])
        if 'external_antivirus_subscribed' in data:
            self.external_antivirus_subscribed = bool(data['external_antivirus_subscribed'])
        if 'outbound_filtering_subscribed' in data:
            self.outbound_filtering_subscribed = bool(data['outbound_filtering_subscribed'])
        if 'template_id' in data:
            self.template_id = int(data['template_id'])
        self.max_address_count = int(data['max_address_count'])
        self.max_domain_count = int(data['max_domain_count'])
        
 
#
# ACCOUNT ( for ENV/OEM or SITE/USER)
#       
class Account:
    
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.account_id = 0
        self.accunt_owner_id = 0
        self.account_login = ''
        
        self.address = Address()        
        # id de la langue (1 par défaut)
        self.language_id = 1        
        # id EPPN
        self.eppn_login = ''
        
        # do no change
        self.subscription = Subscription()
        
        # globale filtering settings for the account , compound with domains
        self.settings = Settings();
        
    
    def getName(self):
        return self.address.getCompany()

    def setName(self, value):
        self.address.setCompany(value)

    def getAddress(self):
        return self.address
    
    def getSubscription(self):
        return self.subscription

    def setSubscription(self, value):
        self.subscription = value
    
    def getSettings(self):        
        return self.settings;

    def getId(self):
        return int(self.account_id)
    
    def getOwnerId(self):
        return int(self.account_owner_id)

    def setOwnerId(self, value):
        self.account_owner_id = value

    def getLogin(self):           
        return self.account_login

    def setLogin(self, value):   
        self.account_login = value

    def getEppn(self):
        return self.eppn_login

    def setEppn(self, value):
        self.eppn_login = value

        
    def explore(self, data):
        if data is None:
            return        
        self.account_id = int(data['account_id'])        
        self.account_owner_id = int(data['account_owner_id'])
        self.account_login = str(data['account_login'])    
        self.address = Address(data['address'])
                        
        if 'language_id' in data:        
            self.language_id = int(data['language_id'])
        
        if 'eppn_login' in data:    
            self.eppn_login = str(data['eppn_login'])
                                
        if 'subscription' in data:
           self.subscription = Subscription(data['subscription'])        

        if 'settings' in data:
           self.settings = Settings(data['settings'])
        
        
    def __repr__(self):
        return """
        id: %s\n
        login: %s\n
        address: {\n%s}\n
        eppn_login: %s\n
        """ % (str(self.account_id), str(self.account_login), str(self.address), str(self.eppn_login))


#
# SUBSCRIPTIONLIST
#         
class SubscriptionList: 
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)        
        
    def setDefault(self):        
        self.subscriptionList = []        
        
    def explore(self, data):
        if data is None:
            return            
        if 'subscriptionList' in data:                          
            items = data['subscriptionList']
            if isinstance(items, list):
               for item in items:                                                
                  self.subscriptionList.append(Subscription(item))
               
    def __len__(self):
        return len(self.subscriptionList)
    
    def __getitem__(self, index):
        return self.subscriptionList[index] 


#
# ACCOUNTLIST
#         
class AccountList: 
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)        
        
    def setDefault(self):
        self.accountList = []
        
    def explore(self, data):
        if data is None:
            return            
        if 'accountList' in data:                          
            items = data['accountList']
            if isinstance(items, list):
                    for item in items:                                                
                        self.accountList.append(Account(item))

    def getFromLogin(self, login):
        for a in self.accountList:
            if a.getLogin() == login:
                return a
        return None

    def getFromName(self, name):
        for a in self.accountList:
            if a.getName() == name:
                return a
        return None
                     
                   
    def __len__(self):
        return len(self.accountList)
    
    def __getitem__(self, index):
        return self.accountList[index] 
    
        
#
# LDAP
#
class Ldap:
    
    def __init__(self, data=None):  
        self.setDefault()
        self.explore(data) 
        
    def setDefault(self):        
        # info
        self.description = ""                
        # id de l'annuaire
        self.ldap_id = 0        
        # host
        self.servername = ""
        # port
        self.port = 389
        # searchbase
        self.searchbase = ''
        # search filter
        self.searchfilter = ''
        # login
        self.login = ''
        # password
        self.password = ''        
        # timeout en secondes ( 0 = inf)
        self.timeout = 0
        # posftix specifix
        self.others = ''
        
        # posftix specifix
        self.weight = 10
        
        # attribut par défaut
        self.result_attribute = ''
        
    def getDescription(self):
        return self.description
    
    def setDescription(self, value):
        self.description = value
        
    def getServer(self):
        return self.servername
    
    def setServer(self, value):
        self.servername = value
        
    def getPort(self):
        return self.port
    
    def setPort(self, value):
        self.port = int(value)
                    
    def getSearchFilter(self, value):
        return self.searchfilter
        
    def setSearchFilter(self, value):
        self.searchfilter = value
        
    def getLogin(self, value):
        return self.login
        
    def setLogin(self, value):
        self.login = value
        
    def getPassword(self, value):
        return self.password
            
    def setPassword(self, value):
        self.password = value
                
    def getTimeout(self, value):
        return self.timeout
            
    def setTimeout(self, value):
        self.timeout = value
        
    def getWeight(self, value):
        return self.weight
            
    def setWeight(self, value):
        self.weight = int(value)
        
    def getOthers(self, value):
        return self.others
            
    def setOthers(self, value):
        self.others = int(value)
                    
    def explore(self, data):
        if data is None:
            return            
        if "description" in data:
            self.description = data['description']
        self.ldap_id = int(data['ldap_id'])
        self.servername = str(data['servername'])
        self.port = int(data['port'])
        self.searchbase = str(data['searchbase'])
        self.searchfilter = str(data['searchfilter'])
        self.login = str(data['login'])
        self.password = str(data['password'])
        self.timeout = int(data['timeout'])
        self.others = str(data['others'])
        self.weight = int(data['weight'])
        self.result_attribute = str(data['result_attribute'])
    
    def __repr__(self):
        return """
        description: %s\n
        id: %s\n
        server name: %s\n
        port: %d\n
        search base: %s\n
        search filter: %s\n
        login: %s\n
        password: %s\n
        timeout: %d\n
        others: %s\n
        weight: %d\n
        result attribute: %s\n""" % (
        self.description,
        self.ldap_id,
        self.servername,
        self.port,
        self.searchbase,
        self.searchfilter,
        self.login,
        self.password,
        self.timeout,
        self.others,
        self.weight,
        self.result_attribute)
                                     
                              

#
# Relay
#
class Relay:    
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.domain_relay_id = 0
        self.domain_relay_address = ''
        self.domain_relay_hostname = ''
        self.domain_relay_network_id = 0
        self.domain_id = 0
        self.domain_relay_port = 25
        self.login = ''
        self.domain_relay_priority = 10
        self.is_attach = False
        
    def getId(self):
        return self.domain_relay_id

    def getAddress(self):
        return self.domain_relay_address

    def setAddress(self, value):
        self.domain_relay_address = value
    
    def getHostName(self):
        return self.domain_relay_hostname

    def setHostName(self, value):
        self.domain_relay_hostname = value

    def getPriority(self):
        return self.domain_relay_priority

    def setPriority(self, value):
        self.domain_relay_priority = value
  
        
    def explore(self, data):
        if data is None:
            return            
        self.domain_relay_id = int(data['domain_relay_id'])
        self.domain_relay_address = str(data['domain_relay_address'])
        self.domain_relay_hostname = str(data['domain_relay_hostname'])
        self.domain_relay_network_id = int(data['domain_relay_network_id'])
        self.domain_id = int(data['domain_id']) 
        self.domain_relay_port = int(data['domain_relay_port'])        
        self.domain_relay_priority = int(data['domain_relay_priority'])
        self.is_attach = int(data['domain_relay_priority']) != 0 
           

           
#
# Settings
#
class Settings:
        
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.notification_marking_label = ''
        
        # string :DELIVER,MARK,QUARANTINE,DROP,REJECTED
        self.notification_marking_operation = 'DELIVER'

        # string:LOCKED,UNLOCKED,USE_GLOBAL
        self.notification_marking_lock = 'LOCKED'
        
        # high spam    
        self.spam_high_marking_label = "* HIGH SPAM *"        
        self.spam_high_marking_operation = "DROP"        
        self.spam_high_marking_lock = 'LOCKED'
        
        # medium spam       
        self.spam_medium_marking_label = "* MEDIUM SPAM *"        
        self.spam_medium_marking_operation = "TAG"
        self.spam_medium_marking_lock = "LOCKED"

        # low spam
        self.spam_low_marking_label = "* LOW SPAM *"
        self.spam_low_marking_operation = "TAG"
        self.spam_low_marking_lock = "LOCKED"
        
        # virus
        self.virus_marking_label = "!!!VIRUS!!!"
        self.virus_marking_operation = "DROP"
        self.virus_low_marking_lock = "LOCKED"

        self.message_max_size = 0
        self.rbl_enabled = "true"
        self.bad_extensions = ''
        
    def getNotificationLabel(self):
        return self.notification_marking_label
    
    def setNotificationLabel(self, value):
        self.notification_marking_label = str(value)
        
    def getNotificationOperation(self):
        return self.notification_marking_operation
    
    def setNotificationOperation(self, value):
        self.notification_marking_operation = str(value)
        
    
        
    def __repr__(self):
        return """
        bounce label: %s\n
        bounce operation: %s\n
        bounce lock: %s\n
        
        high spam label: %s\n
        high spam operation: %s\n
        high spam lock: %s\n
        
        medium spam label: %s\n
        medium spam operation: %s\n
        medium spam lock: %s\n
        
        high spam label: %s\n
        high spam operation: %s\n
        high spam lock: %s\n
        
        virus spam label: %s\n
        virus spam operation: %s\n
        virus spam lock: %s\n
        
        message max size: %d\n
        rbl enabled: %s\n
        bad extensions: %s\n
        """ % (
        self.notification_marking_label,
        self.notification_marking_operation,
        self.notification_marking_lock,
        self.spam_high_marking_label,
        self.spam_high_marking_operation,
        self.spam_high_marking_lock,
        self.spam_medium_marking_label,
        self.spam_medium_marking_operation,
        self.spam_medium_marking_lock,
        self.spam_low_marking_label,
        self.spam_low_marking_operation,
        self.spam_low_marking_lock,
        self.virus_marking_label,
        self.virus_marking_operation,
        self.virus_low_marking_lock,
        self.message_max_size,
        self.rbl_enabled,
        self.bad_extensions)
        
                    
    def explore(self, data):
        if data is None:
            return    
        
        # bounce
        self.notification_marking_label = str(data['notification_marking_label'])        
        self.notification_marking_operation = str(data['notification_marking_operation'])
        
        if 'notification_marking_lock' in data:
            self.notification_marking_lock = str(data['notification_marking_lock'])
        
        # high spam    
        self.spam_high_marking_label = str(data['spam_high_marking_label'])        
        self.spam_high_marking_operation = str(data['spam_high_marking_operation'])
        
        if 'spam_high_marking_lock' in data:    
            self.spam_high_marking_lock = str(data['spam_high_marking_lock'])
        
        # medium spam       
        self.spam_medium_marking_label = str(data['spam_medium_marking_label'])        
        self.spam_medium_marking_operation = str(data['spam_medium_marking_operation'])
        
        if 'spam_medium_marking_lock' in data:
            self.spam_medium_marking_lock = str(data['spam_medium_marking_lock'])

        # low spam
        self.spam_low_marking_label = str(data['spam_low_marking_label'])
        self.spam_low_marking_operation = str(data['spam_low_marking_operation'])
        
        if 'spam_low_marking_lock' in data:
            self.spam_low_marking_lock = str(data['spam_low_marking_lock'])
        
        # virus
        self.virus_marking_label = str(data['virus_marking_label'])
        self.virus_marking_operation = str(data['virus_marking_operation'])
        
        if 'virus_marking_lock' in data:
            self.virus_marking_lock = str(data['virus_marking_lock'])

        if "message_max_size" in data:
            self.message_max_size = int(data['message_max_size'])
            
        if "rbl_enabled" in data:
            self.rbl_enabled = str(data['rbl_enabled']);
            
        if "bad_extensions" in data:
            self.bad_extensions = str(data['bad_extensions'])
        
        
        
#
# Header 
#
class Header:
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.name = ''
        self.value = ''
        self.value_id = 0
        
    def explore(self, data):
        if data is None:
            return    
        if 'value_id' in data: 
           self.value_id = int(data['value_id'])
        self.name = str(data['name'])
        self.value = str(data['value'])
        
#
# DOMAIN
#
class Domain:
    
    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.state = ''
        self.domain_id = 0
        self.domain_name = ''
        self.contact_address = ''
        self.settings = Settings()
        self.domainRelayEntryList = []
        self.domainHeaderEntryList = []
        self.domainLDAPEntryList = []
        
    def getId(self):
        return int(self.domain_id)
        
    def getName(self):
        return self.domain_name

    def setName(self, value):
        self.domain_name = value 
        
    def getState(self):
        return self.domain_state

    def setState(self, value):
        self.domain_state = value

    def getSettings(self):
        return self.settings

    def getContactAddress(self):
        return self.contact_address

    def setContactAddress(self,value):
        self.contact_address = value


    def getRelays(self):
        return self.domainRelayEntryList

    def getHeaders(self):
        return self.domainHeaderEntryList
    
    def explore(self, data):
        if data is None:
            return            
        self.state = str(data['state'])
        self.domain_id = int(data['domain_id'])
        self.domain_name = data['domain_name']
        self.contact_address = str(data['contact_address'])
        self.settings = Settings(data['settings'])
        
        items = data['domainRelayEntryList']
        if isinstance(items, list):                        
            for item in items:                                                
                self.domainRelayEntryList.append(Relay(item))
                
        items = data['domainHeaderEntryList']
        if isinstance(items, list):                        
            for item in items:                                                
                self.domainHeaderEntryList.append(Header(item))
                
        # items = data['domainLDAPEntryList']        
        # if isinstance(items, list):                        
        #    for item in items:
        #        self.domainLDAPEntryList.append(Ldap(item))
    
    def __repr__(self):        
        result = """
        domain id    : %d\n
        domain name  : %s\n
        domain state : %s\n        
        domain contact : %s\n        
        """ % (self.domain_id, self.domain_name, self.state, self.contact_address)
        result = result + "settings:{ %s }" % str(self.settings)
        return result
        
        
#
# DOMAINLIST
#
class DomainList:

    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.entries = []
        
    def explore(self, data):
        if data is None:
            return            
        items = data['entries']
        if isinstance(items, list):                        
            for item in items:                                                
                self.entries.append(Domain(item))
                
    def __len__(self):
        return len(self.entries)
    
    def __getitem__(self, index):
        return self.entries[index]
    
    
        
#
# LDAPLIST
#
class LdapList:

    def __init__(self, data=None):
        self.setDefault()
        self.explore(data)
        
    def setDefault(self):        
        self.LDAPList = []
        
    def explore(self, data):
        if data is None:
            return    
        items = data['LDAPList']
        if isinstance(items, list):                        
            for item in items:                                                
                self.LDAPList.append(Ldap(item))
                
    def __len__(self):
        return len(self.LDAPList)
    
    def __getitem__(self, index):
        return self.LDAPList[index] 
 
