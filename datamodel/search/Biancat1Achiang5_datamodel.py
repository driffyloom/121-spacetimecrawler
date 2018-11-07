'''
Created on Oct 20, 2016
@author: Rohan Achar
'''
from rtypes.pcc.attributes import dimension, primarykey, predicate
from rtypes.pcc.types.subset import subset
from rtypes.pcc.types.set import pcc_set
from rtypes.pcc.types.projection import projection
from rtypes.pcc.types.impure import impure
from datamodel.search.server_datamodel import Link, ServerCopy

@pcc_set
class Biancat1Achiang5Link(Link):
    USERAGENTSTRING = "Biancat1Achiang5"

    @dimension(str)
    def user_agent_string(self):
        return self.USERAGENTSTRING

    @user_agent_string.setter
    def user_agent_string(self, v):
        # TODO (rachar): Make it such that some dimensions do not need setters.
        pass


@subset(Biancat1Achiang5Link)
class Biancat1Achiang5UnprocessedLink(object):
    @predicate(Biancat1Achiang5Link.download_complete, Biancat1Achiang5Link.error_reason)
    def __predicate__(download_complete, error_reason):
        return not (download_complete or error_reason)


@impure
@subset(Biancat1Achiang5UnprocessedLink)
class OneBiancat1Achiang5UnProcessedLink(Biancat1Achiang5Link):
    __limit__ = 1

    @predicate(Biancat1Achiang5Link.download_complete, Biancat1Achiang5Link.error_reason)
    def __predicate__(download_complete, error_reason):
        return not (download_complete or error_reason)

@projection(Biancat1Achiang5Link, Biancat1Achiang5Link.url, Biancat1Achiang5Link.download_complete)
class Biancat1Achiang5ProjectionLink(object):
    pass
