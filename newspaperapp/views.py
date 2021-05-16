from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, QueryDict, JsonResponse
from newspaperapp.models import newsCategory, userInfo, newsCategory, newsArticle, Comment, subComment
from .forms import CreateUserForm, CommentForm, UserForm, ImageForm, FavoritesForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

@login_required(login_url='login')
def viewArticles(request):
    return render(request, 'newspaperapp/index.html', {
    'categories': newsCategory.objects.all(),
    })

@login_required(login_url='login')
def viewcategories(request):
    return render(request, 'newspaperapp/categories.html', {
    'categories': newsCategory.objects.all(),
    })

@login_required(login_url='login')
def viewuserinfo(request):
    form = ImageForm(instance=request.user)
    categories = newsCategory.objects.all()
    return render(request, 'newspaperapp/profile.html', {'imageForm': form, 'categories': categories})

def addPic(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=request.user.userinfo)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile has been updated!')
            return redirect('viewuserinfo')
    return redirect('viewuserinfo')

def addFavorite(request, id):
    favorite = get_object_or_404(newsCategory, pk=id)
    request.user.userinfo.favourites.add(favorite)
    messages.success(request,'Favorites have been updated!')
    return HttpResponse("Favorite was added successfully")

def removeFavorite(request, id):
    favorite = get_object_or_404(newsCategory, pk=id)
    request.user.userinfo.favourites.remove(favorite)
    messages.success(request,'Favorites have been updated!')
    return HttpResponse("Favorite was removed successfully")

def deleteProfilePic(request):
    if request.method == 'POST':
        request.user.userinfo.pic.delete()
        return redirect('viewuserinfo')
    
@login_required(login_url='login')
def viewCategory(request, category_id):
    try:
        category = newsCategory.objects.get(id=category_id)
        return render(request, 'newspaperapp/category.html', {
            'category':category,
        })
        return HttpResponse("Found")
    except newsCategory.DoesNotExist:
        return HttpResponseBadRequest("Invalid")

def registerPage(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        profileForm = CreateUserForm(request.POST)
        if form.is_valid() and profileForm.is_valid():
            user = form.save()
            profile = profileForm.save(commit = False)
            profile.user = user
            profile.save()

            mail_subject = 'Thank you for joining NewsPaper.'
            message = render_to_string('newspaperapp/email.html', {
                'user': user,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()


            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    
    form = UserForm()
    profileForm = CreateUserForm()
    context = {'form':form, 'profileForm': profileForm}
    return render(request, 'newspaperapp/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'newspaperapp/login.html', {})

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='login')
def viewArticle(request, id):
    try:
        form = CommentForm
        fform = FavoritesForm
        article = newsArticle.objects.get(id=id)
        return render(request, 'newspaperapp/article.html', {
            'article':article,
            'form': form,
            'favform': fform
        })
    except newsArticle.DoesNotExist:
        return HttpResponseBadRequest("Invalid")

def addComment(request):
    if request.method == 'POST':
        fields = QueryDict(request.body, encoding='utf-8')
        comment = Comment(body=fields.get("body"), article=newsArticle.objects.get(id=fields.get("article")), commenter=request.user)
        comment.save()
        data = {
        'id': comment.id,
        'body': comment.body,
        'commenter': comment.commenter.username
        }
        return JsonResponse({'comment': data}, status = 200)
        
    else:
        return HttpResponse("post error")

def deleteComment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponse("deleted comment")

def addSubComment(request):
    if request.method == 'POST':
        fields = QueryDict(request.body, encoding='utf-8')
        subcomment = subComment(body=fields.get("subcomment"), comment=Comment.objects.get(id=fields.get("comment")), subcommenter=request.user)
        subcomment.save()
        data = {
        'id': subcomment.id,
        'body': subcomment.body,
        'subcommenter': subcomment.subcommenter.username
        }
        return JsonResponse({'comment': data}, status = 200)
        
    else:
        return HttpResponse("post error")

def deleteSubComment(request, id):
    subcomment = subComment.objects.get(id=id)
    subcomment.delete()
    return HttpResponse("deleted subcomment")

def editComment(request, id):
    if request.method == 'POST':
        fields = QueryDict(request.body, encoding='utf-8')
        comment = Comment.objects.get(id=id)
        comment.body = fields.get("editcomment")
        comment.save()
        data = {
        'id': comment.id,
        'body': comment.body,
        }
        return JsonResponse({'comment': data}, status = 200)
        
    else:
        return HttpResponse("post error")
    
def addLike(request, id):
    article = get_object_or_404(newsArticle, pk=id)
    article.likes.add(request.user)
    messages.success(request,'Added to liked articles!')
    return HttpResponse("You have liked this article!")

def removeLike(request, id):
    article = get_object_or_404(newsArticle, pk=id)
    article.likes.remove(request.user)
    messages.success(request,'Removed from liked articles!')
    return HttpResponse("You have disliked this article!")

def showLikes(request):
    articles = []
    for article in newsArticle.objects.all():
        if request.user in article.likes.all():
            articles.append(article)
    return render(request, 'newspaperapp/likes.html', {
    'articles': articles,
    })
