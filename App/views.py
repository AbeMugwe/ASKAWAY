from django.shortcuts import render,redirect
from .models import Q,A,Comments,Upvotes,Downvotes
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import AnswerForm,QuestionForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count 


# Create your views here.

def home(request):
    if 'Search' in request.GET:
        Search=request.GET['Search']
        Questions=Q.objects.annotate(total_comments=Count('answer_set__content_set')).filter(title__icontains=Search).order_by('-id')
    else:
        Questions=Q.objects.annotate(total_comments=Count('answer_set__content_set')).all().order_by('-id')
    
    paginator=Paginator(Questions,10)
    pag_num=request.GET.get('page',1)
    Questions=paginator.page(pag_num)

    return render(request,'home.html',{'questions':Questions})

def detail(request,id):
    Questions=Q.objects.get(pk=id)
    tags=Questions.tags.split(',')
    Answer=A.objects.filter(q=Questions)
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.q=Questions
            answer.user=request.user
            answer.save()
            messages.success(request,'Answer submitted')
            
    return render(request,'detail.html',{'questions': Questions,'tags':tags, 'answers':Answer,'answerform':answerform})


def save_comment(request):
    if request.method== 'POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=A.objects.get(pk=answerid)
        user=request.user
        Comments.objects.create(
            answer=answer,
            content=comment,
            user=user,

        )
        return JsonResponse({'bool':True})

def save_upvote(request):
    if request.method== 'POST':
        answerid=request.POST['answerid']
        answer=A.objects.get(pk=answerid)
        user=request.user
        check=Upvotes.objects.filter(answer=answer, user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Upvotes.objects.create(
                answer=answer,
                user=user,
            )
            return JsonResponse({'bool':True})

def save_downvote(request):
    if request.method== 'POST':
        answerid=request.POST['answerid']
        answer=A.objects.get(pk=answerid)
        user=request.user
        check=Downvotes.objects.filter(answer=answer, user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Downvotes.objects.create(
                answer=answer,
                user=user,
            )
            return JsonResponse({'bool':True})


def register(request):
    form=UserCreationForm
    if request.method =='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,('Registered successfully'))
    return render(request,'registration/signin.html',{'form':form})

def ask_q(request):
    form=QuestionForm
    if request.method =='POST':
        qForm=QuestionForm(request.POST)
        if qForm.is_valid():
            qForm=qForm.save(commit=False)
            qForm.user=request.user
            qForm.save()
            messages.success(request,('Question posted successfully'))
    return render(request,'ask_q.html',{'form':form})


        
def tag(request,tag):
    quests=Q.objects.filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'tag.html',{'questions':quests,'tag':tag})


def profile(request):
    quests=Q.objects.filter(user=request.user).order_by('-id')
    answers=A.objects.filter(user=request.user).order_by('-id')
    comments=Comments.objects.filter(user=request.user).order_by('-id')
    upvotes=Upvotes.objects.filter(user=request.user).order_by('-id')
    downvotes=Downvotes.objects.filter(user=request.user).order_by('-id')
    if request.method=='POST':
        profileForm=ProfileForm(request.POST,instance=request.user)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request,'Profile has been updated.')
    form=ProfileForm(instance=request.user)
    return render(request,'registration/profile.html',{
        'form':form,
        'q':quests,
        'answers':answers,
        'comments':comments,
        'upvotes':upvotes,
        'downvotes':downvotes,
    })

def tags(request):
    quests=Q.objects.all()
    tags=[]
    for q in quests:
        qtags=[tag.strip() for tag in q.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Q.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})





    



