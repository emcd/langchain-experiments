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


''' Callbacks and their helpers for Panel GUI. '''


def add_conversation_indicator( gui, descriptor, position = 0 ):
    from panel import Row
    from .classes import ConversationIndicator
    # TODO: Handle style to indicate active/previous/unloaded conversation.
    text_title = ConversationIndicator(
        descriptor[ 'title' ], descriptor[ 'identity' ],
        height_policy = 'fit',
        sizing_mode = 'stretch_width' )
    text_title.param.watch(
        lambda event: select_conversation( gui, event ), 'selected' )
    row = Row(
        text_title,
        # TODO: Edit button, delete button, etc...
    )
    conversations = gui.column_conversations_index
    if 'END' == position: conversations.append( row )
    else: conversations.insert( position, row )
    conversations.index__[ descriptor[ 'identity' ] ] = descriptor
    from .classes import ConversationTuple
    return ConversationTuple( *row )


def add_conversation_indicator_if_necessary( pane_gui ):
    from .classes import MessageTuple
    # TODO: Track AI message count on conversation to avoid recalculation.
    ai_message_count = sum(
        1 for conversation_tuple
        in map(
            lambda row: MessageTuple( *row ),
            pane_gui.column_conversation_history )
        if 'AI' == conversation_tuple.text_message.metadata__[ 'role' ] )
    if 1 != ai_message_count: return
    # TODO: Generate blurb.
    # TODO: Generate labels.
    descriptor = {
        'gui': pane_gui,
        'identity': pane_gui.identity__,
        'labels': [ ],
        'title': 'test',
    }
    dashboard_gui = pane_gui.parent__
    conversation_tuple = add_conversation_indicator(
        dashboard_gui, descriptor )
    # TODO: Select new indicator. (Deselects current pane, if there is one.)


def add_message( gui, role, content, include = True ):
    from panel import Row
    from panel.pane import Markdown
    from panel.widgets import Checkbox, StaticText
    from ..messages import count_tokens
    if 'Document' == role:
        content = f'''## Supplement ##\n\n{content}'''
        emoji = '📄'
        style = { 'background-color': 'WhiteSmoke' }
    elif 'AI' == role:
        emoji = '🤖'
        style = { 'border': '2px solid LightGray', 'padding': '3px' }
    else:
        emoji = '🧑'
        style = { 'background-color': 'White' }
    # TODO: Create cell based on MIME type of content rather than role.
    if role in ( 'Document', ):
        message_cell = StaticText(
            value = content,
            height_policy = 'fit',
            sizing_mode = 'stretch_width',
            style = style )
    else:
        message_cell = Markdown(
            content,
            height_policy = 'fit',
            sizing_mode = 'stretch_width',
            style = style )
    message_cell.metadata__ = {
        'role': role,
        'token_count': count_tokens( content ),
    }
    checkbox = Checkbox( name = emoji, value = include, width = 40 )
    checkbox.param.watch( lambda event: update_token_count( gui ), 'value' )
    row = Row(
        checkbox,
        message_cell,
        # TODO: Copy button, edit button, etc...
    )
    gui.column_conversation_history.append( row )
    from .classes import MessageTuple
    return MessageTuple( *row )


def create_conversation( dashboard_gui ):
    from types import SimpleNamespace
    from uuid import uuid4
    from .layouts import conversation_layout as layout
    components = { }
    generate_component( components, layout, 'conversation_pane' )
    pane_gui = SimpleNamespace( **components )
    pane_gui.auxiliary_data__ = dashboard_gui.auxiliary_data__
    pane_gui.identity__ = uuid4( )
    pane_gui.parent__ = dashboard_gui
    populate_conversation_pane( pane_gui )
    register_conversation_pane_callbacks( pane_gui )
    return pane_gui


def generate_component( components, layout, component_name ):
    entry = layout[ component_name ]
    elements = [ ]
    for element_name in entry.get( 'contains', ( ) ):
        elements.append( generate_component(
            components, layout, element_name ) )
    component_class = entry[ 'component_class' ]
    component_arguments = entry.get( 'component_arguments', { } )
    component = component_class( *elements, **component_arguments )
    components[ component_name ] = component
    return component


