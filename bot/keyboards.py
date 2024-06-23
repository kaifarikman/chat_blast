from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_buttons = [
    [
        InlineKeyboardButton(text="Создать новую рассылку", callback_data="create_newsletter")
    ],
    [
        InlineKeyboardButton(text="Просмотреть активные рассылки", callback_data="newsletters_data_active")
    ],
    [
        InlineKeyboardButton(text="Просмотреть неактивные рассылки", callback_data="newsletters_data_inactive")
    ],
    [
        InlineKeyboardButton(text="Изменить ПРАЙС во всех чатах", callback_data="change_price_in_all_chats")
    ]
]

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=admin_buttons)

yes_no_buttons = [
    [
        InlineKeyboardButton(text="Создать", callback_data="yes_create")
    ],
    [
        InlineKeyboardButton(text="Удалить", callback_data="no_create")
    ]
]

yes_no_keyboard = InlineKeyboardMarkup(inline_keyboard=yes_no_buttons)

back_buttons = [
    [
        InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start")
    ]
]
back_keyboard = InlineKeyboardMarkup(inline_keyboard=back_buttons)


def create_newsletters_tables(names: dict, page: int, status: str):
    buttons = []

    ind = (page - 1) * 9
    for i in range(3):
        lst = []
        for j in range(3):
            try:
                button = InlineKeyboardButton(text=str(names[ind][1]),
                                              callback_data=f"check_newsletter_{names[ind][0]}_{page}")
                lst.append(button)
            except Exception as e:
                '''рализация indexError , для 9 кнопок без мучений и ифов'''
                ...
            ind += 1
        buttons.append(lst)

    pages_count = len(names) // 9 + 1 if len(names) % 9 != 0 else len(names) // 9
    left_page = page - 1 if page != 1 else pages_count
    right_page = page + 1 if page != pages_count else 1
    buttons.append(
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"change_data_{status}_{left_page}"),
            InlineKeyboardButton(text=f"{page} из {pages_count}", callback_data="dummy"),
            InlineKeyboardButton(text="➡️", callback_data=f"change_data_{status}_{right_page}")
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start")
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def newsletter_keyboard(id_: int, status: bool, page: int):
    status_ = "active" if status else "inactive"

    buttons = [
        [
            InlineKeyboardButton(text="Название группы", callback_data=f"edit_group_name_{id_}_{page}"),
            InlineKeyboardButton(text="ID группы", callback_data=f"edit_group_id_{id_}_{page}")
        ],
        [
            InlineKeyboardButton(text="Время рассылки", callback_data=f"edit_mailing_times_{id_}_{page}"),
            InlineKeyboardButton(text="ПРАЙС", callback_data=f"edit_text_{id_}_{page}")
        ],
        [
            InlineKeyboardButton(text="Статус группы", callback_data=f"edit_status_{id_}_{page}"),
        ],
        [
            InlineKeyboardButton(text="Просмотреть карточку", callback_data=f"watch_card_{id_}_{page}")
        ],
        [
            InlineKeyboardButton(text="Вернуться к списку групп", callback_data=f"""change_data_{status_}_{page}""")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def go_to_newsletter(id_, page_):
    buttons = [
        [
            InlineKeyboardButton(text="Вернуться обратно", callback_data=f"check_newsletter_{id_}_{page_}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def edit_status(id_, page):
    buttons = [
        [
            InlineKeyboardButton(text="Активная", callback_data=f"status_edit_{id_}_{page}_active")
        ],
        [
            InlineKeyboardButton(text="Неактивный", callback_data=f"status_edit_{id_}_{page}_inactive")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
