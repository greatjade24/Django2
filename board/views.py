import os
from django.shortcuts import render, redirect, HttpResponse
from board.models import Board
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from main import settings
import urllib
import shutil

# Create your views here.
def index(request, page):
    boardTable = Board.objects.all()

    paging = Paginator(boardTable, 2)
    try:
        context = {
            "boardTable" : paging.page(page),
        }
    except EmptyPage:
        context = {
            'boardEmpty': paging.page(paging.num_pages)
        }
    return render(request, 'board/index.html', context)

def detail(request, boardId):
    boardInfo = Board.objects.get(id = boardId)
    boardInfo.조회수 += 1;
    boardInfo.save()
    try:
        dirList = os.listdir(settings.MEDIA_ROOT + "\\" + str(boardId))
        context = {
            "boardInfo": boardInfo,
            "dirList":dirList,
        }
    except:
        context = {
            "boardInfo": boardInfo
        }
    return render(request, 'board/detail.html', context)

def update(request, boardId):
    boardInfo = Board.objects.get(id = boardId)

    if(request.user.username == ''):
        return redirect('login')
    elif(request.user.username != boardInfo.작성자):        
        message = '''
            <script>
                alert('접근할 수 없는 URL 입니다.');
                document.location.href="/board/page/1";
            </scrip>
        '''
        return HttpResponse(message)
    if(request.method == 'GET'):
        try:
            dirList = os.listdir(settings.MEDIA_ROOT + "\\" + str(boardId))
            context = {
                "boardInfo":boardInfo,
                "dirList":dirList,
            }
        except:
            context = {
                "boardInfo":boardInfo,
            }
        return render(request, 'board/update.html', context)
    else :
        boardInfo.제목 = request.POST.get('title')
        boardInfo.내용 = request.POST.get('context')
        boardInfo.수정일 = datetime.now()
        boardInfo.save()

        return redirect('BD:D', boardId)

def delete(request, boardId):
    Board.objects.get(id=boardId).delete()

    if os.path.isdir(settings.MEDIA_ROOT + "\\" + str(boardId) + "\\"):
        shutil.rmtree(settings.MEDIA_ROOT + "\\" + str(boardId) + "\\")
    message = '<script> alert("' + boardId + '번 글을 삭제 했습니다."); document.location.href="/board/"; </script>';
    return HttpResponse(message)

def add(request):
    if(request.method == 'POST'):
        if(request.user.username == ""):
            return redirect('login')
        
        boardTable = Board();
        boardTable.제목 = request.POST.get('title')
        boardTable.내용 = request.POST.get('context')
        boardTable.작성자 = request.user.username
        boardTable.작성일 = datetime.now()
        boardTable.수정일 = datetime.now()
        boardTable.조회수 = 0
        boardTable.save()

        path = settings.MEDIA_ROOT + "\\" + str(boardTable.id) + "\\"
        os.mkdir(path)
        for x in request.FILES.getlist('files'):
            upLoadFile = open(path + "\\" + str(x), 'wb')
            for chunk in x.chunks():
                upLoadFile.write(chunk)

        return redirect('BD:D', boardTable.id)
    else :
        if(request.user.username == ''):
            return redirect('login')

        return render(request, 'board/add.html')

def upload(request):
    if request.method=='POST':
        for x in request.FILES.getlist('files'):
            upLoadFile = open(settings.MEDIA_ROOT + "\\" + str(x), 'wb')
            for chunk in x.chunks():
                upLoadFile.write(chunk)
    
    return render(request, 'board/upload.html')

def updown(request):
    dirList = os.listdir(settings.MEDIA_ROOT)
    context = {
        "dirList":dirList,
    }
    return render(request,'board/updown.html',context)

def download(request, boardId, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, str(boardId) + "\\" + str(filename))
    file_name = urllib.parse.quote(filename.encode('utf-8'))
    readFile = open(file_path, 'rb')
    response = HttpResponse(readFile.read())
    response['Content-Disposition'] = 'attachment; filename*=UTF8\'\'%s'%file_name
    return (response)

def boardDel(request, boardId, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, str(boardId) + "\\" + str(filename))
    os.remove(file_path)

    return redirect('BD:U', boardId)