def generate_messages( gui ):
    from .classes import MessageTuple
    system_message = gui.text_system_prompt.object
    sysprompt_honor = gui.selector_model.metadata__[
        gui.selector_model.value ][ 'honors-system-prompt' ]
    role = 'system' if sysprompt_honor else 'user'
    messages = [ { 'role': role, 'content': system_message } ]
    for item in map(
        lambda row: MessageTuple( *row ),
        gui.column_conversation_history
    ):
        if not item.checkbox_inclusion.value: continue
        text_message = item.text_message
        role = (
            'user'
            if text_message.metadata__[ 'role' ] in ( 'Human', 'Document' )
            else 'assistant' )
        content = text_message.object
        messages.append( { 'role': role, 'content': content } )
    return messages


def locate_and_restore_conversation( gui ):
    from pathlib import Path
    configuration = gui.auxiliary_data__[ 'configuration' ]
    directories = gui.auxiliary_data__[ 'directories' ]
    state_path = Path( configuration[ 'locations' ][ 'state' ].format(
        user_state_path = directories.user_state_path ) )
    conversations_path = state_path / 'conversations'
    restore_conversation( gui, conversations_path / f"{gui.identity__}.json" )


def locate_and_save_conversation( gui ):
    add_conversation_indicator_if_necessary( gui )
    from pathlib import Path
    configuration = gui.auxiliary_data__[ 'configuration' ]
    directories = gui.auxiliary_data__[ 'directories' ]
    state_path = Path( configuration[ 'locations' ][ 'state' ].format(
        user_state_path = directories.user_state_path ) )
    conversations_path = state_path / 'conversations'
    save_conversation( gui, conversations_path / f"{gui.identity__}.json" )


def populate_conversation_pane( gui ):
    populate_providers_selector( gui )
    populate_models_selector( gui )
    populate_system_prompts_selector( gui )
    populate_summarization_prompts_selector( gui )
    populate_vectorstores_selector(
        gui, gui.auxiliary_data__[ 'vectorstores' ] )


def populate_dashboard( gui ):
    gui.column_conversations_index.index__ = { }
    gui.column_conversations_index.current_id__ = None
    restore_conversations_index( gui )
    pane_gui = create_conversation( gui )
    gui.conversation_panes.append( pane_gui.conversation_pane )


def populate_models_selector( gui ):
    provider = gui.selector_provider.metadata__[
        gui.selector_provider.value ][ 'model-provider' ]
    models = provider( )
    gui.selector_model.options = list( models.keys( ) )
    gui.selector_model.metadata__ = models


def populate_providers_selector( gui ):
    gui.selector_provider.options = [
        'OpenAI',
    ]
    gui.selector_provider.metadata__ = {
        'OpenAI': { 'model-provider': _provide_openai_models },
    }


def populate_system_prompts_selector( gui ):
    from pathlib import Path
    _populate_prompts_selector(
        gui.selector_system_prompt,
        Path( '.local/data/system-prompts' ) )
    update_system_prompt_variables( gui )


def populate_summarization_prompts_selector( gui ):
    from pathlib import Path
    _populate_prompts_selector(
        gui.selector_summarization_prompt,
        Path( '.local/data/summarization-prompts' ) )
    update_summarization_prompt_variables( gui )


def populate_vectorstores_selector( gui, vectorstores ):
    gui.selector_vectorstore.metadata__ = vectorstores
    gui.selector_vectorstore.options = list( vectorstores.keys( ) )


def register_conversation_pane_callbacks( gui ):
    gui.button_chat.on_click( lambda event: run_chat( gui ) )
    gui.button_query.on_click( lambda event: run_query( gui ) )
    gui.checkbox_display_system_prompt.param.watch(
        lambda event: toggle_system_prompt_display( gui ), 'value' )
    gui.checkbox_summarize.param.watch(
        lambda event: toggle_summarization_prompt_display( gui ), 'value' )
    gui.selector_summarization_prompt.param.watch(
        lambda event: update_summarization_prompt_variables( gui ), 'value' )
    gui.selector_system_prompt.param.watch(
        lambda event: update_system_prompt_variables( gui ), 'value' )
    gui.text_input_user.param.watch(
        lambda event: update_token_count( gui ), 'value' )


