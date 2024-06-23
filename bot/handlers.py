from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import config

import bot.texts as texts
import bot.keyboards as keyboards
import bot.utils as utils

import bot.db.crud.newsletters as crud_newsletters
from bot.db.models.newsletters import Newsletters as NewslettersModel

router = Router()


@router.message(Command("start"))
async def start_(message: Message, state: FSMContext):
    await state.clear()

    user_id = int(message.from_user.id)
    if user_id not in config.admins:
        return await message.answer(
            text="У вас нет доступа к боту",
        )
    await message.answer(
        text=texts.start_text,
        reply_markup=keyboards.admin_keyboard
    )


@router.callback_query(F.data == "start")
async def start_(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()
        await callback.message.edit_reply_markup()
    except Exception as e:
        print(e)
    """по факту проверка не нужна. на всякий случай"""
    user_id = int(callback.from_user.id)
    if user_id not in config.admins:
        return await callback.message.answer(
            text="У вас нет доступа к боту",
        )
    await callback.message.answer(
        text=texts.start_text,
        reply_markup=keyboards.admin_keyboard
    )


class CreateNewsletter(StatesGroup):
    group_name = State()
    group_id = State()
    mailing_times = State()
    text = State()
    last = State()


@router.callback_query(F.data == "create_newsletter")
async def create_newsletter_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await state.clear()
    await callback.message.answer(
        text=texts.group_name_text
    )
    await state.set_state(CreateNewsletter.group_name)


@router.message(CreateNewsletter.group_name)
async def group_name_(message: Message, state: FSMContext):
    group_name = str(message.text)
    await state.update_data({"group_name": group_name})
    await message.answer(
        text=texts.group_id_text
    )

    await state.set_state(CreateNewsletter.group_id)


@router.message(CreateNewsletter.group_id)
async def group_id_(message: Message, state: FSMContext):
    try:
        group_id = int(message.text)
    except Exception as e:
        print(e)
        return await message.answer(
            text="Вы ввели не id. Можете ввести еще раз"
        )
    await state.update_data({"group_id": group_id})
    await message.answer(
        text=texts.mailing_times_text
    )

    await state.set_state(CreateNewsletter.mailing_times)


@router.message(CreateNewsletter.mailing_times)
async def mailing_times_(message: Message, state: FSMContext):
    mailing_times = str(message.text)
    if not utils.valid_times(mailing_times):
        return await message.answer(
            text="""Формат неверный. Введите время через enter, разделив часы и минуты символом ":" """
        )
    await state.update_data({"mailing_times": " ".join(utils.valid_times(mailing_times))})
    await message.answer(
        text=texts.text_text
    )
    await state.set_state(CreateNewsletter.text)


@router.message(CreateNewsletter.text)
async def text_(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data({"text": text})

    data = await state.get_data()

    await message.answer(
        text=texts.create_text(data),
        reply_markup=keyboards.yes_no_keyboard,
        parse_mode="HTML"
    )

    await state.set_state(CreateNewsletter.last)


@router.callback_query(F.data == "yes_create", CreateNewsletter.last)
async def yes_create_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    data = await state.get_data()
    await state.clear()

    newsletter = NewslettersModel(
        group_name=data["group_name"],
        group_id=int(data["group_id"]),
        mailing_times=str(data["mailing_times"]),
        text=data["text"],
        status=True
    )

    crud_newsletters.add_newsletter(newsletter)

    await callback.message.answer(
        text=texts.yes_created,
        reply_markup=keyboards.back_keyboard
    )


@router.callback_query(F.data == "no_create", CreateNewsletter.last)
async def no_create_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await state.clear()
    await callback.message.answer(
        text=texts.no_created,
        reply_markup=keyboards.back_keyboard
    )


@router.callback_query(F.data.startswith("newsletters_data_"))
async def active_newsletters_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()

    data = str(callback.data).split("_")
    page = 1
    if data[-1] == "active":
        text_message = "Ваши активные рассылки"
        status = "active"
    else:
        text_message = "Ваши неактивные рассылки"
        status = "inactive"
    names = crud_newsletters.get_newsletters_by_status(status)
    if len(names) == 0:
        return await callback.message.answer(
            text=texts.no_created_newsletters,
            reply_markup=keyboards.back_keyboard
        )
    await callback.message.answer(
        text=text_message,
        reply_markup=keyboards.create_newsletters_tables(names, page, status)
    )


@router.callback_query(F.data.startswith("change_data_"))
async def change_data_(callback: CallbackQuery):
    await callback.answer()
    data = str(callback.data).split("_")

    status, page = data[2], int(data[3])
    names = crud_newsletters.get_newsletters_by_status(status)
    await callback.message.edit_reply_markup(reply_markup=keyboards.create_newsletters_tables(names, page, status))


@router.callback_query(F.data == "dummy")
async def dummy_(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data.startswith("check_newsletter_"))
async def check_newsletter_(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    data = str(callback.data).split("_")
    page = int(data[-1])
    newsletter = crud_newsletters.get_newsletter_by_id(int(data[-2]))
    text = texts.newsletter_text.format(group_name=newsletter.group_name)

    keyboard = keyboards.newsletter_keyboard(newsletter.id, newsletter.status, page)

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )


class EditGroupName(StatesGroup):
    info = State()


@router.callback_query(F.data.startswith("edit_group_name_"))
async def edit_group_name_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]

    await callback.message.answer(
        text=texts.edit_group_name_text
    )

    await state.set_state(EditGroupName.info)
    await state.update_data({"info": info})


@router.message(EditGroupName.info)
async def edit_group_name_state(message: Message, state: FSMContext):
    new_name = str(message.text)
    data = await state.get_data()

    id_, page_ = data["info"]
    id_, page_ = int(id_), int(page_)

    await state.clear()

    crud_newsletters.edit_newsletter_group_name_by_id(id_, new_name)

    await state.clear()

    await message.answer(
        text="Успешно сменилось название группы",
        reply_markup=keyboards.go_to_newsletter(id_, page_)
    )


class EditGroupID(StatesGroup):
    info = State()


@router.callback_query(F.data.startswith("edit_group_id_"))
async def edit_group_id_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]

    await callback.message.answer(
        text=texts.edit_group_id_text
    )

    await state.set_state(EditGroupID.info)
    await state.update_data({"info": info})


