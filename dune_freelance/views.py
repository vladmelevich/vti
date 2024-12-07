import pandas as pd
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from . import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime
from urllib.parse import urlparse
import string
import random
from django.contrib import messages
from datetime import timedelta


def is_meneger(user):
    return user.groups.filter(name='manager').exists()



def index(request):
    return render(request, 'index.html')

def prof(request):
    return render(request, 'proff.html', )


def reg(request):
    if request.method == 'POST':
        log_in = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password1')
        if password2!= password:
            messages.error(request, 'Пароли не совпадают!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким EMAIL уже существует!')
        elif User.objects.filter(username=log_in).exists():
            messages.error(request, 'Пользователь с таким LOGIN уже существует!')
        else:
            user = User(username = log_in, email=email, password = password)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('spec')
    return render(request, 'registration.html')

def auth(request):
    if request.method == 'POST':
        name = request.POST.get('login')
        pasword = request.POST.get('password')
        remember = request.POST.get('remember_me')
        us = authenticate(request, username=name, password=pasword)
        if us:
            login(request,us)
            if remember:
                request.session.set_expiry(timedelta(days=30))
            else:
                request.session.set_expiry(0)
            return redirect('projects')
        else:
            messages.error(request,"Пароль или Почта не совпадают!")
    return render(request, 'auth.html')

def auth_men(request):
    if request.method == 'POST':
        name = request.POST.get('login')
        password = request.POST.get('passsword')
        uss = authenticate(request, username=name, password=password)
        if uss:
            login(request,uss)
            return redirect('projects_m')
        else:
            messages.error(request,"Пароль или Почта не совпадают!")
    return render(request, 'auth_men.html')

@login_required()
def profile(request):
    us_infor = request.user
    us_information = {'name':us_infor.username, 'email':us_infor.email}
    spec_inf_user = models.spec.objects.get(us_cpec=request.user)
    return render(request, 'profile.html', {'us_information':us_information, 'siu':spec_inf_user})

@login_required()
def blogers(request):
    try:
        if request.method == 'POST':
            nickname = request.POST.get('nickname')
            categr = request.POST.get('categor')
            subs = request.POST.get('subs')
            tem = request.POST.get('tem')
            url_soc = request.POST.get('url_input_project')
            if models.Bloger.objects.filter(url_social_net=url_soc).exists():
                messages.error(request, "Этот блогер закреплен за другим скаутом")
                return redirect('blogers')

            number_photo_bloger = random.randint(1,25)
            blog = models.Bloger(user=request.user, name_first=nickname, social_net=categr, subs=subs,tem=tem, url_social_net=url_soc,number_photo=number_photo_bloger)
            blog.save()
            return redirect('blogers')
    except:
        messages.error(request, 'Не вспе поля заполнены')


    fil1 = request.GET.get('filter_1')
    filters_name = request.GET.get('filters_name')


    try:
        blog_us = models.Bloger.objects.filter(user=request.user)
        if fil1 == "vse0":
            blog_us = models.Bloger.objects.filter(user=request.user)
        elif fil1:
            blog_us = models.Bloger.objects.filter(user=request.user, social_net=fil1)
        elif filters_name:
            blog_us = models.Bloger.objects.filter(user=request.user, name_first=fil1)
    except:
        messages.error(request, 'Возникла Ошибка')

    return render(request, 'bloger.html', {'blog_us':blog_us})

@login_required()
def post(request):
    try:
        if request.method == 'POST':
            input_data_post = request.POST.get('input_data_post')
            ip_id = request.POST.get('id_apl')
            d_p_s = models.date_post_start.objects.create(apl_date_id = ip_id, date_nach=input_data_post)
            if not input_data_post:
                messages.error(request, 'Дата не указана')
            return redirect('post')
    except:
        messages.error(request, 'Не вспе поля заполнены')

    filter = request.GET.get('fill_post')


    try:
        post = models.Posts.objects.filter(projects_post__blog__user=request.user).prefetch_related('date_post_start_set')
        post_list = []
        for d in post:
            d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
            post_url = d.projects_post.pr.url_reklam
            post_u = post_url.replace('tinyurl.com', 'duna.ru')
            post_list.append({
                'applic_post': d,
                'url_post': post_u
            })
        if filter == 'my':
            post = models.Posts.objects.filter(projects_post__blog__user=request.user).prefetch_related(
                'date_post_start_set')
            post_list = []
            for d in post:
                d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
                post_url = d.projects_post.pr.url_reklam
                post_u = post_url.replace('tinyurl.com', 'duna.ru')
                post_list.append({
                    'applic_post': d,
                    'url_post': post_u
                })
        elif filter == 'my_blog':
            con = models.connect.objects.filter(user2=request.user)
            us = User.objects.filter(connections_as_user1__in=con)
            post = models.Posts.objects.filter(projects_post__blog__user__in=us).prefetch_related('date_post_start_set')
            post_list = []
            for d in post:
                d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
                post_url = d.projects_post.pr.url_reklam
                post_u = post_url.replace('tinyurl.com', 'duna.ru')
                post_list.append({
                    'applic_post': d,
                    'url_post': post_u
                })
    except:
        messages.error(request, 'Возникла Ошибка')

    return render(request, 'post.html', {'post': post_list})

