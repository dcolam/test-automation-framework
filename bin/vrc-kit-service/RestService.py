#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-#
#
# VRC - VadeRetro Technology - Copyright 2013
#
# Python sample using the VadeRetro Cloud Rest Client API
# service class
# 
# $LastChangedDate:$
# $Rev:$
#
import urllib.request, urllib.error, urllib.parse
import json
import jsonpickle
from . import Entities


class ServiceError(Exception):    
    def __init__(self, json_error):
        self.error = Entities.Error(json_error)
        
    def __str__(self):
        return str(self.error)
    
    def getDetail(self):
        return self.error
        

class Service:
    
    def __init__(self, eppn, urlbase=None, debugEnabled=False):
        self.eepn = ''
        self.debugEnabled = debugEnabled        
        if urlbase is not None:
            self.urlbase = urlbase
        else:
            self.urlbase = "http://192.168.15.42:8480"
        self.eppn = eppn

    def getUrlBase(self):      
        return self.urlbase

    def setEPPN(self, value):
        self.eppn = value


    #
    #  getBanner()
    #  return the banner to see if service is available or None on error
    #
    def getBanner(self):
        # only get
        d = self.jsonrequest("account/ping", None, False)   
        if 'banner' not in d:
            return None
        return d['banner']

     
    #
    #  getSubscriptionList()
    #  return the list of all accounts    
    #  @return: return an object Entities.Subscription
    #
    def getSubscriptionList(self):
        d = self.jsonrequest("subscription/list", None)         
        if d is None:
            return None
        return Entities.SubscriptionList(d)   


    # 
    # getAccountList()   
    # return the list of all accounts   
    # @return: return an object Entities.AccountList
    #
    def getAccountList(self):        
        d = self.jsonrequest("account/list", None)         
        if d is None:
            return None
        return Entities.AccountList(d)
   
 
    # 
    # addAccount()
    #  create a new empty account, after it will be updated
    # @return: return an object Entities.Account or None    
    #     
    def addAccount(self, account):           
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")
        
        # internal AccountEntry
        # INVERSE!!!  account_owner_id --> owner_account_id
        args = {}        
        args['owner_account_id'] = account.getOwnerId()
        args['account'] = account

        d = self.jsonrequest("account/add", args)         
        if d is None:
            return None
        return Entities.Account(d)
    
    
    # 
    # updateAccount(account)
    # update properties of an existing account
    # @return: return an object Entities.Account or None
    #     
    def updateAccount(self, account):
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")
        
        # internal AccountEntry
        # INVERSE!!!  account_owner_id --> owner_account_id
        args = {}
        args['account_id'] = account.getId()
        args['owner_account_id'] = account.getOwnerId()
        args['account'] = account
                                        
        d = self.jsonrequest("account/update", args)                 
        if 'account' not in d:
            return None
        return Entities.Account(d['account'])


    # 
    # getAccountByLogin()
    # @return: Account or nil      
    #
    def getAccountByLogin(self, login):
        searchAccount = Entities.Account()
        searchAccount.setLogin(login)
        searchAccount.setOwnerId(1)
        args = {}        
        args['owner_account_id'] = searchAccount.getOwnerId()        
        args['account'] = searchAccount
        d = self.jsonrequest("account/find", args)         
        if d is None:
            return None
        list = Entities.AccountList(d)
        if len(list) == 0:
            return None            
        return list[0]
    
    
        

    
    # 
    # deleteAccount(account)
    # delete an account
    # @return: true if account is deleted      
    #     
    def deleteAccount(self, account):
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")                        
        # internal AccountEntry
        # INVERSE!!!  account_owner_id --> owner_account_id
        args = {}
        args['account_id'] = account.getId()
        args['owner_account_id'] = account.getOwnerId()
        args['account'] = account
                                        
        d = self.jsonrequest("account/delete", args)                 
        if d is None:
            return False                 
        if 'account_id' not in d:
            return False
        if 'account_login' not in d:
            return False
        return True
    
            
    # 
    # getDomainList(account)
    # return the list of domains for an account
    # @return: return an object Entities.DomainList
    #
    def getDomainList(self, account):        
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")            
        d = self.jsonrequest("domain/list", account)         
        if d is None:
            return None
        return Entities.DomainList(d)
    
    
    # 
    # addDomain(account,domain)
    # add a new domain for the account
    # @param  account (Entities.Account)
    # @param  domain (Entities.Domain)
    # @return: return an object Entities.Domain or None if error
    #
    def addDomain(self, account, domain):        
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")    
        if not isinstance(domain, Entities.Domain):
            raise Exception("domain parameter must be a class Entities.Domain")                    

        args = {}
        args['account_id'] = account.getId()
        args['account_login'] = account.getLogin()
        args['domain'] = domain

        d = self.jsonrequest("domain/add", args)         
        if d is None:
            return None 
        if 'account_id' not in d:
            return None
        if 'domain' not in d:
            return None
        return Entities.Domain(d['domain'])
    
                
    # 
    # deleteDomain(account,domain)
    # delete a domain for the account
    # @return: return true if domains is deleted
    #
    def deleteDomain(self, account, domain):        
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")            
        if not isinstance(domain, Entities.Domain):
            raise Exception("domain parameter must be a class Entities.Domain")                    
     

        # internal AccountEntry
        # INVERSE!!!  account_owner_id --> owner_account_id
        args = {}
        args['account_id'] = account.getId()
        args['domain_id'] = domain.getId()
 
        d = self.jsonrequest("domain/delete", args)         
        if d is None:
            return False        
        if 'domain_id' not in d:
            return False
        return True
    
    
    # 
    # updateDomain(domain)
    # update a domain object
    # @return: return an object Entities.Domain or None if error
    #
    def updateDomain(self, account, domain):
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")     
        if not isinstance(domain, Entities.Domain):
            raise Exception("domain parameter must be a class Entities.Domain")
    
        args = {}
        args['account_id'] = account.getId()
        args['account_login'] = account.getLogin()
        args['domain'] = domain
        
        d = self.jsonrequest("domain/update", args)         
        if d is None:
            return False        
        if 'account_id' not in d:
            return False
        if 'domain' not in d:
            return False
        return Entities.Domain(d['domain'])
    
    
    # 
    # getAccountLdapList(account)
    # return the list of LDAP for an account
    # @return: return an object Entities.LdapList
    #
    def getLdapList(self, account):        
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")            
        d = self.jsonrequest("ldap/list", account)         
        if d is None:
            return None
        return Entities.LdapList(d)
    
    
        
    # 
    # addLdap(account,ldap)   
    # create a new ldap for the account
    # @param : account (Entities.Account)
    # @param : ldap (Entities.Ldap)
    # @return: return true if Ldap was added
    #
    def addLdap(self, account, ldap):        
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")
        if not isinstance(ldap, Entities.Ldap):
            raise Exception("ldap parameter must be a class Entities.Ldap")        
        d = self.jsonrequest("ldap/add", account)         
        if d is None:
            return False        
        if 'account_id' not in d:
            return None
        if 'ldap' not in d:
            return None
        return Entities.Domain(d['ldap'])


    
    # 
    # updateLdap(account,ldap)
    # update an LDAP entry
    # @param : account (Entities.Account)
    # @param : ldap (Entities.Ldap)
    # @return: return an object Entities.Ldap
    #
    def updateLdap(self, account, ldap):            
        if not isinstance(account, Entities.Account):
            raise Exception("account parameter must be a class Entities.Account")            
        if not isinstance(ldap, Entities.Ldap):
            raise Exception("sldap parameter must be a class Entities.Ldap")        
        args = {}
        args['account_id'] = account.getId()        
        args['ldap'] = ldap
                    
        d = self.jsonrequest("ldap/update", args)         
        if d is None:
            return None
        if 'account_id' not in d:
            return None
        if 'ldap' not in d:
            return None
        return Entities.Domain(d['ldap'])


            
    # 
    # deleteLdap(ldap)
    # delete a ldap entry for the account
    # @return: return True if ldap is removed
    #
    def deleteLdap(self, account, ldap):
        if not isinstance(account, Entities.Ldap):
            raise Exception("account parameter must be a class Entities.Ldap")        
        args = {}
        args['account_id'] = account.getId()        
        args['ldap'] = ldap        
        d = self.jsonrequest("ldap/delete", account)                 
        if d is None:
            return False    
        if 'account_id' not in d:
            return False
        if 'ldap_id' not in d:
            return False
        if 'ldap_name' not in d:
            return False
        return True              
        
        
    def debug(self, msg):
        print(msg)
        print('\n')
        
    #
    # json REST jsonraw json in, raw json out
    # 
    def jsonrequest(self, uri, obj=None, post=True):
        url = "%s/service/%s" % (self.urlbase, uri)
        if self.debugEnabled:
            self.debug("json " + url)
        post_data = None
        if obj is None:
            if post == True :
                post_data = "".encode("utf-8")
        else:         
            post_data = jsonpickle.encode(obj)
            if self.debugEnabled:
                self.debug("post with json: " + post_data.decode("utf-8"))                
        if post_data is None:           
            json = urllib.request.Request(url, None, {"REMOTE_USER" : str(self.eppn) })        
        else:
            json = urllib.request.Request(url, post_data, {"REMOTE_USER" : str(self.eppn), 'Content-Type': 'application/json', 'Content-Length': len(post_data) })        
        f = urllib.request.urlopen(json)
        result = f.read().decode("utf-8")
        f.close()
        if self.debugEnabled:
            self.debug("result=" + result)        
        if result is None:
            return None
        d = jsonpickle.decode(result)
        if not isinstance(d, dict):
            return None
        if 'error' in d:
            raise ServiceError(d['error'])        
        return d
     
