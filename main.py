from typing import List
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from auth import Auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBearer()
auth_handler = Auth()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/', response_model=List[schemas.Post])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_posts = crud.get_posts(db, skip=skip, limit=limit)
    return all_posts

@app.get('/post/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: Session=Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    return db_post

@app.post('/post/{post_id}/like', response_model=schemas.Post, dependencies=[Depends(auth_handler.decode_token)])
def like_post(post_id: int, db: Session=Depends(get_db)):
    return crud.update_post(db, post_id, like=1)

@app.post('/post/{post_id}/dislike', response_model=schemas.Post, dependencies=[Depends(auth_handler.decode_token)])
def like_post(post_id: int, db: Session=Depends(get_db)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return crud.update_post(db, post_id, like=-1)

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user


@app.post('/users/{user_id}/posts/', response_model=schemas.Post, dependencies=[Depends(auth_handler.decode_token)])
def create_user_post(user_id: int, content:str, db: Session = Depends(get_db)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return crud.create_user_post(db=db, user_id=user_id, content=content)


@app.get('/users/{user_id}/posts/', response_model=List[schemas.Post])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_user(db, user_id=user_id)
    if not posts:
        raise HTTPException(status_code=404, 
        detail=f'There is no posts by {user_id}')
    return posts

####auth futures#######
@app.post('/signup')
def signup(user_details: schemas.AuthModel, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user_details.username) != None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        user = {'key': user_details.username, 'password': hashed_password}
        return crud.create_user(db, user=user)
    except:
        error_msg = 'Failed to signup user'
        return error_msg   

@app.post('/login')
def login(user_details: schemas.AuthModel, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=user_details.username)
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user.hashed_password)):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(user.email)
    refresh_token = auth_handler.encode_refresh_token(user.email)
    return {'access_token': access_token, 'refresh_token': refresh_token}

@app.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}
###################################################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)