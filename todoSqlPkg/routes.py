from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .models import db, User, Todos
from .forms import TodoForm, UserForm
from .extensions import login_manager
from flask_login import login_user, logout_user, login_required, current_user


main = Blueprint('main', '__name__')

# With "id"
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)


# With "username"
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


@main.route('/', methods=['POST', 'GET'])
def index():
    message = ''
    login_form = UserForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        print(f'\nValid user: {user_object.username}\n')
        return redirect(url_for('main.view_todos'))
    
    return render_template('index.html', form=login_form)


@main.route('/view_todos')
@login_required
def view_todos():
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')

    # Query task counts
    task_counter = Todos.query.count()
    task_done = Todos.query.filter_by(completed=True).count()
    task_todo = Todos.query.filter_by(completed=False).count()
    per_page=2

    # Check if all task counts are zero
    if task_counter == 0:
        message = "沒有任何待辦事項，請「增加」！"
    elif filter_type == 'completed' and task_done == 0:
        message = "沒有完成任何一件待辦事項！"
    elif filter_type == 'incompleted' and task_todo == 0:
        message = "很棒！待辦事項全部完成！"
    else:
        message = ""

    # Filter todos based on filter_type
    if filter_type == 'completed':
        todos_query = Todos.query.filter_by(completed=True)
    elif filter_type == 'incompleted':
        todos_query = Todos.query.filter_by(completed=False)
    else:
        todos_query = Todos.query

    # Paginate the filtered query
    todos = todos_query.order_by(Todos.date_created.desc()).paginate(page=page, per_page=per_page)

    return render_template(
        'view_todos.html',
        todos=todos,
        task_counter=task_counter,
        task_done=task_done,
        task_todo=task_todo,
        message=message,
        filter_type=filter_type
    )




# @main.route('/view_todos')
# @login_required
# def view_todos():
    
#         all_todos = Todos.query.order_by(Todos.date_created.desc()).all()
#         print('\n')
#         print(all_todos)
#         task_counter = Todos.query.count()
#         task_done = Todos.query.filter(Todos.completed == True).count()
#         print('task_done : ' + str(task_done))
#         task_todo = task_counter - task_done
#         print('task_todo : ' + str(task_todo) + '\n')


#         todos = all_todos
#         message = ''
#         # filter_type = request.args.get('filter')  # Default filter
#         # print(filter_type)
#         page = request.args.get('page', 1, type=int)
#         per_page = 2
#         filter_type = request.args.get('filter', 'all')
#         filter_type = request.args.get('filter')
        

#         if filter_type == 'completed':
#             counter = Todos.query.filter(Todos.completed == True).count()
#             print('counter = ' + str(counter))
#             if counter != 0:
#                 # todos = Todos.query.filter(Todos.completed == True).order_by(Todos.date_created.desc()).all()
#                 todos = Todos.query.filter(Todos.completed == True).order_by(Todos.date_created.desc()).paginate(page=page, per_page=per_page)
                
#             else:
#                 # todos = None
#                 todos = []
#                 message = '都尚未完成！'
#         elif filter_type == 'incompleted':
#             counter = Todos.query.filter(Todos.completed == False).count()
#             print('counter = ' + str(counter))
#             if counter != 0:
#                 todos = Todos.query.filter(Todos.completed == False).order_by(Todos.date_created.desc()).paginate(page=page, per_page=per_page)
                
#             else:
#                 todos = []
#                 message = '全部完成！'
#         else:
#             if Todos.query.count() != 0:
#                 todos = Todos.query.order_by(Todos.date_created.desc()).paginate(page=page, per_page=per_page)
                
#             else:
#                 # todos = None
#                 todos = []
#                 message = '沒有任何要做的事項！'
        
#         return render_template('view_todos.html', todos=todos, task_counter=task_counter, task_done=task_done, task_todo=task_todo, message=message)
    

@main.route('/add_todo', methods=['POST', 'GET'])
@login_required
def add_todo():
    if request.method == 'POST':
        form = TodoForm(request.form)
        todo_title = form.title.data
        todo_description = form.description.data
        completed = form.completed.data == "True"
        # date_created = datetime.now(timezone.utc).replace(microsecond=0)
        date_created = datetime.now(ZoneInfo('Asia/Taipei')).replace(microsecond=0)

        new_todo = Todos(
            title= todo_title,
            description=todo_description,
            completed=completed,
            date_created=date_created
        )
        db.session.add(new_todo)
        db.session.commit()
        print(Todos.query.all())
        flash("Todo successfully added", "success")

        # Preserve the filter parameter in the redirect
        filter_type = request.args.get('filter', 'all')

        return redirect('/view_todos')
        
    else:
        form = TodoForm()
    return render_template('add_todo.html', form=form)


@main.route('/delete_todo/<id>')
@login_required
def delete_todo(id):
    
    todo = Todos.query.filter_by(id=id).one()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo successfully deleted", "success")
    # Preserve the filter parameter in the redirect
    filter_type = request.args.get('filter', 'all')

    return redirect(url_for('main.view_todos', filter=filter_type))


@main.route('/update_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def update_todo(id):
    # Retrieve the todo by id
    todo = Todos.query.get(id)

    # Create an instance of the form
    form = TodoForm(request.form)
    if request.method == 'GET':
        
        # Prepopulate the form fields with the current todo data
        form.title.data = todo.title
        form.description.data = todo.description
        form.completed.data = 'True' if todo.completed else 'False'

    if request.method == 'POST':
        # Update the todo fields with the form data
        todo = Todos.query.filter_by(id=id).first()
        print(todo)
        if form.validate_on_submit():
            # form = TodoForm(request.form)
            todo.title = form.title.data
            todo.description = form.description.data
            todo.completed = form.completed.data == 'True' # Convert to boolean
            # todo.date_created = datetime.now(ZoneInfo('Asia/Taipei')).replace(microsecond=0)
            
        #     db.session.commit()
        #     flash("Todo updated successfully!", "success")
        #     return redirect(url_for('main.view_todos'))
        # else:
        #     print(form.errors)

        try:
            db.session.commit()
            flash("Todo updated successfully!", "success")
            # Preserve the filter parameter in the redirect
            filter_type = request.args.get('filter', 'all')
            return redirect(url_for('main.view_todos', filter=filter_type))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating todo: {e}', 'danger')


    # 以下的方式也： OK!
    # form = TodoForm(request.form)
    # if request.method == 'POST':
        
    #     todo = Todos.query.get_or_404(id)
    #     todo.title = form.title.data
    #     todo.description = form.description.data
    #     todo.completed = form.completed.data == "True"
        
    #     db.session.commit()
    #     # print(Todos.query.all())
    #     flash("Todo successfully updated", "success")
    #     return redirect('/view_todos')
    
    # elif request.method == 'GET':
    #     form = TodoForm()
    #     todo = Todos.query.get_or_404(id)
    #     print(todo)
    #     # Prepopulate the form fields with the current todo data
    #     form.title.data = todo.title
    #     form.description.data = todo.description
    #     form.completed.data = form.completed.data == "True"


    return render_template('add_todo.html', form=form)

        

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))




@main.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@main.route('/debug')
def debug():
    return f"Current user: {current_user.username if current_user.is_authenticated else 'None'}"