from django.shortcuts import render, redirect
from .forms import *
from .models import *


def index_view(request):
    context = {}
    return render(request, 'tomapp/index.html', context)


def SalesPerson(request):
    form = JobForm(request.POST or None)
    orders_reg = Job.objects.filter(stage="registered").order_by('-date_created')
    orders_que = Job.objects.filter(stage="production queue").order_by('-date_created')

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            # Adding the Remark to the History table
            job_no = form.cleaned_data.get('job_id')
            job_no = Job.objects.get(job_id=job_no)
            new_history_record = History(job_id=job_no, status=str(job_no) + '-' + 'registered')
            new_history_record.save()

            form = JobForm()

    context = {'form': form, 'orders_reg': orders_reg, 'orders_que': orders_que}
    return render(request, 'tomapp/sales_person_view.html', context)


def MoveToQueue(request, pk):
    order_to_que = Job.objects.get(job_id=pk)

    if request.method == 'POST':
        order_to_que.stage = 'production queue'
        order_to_que.save(update_fields=['stage'])

        # Adding the Remark to the History table
        new_history_record = History(job_id=order_to_que, status=str(order_to_que.job_id) + '-' + 'moved to queue')
        new_history_record.save()

        return redirect('sales_person_view')

    context = {}
    return render(request, 'tomapp/sales_person_view.html', context)


def MoveToReg(request, pk):
    order_to_reg = Job.objects.get(job_id=pk)

    if request.method == 'POST':
        order_to_reg.stage = 'registered'
        order_to_reg.save(update_fields=['stage'])

        # Adding the Remark to the History table
        new_history_record = History(job_id=order_to_reg,
                                     status=str(pk) + '-' + 'moved back to registered orders')
        new_history_record.save()

        return redirect('sales_person_view')

    context = {}
    return render(request, 'tomapp/sales_person_view.html', context)


def ProductionManager(request):
    orders_que = Job.objects.filter(stage="production queue").order_by('job_id')
    orders_ws = Sub_Workshop.objects.filter(status="pending").order_by('sub_workshop_id')
    orders_wip = Sub_WIP.objects.filter(status="in progress").order_by('sub_wip_id')

    context = {'orders_que': orders_que, 'orders_wip': orders_wip, 'orders_ws': orders_ws}
    return render(request, 'tomapp/production_manager_view.html', context)


def SplitWorkShop(request, pk):
    order = Sub_Workshop.objects.get(sub_workshop_id=pk)
    if request.method == 'POST':
        split_value = float(request.POST.get('sub_val'))
        remain_value = order.value - split_value

        if remain_value > 0:
            new_job_no = order.job_id
            no_of_subs = str(Sub_Workshop.objects.filter(job_id=new_job_no).count() + 1)
            sub_no = str(order.job_id) + '-' + no_of_subs

            new_split = Sub_Workshop(sub_workshop_id=sub_no, job_id=order.job_id, quantity=120, value=split_value,
                                     status='pending')
            new_split.save()

            a = str(order.job_id)
            b = str(order.sub_workshop_id)
            if a == b:
                order.value = order.value - split_value
                new_split = Sub_Workshop(sub_workshop_id=str(order.job_id) + '-' + '1', job_id=order.job_id,
                                         quantity=120,
                                         value=order.value, status='pending')
                new_split.save()
                order.delete()

                # Adding the Remark to the History table
                new_history_record = History(sub_workshop_id=new_split,
                                             status=str(pk) + '-' + 'splitted in the workshop')
                new_history_record.save()

            else:
                order.value = order.value - split_value
                order.save(update_fields=['value'])

                # Adding the Remark to the History table
                new_history_record = History(sub_workshop_id=order,
                                             status=str(pk) + '-' + 'splitted in the workshop')
                new_history_record.save()


            return redirect('production_manager_view')


        else:
            return redirect('production_manager_view')

    context = {}
    return render(request, 'tomapp/sub_ws_value.html', context)


