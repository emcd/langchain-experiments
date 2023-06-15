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


''' GUI layouts with Panel widgets. '''


from panel.layout import Column, HSpacer, Row
from panel.pane import Markdown
from panel.widgets import (
    Button,
    Checkbox,
    FloatSlider,
    IntSlider,
    Select,
    StaticText,
    TextAreaInput,
    TextInput,
)

dashboard_layout = {
    'dashboard': dict(
        component_class = Row,
        contains = [
            'column_conversations_manager',
            'conversation_panes',
        ]
    ),
    'column_conversations_manager': dict(
        component_class = Column,
        component_arguments = dict( width = 640 ),
        contains = [
            'button_new_conversation',
            'column_conversations_index',
        ],
    ),
    'button_new_conversation': dict(
        component_class = Button,
        component_arguments = dict(
            name = 'New Conversation',
            width_policy = 'min',
        ),
    ),
    'column_conversations_index': dict( component_class = Column ),
    'conversation_panes': dict(
        component_class = Column,
        component_arguments = dict( width_policy = 'max' ),
    ),
}

conversation_layout = {
    'conversation_pane': dict(
        component_class = Row,
        contains = [
            #'left_spacer',
            'column_conversation',
            'right_spacer',
            'column_conversation_control',
        ]
    ),
}

conversation_layout.update( {
    #'left_spacer': dict( component_class = HSpacer ),
    'column_conversation': dict(
        component_class = Column,
        component_arguments = dict(
            sizing_mode = 'stretch_height', width = 1024,
        ),
        contains = [
            'row_system_prompt',
            'column_conversation_history',
            'row_summarization_prompt',
            'row_user_prompt',
        ],
    ),
    'row_system_prompt': dict(
        component_class = Row,
        contains = [ 'label_system', 'column_system_prompt', ],
    ),
    'label_system': dict(
        component_class = StaticText,
        component_arguments = dict( value = '💬📏', width = 40, ),
        persist = False,
    ),
    'column_system_prompt': dict(
        component_class = Column,
        contains = [
            'row_system_prompt_selector',
            'row_system_prompt_variables',
            'text_system_prompt',
        ],
    ),
    'row_system_prompt_selector': dict(
        component_class = Row,
        contains = [
            'selector_system_prompt',
            'checkbox_display_system_prompt',
        ],
    ),
    'selector_system_prompt': dict(
        component_class = Select,
        component_arguments = dict(
            options = [ 'None', ],
            value = 'None',
        ),
    ),
    'checkbox_display_system_prompt': dict(
        component_class = Checkbox,
        component_arguments = dict(
            align = 'center',
            name = 'Display',
            value = False,
        ),
    ),
    'row_system_prompt_variables': dict(component_class = Row, ),
    'text_system_prompt': dict(
        component_class = Markdown,
        component_arguments = dict(
            height_policy = 'fit',
            width_policy = 'max',
            visible = False,
        ),
    ),
    'column_conversation_history': dict(
        component_class = Column,
        component_arguments = dict( sizing_mode = 'stretch_both' ),
        persistence_functions = dict(
            save = 'save_conversation_messages',
            restore = 'restore_conversation_messages',
        ),
    ),
    'row_summarization_prompt': dict(
        component_class = Row,
        contains = [
            'label_summarization',
            'column_summarization_prompt',
        ],
    ),
    'label_summarization': dict(
        component_class = StaticText,
        component_arguments = dict( value = '💬∑', width = 40, ),
        persist = False,
    ),
    'column_summarization_prompt': dict(
        component_class = Column,
        contains = [
            'row_summarizer_selection',
            'row_summarization_prompt_variables',
            'text_summarization_prompt',
        ],
    ),
    'row_summarizer_selection': dict(
        component_class = Row,
        contains = [
            'selector_summarization_prompt',
            'checkbox_summarize',
        ],
    ),
    'selector_summarization_prompt': dict(
        component_class = Select,
        component_arguments = dict(
            options = [ 'None' ],
            value = 'None',
        ),
    ),
    'checkbox_summarize': dict(
        component_class = Checkbox,
        component_arguments = dict(
            align = 'center',
            name = 'Display and Activate',
            value = False,
        ),
    ),
    'row_summarization_prompt_variables': dict( component_class = Row, ),
    'text_summarization_prompt': dict(
        component_class = Markdown,
        component_arguments = dict(
            height_policy = 'fit',
            width_policy = 'max',
            visible = False,
        ),
    ),
    'row_user_prompt': dict(
        component_class = Row,
        contains = [ 'label_user', 'column_user_prompt' ],
    ),
    'label_user': dict(
        component_class = StaticText,
        component_arguments = dict( value = '💬🧑', width = 40, ),
        persist = False,
    ),
    'column_user_prompt': dict(
        component_class = Column,
        contains = [ 'text_input_user', 'row_actions', ],
    ),
    'text_input_user': dict(
        component_class = TextAreaInput,
        component_arguments = dict(
            height_policy = 'fit',
            max_height = 480,
            placeholder = 'Enter user message here...',
            value = '',
            width_policy = 'max',
        ),
    ),
    'row_actions': dict(
        component_class = Row,
        contains = [ 'button_chat', 'button_query', ],
    ),
    'button_chat': dict(
        component_class = Button,
        component_arguments = dict( name = 'Chat' ),
    ),
    'button_query': dict(
        component_class = Button,
        component_arguments = dict( name = 'Query' ),
    ),
} )

conversation_layout.update( {
    'right_spacer': dict( component_class = HSpacer ),
    'column_conversation_control': dict(
        component_class = Column,
        contains = [
            'selector_provider',
            'selector_model',
            'slider_temperature',
            'selector_vectorstore',
            'slider_documents_count',
            'text_tokens_total',
            'text_status',
        ],
    ),
    'selector_provider': dict(
        component_class = Select,
        component_arguments = dict(
            name = 'Provider',
            options = [ 'OpenAI' ],
            value = 'OpenAI',
        ),
    ),
    'selector_model': dict(
        component_class = Select,
        component_arguments = dict(
            name = 'Model',
            options = [ 'gpt-3.5-turbo-0613' ],
            value = 'gpt-3.5-turbo-0613',
        ),
    ),
    'slider_temperature': dict(
        component_class = FloatSlider,
        component_arguments = dict(
            name = 'Temperature',
            start = 0, end = 2, step = 0.1, value = 0,
        ),
    ),
    'selector_vectorstore': dict(
        component_class = Select,
        component_arguments = dict(
            name = 'Vector Store',
        ),
    ),
    'slider_documents_count': dict(
        component_class = IntSlider,
        component_arguments = dict(
            name = 'Number of Documents',
            start = 0, end = 5, step = 1, value = 3,
        ),
    ),
    'text_tokens_total': dict(
        component_class = StaticText,
        component_arguments = dict( name = 'Token Counter', value = '0', ),
        persist = False,
    ),
    'text_status': dict(
        component_class = StaticText,
        component_arguments = dict( name = 'Status', value = 'OK', ),
        persist = False,
    ),
} )