@login_required()
def pole(request, post_id):
    try:
        if request.method == 'POST':
            screenshot_add = request.FILES.get('screenshot_add')
            url = request.POST.get('url_input_project')
            date_finish = request.POST.get('date_finish')
            forma = request.POST.get('format')
            name_url = request.POST.get('url_input_project_name')
            if screenshot_add and url and date_finish and forma and name_url:
                posts_p = models.Posts.objects.get(id=post_id)
                posts_p.data_konec = date_finish
                posts_p.format = forma
                posts_p.work_url = url
                posts_p.kol_p += 1
                posts_p.photo = screenshot_add
                posts_p.name_url = name_url
                posts_p.save()
                return redirect('post')
            else:
                messages.error(request, 'Возникла ошибка')
                return render(request, 'pole.html')
    except:
        messages.error(request, 'Возникла ошибка')
    return render(request, 'pole.html')

@login_required()
def result_b(request):
    try:
        sum_res = 0
        result = models.result.objects.filter(pst__projects_post__blog__user = request.user)
        for r in result:
            sum_res+=r.summ_off
    except:
        messages.error(request, 'Произошла ошибка')

    try:
        summ_pay = 0
        pay_my_blogers = models.pay.objects.filter(bloger__user = request.user)
        for pay in pay_my_blogers:
            summ_pay+=pay.summ
    except:
        messages.error(request, 'Произошла ошибка')
    return render(request, 'result_blog.html', {'result':result, 'pmb':summ_pay,'sr':sum_res})



@login_required()
@user_passes_test(is_meneger)
def result(request):
    try:
        if request.method == 'POST':
            excel = request.FILES.get('u_input_project')
            df = pd.read_excel(excel)
            errors = []
            for _, row in df.iterrows():
                try:
                    post_ex = models.Posts.objects.get(name_url=row['Название блогера'])
                    date_value = pd.to_datetime(row['Дата и время заявки / заказа'], format='%d.%m.%Y')
                    models.result.objects.create(
                        pst=post_ex,
                        id_res=row['ID заявки'],
                        id_off=row['ID Оффера'],
                        name_off=row['Название Оффера'],
                        status_off=row['Status'],
                        date_off=date_value,
                        summ_off=row['Сумма вознаграждения']
                    )
                except:
                    errors.append(f'Блогер с именем {row["Название блогера"]} не найден.')

            if errors:
                er = ''
                for e in errors:
                    er+=" "+e
                messages.error(request,er)
            else:
                return redirect('result')
    except:
        messages.error(request, f'Произошла ошибка')


    try:
        resul = models.result.objects.all()
    except:
        messages.error(request, 'Произошла ошибка')

    return render(request, 'result.html', {'result':resul})

@login_required()
@user_passes_test(is_meneger)
def random_m(requst):
    pass_random = ''
    if requst.method == 'POST':
        password_random = string.ascii_letters + string.digits
        for rando in range(1,12):
            char = random.choice(password_random)
            pass_random+=char
    return render(requst, 'random.html', {'pr':pass_random})

def spec(request):
    try:
        if request.method == 'POST':
            tn = request.POST.get('phone_number')
            rol = request.POST.get('profession_position')
            if tn or rol is None:
                messages.error(request, 'Произошла ошибка')
            spe = models.spec(us_cpec=request.user, tel_number=tn, rol = rol)
            spe.save()
            return redirect('conn')
    except:
        messages.error(request, 'Возникла ошибка, не все поля заполнены')

    return render(request, 'spec.html')

