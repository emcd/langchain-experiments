# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Assorted data structures to help with GUI development. '''


from panel.reactive import ReactiveHTML
import param


class ConversationIndicator( ReactiveHTML ):

    content = param.String( default = None )
    identity = param.String( default = None )
    selected = param.Event( default = False )

    _template = (
        '''<div id="ConversationIndicator" onclick="${_div_click}">'''
        '''${content}</div>''' )

    def __init__( self, content, identity, **params ):
        self.content = content
        self.identity = identity
        super( ).__init__( **params )

    def _div_click( self, event ):
        self.selected = not self.selected
        print( f"DEBUG: selected = {self.selected}" )


def _provide_auxiliary_classes( ):
    from collections import namedtuple
    return (
        namedtuple( 'ConversationTuple', ( 'text_title', ) ),
        namedtuple(
            'MessageTuple',
            ( 'checkbox_inclusion', 'text_message', ) ),
    )

(   ConversationTuple,
    MessageTuple,
) = _provide_auxiliary_classes( )