def MoveToWorkShop(request, pk):
    order_in_que = Job.objects.get(job_id=pk)

    if request.method == 'POST':
        order_in_que.stage = 'workshop'
        order_in_que.save(update_fields=['stage'])
        order_value = order_in_que.value
        job_no = order_in_que.job_id
        q_value = order_in_que.quantity

        new_ws_record = Sub_Workshop(sub_workshop_id=job_no, job_id=order_in_que, quantity=q_value, value=order_value,
                                     status='pending')
        new_ws_record.save()

        # Adding the Remark to the History table
        new_history_record = History(job_id=order_in_que,
                                     status=str(pk) + '-' + 'moved to workshop')
        new_history_record.save()

        return redirect('production_manager_view')

    context = {}
    return render(request, 'tomapp/production_manager_view.html', context)


def MoveToQueueW(request, pk):
    order_to_que = Sub_Workshop.objects.get(sub_workshop_id=pk)
    sub_id = order_to_que.job_id
    order_in_que = Job.objects.get(job_id=sub_id)

    a = str(order_to_que.job_id)
    b = str(order_to_que.sub_workshop_id)

    if a == b:
        if request.method == 'POST':
            order_in_que.stage = 'production queue'
            order_in_que.save(update_fields=['stage'])

            order_to_que.delete()

            # Adding the Remark to the History table
            new_history_record = History(job_id=order_in_que,
                                         status=str(pk) + '-' + 'moved back to Queue from Workshop')
            new_history_record.save()

            return redirect('production_manager_view')
    else:
        return redirect('production_manager_view')

    context = {}
    return render(request, 'tomapp/production_manager_view.html', context)


def MoveToWIP(request, pk):
    order_in_ws = Sub_Workshop.objects.get(sub_workshop_id=pk)

    if request.method == 'POST':
        order_in_ws.status = 'in progress'
        order_in_ws.save(update_fields=['status'])

        order_value = order_in_ws.value
        q_value = order_in_ws.quantity
        job_no = order_in_ws.sub_workshop_id

        new_wip_record = Sub_WIP(sub_wip_id=job_no, sub_workshop_id=order_in_ws, quantity=q_value, value=order_value,
                                 status='in progress')
        new_wip_record.save()

        # Adding the Remark to the History table
        new_history_record = History(sub_workshop_id=order_in_ws, status=str(pk) + '-' + 'moved to WIP')
        new_history_record.save()

        return redirect('production_manager_view')

    context = {}
    return render(request, 'tomapp/production_manager_view.html', context)


def ProductionEngineer(request):
    orders_wip = Sub_WIP.objects.filter(status__in=['in progress', 'pause']).order_by('sub_wip_id')
    orders_comp = Sub_WIP.objects.filter(status="complete").order_by('sub_wip_id')
    pend_invoice = Invoice.objects.all().order_by('invoice_id')

    context = {'orders_wip': orders_wip, 'orders_comp': orders_comp, 'pend_invoice': pend_invoice}
    return render(request, 'tomapp/production_engineer_view.html', context)


def PauseWIP(request, pk):
    order_to_pause = Sub_WIP.objects.get(sub_wip_id=pk)

    if request.method == 'POST':
        order_to_pause.status = 'pause'
        order_to_pause.save(update_fields=['status'])

        # Adding the Remark to the History table
        new_history_record = History(sub_wip_id=order_to_pause, status=str(pk) + '-' + 'order paused')
        new_history_record.save()

        return redirect('production_engineer_view')

    context = {}
    return render(request, 'tomapp/production_engineer_view.html', context)


def ResumeWIP(request, pk):
    order_to_resume = Sub_WIP.objects.get(sub_wip_id=pk)

    if request.method == 'POST':
        order_to_resume.status = 'in progress'
        order_to_resume.save(update_fields=['status'])

        # Adding the Remark to the History table
        new_history_record = History(sub_wip_id=order_to_resume, status=str(pk) + '-' + 'order resumed')
        new_history_record.save()

        return redirect('production_engineer_view')

    context = {}
    return render(request, 'tomapp/production_engineer_view.html', context)


