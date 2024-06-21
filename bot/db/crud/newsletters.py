from bot.db.models.newsletters import Newsletters
from bot.db.schemas.newsletters import Newsletters as NewslettersDB
from sqlalchemy.orm import sessionmaker
from bot.db.db import engine


def add_newsletter(newsletter: Newsletters):
    session = sessionmaker(engine)()
    newsletter_db = NewslettersDB(
        group_name=newsletter.group_name,
        group_id=newsletter.group_id,
        mailing_times=newsletter.mailing_times,
        text=newsletter.text,
        status=newsletter.status,
    )
    session.add(newsletter_db)
    session.commit()


def get_newsletter_by_id(newsletter_id: int):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(
        id=newsletter_id
    ).first()
    return query


def get_all_newsletters():
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).all()
    return query


def get_newsletters_by_status(status: str):
    flag = True
    if status == "inactive":
        flag = False
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).all()
    dictionary = dict()
    index = 0
    for newsletter in query:
        if bool(newsletter.status) == flag:
            dictionary[index] = [newsletter.id, newsletter.group_name]
            index += 1
    return dictionary


def edit_newsletter_group_name_by_id(id_: int, new_name: str):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(id=id_).first()
    query.group_name = new_name
    session.commit()


def edit_newsletter_group_id_by_id(id_: int, new_id: int):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(id=id_).first()
    query.group_id = new_id
    session.commit()


def edit_newsletter_mailing_times_by_id(id_: int, mailing_times: str):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(id=id_).first()
    query.mailing_times = mailing_times
    session.commit()


def edit_newsletter_text_by_id(id_: int, new_text: str):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(id=id_).first()
    query.text = new_text
    session.commit()


def edit_newsletter_status_by_id(id_: int, status: str):
    session = sessionmaker(engine)()
    query = session.query(NewslettersDB).filter_by(id=id_).first()
    if status == "active":
        query.status = 1
    else:
        query.status = 0
    session.commit()


