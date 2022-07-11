from django.contrib import admin

import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # csv 파일 컬럼 타이틀 줄
    writer.writerow([field.verbose_name for field in fields])

    # 실제 데이터 출력
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


from .models import OrderItem, Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','address','tel','postal_code','paid','created','updated']
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline] # 다른 모델과 연결되어있는 경우 한페이지 표시하고 싶을 때
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)
