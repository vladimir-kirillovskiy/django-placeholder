from django.shortcuts import render
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import requests

from .models import User, Todo, Album, Photo, Post, Comment

class ApiPageView(TemplateView):
    def get(self, request, **kwargs):
        users = User.objects.all()
        return render(request, 'apifetch/index.html', {'title': 'List of users', 'users': users})

class UserPageView(TemplateView):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        todos = Todo.objects.filter(userId=user_id)

        posts = list(Post.objects.filter(userId=user_id))

        albums = list(Album.objects.filter(userId=user_id))
        for album in albums:
            album.photos = Photo.objects.filter(albumId=album.id)

        return render(request, 'apifetch/users.html', {
            'title': 'User Page',
            'user': user,
            'todos': todos,
            'posts': posts,
            'albums': albums,
        })

# PDF Export
class ExportPage(TemplateView):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']

        user = User.objects.filter(id=user_id)[0]
        todos = Todo.objects.filter(userId=user_id)

        posts = list(Post.objects.filter(userId=user_id))
        # for post in posts:
        #     post.comments = Comment.objects.filter(postId=post.id)
        albums = list(Album.objects.filter(userId=user_id))
        # for album in albums:
        #     album.photos = Photo.objects.filter(albumId=album.id)



        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + user.name + '.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(250, 800, user.name)
        p.drawString(230, 780, user.email)
        p.drawString(50, 760, 'Address:')
        address = user.city + ", " + user.street + ", " + user.suite + ", " + user.zipcode
        p.drawString(50, 740, address)
        p.drawString(50, 720, "Phone: " + user.phone)
        p.drawString(50, 700, "Web site: " + user.website)
        p.drawString(50, 680, "Company: " + user.companyname)
        p.drawString(50, 660, "Catch Phrase: " + user.catchPhrase)

        p.drawString(250, 640, "Posts")
        height = 620
        for post in posts:
            p.drawString(50, height, post.title)
            height = height - 20

        p.drawString(250, height, "Albums")
        for album in albums:
            height = height - 20
            p.drawString(50, height, album.title)

        p.showPage()

        height = 780
        p.drawString(250, height, "Todos")
        for todo in todos:
            height = height - 20
            p.drawString(50, height, todo.title)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

class PostPageView(TemplateView):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']
        post_id = kwargs['post_id']
        post = Post.objects.filter(id=post_id)[0]
        comments = Comment.objects.filter(postId=post_id)

        return render(request, 'apifetch/posts.html', {
            'post': post,
            'comments': comments
        })


# Just a test page
class TestPageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://jsonplaceholder.typicode.com/posts'
        req = requests.get(url)
        r = req.json()

        posts = list(Post.objects.filter(userId=1))
        for post in posts:
            post.comments = Comment.objects.filter(postId=1)

        return render(request, 'test.html', {'foo': posts})

# class to fetch data from API and to save it to the database.
class GetUsersPageView(TemplateView):

    def saveComment(commentData):
        comment = Comment()
        comment.id = commentData['id']
        comment.postId = Post.objects.get(id=commentData['postId'])
        comment.name = commentData['name']
        comment.email = commentData['email']
        comment.body = commentData['body']

        comment.save()

    def savePost(postData):
        post = Post()
        post.id = postData['id']
        post.userId = User.objects.get(id=postData['userId'])
        post.title = postData['title']
        post.body = postData['body']

        post.save()

    def savePhoto(photoData):
        photo = Photo()
        photo.id = photoData['id']
        photo.albumId = Album.objects.get(id=photoData['albumId'])
        photo.title = photoData['title']
        photo.url = photoData['url']
        photo.thumbnailUrl = photoData['thumbnailUrl']

        photo.save()

    def saveAlbum(albumData):
        album = Album()
        album.id = albumData['id']
        album.userId = User.objects.get(id=albumData['userId'])
        album.title = albumData['title']

        album.save()

    def saveTodo(todoData):
        todo = Todo()
        todo.id = todoData['id']
        todo.userId = User.objects.get(id=todoData['userId'])
        todo.title = todoData['title']
        todo.completed = todoData['completed']

        todo.save()


    def saveUser(userData):
        user = User()
        user.id = userData['id']
        user.name = userData['name']
        user.username = userData['username']
        user.email = userData['email']
        user.street = userData['address']['street']
        user.suite = userData['address']['suite']
        user.city = userData['address']['city']
        user.zipcode = userData['address']['zipcode']
        user.lat = userData['address']['geo']['lat']
        user.lng = userData['address']['geo']['lng']
        user.phone = userData['phone']
        user.website = userData['website']
        user.companyname = userData['company']['name']
        user.catchPhrase = userData['company']['catchPhrase']
        user.bs = userData['company']['bs']

        user.save()

    # @desc generic function to fetch a specific data
    # takes 2 parameters
    # @param res string - resourses requested(posts, photos, users, etc...)
    # @param func function - callback function, ussualy to save fetched data
    def getData(res, func):
        url = 'http://jsonplaceholder.typicode.com/' + res
        req = requests.get(url)
        r = req.json()
        for x in r:
            func(x)


    # @desc function to fetch all the data from API
    # I fetch almost all data as there are less that 30 users and less
    # than 30 posts per user and so on
    def get(self, request, **kwargs):
        GetUsersPageView.getData('users', GetUsersPageView.saveUser)
        GetUsersPageView.getData('todos', GetUsersPageView.saveTodo)
        GetUsersPageView.getData('albums', GetUsersPageView.saveAlbum)
        # there are too many pictures so I limit them to 5 pictures per album
        # I use loop here to utilize generic function.
        for x in range(0, Album.objects.latest('id').id + 1):
            # fetch 5 items per given albumId
            GetUsersPageView.getData('photos?albumId=' +str(x)+ '&_start=5&_limit=5', GetUsersPageView.savePhoto)
        GetUsersPageView.getData('posts', GetUsersPageView.savePost)
        GetUsersPageView.getData('comments', GetUsersPageView.saveComment)

        return render(request, 'apitest.html', {'foo': 'data fetched'})
