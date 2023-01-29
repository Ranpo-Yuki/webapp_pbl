from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from models import *
import db
import os
 
app = FastAPI(
    title='出席アプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルな出席アプリを作る．',
    version='0.9 beta'
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

 # new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
 

async def test(request: Request):
    if request.method == 'GET':
        db.session.close()

        return templates.TemplateResponse('test.html',
                                        {'request': request})

    if request.method == 'POST':
        data = await request.form()
        username_get = data.get('username')
        """
        if username_get == 'Ranpo':
            id_get = 3039
        elif username_get == 'Jerk':
            id_get = 3151
        elif username_get == 'Apple':
            id_get = 2000
        elif username_get == 'gorilla':
            id_get = 2001
        elif username_get == 'bugle':
            id_get = 2002
        """
        username = User(username=username_get)
        db.session.add(username)  # 追加
        db.session.commit()  # データベースにコミット
        db.session.close()  # セッションを閉じる

        return templates.TemplateResponse('test.html',
                                        {'request': request})

async def index(request: Request):
    # ユーザとタスクを取得
    # とりあえず今はadminユーザのみ取得

    """
    user = db.session.query(User).filter(User.username == 'Ranpo').order_by(User.id.desc()).first()
    #user = db.session.query(User).filter(User.username == 'Ranpo').first()
    db.session.close()
    print('ランポ：', user)
    print('ID', user.id) 
    print('ユーザーネーム:', user.username)
    print('日付：', user.datetime) 
    """  

    if request.method == 'GET':
        db.session.close()

        log  = ' '

        return templates.TemplateResponse('index.html',
                                        {'request': request,
                                        'log': log})

    if request.method == 'POST':
        data = await request.form()
        username_get = data.get('username')
        username = User(username=username_get)
        db.session.add(username)  # 追加
        db.session.commit()  # データベースにコミット
        db.session.close()  # セッションを閉じる

        log = username_get + 'が出席しました'

        return templates.TemplateResponse('index.html',
                                        {'request': request,
                                        'log': log})

async def DisplayDate(request: Request):
    Jerk = db.session.query(User).filter(User.username == 'Jerk').order_by(User.id.desc()).first()
    Ranpo = db.session.query(User).filter(User.username == 'Ranpo').order_by(User.id.desc()).first()
    Apple = db.session.query(User).filter(User.username == 'Apple').order_by(User.id.desc()).first()
    Gorilla = db.session.query(User).filter(User.username == 'gorilla').order_by(User.id.desc()).first()
    Bugle = db.session.query(User).filter(User.username == 'bugle').order_by(User.id.desc()).first()

    db.session.close()    

    return templates.TemplateResponse('DisplayDate.html',
                                        {'request': request,
                                        'Jerk': Jerk,
                                        'Ranpo': Ranpo,
                                        'Apple': Apple,
                                        'Gorilla': Gorilla,
                                        'Bugle': Bugle})


async def DateSearch(request: Request):
    return templates.TemplateResponse('DateSearch.html',
                                        {'request': request})

async def NameSearch(request: Request):
    member = db.session.query(User).all()

    s_m = set()
    for m in member:        
        u_m = m.username
        if u_m =='〇〇':
            continue
        elif u_m =='Ranp':
            continue
        else:
            s_m.add(u_m)        

    l_m = list(s_m)

    if request.method =='GET':
        member = db.session.query(User).all()
        user = db.session.query(User).filter(User.username == '〇〇').first()
        user_all = '-'
        db.session.close() 
        return templates.TemplateResponse('NameSearch.html',
                                        {'request': request,
                                        'member': l_m,
                                        'user': user,
                                        'user_all': user_all})
    
    if request.method =='POST':
        data = await request.form()
        name = data.get('name')
        print('名前：', name)

        user = db.session.query(User).filter(User.username == name).order_by(User.id.desc()).first()
        user_all = db.session.query(User).filter(User.username == name).order_by(User.id.desc()).all()

        db.session.close()  
        
        s_d = set()
        for u in user_all:
            u_d = u.datetime.date()
            s_d.add(u_d)

        l_d = list(s_d)
        l_d.sort(reverse=True)
        
        return templates.TemplateResponse('NameSearch.html',
                                        {'request': request,
                                        'member': l_m,
                                        'user': user,
                                        'user_all': l_d})   


"""
def DateSearch(request: Request):
    return templates.TemplateResponse('DateSearch.html',
                                      {'request': request})
def NameSearch(request: Request):
    return templates.TemplateResponse('NameSearch.html',
                                      {'request': request})


def admin(request: Request):
    # ユーザとタスクを取得
    # とりあえず今はadminユーザのみ取得
    user = db.session.query(User).filter(User.username == 'Ranpo').first()
    db.session.close()
 
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})

"""
