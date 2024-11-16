from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from datetime import datetime, timezone
from .models import db, User, Todos
from .forms import TodoForm, UserForm
from .extensions import login_manager
from flask_login import login_user, logout_user, login_required, current_user


main = Blueprint('main', '__name__')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@main.route('/', methods=['POST', 'GET'])
def index():
    message = ''
    login_form = UserForm()
    # if request.method == 'POST':
    #     username = form.username.data
    #     password = form.password.data

    #     user = User.query.filter_by(username=username).first_or_404()
    #     if user is not None:
    #         message = f'The user is {user.username}'
    #         return redirect(url_for('main.view_todos'))
    #     else:
    #         message = 'No such a user!'
    #         return redirect(url_for('main.index'))
            
        
    # return render_template('index.html', message=message, form=form)
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        print(f'\nValid user: {user_object.username}\n')
        return redirect(url_for('main.view_todos'))
    # else:
    #     message = 'Invalid password. Please try again.'
    #     return render_template('index.html', form=login_form, message=message)
    
    return render_template('index.html', form=login_form)


@main.route('/view_todos')
@login_required
def view_todos():
    # all_todos = Todos.query.all().sort('date_created', -1)
    # if current_user.is_authenticated:
        all_todos = Todos.query.order_by(Todos.date_created.desc()).all()
        print(all_todos)
        return render_template('view_todos.html', todos=all_todos)
    # return redirect(url_for('main.index'))

@main.route('/add_todo', methods=['POST', 'GET'])
@login_required
def add_todo():
    if request.method == 'POST':
        form = TodoForm(request.form)
        todo_title = form.title.data
        todo_description = form.description.data
        completed = form.completed.data == "True"
        date_created = datetime.now(timezone.utc).replace(microsecond=0)

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
    return redirect('/view_todos')


@main.route('/update_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def update_todo(id):
    # # Retrieve the todo by id
    # todo = Todos.query.get_or_404(id)

    # # Create an instance of the form
    # form = TodoForm()
    # if request.method == 'GET':
        
    #     # Prepopulate the form fields with the current todo data
    #     form.title.data = todo.title
    #     form.description.data = todo.description
    #     form.completed.data = 'True' if todo.completed else 'False'

    # if request.method == 'POST':
    #     # Update the todo fields with the form data
    #     if form.validate_on_submit():
    #         form = TodoForm(request.form)
    #         todo.title = form.title.data
    #         todo.description = form.description.data
    #         todo.completed = form.completed.data == 'True' # Convert to boolean
    #             # todo.date_created = datetime.now(timezone.utc).replace(microsecond=0)  # Update timestamp
            
    #         db.session.commit()
    #         flash("Todo updated successfully!", "success")
    #         return redirect(url_for('main.view_todos'))
    #     else:
    #         print(form.errors)

        # try:
        #     db.session.commit()
        #     flash("Todo updated successfully!", "success")
        #     return redirect(url_for('main.view_todos'))
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f'Error updating todo: {e}', 'danger')

    if request.method == 'POST':
        form = TodoForm(request.form)
        todo = Todos.query.get_or_404(id)
        todo.title = form.title.data
        todo.description = form.description.data
        todo.completed = form.completed.data == "True"
        
        db.session.commit()
        # print(Todos.query.all())
        flash("Todo successfully updated", "success")
        return redirect('/view_todos')
    
    elif request.method == 'GET':
        form = TodoForm()
        todo = Todos.query.get_or_404(id)
        print(todo)
        # Prepopulate the form fields with the current todo data
        form.title.data = todo.title
        form.description.data = todo.description
        form.completed.data = form.completed.data == "True"


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