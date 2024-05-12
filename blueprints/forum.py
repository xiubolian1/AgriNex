from flask import Blueprint, request, render_template, g, redirect, url_for, session, send_from_directory
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel, UserModel
from exts import db
from decorators import login_required

bp = Blueprint("forum", __name__, url_prefix="/forum")

@bp.route('/avatar/<path:image_name>')  # 设置/image/img为可访问路径
def get_avatar_name(image_name):
    return send_from_directory("uploads/avatar/", image_name)

# http://127.0.0.1:5000
@bp.route("/record", methods=['GET'])
def record():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()

    return render_template("forum.html", questions=questions)


@bp.route("/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect(url_for("forum.record"))
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


@bp.route("/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("forum.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("forum.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("forum.html", questions=questions)