def register_dashboard_callbacks( gui ):
    gui.button_new_conversation.on_click(
        lambda event: create_conversation( gui ) )


def restore_conversation( gui, path ):
    from json import load
    import panel as pn
    from .layouts import conversation_layout as layout
    with path.open( ) as file: state = load( file )
    for name, data in layout.items( ):
        if not data.get( 'persist', True ): continue
        component_class = data[ 'component_class' ]
        if component_class in ( pn.widgets.Button, pn.layout.HSpacer ):
            continue
        component = getattr( gui, name )
        if component_class in ( pn.layout.Column, pn.layout.Row, ):
            if 'persistence_functions' not in data: continue
            restorer_name = data[ 'persistence_functions' ][ 'restore' ]
            restorer = globals( )[ restorer_name ]
            restorer( gui, component, state )
        elif hasattr( component, 'value' ):
            component.value = state[ name ][ 'value' ]
        elif hasattr( component, 'object' ):
            component.object = state[ name ][ 'value' ]
        else:
            raise ValueError(
                f"Unrecognized component class '{component_class}' "
                f"for component '{name}'." )


def restore_conversation_messages( gui, column, state ):
    column.clear( )
    for row_state in state.get( 'column_conversation_history', [ ] ):
        role = row_state[ 'role' ]
        content = row_state[ 'content' ]
        include = row_state[ 'include' ]
        add_message( gui, role, content, include = include )


def restore_conversations_index( gui ):
    from pathlib import Path
    configuration = gui.auxiliary_data__[ 'configuration' ]
    directories = gui.auxiliary_data__[ 'directories' ]
    state_path = Path( configuration[ 'locations' ][ 'state' ].format(
        user_state_path = directories.user_state_path ) )
    conversations_path = state_path / 'conversations'
    conversations_path.mkdir( exist_ok = True, parents = True )
    index_path = conversations_path / 'index.toml'
    from tomli import load
    from tomli_w import dump
    if not index_path.exists( ):
        with index_path.open( 'wb' ) as file:
            dump( { 'format-version': 1 }, file )
        return
    with index_path.open( 'rb' ) as file:
        descriptors = load( file )[ 'descriptors' ]
    for descriptor in descriptors:
        add_conversation_indicator( gui, descriptor, position = 'END' )


def run_chat( gui ):
    from .classes import MessageTuple
    gui.text_status.value = 'OK'
    if gui.checkbox_summarize.value:
        query = gui.text_summarization_prompt.object
    else:
        query = gui.text_input_user.value
        gui.text_input_user.value = ''
    if query: add_message( gui, 'Human', query )
    messages = generate_messages( gui )
    conversation_tuple = add_message( gui, 'AI', '', include = False )
    # TODO: Choose completion function according to provider.
    status = _try_run_openai_chat( gui, conversation_tuple, messages )
    gui.text_status.value = status
    if 'OK' == status:
        update_message( conversation_tuple, include = True )
        locate_and_save_conversation( gui )
        if gui.checkbox_summarize.value:
            gui.checkbox_summarize.value = False
            # Exclude conversation items above summarization.
            for i in range( len( gui.column_conversation_history ) - 2 ):
                conversation_tuple = MessageTuple(
                    *gui.column_conversation_history[ i ] )
                conversation_tuple.checkbox_inclusion.value = False
    update_token_count( gui )


def run_query( gui ):
    gui.text_status.value = 'OK'
    query = gui.text_input_user.value
    gui.text_input_user.value = ''
    if not query: return
    add_message( gui, 'Human', query )
    documents_count = gui.slider_documents_count.value
    if not documents_count: return
    vectorstore = gui.selector_vectorstore.metadata__[
        gui.selector_vectorstore.value ][ 'instance' ]
    documents = vectorstore.similarity_search( query, k = documents_count )
    for document in documents:
        add_message( gui, 'Document', document.page_content )
    update_token_count( gui )


