from sqladmin import ModelView, Admin
from model import Question, QuizSession, User, UserScore, LevelAttempt, GeneratedProblem, GeneratedProblem, FMCQuestionSave 
from model import UserLog
from database import engine, get_db
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import session


# Define all admin views
class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.question_text, Question.correct_answer]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.ninja_stars, User.awarded_title, User.is_active]

class FMCAdmin(ModelView, model=UserScore):
    column_list = [UserScore.id, UserScore.score]

class LevelAttemptAdmin(ModelView, model=LevelAttempt):
    column_list = [
        LevelAttempt.id,
        LevelAttempt.user_id,
        LevelAttempt.user_name,
        LevelAttempt.operation,
        LevelAttempt.level,
        LevelAttempt.attempt_number,
        LevelAttempt.score,
        LevelAttempt.total_questions,
        LevelAttempt.is_passed,
        LevelAttempt.timestamp
    ]

class QuizSessionAdmin(ModelView, model=QuizSession):
    column_list = [
        QuizSession.id,
        QuizSession.user_id,
        QuizSession.operation,
        QuizSession.level,
        QuizSession.session_id,
        QuizSession.score,
        QuizSession.timestamp,
        QuizSession.start_time,
        QuizSession.end_time,
    ]


class GeneratedProblemAdmin(ModelView, model=GeneratedProblem):
    column_list = [
        GeneratedProblem.id,
        GeneratedProblem.operation,
        GeneratedProblem.level,
        GeneratedProblem.answer,
    ]
class FMCQuestionSaveAdmin(ModelView, model=FMCQuestionSave):
    column_list = [
        FMCQuestionSave.id,
        FMCQuestionSave.user_id,
        FMCQuestionSave.level,
        FMCQuestionSave.paper_id,
        FMCQuestionSave.questions,
        FMCQuestionSave.is_exam_ready,
        FMCQuestionSave.created_at,
        FMCQuestionSave.updated_at
    ]
class UserLogAdmin(ModelView, model=UserLog):
    column_list = [
        UserLog.id,
        UserLog.user_id,
        UserLog.action,
        UserLog.timestamp
    ]
    
# Function to register admin views
def register_admin_views(app):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(FMCAdmin)
    admin.add_view(LevelAttemptAdmin)
    admin.add_view(QuizSessionAdmin)
    admin.add_view(GeneratedProblemAdmin)  
    admin.add_view(FMCQuestionSaveAdmin)
    admin.add_view(UserLogAdmin)
