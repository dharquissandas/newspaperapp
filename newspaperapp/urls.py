from django.urls import include, path
from .views import viewArticles, viewuserinfo, viewCategory, viewcategories, loginPage, registerPage, logoutPage, viewArticle, addComment, deleteComment, addSubComment, deleteSubComment,editComment,deleteProfilePic, addPic, addFavorite, removeFavorite, addLike, removeLike,showLikes


urlpatterns = [
    path('', viewArticles, name='index'),
    path('category/<int:category_id>/', viewCategory, name='category'),
    path('categories/', viewcategories, name='viewcategories'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('profile/', viewuserinfo, name='viewuserinfo'),
    path('article/<int:id>/', viewArticle, name='viewArticle'),
    path('addcomment/', addComment, name='addComment'),
    path('addsubcomment/', addSubComment, name='addSubComment'),
    path('deletecomment/<int:id>/', deleteComment, name='deleteComment'),
    path('deletesubcomment/<int:id>/', deleteSubComment, name='deleteSubComment'),
    path('editcomment/<int:id>/', editComment, name='editComment'),
    path('deleteimage/', deleteProfilePic, name='deleteProfilePic'),
    path('addprofilepic/', addPic, name='addProfilePic'),
    path('addfavorite/<int:id>/', addFavorite, name='addFavorite'),
    path('removefavorite/<int:id>/', removeFavorite, name='removeFavorite'),
    path('addlike/<int:id>/', addLike, name='addLike'),
    path('removelike/<int:id>/', removeLike, name='removeLike'),
    path('likes/', showLikes, name='showLikes'),
] 
