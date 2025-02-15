from django.db import models
import uuid

class StockInfo(models.Model):
    code = models.CharField(max_length=4)
    stock_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.stock_name
    
class Calendar(models.Model):
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

class Record(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    title = models.CharField(max_length=100, verbose_name="タイトル")
    get_date = models.DateField(verbose_name="取得日", blank=True, null=True)
    label = models.PositiveSmallIntegerField(
        choices=(
            (1, 'クロス'),
            (2, '現渡'),
            (4, '株主書類のみ'),
            (5, '優待到着'),
            (9, 'その他'),
        ),
        verbose_name="ラベル"
    )
    code = models.CharField(max_length=4, verbose_name="銘柄コード")
    stock_name = models.CharField(max_length=100, verbose_name="銘柄名")
    get_month = models.PositiveSmallIntegerField(
        choices=[(i, f'{i}月') for i in range(1, 13)],
        verbose_name="優待月"
    )
    quantity = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(100, 1100, 100)],
        default=100,
        verbose_name="株数"
    )
    stock_price = models.IntegerField(verbose_name="株価", blank=True, null=True)
    fee = models.IntegerField(verbose_name="手数料", blank=True, null=True)
    category = models.IntegerField(
        choices=(
            (1, '食事券'),
            (2, '商品券'),
            (3, '金券・クオカ'),
            (4, '商品'),
            (9, 'その他'),
        ),
        verbose_name="優待カテゴリ"
    )
    arrival_date = models.DateField(verbose_name="優待到着日", blank=True, null=True)
    timing = models.PositiveSmallIntegerField(
        choices=(
            (1, '早い'),
            (2, '遅い'),
            (3, '普通'),
            (9, 'その他'),
        ),
        blank=True, null=True,
        verbose_name="取得タイミング"
    )
    rank = models.PositiveSmallIntegerField(
        choices=(
            (1, '★'),
            (2, '★★'),
            (3, '★★★'),
        ),
        blank=True, null=True,
        verbose_name="ランク"
    )
    memo = models.TextField(max_length=2000, verbose_name="メモ", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    def __str__(self):
        return self.title