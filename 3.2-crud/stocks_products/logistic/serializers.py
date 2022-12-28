from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'address']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # заполняем связанную таблицу StockProduct с помощью списка positions
        positions_obj_list = [StockProduct(stock=stock, **itm) for itm in positions]
        StockProduct.objects.bulk_create(positions_obj_list)

        return stock

    def update(self, instance, validated_data):
        """Метод обновляет существующие записи в связанной таблице StockProduct и,
        также, создает новые записи в таблице StockProduct, если это нужно"""

        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # Получаем список нужных нам ИМЕЮЩИХСЯ записей (объектов) в связанной таблице StockProduct
        # для обновления соответствующих записей.
        stock_products = list(instance.positions.filter(product_id__in=[elem.get('product') for elem in positions],
                                                        stock=stock))
        # Обновляем ИМЕЮЩИЕСЯ записи в связанной таблице StockProduct
        stock_products_to_update = []
        for itm in stock_products:
            positions_lst = list(filter(lambda pos: pos.get('product') == itm.product, positions))
            if len(positions_lst) > 0:
                position = positions_lst[0]
                positions.remove(position)
                itm.quantity = position.get('quantity', itm.quantity)
                itm.price = position.get('price', itm.price)
                stock_products_to_update.append(itm)

        # обновляем связанную таблицу StockProduct (ИМЕЮЩИЕСЯ записи) с помощью списка positions
        StockProduct.objects.bulk_update(objs=stock_products_to_update, fields=['price', 'quantity'])

        # Проверяем, есть ли в списке positions НОВЫЕ записи, которые нужно создать
        # Если есть, то создаем НОВЫЕ позиции на складе
        if len(positions) > 0:
            positions_obj_list = [StockProduct(stock=stock, **itm) for itm in positions]
            StockProduct.objects.bulk_create(positions_obj_list)

        return stock
