# app.py


from todoSqlPkg import create_app

app = create_app()
app.run(debug=True)