def save_conversation( gui, path ):
    import panel as pn
    from .layouts import conversation_layout as layout
    state = { }
    for name, data in layout.items( ):
        if not data.get( 'persist', True ): continue
        component_class = data[ 'component_class' ]
        if component_class in (
            pn.widgets.Button,
            pn.layout.HSpacer,
        ): continue
        component = getattr( gui, name )
        if component_class in ( pn.layout.Column, pn.layout.Row, ):
            if 'persistence_functions' not in data: continue
            saver_name = data[ 'persistence_functions' ][ 'save' ]
            saver = globals( )[ saver_name ]
            state.update( saver( component ) )
        elif hasattr( component, 'value' ):
            state[ name ] = dict( value = component.value )
        elif hasattr( component, 'object' ):
            state[ name ] = dict( value = component.object )
        else:
            raise ValueError(
                f"Unrecognized component class '{component_class}' "
                f"for component '{name}'." )
    from json import dump
    with path.open( 'w' ) as file: dump( state, file, indent = 2 )


def save_conversation_messages( column ):
    from .classes import MessageTuple
    state = [ ]
    for row in column:
        row_tuple = MessageTuple( *row )
        text_message = row_tuple.text_message
        state.append( {
            'role': text_message.metadata__[ 'role' ],
            # TODO: Save MIME type of content.
            'content': (
                text_message.value if isinstance( text_message, StaticText )
                else text_message.object ),
            'include': row_tuple.checkbox_inclusion.value,
        } )
    return { 'column_conversation_history': state }


def select_conversation( gui, event ):
    conversations = gui.column_conversations_index
    old_id = conversations.current_id__
    new_id = event.obj.identity
    if old_id == new_id: return
    if None is old_id: gui.conversation_panes.pop( -1 )
    else:
        old_descriptor = conversations.index__[ old_id ]
        old_pane_gui = old_descriptor[ 'gui' ]
        old_pane_gui.conversation_pane.visible = False
    new_descriptor = conversations.index__[ new_id ]
    if None is new_descriptor.get( 'gui' ):
        new_pane_gui = create_conversation( gui )
        new_pane_gui.identity__ = new_id
        locate_and_restore_conversation( new_pane_gui )
        gui.conversation_panes.append( new_pane_gui.conversation_pane )
    else:
        new_pane_gui = new_descriptor[ 'gui' ]
        new_pane_gui.visible = True
    conversations.current_id__ = new_id
    from pprint import pprint
    pprint( event )


def toggle_summarization_prompt_display( gui ):
    gui.text_summarization_prompt.visible = gui.checkbox_summarize.value
    update_token_count( gui )


def toggle_system_prompt_display( gui ):
    gui.text_system_prompt.visible = gui.checkbox_display_system_prompt.value


def update_message( conversation_tuple, include = True ):
    from panel.widgets import StaticText
    from ..messages import count_tokens
    conversation_tuple.checkbox_inclusion.value = include
    text_message = conversation_tuple.text_message
    content = (
        text_message.value if isinstance( text_message, StaticText )
        else text_message.object )
    text_message.metadata__[ 'token_count' ] = count_tokens( content )


def update_prompt_text( gui, row_name, selector_name, text_prompt_name ):
    row = getattr( gui, row_name )
    selector = getattr( gui, selector_name )
    text_prompt = getattr( gui, text_prompt_name )
    template = selector.metadata__[ selector.value ][ 'template' ]
    variables = {
        element.metadata__[ 'id' ]: element.value for element in row
    }
    # TODO: Support alternative template types.
    text_prompt.object = template.format( **variables )


def update_summarization_prompt_text( gui ):
    update_prompt_text(
        gui,
        'row_summarization_prompt_variables',
        'selector_summarization_prompt',
        'text_summarization_prompt' )


def update_system_prompt_text( gui ):
    update_prompt_text(
        gui,
        'row_system_prompt_variables',
        'selector_system_prompt',
        'text_system_prompt' )
    update_token_count( gui )


