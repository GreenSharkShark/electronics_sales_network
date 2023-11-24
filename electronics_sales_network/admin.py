from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from electronics_sales_network.models import ChainLink
from electronics_sales_network.validators import ChainLinkSerializerValidator


class ChainLinkAdmin(admin.ModelAdmin):
    list_filter = ('contacts__city',)
    actions = ['clear_debt']
    readonly_fields = ['supplier_link']

    def supplier_link(self, obj):
        """
        Добавляет ссылку на поставщика на страницу подробного просмотра объекта
        """
        if obj.supplier:
            return format_html('<a href="{}">{}</a>',
                               reverse('admin:electronics_sales_network_chainlink_change',
                                       args=[obj.supplier.id]), obj.supplier.name)
        return '-'
    supplier_link.short_description = 'Поставщик'
    supplier_link.allow_tags = True

    def clear_debt(self, queryset):
        """
        Добавляет admin-action "Очистить задолженность перед поставщиком"
        """
        queryset.update(debt_to_the_supplier=None)
    clear_debt.short_description = 'Очистить задолженность перед поставщиком'

    def get_list_display(self, request):
        """
        Отвечает за вывод полей модели на страницу со списком объектов
        """
        list_display = ['name', 'is_factory', 'is_retail_network', 'is_individual_entrepreneur']
        return list_display

    def save_form(self, request, form, change):
        """
        Вызов валидатора перед сохранением модели через админ панель
        """
        validator = ChainLinkSerializerValidator({
            'is_factory': form.cleaned_data['is_factory'],
            'is_retail_network': form.cleaned_data['is_retail_network'],
            'is_individual_entrepreneur': form.cleaned_data['is_individual_entrepreneur'],
            'supplier': form.cleaned_data['supplier'],
            'debt_to_the_supplier': form.cleaned_data['debt_to_the_supplier'],
        })

        validator()
        super().save_form(request, form, change)


admin.site.register(ChainLink, ChainLinkAdmin)
