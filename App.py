from flask import Flask, render_template, request, redirect , url_for,flash
from flask_mysqldb import MySQL


app = Flask(__name__)
#MySql conncetion 
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='password'
app.config['MYSQL_DB'] = 'billares_la_taberna'
mysql = MySQL(app)

#Settings

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')


#-----------Login-----------
@app.route('/signup')
def sign():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        ide = request.form['identificacion']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute('SELECT identificacion, contraseña FROM persona WHERE identificacion = %s AND contraseña = %s', (ide,contraseña))
        data = cur.fetchall()
        mysql.connection.commit()
        if str (data) != "(("+ide+", '"+contraseña+"'),)":
            return render_template('loginfailed.html')
        else:
            return redirect(url_for('Invent'))

@app.route('/Persona')
def persona():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM persona')
    persona = cur.fetchall()
    return render_template('persona.html', person = persona)

@app.route('/Persona/add', methods=['POST'])
def addPersona():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ide = request.form['identificacion']
        tel = request.form['telefono']
        direc = request.form['direccion']
        contraseña = request.form['contraseña']
        rol = request.form['rol']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO persona (nombre, identificacion, telefono, rol, direccion, contraseña) VALUES (%s, %s, %s, %s, %s, %s)',(nombre, ide, tel, rol, direc, contraseña))
        mysql.connection.commit()
        return redirect(url_for('persona'))