def update_prompt_variables( gui, row_name, selector_name, callback ):
    from panel.widgets import TextInput
    row = getattr( gui, row_name )
    selector = getattr( gui, selector_name )
    row.clear( )
    variables = selector.metadata__[ selector.value ].get( 'variables', ( ) )
    for variable in variables:
        # TODO: Support other widget types, such as selectors and checkboxes.
        text_input = TextInput(
            name = variable[ 'label' ], value = variable[ 'default' ] )
        text_input.metadata__ = variable
        text_input.param.watch( lambda event: callback( gui ), 'value' )
        row.append( text_input )
    callback( gui )


def update_summarization_prompt_variables( gui ):
    update_prompt_variables(
        gui,
        'row_summarization_prompt_variables',
        'selector_summarization_prompt',
        update_summarization_prompt_text )


def update_system_prompt_variables( gui ):
    update_prompt_variables(
        gui,
        'row_system_prompt_variables',
        'selector_system_prompt',
        update_system_prompt_text )


def update_token_count( gui ):
    from ..messages import count_tokens
    total_tokens = 0
    for item in gui.column_conversation_history:
        checkbox, message_cell = item
        if checkbox.value:
            total_tokens += message_cell.metadata__[ 'token_count' ]
    if gui.checkbox_summarize.value:
        total_tokens += count_tokens( gui.text_summarization_prompt.object )
    else:
        total_tokens += count_tokens( gui.text_input_user.value )
    total_tokens += count_tokens( gui.text_system_prompt.object )
    tokens_limit = gui.selector_model.metadata__[
        gui.selector_model.value ][ 'tokens-limit' ]
    # TODO: Change color of text, depending on percentage of tokens limit.
    gui.text_tokens_total.value = f"{total_tokens} / {tokens_limit}"


def _populate_prompts_selector( gui_selector, prompts_directory ):
    from yaml import safe_load
    metadata = { }; prompt_names = [ ]
    for prompt_path in (
        prompts_directory.resolve( strict = True ).glob( '*.yaml' )
    ):
        with prompt_path.open( ) as file:
            contents = safe_load( file )
            id_ = contents[ 'id' ]
            metadata[ id_ ] = contents
            prompt_names.append( id_ )
    gui_selector.metadata__ = metadata
    gui_selector.options = prompt_names


def _provide_openai_models( ):
    from collections import defaultdict
    from operator import itemgetter
    import openai
    # TODO: Only call API when explicitly desired. Should persist to disk.
    model_names = sorted( map(
        itemgetter( 'id' ),
        openai.Model.list( ).to_dict_recursive( )[ 'data' ] ) )
    sysprompt_honor = defaultdict( lambda: False )
    sysprompt_honor.update( {
        'gpt-3.5-turbo-0613': True,
        'gpt-3.5-turbo-16k-0613': True,
        'gpt-4': True,
        'gpt-4-32k': True,
        'gpt-4-0613': True,
        'gpt-4-32k-0613': True,
    } )
    tokens_limits = defaultdict( lambda: 4096 ) # Some are 4097... _shrug_.
    tokens_limits.update( {
        'code-davinci-002': 8000,
        'gpt-3.5-turbo-16k': 16384,
        'gpt-3.5-turbo-16k-0613': 16384,
        'gpt-4': 8192,
        'gpt-4-32k': 32768,
        'gpt-4-0613': 8192,
        'gpt-4-32k-0613': 32768,
    } )
    return {
        model_name: {
            'honors-system-prompt': sysprompt_honor[ model_name ],
            'tokens-limit': tokens_limits[ model_name ],
        }
        for model_name in model_names
    }


# TODO? Move to dedicated OpenAI module.
def _try_run_openai_chat( gui, conversation_tuple, messages ):
    from openai import ChatCompletion, OpenAIError
    try:
        response = ChatCompletion.create(
            messages = messages,
            model = gui.selector_model.value,
            stream = True,
            temperature = gui.slider_temperature.value )
        initial_chunk = next( response )
        # TODO? Validate initial chunk.
        for chunk in response:
            delta = chunk.choices[ 0 ].delta
            if not delta: break
            conversation_tuple.text_message.object += delta[ 'content' ]
    except OpenAIError as exc: return f"Error: {exc}"
    return 'OK'
