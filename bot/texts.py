def create_text(data: dict) -> str:
    answer = "Проверьте вашу заявку:\n\n"
    answer += f"""Название группы: {data["group_name"]}\n"""
    answer += f"""ID группы: {data["group_id"]}\n"""
    answer += f"""Время рассылки: {", ".join(data["mailing_times"].split())}\n"""
    answer += f"""Прайс:\n{data["text"]}"""
    return answer


def create_text_for_edit_menu(group_name, group_id, mailing_times, text, status):
    answer = "Карточка группы:\n\n"
    answer += f"""Название группы: {group_name}\n"""
    answer += f"""ID группы: {group_id}\n"""
    answer += f"""Время рассылки: {mailing_times}\n"""
    answer += f"""Прайс:\n{text}\n"""
    answer += f"""Статус: {"активный" if status else "неактивный"}"""
    return answer


start_text = "У вас есть подобный функционал"
group_name_text = "Введите название группы"
group_id_text = "Введите id группы"
mailing_times_text = "Введите время рассылка формата:\nhh:mm"
text_text = "Введите прайс"
yes_created = "Ваша рассылка создалась. Можете вернуться в главное меню"
no_created = "Вы отменили создание рассылки. Можете вернуться в главное меню"
no_created_newsletters = "Вы еще не создали заявку данного типа. Создайте!"
newsletter_text = "Ваша группа: {group_name}\nЧто вы хотите изменить в группе?"

edit_group_name_text = "Напишите новое название для группы"
edit_group_id_text = "Напишите новый ID группы"
edit_mailing_times_text = "Напишите новое время рассылки формата:\nhh:mm"
edit_text_text = "Напишите новый прайс"
edit_status_text = "Измените статус"

new_price = "Введите новый ПРАЙС для всех групп"
