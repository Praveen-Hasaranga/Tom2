from django.db import models


class Sales_Person(models.Model):
    sales_person_id = models.CharField(max_length=100, primary_key=True, verbose_name='sales person id')
    name = models.CharField(max_length=250)
    contact_no = models.CharField(max_length=15, verbose_name='contact number')
    address = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    date_created = models.DateField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.name}"


class Job(models.Model):
    category_choice = (
        ('mechanical', 'mechanical'),
        ('electrical', 'electrical')
    )

    stage_choice = (
        ('registered', 'registered'),
        ('production queue', 'production queue'),
        ('workshop', 'workshop'),
    )

    job_id = models.CharField(max_length=100, primary_key=True, verbose_name='job id')
    customer_name = models.CharField(max_length=250, verbose_name='customer name')
    description = models.TextField(max_length=1000)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=50, decimal_places=2)
    sales_person = models.ForeignKey(Sales_Person, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=category_choice)
    stage = models.CharField(max_length=100, choices=stage_choice, default='registered')
    date_created = models.DateField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.job_id}"


class Sub_Workshop(models.Model):
    status_choice = (
        ('in progress', 'in progress'),
        ('pending', 'pending'),
    )

    sub_workshop_id = models.CharField(max_length=100, primary_key=True, verbose_name='sub workshop id')
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='job id')
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=50, decimal_places=2)
    status = models.CharField(max_length=100, choices=status_choice, default='pending')
    date_created = models.DateField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.sub_workshop_id}"


class Sub_WIP(models.Model):
    status_choice = (
        ('complete', 'complete'),
        ('in progress', 'in progress'),
        ('pause', 'pause'),
        ('invoice', 'invoice'),
    )

    sub_wip_id = models.CharField(max_length=100, primary_key=True, verbose_name='sub WIP id')
    sub_workshop_id = models.ForeignKey(Sub_Workshop, on_delete=models.CASCADE, verbose_name='sub workshop id')
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=50, decimal_places=2)
    status = models.CharField(max_length=100, choices=status_choice, default='in progress')
    date_created = models.DateField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.sub_wip_id}"


class Invoice(models.Model):
    stage_choice = (
        ('pending invoice', 'pending invoice'),
        ('invoice', 'invoice')
    )

    invoice_id = models.CharField(max_length=100, primary_key=True, verbose_name='invoice id')
    sub_wip_id = models.OneToOneField(Sub_WIP, on_delete=models.CASCADE, verbose_name='sub WIP id', null=True)
    customer_name = models.CharField(max_length=250, verbose_name='customer name')
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=50, decimal_places=2)
    stage = models.CharField(max_length=100, choices=stage_choice, default='pending invoice')
    date_created = models.DateField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.invoice_id}"


class History(models.Model):
    status_choice = (
        ('registered', 'registered'),
        ('moved queue', 'moved queue'),
        ('moved to workshop', 'moved to workshop'),
        ('workshop splitted', 'workshop splitted'),
        ('moved to WIP', 'moved to WIP'),
        ('WIP splitted', 'WIP splitted'),
        ('WIP paused', 'WIP paused'),
        ('WIP resumed', 'WIP resumed'),
        ('WIP completed', 'WIP completed'),
        ('job completed', 'job completed'),
        ('invoiced', 'invoiced')
    )

    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='job id', null=True)
    sub_workshop_id = models.ForeignKey(Sub_Workshop, on_delete=models.CASCADE, verbose_name='sub workshop id',
                                        null=True)
    sub_wip_id = models.ForeignKey(Sub_WIP, on_delete=models.CASCADE, verbose_name='sub WIP id', null=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='sub WIP id', null=True)
    status = models.CharField(max_length=100)
    remark = models.CharField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='date created')

    def __str__(self):
        return f"{self.status}"