@router.message(EditGroupID.info)
async def edit_group_name_state(message: Message, state: FSMContext):
    new_id = int(message.text)
    data = await state.get_data()

    id_, page_ = data["info"]
    id_, page_ = int(id_), int(page_)

    await state.clear()

    crud_newsletters.edit_newsletter_group_id_by_id(id_, new_id)

    await state.clear()

    await message.answer(
        text="Успешно сменился ID группы",
        reply_markup=keyboards.go_to_newsletter(id_, page_)
    )


class EditGroupMailingTimes(StatesGroup):
    info = State()


@router.callback_query(F.data.startswith("edit_mailing_times_"))
async def edit_group_id_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]

    await callback.message.answer(
        text=texts.edit_mailing_times_text
    )

    await state.set_state(EditGroupMailingTimes.info)
    await state.update_data({"info": info})


@router.message(EditGroupMailingTimes.info)
async def edit_group_name_state(message: Message, state: FSMContext):
    new_mailing_time = str(message.text)
    if not utils.valid_times(new_mailing_time):
        return await message.answer(
            text="""Формат неверный. Введите время через enter, разделив часы и минуты символом ":" """
        )
    new_mailing_time = " ".join(utils.valid_times(new_mailing_time))

    data = await state.get_data()

    id_, page_ = data["info"]
    id_, page_ = int(id_), int(page_)

    await state.clear()

    crud_newsletters.edit_newsletter_mailing_times_by_id(id_, new_mailing_time)

    await state.clear()

    await message.answer(
        text="Успешно сменилось время рассылки группы",
        reply_markup=keyboards.go_to_newsletter(id_, page_)
    )


class EditGroupText(StatesGroup):
    info = State()


@router.callback_query(F.data.startswith("edit_text_"))
async def edit_group_id_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]

    await callback.message.answer(
        text=texts.edit_text_text
    )

    await state.set_state(EditGroupText.info)
    await state.update_data({"info": info})


@router.message(EditGroupText.info)
async def edit_group_name_state(message: Message, state: FSMContext):
    new_text = message.html_text
    data = await state.get_data()

    id_, page_ = data["info"]
    id_, page_ = int(id_), int(page_)

    await state.clear()

    crud_newsletters.edit_newsletter_text_by_id(id_, new_text)

    await state.clear()

    await message.answer(
        text="Успешно сменился Прайс",
        reply_markup=keyboards.go_to_newsletter(id_, page_)
    )


@router.callback_query(F.data.startswith("edit_status_"))
async def edit_status_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]
    id_, page = map(int, info)
    await callback.message.answer(
        text=texts.edit_status_text,
        reply_markup=keyboards.edit_status(id_, page)
    )


@router.callback_query(F.data.startswith("status_edit_"))
async def edit_status_(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    data = str(callback.data).split("_")
    id_, page_, status = data[-3], data[-2], data[-1]
    id_, page_ = int(id_), int(page_)

    crud_newsletters.edit_newsletter_status_by_id(id_, status)

    await callback.message.answer(
        text="Успешно изменился статус",
        reply_markup=keyboards.go_to_newsletter(id_, page_)
    )


@router.callback_query(F.data.startswith("watch_card_"))
async def watch_card_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.clear()

    data = str(callback.data).split("_")
    info = [data[-2], data[-1]]
    id_, page = map(int, info)
    newsletter = crud_newsletters.get_newsletter_by_id(id_)
    text = texts.create_text_for_edit_menu(newsletter.group_name, newsletter.group_id, newsletter.mailing_times,
                                           newsletter.text, newsletter.status)
    keyboard = keyboards.go_to_newsletter(id_, page)
    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )


class NewPrice(StatesGroup):
    new_price = State()


@router.callback_query(F.data == "change_price_in_all_chats")
async def change_price_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()

    await callback.message.answer(
        text=texts.new_price,
        reply_markup=keyboards.back_keyboard
    )
    await state.set_state(NewPrice.new_price)


@router.message(NewPrice.new_price)
async def new_price_(message: Message, state: FSMContext):
    await state.clear()

    text = message.html_text
    crud_newsletters.edit_all_text(text)
    await message.answer(
        text="ПРАЙС успешно сменился",
        reply_markup=keyboards.back_keyboard
    )


@router.message(Command("ui"))
async def m(message: Message):
    import bot.mailer as mailer
    await mailer.mailer()


class ForMeCommand(StatesGroup):
    info = State()


@router.message(Command("for_me"))
async def for_me(message: Message, state: FSMContext):
    await message.answer(text="введите инфо")
    await state.set_state(ForMeCommand.info)


@router.message(ForMeCommand.info)
async def for_me(message: Message, state: FSMContext):
    await state.clear()
    text = message.text
    group_name, group_id, mailing_times, text, status = text.split(" ")
    newsletter = NewslettersModel(
        group_name=group_name, group_id=int(group_id),
        mailing_times="10:00", text=text, status=bool(status)
    )
    crud_newsletters.add_newsletter(newsletter)
