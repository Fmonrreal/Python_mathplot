import functools
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

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


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')

@bp.route('/graphics',methods=['POST'])
def graphics():
    db,c = get_db()

    request_data = request.get_json()

    in_date1 = request_data['date_start']
    in_date2 = request_data['date_end']

    print(in_date1)
    print(in_date2)

    c.execute(
        # "SELECT id_ventas,id_detalles_ventas FROM detalles_ventas"
        # "SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas GROUP BY v.id_ventas"
        # """SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha between '2022-04-10 00:00:00' and '2022-04-14 00:00:00' GROUP BY v.id_ventas;"""
        f"SELECT dv.id_ventas, count(dv.id_ventas) AS TOTAL_AMOUNT FROM detalles_ventas as dv INNER JOIN ventas as v ON dv.id_ventas=v.id_ventas WHERE v.fecha between '{in_date1}' and '{in_date2}' GROUP BY v.id_ventas;"
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
    ax.set_title('Ventas por periodo')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"