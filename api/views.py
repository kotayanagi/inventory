import csv
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from .models import Stock

# Create your views here.


def str2bool(s):
     return s.lower() in ["true", "t", "yes", "1"]

def admin_page(request):
    if request.method == "POST":
        post = request.POST
        file_post = request.FILES

        if 'register' in post:
            data_type = int(post['type'])

            if data_type == 1:
                Stock.objects.all().delete()
                ### 在庫商品のデータを登録する
                # 保存
                uploaded_data = file_post['csv']

                fout = open("stock.csv", 'wb')
                for chunk in uploaded_data.chunks():
                    fout.write(chunk)
                fout.close()

                # 登録
                with open("stock.csv", 'r') as f:
                    readlines = f.read().split('\n')
                for readline in readlines[1:]:
                    row = readline.split(',')
                    # [id, name, price, on_sale, stock, discount]
                    name = row[1]
                    price = row[2]
                    on_sale = bool(row[3])
                    stock_cnt = int(row[4])
                    discount = int(row[5])
                    print(name)
                    print(price)
                    print(on_sale)
                    print(stock_cnt)
                    print(discount)
                    # Stock.objects.create(
                    #     name=name,
                    #     price=price,
                    #     on_sale=on_sale,
                    #     stock=stock_cnt,
                    #     discount=discount,
                    # )



            elif data_type == 2:
                ### 購買履歴のデータを登録する
                Transaction.objects.all().delete()
                # 保存
                uploaded_data = file_post['csv']

                fout = open("transaction.csv", 'wb')
                for chunk in uploaded_data.chunks():
                    fout.write(chunk)
                fout.close()

                # 登録
                with open("transaction.csv", 'r') as f:
                    readlines = f.read().split('\n')
                for readline in readlines:
                    row = readline.split(',')
                    print(row)
                    # [id, transaction_id, stock, discount, number, person]
                    transaction_id = int(row[1])
                    stock_id = int(row[2])
                    discount = int(row[3])
                    number = int(row[4])
                    person = row[5]
                    print(transaction_id)
                    print(stock)
                    print(discount)
                    print(number)
                    print(person)
                    # Transaction.objects.create(
                    #     transaction_id=transaction_id,
                    #     stock_id=stock_id,
                    #     discount=discount,
                    #     number=number,
                    #     person=person,
                    # )

        return redirect('/')

    stocks = Stock.objects.all()
    print(stocks)

    return render(request, 'index.html', {})

@csrf_exempt
def check(request):
    if request.method == "POST":
        response = {
            'status_code': 200,
            'method': "POST",
        }
        return JsonResponse(response)
    if request.method == "GET":
        response = {
            'status_code': 200,
            'method': "GET",
        }
        return JsonResponse(response)


@csrf_exempt
def get_stock_list(request):
    if request.method == 'GET':
        min_stock = request.GET.get('min_stock')
        max_stock = request.GET.get('max_stock')
        on_sale = request.GET.get('on_sale')
        condition = {}

        if min_stock:
            min_stock = int(min_stock)
            condition['stock__gte'] = min_stock
        if max_stock:
            max_stock = int(max_stock)
            condition['stock__lte'] = max_stock
        if on_sale:
            on_sale = str2bool(on_sale)
            condition['on_sale'] = on_sale

        response = {
            'status_code': 200,
            'method': request.method,
            'data': [],
        }
        stocks = list(Stock.objects.filter(**condition).order_by('id').values())
        response['data'] = stocks
        print(response)
        return JsonResponse(response)
    else:
        raise Http404()


@csrf_exempt
def get_stock_detail(request, pk):
    if request.method == 'GET':
        response = {
            'status_code': 200,
            'method': request.method,
            'data': {},
        }
        if Stock.objects.filter(id=pk).exists():
            stock = dict(Stock.objects.values().get(id=pk))
            response['data'] = stock
        else:
            response['status_code'] = 404
        return JsonResponse(response)
    else:
        raise Http404()


@csrf_exempt
def create_stock(request):
    if request.method == 'POST':
        response = {
            'status_code': 200,
            'method': request.method,
        }
        params = json.loads(request.body)
        request_datas = {
            'id': params['id'],
            'name': params['name'],
            'on_sale': str2bool(params['on_sale']),
            'price': params['price'],
            'stock': params['stock'],
            'discount': params['discount'],
        }
        try:
            Stock.objects.create(
                id=request_datas['id'],
                name=request_datas['name'],
                on_sale=request_datas['on_sale'],
                price=request_datas['price'],
                stock=request_datas['stock'],
                discount=request_datas['discount'],
            )
        except:
            response['status_code'] = 400
        return JsonResponse(response)


@csrf_exempt
def update_stock(request, pk):
    if request.method == 'POST':
        response = {
            'status_code': 200,
            'method': request.method,
        }
        params = json.loads(request.body)
        try:
            condition = params
            Stock.objects.filter(id=pk).update(**condition)
            return JsonResponse(response)
        except:
            response['status_code'] = 400
            return JsonResponse(response)
    return Http404()

@csrf_exempt
def delete_stock(request, pk):
    if request.method == 'POST':
        response = {
            'status_code': 200,
            'method': request.method,
        }
        Stock.objects.filter(id=pk).delete()
        return JsonResponse(response)
    return Http404()

@csrf_exempt
def create_stock_items(request):
    if request.method == 'POST':
        response = {
            'status_code': 200,
            'method': request.method,
        }
        params = json.loads(request.body)
        items = params['items']
        stock_bulk = []
        for item in items:
            pseudo = {
                'id': item['id'],
                'name': item['name'],
                'on_sale': str2bool(item['on_sale']),
                'price': item['price'],
                'stock': item['stock'],
                'discount': item['discount'],
            }
            pseudo_stock = Stock(
                id=pseudo['id'],
                name=pseudo['name'],
                on_sale=pseudo['on_sale'],
                price=pseudo['price'],
                stock=pseudo['stock'],
                discount=pseudo['discount'],
            )
            stock_bulk.append(pseudo_stock)
        Stock.objects.bulk_create(stock_bulk)
        return JsonResponse(response)
    return Http404()