def conn(request):
    try:
        group = Group.objects.get(name='manager')
        use = group.user_set.all()
        us_sk = models.spec.objects.filter(rol='Скаут')
        if request.method == 'POST':
            um = request.POST.get('um')
            if um:
                users = models.User.objects.get(id=um)
                connec = models.connect(user1 = request.user, user2 = users)
                connec.save()
                return redirect('projects')
    except:
        messages.error(request, 'Возникла ошибка')
    return render(request, 'connection.html',{'usm':use, 'usk':us_sk})


@login_required()
@user_passes_test(is_meneger)
def posts_m(request):
    try:
        if request.method == 'POST':
            input_data_post = request.POST.get('input_data_post')
            ip_id = request.POST.get('id_apl')
            d_p_s = models.date_post_start.objects.create(apl_date_id=ip_id, date_nach=input_data_post)
            if not input_data_post:
                messages.error(request, 'Дата не указана')
            return redirect('post_m')
    except:
        messages.error(request, 'Не вспе поля заполнены')

    fil_post = request.GET.get('fill_post')


    try:
        aplic_m_post = models.Posts.objects.filter(projects_post__blog__user=request.user).prefetch_related(
            'date_post_start_set')
        aplic_post_list = []
        for d in aplic_m_post:
            d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
            post_url = d.projects_post.pr.url_reklam
            post_u = post_url.replace('tinyurl.com', 'duna.ru')
            aplic_post_list.append({
                'applic_post':d,
                'url_post':post_u
            })

        if fil_post == 'my':
            aplic_m_post = models.Posts.objects.filter(projects_post__blog__user=request.user).prefetch_related(
                'date_post_start_set')
            aplic_post_list = []
            for d in aplic_m_post:
                d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
                post_url = d.projects_post.pr.url_reklam
                post_u = post_url.replace('tinyurl.com', 'duna.ru')
                aplic_post_list.append({
                    'applic_post': d,
                    'url_post': post_u
                })
        elif fil_post == 'my_blog':
            con = models.connect.objects.filter(user2=request.user)
            us = User.objects.filter(connections_as_user1__in=con)
            aplic_m_post = models.Posts.objects.filter(projects_post__blog__user__in=us).prefetch_related(
                'date_post_start_set')
            aplic_post_list = []
            for d in aplic_m_post:
                d.projects_post.pr.social_category = d.projects_post.pr.social_category.split(',')
                post_url = d.projects_post.pr.url_reklam
                post_u = post_url.replace('tinyurl.com', 'duna.ru')
                aplic_post_list.append({
                    'applic_post': d,
                    'url_post': post_u
                })
    except:
        messages.error(request, 'Возникла Ошибка')

    return render(request, 'posts_m.html', {'apm': aplic_post_list})

@login_required()
@user_passes_test(is_meneger)
def pole_m(request, post_id):
    try:
        if request.method == 'POST':
            screenshot_add_m = request.FILES.get('screenshot_add_m')
            url_m = request.POST.get('url_m')
            date_finish_m = request.POST.get('date_finish_m')
            format_m = request.POST.get('format_m')
            url_name_m = request.POST.get('url_name_m')
            if screenshot_add_m and url_m and date_finish_m and format_m and url_name_m:
                posts_p = models.Posts.objects.get(id=post_id)
                posts_p.data_konec = date_finish_m
                posts_p.format = format_m
                posts_p.work_url = url_m
                posts_p.kol_p += 1
                posts_p.photo = screenshot_add_m
                posts_p.name_url = url_name_m
                posts_p.save()
                return redirect('post_m')
            else:
                messages.error(request, 'Возникла ошибка')
                return render(request, 'pole_m.html')
    except:
        messages.error(request, 'Возникла ошибка')
    return render(request, 'pole_m.html')



