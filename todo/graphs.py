import functools
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from flask_cors import CORS, cross_origin

from flask import (Blueprint, flash, g, render_template, request, url_for, session)

from todo.db import get_db

bp= Blueprint('graphs',__name__,url_prefix='/graphs')

# @bp.route('/graphics',methods=['GET','POST'])
# def graphics():
#     db,c = get_db()

#     c.execute(
#         # "SELECT id_ventas,id_detalles_ventas FROM detalles_ventas"
#         "SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas GROUP BY v.id_ventas"
#         # """SELECT * from userpython"""
#     )

#     result = c.fetchall()
#     # result = [1,2,3]
#     Names = []
#     Marks = []

#     print(result)

#     # for i in result:
#     #     print(i[0])
#     for i in result:
#         Names.append(i['id_ventas'])
#         Marks.append(i['TOTAL_AMOUNT'])
#         # print(i['id_ventas'])
#         # print()
        
#     print(Names)
#     print(Marks)
#     # return f"<p>{result}</p>"
#     # return render_template('base.html', result = result)
    
#     # Generate the figure **without using pyplot**.

#     fig = Figure()
#     ax = fig.subplots()
#     ax.plot([Marks,Names])
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/>"

    

@bp.route('/prueba',methods=['GET','POST'])
def hola():
    return "<p>Prueba</p>"

@bp.route('/graphics',methods=['POST'])
def graphics():
    db,c = get_db()

    request_data = request.get_json()

    in_date1 = request_data['dateStart']
    in_date2 = request_data['dateEnd']

    print(in_date1)
    print(in_date2)

    newDate = changeDate(in_date1)
    newDate2 = changeDate(in_date2)

    print(newDate)
    print(newDate2)

    c.execute(
        # "SELECT id_ventas,id_detalles_ventas FROM detalles_ventas"
        # "SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas GROUP BY v.id_ventas"
        # """SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha between '2022-04-10 00:00:00' and '2022-04-14 00:00:00' GROUP BY v.id_ventas;"""
        # f"SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha between '{in_date1}' and '{in_date2}' GROUP BY v.id_ventas;"
        f"SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha between '{newDate}' and '{newDate2}' GROUP BY v.id_ventas;"
    )

    result = c.fetchall()
    # result = [1,2,3]
    Names = []
    Marks = []

    print(result)

    # for i in result:
    #     print(i[0])
    for i in result:
        Names.append(i['id_ventas'])
        Marks.append(i['TOTAL_AMOUNT'])
        # print(i['id_ventas'])
        # print()
        
    print(Names)
    print(Marks)
    # return f"<p>{result}</p>"
    # return render_template('base.html', result = result)
    
    # Generate the figure **without using pyplot**.

    x = np.array(Names)
    y = np.array(Marks)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(x,y)
    ax.set_ylabel('Cantidad de usuarios')
    ax.set_xlabel('Lenguajes de programación')
    ax.set_title('Ventas por mes')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return data
    # return newDate
    # return "Hola Mundo"

@bp.route('/graphicsByYear',methods=['POST'])
def graphics2():

    db,c = get_db()

    request_data = request.get_json()

    Months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    Amount = []

    Yeargraph = request_data['Year']
    # id_articulos_provedores = request_data['id_articulos_provedores']

    print(Yeargraph)

    for n in range(1,13):
        if n < 10: 
            dateMonth = f"{Yeargraph}-0{n}"
        else:
            dateMonth = f"{Yeargraph}-{n}"
        c.execute(
            # f"SELECT dv.id_articulos_provedores, sum(dv.cantidad) as cantidad FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas  WHERE v.fecha like '%{dateMonth}%' AND dv.id_articulos_provedores = '{id_articulos_provedores}';"
            # f"SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha like '{dateMonth}' AND ;"
            f"SELECT count(*) AS TOTAL_AMOUNT FROM ventas WHERE fecha like '%{dateMonth}%';"
        )
        result = c.fetchall()
        Amount.append(result[0]['TOTAL_AMOUNT'])
    
    print(Amount)

    x = np.array(Months)
    y = np.array(Amount)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(x,y)
    # ax.set_ylabel('Cantidad de usuarios')
    # ax.set_xlabel('Lenguajes de programación')
    ax.set_title('Ventas anuales')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    # return data
    # return "calculado"
  
@bp.route('/graphicsByYearProd',methods=['POST'])
def graphics3():

    db,c = get_db()
    try:
        request_data = request.get_json()
    except:
        return "Ambos valores deben incluirse"
    else:
        Months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        Amount = []

    
        Yeargraph = request_data['Year']
        id_articulos_provedores = request_data['id_articulos_provedores']
  

        for n in range(1,13):
            if n < 10: 
                dateMonth = f"{Yeargraph}-0{n}"
            else:
                dateMonth = f"{Yeargraph}-{n}"
            c.execute(
                f"SELECT dv.id_articulos_provedores, sum(dv.cantidad) as TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas  WHERE v.fecha like '%{dateMonth}%' AND dv.id_articulos_provedores = {id_articulos_provedores};"
            )
            result = c.fetchall()
            print(result)
            if result[0]['TOTAL_AMOUNT'] == None:
                Amount.append(0)
            else:
                Amount.append(result[0]['TOTAL_AMOUNT'])
        
        print(Amount)

        x = np.array(Months)
        y = np.array(Amount)

        fig = Figure()
        ax = fig.subplots()
        ax.bar(x,y)
        # ax.set_ylabel('Cantidad de usuarios')
        # ax.set_xlabel('Lenguajes de programación')
        ax.set_title('Ventas anuales')

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # return f"<img src='data:image/png;base64,{data}'/>"
        return data
        
        # return "calculado"

def changeDate(date):
    DAY = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    newDAte = date[11:15] + "-"+ DAY.get(date[4:7]) +"-" + date[8:10] + " " + date[16:25]
    return newDAte

