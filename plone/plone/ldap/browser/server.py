from Acquisition import Implicit
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.formlib.form import FormFields
from zope.formlib.form import applyChanges
from zope.app.container.interfaces import INameChooser
from Products.Five import BrowserView
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone import PloneMessageFactory as _
from simplon.plone.ldap.browser.interfaces import IServerAdding
from simplon.plone.ldap.engine.interfaces import ILDAPServerConfiguration
from simplon.plone.ldap.engine.interfaces import ILDAPConfiguration
from simplon.plone.ldap.engine.server import LDAPServer
from simplon.plone.ldap.browser.baseform import LDAPAddForm
from simplon.plone.ldap.browser.baseform import LDAPEditForm
from simplon.plone.ldap.browser.baseform import Adding


class ServerAdding(Adding):
    implements(IServerAdding)

    def add(self, content):
        """Add the server to the context
        """
        storage = getUtility(ILDAPConfiguration).servers
        chooser = INameChooser(storage)
        storage[chooser.chooseName(None, content)] = content

    def namesAccepted(self):
        return False

    def nameAllowed(self):
        return False


class ServerAddForm(LDAPAddForm):
    """An add form for LDAP servers.
    """
    form_fields = FormFields(ILDAPServerConfiguration)
    label = _(u"Add Server")
    description = _(u"Add an new LDAP or ActiveDirectory server.")
    form_name = _(u"Configure server")
    fieldset = "servers"

    def create(self, data):
        server = LDAPServer()
        applyChanges(server, self.form_fields, data)
        return server


class ServerEditForm(LDAPEditForm):
    """An edit form for LDAP servers.
    """
    form_fields = FormFields(ILDAPServerConfiguration)
    label = _(u"Edit Server")
    description = _(u"Edit a LDAP or ActiveDirectory server.")
    form_name = _(u"Configure server")
    fieldset = "servers"


class ServerNamespace(object):
    """LDAP server traversing.

    Traversing to portal/++ldapserver++id will traverse to the ldap server and
    return it in the current context, acquisition-wrapped.
    """
    implements(ITraversable)
    adapts(ISiteRoot, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context=context
        self.request=request


    def traverse(self, name, ignore):
        storage = getUtility(ILDAPConfiguration).servers
        return storage[name].__of__(self.context)