@login_required()
@user_passes_test(is_meneger)
def blogers_m(request):
    try:
        if request.method == 'POST':
            nickname_m = request.POST.get('nickname_m')
            categr_m = request.POST.get('categor_m')
            subs_m = request.POST.get('subs_m')
            tem_m = request.POST.get('tem')
            url_soc_m = request.POST.get('url_input_project')
            if models.Bloger.objects.filter(url_social_net=url_soc_m).exists():
                messages.error(request, "Этот блогер закреплен за другим скаутом")
                return redirect('blogers')
            number_photo = random.randint(1,25)
            blog_m = models.Bloger(user=request.user,tem=tem_m, name_first=nickname_m, social_net=categr_m, subs=subs_m,  url_social_net=url_soc_m, number_photo=number_photo)
            blog_m.save()
            return redirect('blogers_m')
    except:
        messages.error(request, 'Не вспе поля заполнены')

    f1 = request.GET.get('filter_1')
    flters_name = request.GET.get('filters_name')


    try:
        blog_mus = models.Bloger.objects.filter(user=request.user)
        if f1 == "vse0":
            blog_mus = models.Bloger.objects.filter(user=request.user)
        elif f1:
            blog_mus = models.Bloger.objects.filter(user=request.user, social_net=f1)
        elif flters_name:
            blog_mus = models.Bloger.objects.filter(user=request.user, name_first=flters_name)

    except:
        messages.error(request, 'Возникла ошибка')

    return render(request, 'bloger_m.html', {'blog_mus':blog_mus})

@login_required()
@user_passes_test(is_meneger)
def admin(request):
    project_me = models.Projects_men.objects.filter(us_manager = request.user)
    aplic_project_me = models.Applications.objects.filter(pr__in = project_me, applicat='Принята')
    user_project_me = models.Bloger.objects.filter(blog__in=aplic_project_me)
    list = []
    for upm in user_project_me:
        summa = 0
        result_blogers = models.result.objects.filter(pst__projects_post__blog = upm)
        for r in result_blogers:
            summa+=r.summ_off
        list.append({'upm':upm, 'summ':summa})
    try:
        if request.method == 'POST':
            id_blog_pay = request.POST.get('id_blog_pay')
            pay_blog = request.POST.get('pay_input_project')
            blog_pay = models.Bloger.objects.get(id=id_blog_pay)
            pay_bloger,create = models.pay.objects.get_or_create(bloger=blog_pay)
            pay_bloger.summ+=int(pay_blog)
            pay_bloger.save()
    except:
        messages.error(request, 'Возникла ошибка, вы не выбрали блогера')
    return render(request, 'admin.html', {'list':list})

@login_required()
def applications_b(request):
    apl_b = models.Applications.objects.filter(blog__user = request.user)
    return render(request, 'applications_b.html',{'apl_b':apl_b})



@login_required()
@user_passes_test(is_meneger)
def profile_manager(request):
    us_man = request.user
    us_man_inf = {'name':us_man.username, 'email':us_man.email}
    return render(request, 'profile_meneger.html', {'us_man_inf':us_man_inf})

@login_required()
@user_passes_test(is_meneger)
def applications(request):
    p =models.Projects_men.objects.filter(us_manager=request.user)
    ap =models.Applications.objects.filter(pr__in = p)
    if request.method == 'POST':
        id_ap = request.POST.get('id_a')
        status = request.POST.get('status')
        if status == "Принята":
            possst =models.Posts.objects.create(projects_post_id=id_ap)
        try:
            id_ap =models.Applications.objects.get(id = id_ap)
            if status:
                id_ap.applicat = status
                id_ap.save()
                return redirect('applic')
        except:
            messages.error(request, 'Возникла ошибка')

    return render(request, 'Applications.html',{'aplicat':ap})


@login_required()
def bloger_info(request, bloger_id):
    try:
        bloger_inf = models.Bloger.objects.get(id=bloger_id)
    except:
        messages.error(request, 'Возникла ошибка')

    return render(request, 'bloger_profile.html', {'bloger_info':bloger_inf})


@login_required()
@user_passes_test(is_meneger)
def applications_m(request):
    aplic_m = models.Applications.objects.filter(blog__user = request.user)
    return render(request, 'applic_b.html', {'aplic_m': aplic_m})

@login_required()
def projects(request):
    filter_1 = request.GET.get('filter_1')
    filter_2 = request.GET.get('filter_2')
    filters_name = request.GET.get('filters_name')
    projects_blog = models.Projects_men.objects.all()
    try:

        if filter_1 == "vse0" or filter_2 == "vse":
            projects_blog = models.Projects_men.objects.all()
        elif filter_1:
            projects_blog = models.Projects_men.objects.filter(social_category=filter_1)
        elif filter_2:
            projects_blog = models.Projects_men.objects.filter(pay_category=filter_2)
        elif filters_name:
            projects_blog = models.Projects_men.objects.filter(name=filters_name)

        for d in projects_blog:
            d.social_category = d.social_category.split(',')

    except:
        messages.error(request, 'Возникла ошибка')

    return render(request, 'project.html', {'projects_blog':projects_blog})

