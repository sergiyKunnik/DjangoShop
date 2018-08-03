from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name='Категорія', max_length=200)
    slug = models.SlugField(verbose_name='Slug', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class ProductManager(models.Manager):
    def all(self, cart_items, *args, **kwargs):
        list = super(ProductManager, self).get_queryset().filter(available=True)
        products_in_cart = [item.product for item in cart_items]
        for product in list:
            if product in products_in_cart:
                product.in_cart = True
        return list

    def filter_by_category(self, cart_items, category,  *args, **kwargs):
        list = super(ProductManager, self).get_queryset().filter(available=True, category=category)

        products_in_cart = [item.product for item in cart_items]
        for product in list:
            if product in products_in_cart:
                product.in_cart = True
        return list


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис')
    image = models.ImageField(upload_to='products/images', verbose_name='Зображення')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')
    available = models.BooleanField(default=True, verbose_name='В наявності')
    in_cart = False
    objects = ProductManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


class CartItem(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Загальна ціна')

    def __str__(self):
        return 'Cart item => ' + self.product.title

    class Meta:
        verbose_name = 'Елемент корзини'
        verbose_name_plural = 'Елементи корзини'


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True, verbose_name='Елементи корзини')
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Загальна ціна')

    def add_to_cart(self, product_id):
        product = Product.objects.get(id=product_id)
        new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)
        new_item[0].save()

        if new_item[0] not in self.items.all():
            self.items.add(new_item[0])
            self.save()
        return True

    def remove_from_cart(self, item_id):
        cart_item = CartItem.objects.get(id=item_id)
        if cart_item in self.items.all():
            self.items.remove(cart_item)
            cart_item.delete()
        return True

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзини'


ORDER_STATUS_CHOICES = (
    ('Добавлений до обробки', 'Добавлений до обробки'),
    ('Виконується', 'Виконується'),
    ('Сплачено', 'Сплачено'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    items = models.ManyToManyField(CartItem, verbose_name='Товари')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Загальна ціна покупки')
    first_name = models.CharField(max_length=200, verbose_name='Імя')
    last_name = models.CharField(max_length=200, verbose_name='Прізвище')
    phone = models.CharField(max_length=200, verbose_name='Номер')
    address = models.CharField(max_length=200, verbose_name='Адреса')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comments = models.TextField(verbose_name='Коментарі', blank=True)
    status = models.CharField(max_length=200, verbose_name='Статус замовлення', choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return 'Заказ №' + str(self.id)

    class Meta:
        verbose_name = 'Зомовлення'
        verbose_name_plural = 'Зомовлення'
