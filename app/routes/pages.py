# from fastapi import APIRouter, Request, Depends
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from src.auth.authenticate import authenticate_cookie
# templates = Jinja2Templates(directory="view")  # или "src/view", "app/view" — в зависимости от структуры проекта
# pages_route = APIRouter()
# @pages_route.get("/", response_class=HTMLResponse)
# async def home(request: Request, user=Depends(authenticate_cookie)):
#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request, "user": user}  # добавьте user в контекст, если нужно
    # )
from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates
from src.auth.authenticate import authenticate_cookie
from src.DataBase.engine import get_session
from src.Thread.thread import ThreadRepository
from src.Users.user_repo import UserRepository
from src.Balance.balance import BalanceRepository
from src.Balance.transaction import TransactionRepository
from src.MQ.producer import publish_task

import uuid
from pathlib import Path

templates = Jinja2Templates(directory="view")
pages_route = APIRouter()

AUDIO_DIR = "/app/test_audio"
Path(AUDIO_DIR).mkdir(exist_ok=True)

@pages_route.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    email = Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):  
    user_repo = UserRepository(session)
    user = user_repo.get_by_email(email)
    if not user:
        return RedirectResponse("/login", status_code=302)

    repo = ThreadRepository(session)
    threads = repo.get_threads_by_user_id(user.id)

    balance_repo = BalanceRepository(session)
    balance = balance_repo.get_by_user_id(user.id)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "threads": threads,
            "balance": balance.amount if balance else 0
        }
    )

@pages_route.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    email: str = Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):
    user_repo = UserRepository(session)
    user = user_repo.get_by_email(email)

    if not user:
        return RedirectResponse("/login", status_code=302)

    if not file.filename.endswith(".mp3"):
        return RedirectResponse("/", status_code=302)

    task_id = str(uuid.uuid4())
    file_path = f"{AUDIO_DIR}/{task_id}.mp3"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    publish_task({
        "task_id": task_id,
        "user_id": user.id,
        "audio_name": file.filename,
        "audio_path": file_path
    })

    return RedirectResponse("/", status_code=302)

@pages_route.get("/thread/{user_id}/{thread_id}", response_class=HTMLResponse)
def view_thread(
    user_id: int,
    thread_id: int,
    request: Request,
    # user=Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):
    repo = ThreadRepository(session)
    thread = repo.get_thread_by_id(thread_id)

    if not thread or thread.user_id != user_id:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "thread.html",
        {
            "request": request,
            "thread": thread
        }
    )

@pages_route.get("/balance", response_class=HTMLResponse)
def balance_page(
    request: Request,
    email = Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):
    user = UserRepository(session).get_by_email(email)
    if not user:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse(
        "balance.html",
        {"request": request}
    )


@pages_route.post("/balance")
def balance_post(
    amount: int = Form(...),
    email = Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):
    user = UserRepository(session).get_by_email(email)
    if not user:
        return RedirectResponse("/login", status_code=302)

    balance_repo = BalanceRepository(session)
    transaction_repo = TransactionRepository(session)
    balance_repo.increase_balance(user.id, amount)
    transaction_repo.create_transaction(
        user_id=user.id,
        amount=amount,
        type="credit"
    )

    session.commit()

    return RedirectResponse("/", status_code=302)

@pages_route.get("/admin", response_class=HTMLResponse)
def admin_page(
    request: Request,
    email = Depends(authenticate_cookie),
    session: Session = Depends(get_session)
):
    user_repo = UserRepository(session)
    user = user_repo.get_by_email(email)
    if not user:
        return RedirectResponse("/login", status_code=302)

    users = []
    if user.role == "admin":
        users = user_repo.get_all_users()["users"]

    transaction_repo = TransactionRepository(session)
    if user.role == "admin":
        transactions = []
        for u in user_repo.get_all_users()["users"]:
            trans = transaction_repo.get_all_by_user_id(u["id"])
            for t in trans:
                transactions.append({"transaction_id": t.id, "user_id": t.user_id, "amount": t.amount, "type": t.type})
    else:
        trans = transaction_repo.get_all_by_user_id(user.id)
        transactions = [{"transaction_id": t.id, "user_id": t.user_id, "amount": t.amount, "type": t.type} for t in trans]

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "users": users,
            "transactions": transactions
        }
    )