@login_required()
@user_passes_test(is_meneger)
def bloger_info_m(request, bloger_id):
    try:
        bloger_inf_m = models.Bloger.objects.get(id=bloger_id)
    except:
        messages.error(request, 'Возникла ошибка')
    return render(request, 'bloger_profile_m.html', {'bloger_info_m':bloger_inf_m})

@login_required()
def projects_information(request,projects_id):

    try:
        projects_informations =models.Projects_men.objects.get(id=projects_id)
        projects_informations.social_category = projects_informations.social_category.split(',')
        default_url = projects_informations.url_reklam
        d_url = default_url.replace('tinyurl.com', 'duna.ru')
    except:
        messages.error(request, 'Возникла ошибка')

    try:
        proj_inf_all =models.Projects_men.objects.all()
        for d in proj_inf_all:
            d.social_category = d.social_category.split(',')
    except:
        messages.error(request, 'Возникла ошибка')

    try:
        bl =models.Bloger.objects.filter(user=request.user)
    except:
        messages.error(request, 'Возникла ошибка')

    if request.method == 'POST':
        try:
            appl = request.POST.get('applic')
            bloger = models.Bloger.objects.get(id=appl)
            applic = models.Applications.objects.create(pr=projects_informations)
            applic.blog.add(bloger)
            applic.save()
            return redirect('projects')
        except:
            messages.error(request, 'Возникла ошибка')


    return render(request, 'project_bl_info.html',{'proj_inf':projects_informations, 'prinfal':proj_inf_all, 'bl':bl,'d_url':d_url})




@login_required()
@user_passes_test(is_meneger)
def projects_info(request,projects_men_id):
    try:
        proj_inf = models.Projects_men.objects.get(id=projects_men_id)
        proj_inf.social_category = proj_inf.social_category.split(',')
        default_url = proj_inf.url_reklam
        d_url = default_url.replace('tinyurl.com', 'duna.ru')
    except:
        messages.error(request, 'Возникла ошибка')

    try:
        proj_all = models.Projects_men.objects.all()
        for d in proj_all:
            d.social_category = d.social_category.split(',')
    except:
        messages.error(request, 'Возникла ошибка')


    try:
        bl_m =models.Bloger.objects.filter(user=request.user)
    except:
        messages.error(request, 'Возникла ошибка')
    if request.method == 'POST':
        try:
            id_bl = request.POST.get('id_bl')
            blogers =models.Bloger.objects.get(id=id_bl)
            applic_m =models.Applications.objects.create(pr=proj_inf)
            applic_m.blog.add(blogers)
            applic_m.save()
            return redirect('projects_m')
        except:
            messages.error(request, 'Возникла ошибка')

    return render(request, 'project_info.html', {'proji':proj_inf, 'projal':proj_all,'bl_m':bl_m, 'd_url':d_url})
@login_required()
@user_passes_test(is_meneger)
def projects_m(request):
    if request.method == 'POST':
        name = request.POST.get('name_project')
        email = request.POST.get('email_men')
        number = request.POST.get('summ')
        url = request.POST.get('url')
        type_social = request.POST.getlist('category')
        t_social = ",".join(type_social)
        type_pay = request.POST.get('pay')
        status = request.POST.get('status')
        start = request.POST.get('start')
        finish = request.POST.get('finish')
        try:
            num_r = random.randint(1,10)
            model = models.Projects_men(us_manager=request.user, name=name, men_email=email, pay=number, date_start=start, date_finish=finish, social_category=t_social, pay_category=type_pay, stat=status, nums=num_r, url_reklam = url)
            model.save()
            return redirect('projects_m')
        except:
            messages.error(request, 'Возникла ошибка Отправки')

    f1 = request.GET.get('filter_1')
    f2 = request.GET.get('filter_2')
    filters_name = request.GET.get('filters_name')
    dan = models.Projects_men.objects.all()

    try:

        if f1 == "vse0" or f2 == "vse":
            dan = models.Projects_men.objects.all()
        elif f1:
            dan = models.Projects_men.objects.filter(social_category=f1)
        elif f2:
            dan = models.Projects_men.objects.filter(pay_category=f2)
        elif filters_name:
            dan = models.Projects_men.objects.filter(name=filters_name)

        for d in dan:
            d.social_category = d.social_category.split(',')

    except:
        messages.error(request, 'Возникла ошибка')
    return render(request, 'project_m.html', {'dan':dan})





