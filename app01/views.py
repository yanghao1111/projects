from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
def index(request):
    return render(request,'index.html')



from django import forms

class rdTypeForm(forms.ModelForm):
    class Meta:
        model =models.ReaderType
        fields = ["rdType","rdTypeName","CanLendDay"]
class bookForm(forms.ModelForm):
    class Meta:
        model =models.Book
        fields = ["bkID","bkName","bkStatus","bkCode","bkAuthor"]
class readerForm(forms.ModelForm):
    class Meta:
        model =models.Reader
        fields=["rdID","rdName","rdSex","rdType","rdPwd","rdDept","rdPhone","rdEmail",
                "rdStatus","rdDateReg","rdBorrowQty","rdAdminRoles"]
class borrowForm(forms.ModelForm):
    class Meta:
        model =models.Borrow

        fields=["rdID","bkID","BorrowID","ldDateRetAct","ldDateRetPlan","ldDateOut"]
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
        # 如果是POST请求，获取用户提交的数据
        #print(request.POST)

    username = request.POST.get("user")
    password = request.POST.get("pwd")
    print(username,password)
    # 普通用户登录
    pwd1=models.Reader.objects.filter(rdID=username).first().rdPwd
    print(pwd1)
    if username == 'root' and password == "123":
        # return HttpResponse("登录成功")
        # return render(request,'index.html')
        return redirect('/login/index')
    else:
        # return render(request,'reader.html')
        return redirect('/login/reader')


    # return HttpResponse("登录失败")
    return render(request, 'login.html', {"error_msg": "用户名或密码错误"})
def student_manage(request):
    if request.method == "GET":
        return render(request, "student_manage.html")
    form = readerForm()
    type=request.POST.get("rdType")
    name=request.POST.get("rdName")
    dept=request.POST.get("rdDept")
    print(type,name,dept)
    queryset=models.Reader.objects.all()
    for i in queryset:
        if(i.rdType==type and i.rdName==name and i.rdDept==dept):
            return HttpResponse("该用户已经办理了借阅证")
        else:
            return HttpResponse("该用户没创建")

def reader_add(request):
    if request.method=="GET":
        form = readerForm()
        return render(request,'reader_add.html',{'form':form})
    form = readerForm(data=request.POST)
    data =request.POST.dict()

    day=models.ReaderType.objects.filter(rdType=data['rdType']).first().CanLendDay

    #如果数据合法就保存到数据库
    if form.is_valid():
        form.save()   #保存到数据库
        # models.Reader.objects.filter(rdID=data['rdID']).update(rdBorrowQty=day)
        return redirect('/index/student_manage')
    return render(request, 'reader_add.html', {'form': form})

def reader(request):
    return render(request,'reader.html')

def reader_list(request):
    queryset = models.Reader.objects.all()

    return render(request,'reader_list.html',{'queryset':queryset})


def reader_edit(request,nid):
    """ 编辑用户 """
    row_object = models.Reader.objects.filter(rdID=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = readerForm(instance=row_object)
        return render(request, 'reader_edit.html', {'form': form})

    form = readerForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/index/reader_list')
    return render(request, 'reader_edit.html', {"form": form})

def reader_delete(request,nid):
        models.Reader.objects.filter(rdID=nid).delete()
        return redirect('/index/reader_list')


def book_delete(request, nid):
    models.Book.objects.filter(bkID=nid).delete()
    return redirect('/index/book_list')

def book_add(request):
    if request.method=="GET":
        form = bookForm()
        return render(request,'book_add.html',{'form':form})
    form = bookForm(data=request.POST)
    #如果数据合法就保存到数据库
    if form.is_valid():
        form.save()   #保存到数据库
        return redirect('/index/book_manage')
    return render(request, 'book_add.html', {'form': form})
def  book_manage(request):
    queryset = models.Book.objects.all()
    return render(request,'book_manage.html',{'queryset':queryset})
def borrow_delete(request,nid):
    models.Borrow.objects.filter(BorrowID=nid).delete()
    return redirect('/index/borrow_info')
def book_edit(request,nid):
    """ 编辑图书 """
    row_object = models.Book.objects.filter(bkID=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = bookForm(instance=row_object)
        return render(request, 'book_edit.html', {'form': form})

    form = bookForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()

        return redirect('/index/book_list')
    return render(request, 'reader_edit.html', {"form": form})

def  borrow_manage(request):
    queryset = models.Borrow.objects.all()
    return render(request,'borrow_manage.html',{'queryset':queryset})


def reader_info(request,nid='211115'):
    queryset = models.Reader.objects.filter(rdID=nid).first()
    return  render(request,'reader_info.html',{'queryset':queryset})

import datetime
from django.db.models import Sum,Count,Max,Min
def borrow1(request,nid):
    queryset = models.Book.objects.all()
    now=datetime.datetime.today()

    day=models.ReaderType.objects.filter(rdType=1).first().CanLendDay
    plan = now + datetime.timedelta(days=day)
    n=models.Borrow.objects.aggregate(Max('BorrowID'))
    m=n['BorrowID__max']+1
    bor=models.Borrow(rdID_id=211115,BorrowID=m,bkID_id=nid,IdContinueTimes=day,ldDateOut=now,ldDateRetPlan=plan,ldDateRetAct=plan)
    bor.save()
    return render(request,'borrow.html',{'queryset':queryset})
def borrow(request):
    queryset = models.Book.objects.all()
    return render(request,'borrow.html',{'queryset':queryset})
def borrow_info(requeset):
    queryset=models.Borrow.objects.filter(rdID=211115)
    return render(requeset,'borrow_info.html',{'queryset':queryset})