@app.route('/Persona/edit/<id>')
def get_persona(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM persona WHERE id = %s', (id))
    persona = cur.fetchall()
    mysql.connection.commit()
    print(persona)
    return render_template('edit_person.html', person = persona)

@app.route('/Persona/update/<id>', methods = ['POST'])
def update_persona(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        ide = request.form['identificacion']
        tel = request.form['telefono']
        direc = request.form['direccion']
        contraseña = request.form['contraseña']
        rol = request.form['rol']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE persona SET nombre = %s, identificacion = %s, telefono = %s, rol = %s, direccion = %s, contraseña = %s WHERE id = %s',(nombre, ide, tel, rol, direc, contraseña, id))
        mysql.connection.commit()
        return redirect(url_for('persona'))

@app.route('/Persona/delete/<string:id>')
def delete_persona(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM persona WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('persona'))


#-----------Proveedor-----------


@app.route('/Prov')
def Prov():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ciudad ')
    data = cur.fetchall()
    cur.execute('SELECT C.nombre, P.* FROM ciudad C , proveedor P WHERE P.id_ciudad = C.id;')
    datos = cur.fetchall()
    return render_template('Prov.html', contact = data, contactos = datos)

@app.route('/Prov/add', methods=['POST'])
def add_prov():
    if request.method == 'POST':
        name = request.form['name']
        nit = request.form['nit']
        direccion = request.form['direction']
        telefono = request.form['tel']
        ciudad = request.form['city']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proveedor (nombre_proveedor, nit_proveedor, direccion_proveedor, tel_proveedor,id_ciudad) VALUES (%s, %s, %s, %s, %s)',(name, nit, direccion, telefono, ciudad))
        mysql.connection.commit()
        flash('Proveedor agregado satisfactoriamente')
        return redirect(url_for('Prov'))

@app.route('/Prov/edit/<id>')
def get_prov(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT C.nombre, P.* FROM ciudad C , proveedor P WHERE P.id_ciudad = C.id AND P.id = %s', (id))
    data = cur.fetchall()
    cur.execute('SELECT * FROM ciudad')
    datos = cur.fetchall()
    mysql.connection.commit()
    return render_template('edit_Prov.html', contact = data[0], contactos = datos)

@app.route('/Prov/update/<id>', methods = ['POST'])
def update_prov(id):
    if request.method == 'POST':
        name = request.form['name']
        nit = request.form['nit']
        direccion = request.form['direction']
        telefono = request.form['tel']
        ciudad = request.form['city']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE proveedor SET nombre_proveedor = %s, nit_proveedor= %s, direccion_proveedor= %s, tel_proveedor= %s,id_ciudad = %s WHERE id= %s", (name, nit, direccion,telefono, ciudad, id))
        mysql.connection.commit()
        flash('Contacto actualizado satisfacoriamente')
        return redirect(url_for('Prov'))

@app.route('/Prov/delete/<string:id>')
def delete_prov(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proveedor WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('Prov'))


#-----------Inventario-----------


@app.route('/Inventario')
def Invent():
    cur = mysql.connection.cursor()
    cur.execute('SELECT I.id, I.id_producto, I.cantidad_init_product, I.cantidad_disp_product, P.id, P.nombre_producto, P.vr_unit_product, P.id_proveedor, R.nombre_proveedor FROM inventario I, producto P, proveedor R WHERE I.id_producto = P.id AND p.id_proveedor= R.id;')
    inve = cur.fetchall()
    cur.execute('SELECT * FROM proveedor')
    lista = cur.fetchall()
    mysql.connection.commit()
    
    return render_template('Inventario.html', inventory = inve , Prove = lista)

@app.route('/Inventario/add', methods=['POST'])
def add_Inv():
    if request.method == 'POST':
        Name = request.form['name']
        Cost = request.form['cost']
        Amount = request.form['amount']
        Prov = request.form['prov']
        cur = mysql.connection.cursor()
        
        cur.execute('INSERT INTO producto (nombre_producto, vr_unit_product, id_proveedor) VALUES (%s, %s, %s)',(Name, Cost, Prov))
        cur.execute("SELECT id FROM producto WHERE nombre_producto = %s",[Name])
        datos= cur.fetchall()
        dat= datos[0]
        cur.execute('INSERT INTO inventario (id_producto, cantidad_init_product, cantidad_disp_product) VALUES (%s, %s, %s)',(dat, Amount, Amount))
        
        mysql.connection.commit()
        flash('Producto agregado satisfactoriamente')
        return redirect(url_for('Invent'))

@app.route('/Inventario/delete/<string:id>/<string:id2>')
def delete_Inv(id, id2):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventario WHERE id = {0}'.format(id))
    cur.execute('DELETE FROM producto WHERE id = {0}'.format(id2))
    mysql.connection.commit()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('Invent'))

@app.route('/Inventario/edit/<id>/<id2>')
def get_Inv(id, id2):
    cur = mysql.connection.cursor()
    cur.execute('SELECT I.id, I.id_producto, I.cantidad_init_product, I.cantidad_disp_product, P.id, P.nombre_producto, P.vr_unit_product, P.id_proveedor, R.nombre_proveedor FROM inventario I, producto P, proveedor R WHERE I.id = %s AND P.id=%s AND p.id_proveedor = R.id;', (id,id2))
    inve = cur.fetchall()
    print(inve)
    cur.execute('SELECT * FROM proveedor')
    lista = cur.fetchall()
    mysql.connection.commit()
    return render_template('edit_Inventario.html', contactos = inve, list= lista)

@app.route('/Inventario/update/<id>/<id2>', methods = ['POST'])
def update_Inv(id,id2):
    if request.method == 'POST':
        Name = request.form['name']
        Cost = request.form['cost']
        Amount = request.form['amount']
        Prov = request.form['prov']
        cur = mysql.connection.cursor()
        cur = mysql.connection.cursor()
        cur.execute('UPDATE producto SET nombre_producto= %s, vr_unit_product= %s, id_proveedor= %s WHERE id= %s',(Name, Cost, Prov, id2))
        cur.execute('UPDATE inventario SET id_producto = %s, cantidad_init_product = %s, cantidad_disp_product = %s WHERE id= %s',(id2, Amount, Amount,id))
        mysql.connection.commit()
        flash('Producto actualizado satisfacoriamente')
        return redirect(url_for('Invent'))
    
if __name__== '__main__':
    app.run(port = 5000, debug = True)