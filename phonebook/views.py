from django.shortcuts import render, redirect
import phonebook
from phonebook.models import PhoneBook

# Create your views here.
def index(request):
    alluser = PhoneBook.objects.values('id','이름','전화번호');
    context = {
        "alluser" : alluser,
    }
    return render(request, 'phonebook/index.html', context);

def add(request):
    if(request.method == 'GET'):
        if (str(request.user) != 'AnonymousUser'):
            return render(request, 'phonebook/add.html');
        else :
            return redirect('login');
    elif (request.method == 'POST'):
        name = request.POST.get("name");
        telnum = request.POST.get("telnum");
        email = request.POST.get("email");
        addr = request.POST.get("addr");
        birth = request.POST.get("birth");
        author = request.user.username;

        phonebook_table = PhoneBook();
        phonebook_table.이름 = name;
        phonebook_table.전화번호 = telnum;
        phonebook_table.이메일 = email;
        phonebook_table.주소 =  addr;
        phonebook_table.생년월일 = birth;
        phonebook_table.작성자 = author;
        phonebook_table.save();
        return redirect("PB:I");

def delete(request, userId):
    context = {
        "userId" : userId,
    }
    PhoneBook.objects.get(id = userId).delete();
    return render(request, 'phonebook/delete.html', context);

def detail(request, userId):
    userInfo = PhoneBook.objects.values('id','이름','전화번호','주소','이메일','생년월일', '작성자').get(id = userId)
    context = {
        'userInfo':userInfo,
    }
    return render(request, 'phonebook/detail.html', context);

def update(request, userId):
    if(request.method=='POST'):
        name = request.POST.get("name");
        telnum = request.POST.get("telnum");
        email = request.POST.get("email");
        addr = request.POST.get("addr");
        birth = request.POST.get("birth");

        phonebook_table = PhoneBook.objects.get(id=userId);
        phonebook_table.이름 = name;
        phonebook_table.전화번호 = telnum;
        phonebook_table.이메일 = email;
        phonebook_table.주소 =  addr;
        phonebook_table.생년월일 = birth;
        phonebook_table.save();
        return redirect("PB:I");
    else :
        userInfo = PhoneBook.objects.values('id','이름','전화번호','주소','이메일','생년월일', '작성자').get(id = userId)
        context = {
            'userInfo':userInfo,
        }
        if(request.user.username != ''):
            if(str(request.user) == userInfo['작성자']):
                return render(request, 'phonebook/update.html', context);
            else:
                return redirect('PB:I');
        else :
            return redirect('login');