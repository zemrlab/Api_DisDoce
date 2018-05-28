from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import xlwt


class ExcelView(APIView):
    def get(self, request):
        book = xlwt.Workbook()
        sheet1 = book.add_sheet("PySheet1")

        cols = ["A", "B", "C", "D", "E"]
        txt = "Row %s, Col %s"
        row = sheet1.row(0)
        row.write(0,"hola mundo")

        book.save("Excel/test.xls")
        return Response("hola mundo")
