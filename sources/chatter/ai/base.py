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


import typing as typ

from dataclasses import dataclass


class ChatCompletionError( Exception ): pass


@dataclass
class ChatCallbacks:

    allocator: typ.Callable[ [ str ], typ.Any ] = (
        lambda mime_type: None )
    deallocator: typ.Callable[ [ typ.Any ], None ] = (
        lambda handle: None )
    failure_notifier: typ.Callable[ [ str ], None ] = (
        lambda status: None )
    progress_notifier: typ.Callable[ [ int ], None ] = (
        lambda tokens_count: None )
    success_notifier: typ.Callable[ [ typ.Any ], None ] = (
        lambda status: None )
    updater: typ.Callable[ [ typ.Any, str ], None ] = (
        lambda handle, content: None )