def SplitWIP(request, pk):
    order = Sub_WIP.objects.get(sub_wip_id=pk)
    if request.method == 'POST':
        split_value = float(request.POST.get('sub_val'))
        remain_value = order.value - split_value

        if remain_value > 0:
            new_job_no = order.sub_workshop_id
            no_of_subs = str(Sub_WIP.objects.filter(sub_workshop_id=new_job_no).count() + 1)
            sub_no = str(order.sub_workshop_id) + '-' + no_of_subs

            new_split = Sub_WIP(sub_wip_id=sub_no, sub_workshop_id=order.sub_workshop_id, quantity=120,
                                value=split_value, status='in progress')
            new_split.save()

            a = str(order.sub_wip_id)
            b = str(order.sub_workshop_id)
            if a == b:
                order.value = order.value - split_value
                new_split = Sub_WIP(sub_wip_id=str(order.sub_workshop_id) + '-' + '1',
                                    sub_workshop_id=order.sub_workshop_id, quantity=120, value=order.value,
                                    status='in progress')
                new_split.save()
                order.delete()

                # Adding the Remark to the History table
                new_history_record = History(sub_wip_id=new_split, status=str(pk) + '-' + 'splitted in WIP')
                new_history_record.save()

            else:
                order.value = order.value - split_value
                order.save(update_fields=['value'])

                # Adding the Remark to the History table
                new_history_record = History(sub_wip_id=order, status=str(pk) + '-' + 'splitted in WIP')
                new_history_record.save()

            return redirect('production_engineer_view')

        else:
            return redirect('production_engineer_view')

    context = {}
    return render(request, 'tomapp/sub_ws_value.html', context)


def MoveToComplete(request, pk):
    order_to_que = Sub_WIP.objects.get(sub_wip_id=pk)

    if request.method == 'POST':
        order_to_que.status = 'complete'
        order_to_que.save(update_fields=['status'])

        # Adding the Remark to the History table
        new_history_record = History(sub_wip_id=order_to_que, status=str(pk) + '-' + 'order Completed')
        new_history_record.save()

        return redirect('production_engineer_view')

    context = {}
    return render(request, 'tomapp/production_engineer_view.html', context)


def MoveToInvoice(request, pk):
    order_in_wip = Sub_WIP.objects.get(sub_wip_id=pk)

    if request.method == 'POST':
        order_in_wip.status = 'invoice'
        order_in_wip.save(update_fields=['status'])

        customer_name = "abc"
        description = "description"
        order_value = order_in_wip.value
        q_value = order_in_wip.quantity
        job_no = order_in_wip.sub_wip_id

        new_invoice_record = Invoice(invoice_id=job_no, sub_wip_id=order_in_wip, quantity=q_value, value=order_value,
                                     stage='pending invoice', customer_name=customer_name, description=description)
        new_invoice_record.save()

        # Adding the Remark to the History table
        new_history_record = History(sub_wip_id=order_in_wip, status=str(pk) + '-' + 'moved to Pending Invoices')
        new_history_record.save()

        return redirect('production_engineer_view')

    context = {}
    return render(request, 'tomapp/production_manager_view.html', context)


def Accountant(request):
    invoice_pend = Invoice.objects.filter(stage="pending invoice").order_by('sub_wip_id')
    invoice_comp = Invoice.objects.filter(stage="invoice").order_by('invoice_id')

    context = {'invoice_pend': invoice_pend, 'invoice_comp': invoice_comp}
    return render(request, 'tomapp/accountant_view.html', context)


def MoveToInvoiceComp(request, pk):
    order_to_comp_invoice = Invoice.objects.get(invoice_id=pk)

    if request.method == 'POST':
        order_to_comp_invoice.stage = 'invoice'
        order_to_comp_invoice.save(update_fields=['stage'])

        # Adding the Remark to the History table
        new_history_record = History(invoice_id=order_to_comp_invoice, status=str(pk) + '-' + 'order is Invoiced')
        new_history_record.save()

        return redirect('accountant_view')

    context = {}
    return render(request, 'tomapp/sales_person_view.html', context)
