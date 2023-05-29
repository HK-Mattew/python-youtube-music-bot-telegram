import enum
from time import sleep
from config import Config
from telegram import (
    ParseMode, Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup,
    )
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext, ConversationHandler,
    CommandHandler, MessageHandler, Filters
    )

from core import users


CHOOSE_PAINEL_OPTIONS, GET_USER_ID, ENTER_TEXT_SEND_DM_USERS, ENTER_AMOUNT_OF_USERS_SEND_DM_MESSAGE, CONFIRM_SEND_DM_USERS = range(5)




def admin(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END


    chat_id = update.effective_chat.id
    user_language_code = update.effective_user.language_code

    if not user.id in Config.OWNERS_ID:
        return ConversationHandler.END


    keyboard = [
            ['GET-USER_ID'],
            ['DM-USERS'],
            ['❌ Cancelar']
        ]

    text_pt = """[Painel de Administração]\n\nGET-USER_ID - Pegar ID de um usuário;\nDM-USERS - Enviar mensagem para os usuarios;\n\nSelecione o que deseja fazer:"""
    context.bot.send_message(chat_id=chat_id, text=text_pt,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
    return CHOOSE_PAINEL_OPTIONS




def choose_painel_options(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END

    chat_id = update.effective_chat.id
    user_language_code = update.effective_user.language_code


    if update.message.text.strip() in ['GET-USER_ID']:
        text = """Envie-me o nome de usuário ou uma mensagem encaminhada do usuário para que eu possa obter o ID:"""

        context.bot.send_message(chat_id=chat_id, 
        text=text,
        reply_markup=ReplyKeyboardMarkup([['❌ Cancelar']], resize_keyboard=True, one_time_keyboard=True)
        )
        return GET_USER_ID


    if update.message.text.strip() in ['DM-USERS']:
        text_pt = """Envie-me a mensagem que deseja enviar a todos os usuários:"""
        context.bot.send_message(chat_id=chat_id, text=text_pt, reply_markup=ReplyKeyboardMarkup([['❌ Cancelar']], resize_keyboard=True, one_time_keyboard=True))
        return ENTER_TEXT_SEND_DM_USERS

    

    return ConversationHandler.END

    


def get_user_id(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END

    chat_id = update.effective_chat.id
    user_language_code = update.effective_user.language_code

    # BOT_DATA = context.bot_data
    # CONFIGS = BOT_DATA['configs']

    if update.message.forward_from:
        forward_from = update.message.forward_from
        text = f"Nome: {forward_from.full_name}\nNome de Usuário: {forward_from.username}\nID: {forward_from.id}"

    else:
        username = update.message.text.strip().replace('@', '')
        try:
            u_c = context.bot.get_chat('@'+username)
            text = f"Nome: {u_c.first_name}\nNome de Usuário: {u_c.username}\nID: {u_c.id}"
        except Exception as err:
            text = f'Erro: => {err}'
            pass

    context.bot.send_message(chat_id=chat_id, 
        text=text,
        reply_markup=ReplyKeyboardRemove()
        )


    return ConversationHandler.END





def enter_msg_send_dm_users(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END


    chat_id = update.effective_chat.id
    user_language_code = update.effective_user.language_code

    BOT_DATA = context.bot_data


    forward_from_chat = update.message.forward_from_chat
    if forward_from_chat:
        context.bot.send_message(
            chat_id=chat_id,
            text='Forwarded messages are not allowed. Send a written message:'
        )
        return ENTER_AMOUNT_OF_USERS_SEND_DM_MESSAGE
    else:
        update.message.copy(
            chat_id=chat_id
        )



    _DATA_INFO = {}
    _DATA_INFO['message'] = update.message
    
    context.user_data.setdefault(
        'convs',
        {
            'admin': {
                'send_dm': {}
                }
        }
        )
    context.user_data['convs']['admin']['send_dm'] = _DATA_INFO



    keyboard = [
        ['🌏 ALL'],
        ['❌ Cancel']
    ]
    context.bot.send_message(
        chat_id=chat_id,
        text="""How many users do you want the post to be sent to?""",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True)
    )
    return ENTER_AMOUNT_OF_USERS_SEND_DM_MESSAGE





def amount_send_dm_users(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END


    chat_id = update.effective_chat.id
    user_language_code = update.effective_user.language_code




    if not update.message.text == '🌏 ALL':
        try:
            amount_of_users = int(update.message.text)
        except:
            context.bot.send_message(
                chat_id=chat_id,
                text="""Invalid value. Try again:"""
            )
            return ENTER_AMOUNT_OF_USERS_SEND_DM_MESSAGE
            

        context.user_data['convs']['admin']['send_dm']['amount_of_users'] = amount_of_users
        context.bot.send_message(
                chat_id=chat_id,
                text=f"""Your post will be sent to: {amount_of_users} Users"""
            )


    keyboard = [
        ['✅ Yes, Submit'],
        ['❌ Cancel']
    ]
    context.bot.send_message(
        chat_id=chat_id,
        text="""Do you really want to send this message to users? Click "Yes, Submit" or "Cancel" to proceed.""",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True)
    )

    return CONFIRM_SEND_DM_USERS





def confirm_send_dm_users(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END


    chat_id = update.effective_chat.id



    def send_dm_message_to_users(*args, **kwargs):
        msg_remove_keyboard = context.bot.send_message(
            chat_id=chat_id,
            text='...',
            reply_markup=ReplyKeyboardRemove()
        )
        msg_remove_keyboard.delete()

        tg_msg_template = '[Status]\n{status}\n\nFeedback: {feedback}'
        msg_template = context.bot.send_message(
            chat_id=chat_id,
            text=tg_msg_template.format(status='...',feedback='Iniciando...')
        )


        cursor = users.find({}, ['user_id'])

        data = [x for x in cursor]
        try:
            cursor.close()
        except:
            pass

        if not data:
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_template.message_id,
                text=tg_msg_template.format(status='Ended;',feedback='Not users.'),
            )
            return

        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_template.message_id,
            text=tg_msg_template.format(status='Iniciando...',feedback=f'Será enviada uma mensagem para {len(data)} usuarios.'),
        )
        sleep(5)
        
        status = {
            'has_received': 0,
            'did_not_receive': 0,
            'fail': 0
        }

        index = 0
        next_update_template_msg = 30

        for user in data:
            index += 1

            user_id = user['user_id']


            try:
                #send msg
                obj_msg = context.user_data['convs']['admin']['send_dm']['message']
                obj_msg.copy(
                    chat_id=user_id
                )
            except Exception as err:
                status['fail'] += 1
                continue


            status['has_received'] += 1

            if index == 1 or index >= next_update_template_msg:
                next_update_template_msg = (index+30)
                context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_template.message_id,
                    text=tg_msg_template.format(
                        status='\n'.join([f'{key}: {value}' for key, value in status.items()]),
                        feedback='Enviando...'
                        ),
                    )

            #Se for 0, é para enviar a todos usuarios;
            if not context.user_data['convs']['admin']['send_dm'].get('amount_of_users', 0) == 0:
                if status['has_received'] >= context.user_data['convs']['admin']['send_dm']['amount_of_users']:
                    break

            sleep(0.003)

        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_template.message_id,
            text=tg_msg_template.format(
                status='\n'.join([f'{key}: {value}' for key, value in status.items()]),
                feedback='Finalizado.'
                ),
            )

    
    ponto_msg = context.bot.send_message(
        chat_id=chat_id,
        text='...', reply_markup=ReplyKeyboardRemove())
    ponto_msg.delete()



    context.job_queue.run_once(
        send_dm_message_to_users,
        when=1
    )
    return ConversationHandler.END




def cancel(update, context):
    user = update.effective_user
    if not user or (user and user.is_bot):
        return ConversationHandler.END

    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id=chat_id, 
        text='Cancelled.',
        reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END



admin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('admin', admin, allow_edited=False)],
    states={
        CHOOSE_PAINEL_OPTIONS: [MessageHandler(Filters.regex('^GET-USER_ID|DM-USERS$'), choose_painel_options, edited_updates=False)],
        GET_USER_ID: [MessageHandler(Filters.text & ~(Filters.regex('^❌ Cancelar|❌ Cancel$') | Filters.command), get_user_id, edited_updates=False)],
        ENTER_TEXT_SEND_DM_USERS: [MessageHandler(Filters.all & ~(Filters.regex('^❌ Cancelar|❌ Cancel$') | Filters.command), enter_msg_send_dm_users, edited_updates=False)],
        ENTER_AMOUNT_OF_USERS_SEND_DM_MESSAGE: [
            MessageHandler(Filters.text & ~(Filters.regex('^❌ Cancelar|❌ Cancel$') | Filters.command), amount_send_dm_users, edited_updates=False)
            ],
        CONFIRM_SEND_DM_USERS: [MessageHandler(Filters.regex('^✅ Yes, Submit$') & ~(Filters.regex('^❌ Cancelar|❌ Cancel$') | Filters.command), confirm_send_dm_users, edited_updates=False)]
    },
    fallbacks=[
        MessageHandler(Filters.regex('^❌ Cancelar|❌ Cancel$') & ~Filters.command, cancel, edited_updates=False),
        CommandHandler('cancel', cancel, allow_edited=False)
        ],
    allow_reentry=False,
    per_user=True,
    name='admin'
)