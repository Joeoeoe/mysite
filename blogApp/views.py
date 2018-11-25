from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from blogApp.serializers import UserSerializer, BlogSerializer

# model引入
from django.contrib.auth.models import User
from .models import Blog


# Create your views here.


@api_view(['POST'])
def login_view(request):
    # request.META["CSRF_COOKIE_USED"] = True
    reqUsername = request.data['username']
    reqPassword = request.data['password']
    try:
        querySet = User.objects.get(username=reqUsername)
        print(querySet.username)  # querySet为对象
        serializer = UserSerializer(querySet)
        sqlPassowrd = serializer.data["password"]  # serializer.data为字典
        print(sqlPassowrd)  # !哈希存储密码，无法直接对比密码
        # result = reqPassword == sqlPassowrd
        user = authenticate(request, username=reqUsername, password=reqPassword)
        if user is not None:
            login(request, user)
            return Response({"code": 200, "result": "登录成功"})
        else:
            return Response({"code": 403, "result": "密码错误"})
    except ObjectDoesNotExist:
        return Response({"code": 404, "result": "账号不存在"})


# 前端逻辑：若cookie在后台为not set，调用此函数，重新登录
@api_view(['POST', 'GET'])
def logout_view(request, format=None):
    print(111)
    logout(request)
    # print("退出成功")
    return Response({"code": 200, "msg": "退出登录成功"})


@api_view(['GET', 'POST'])
def is_logined_view(request):
    print("验证连接")
    if request.user.is_authenticated:
        return Response({"code": 200, "msg": "已登录"})
    else:
        return Response({"code": 403, "msg": "未登录"})


@api_view(['POST'])
def is_token_valid(request):
    # token过期情况已被拦截
    # 无token但不知道是否已登录
    if request.user.is_authenticated:
        return Response({"code": 200, "msg": "Token有效,用户已登录"})
    else:
        # 用户未登录，前端统一调用退出登录接口无影响
        # 注意使用status与不使用status的区别
        return Response({"code": 403, "msg": "用户未登录"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def post_blog_view(request):
    if request.user.is_authenticated:
        reqHeader = request.data['header']
        reqContent = request.data['content']
        reqCover = request.data['cover']
        reqMarkdownContent = request.data['markdownContent']
        time = timezone.now()
        date = str(time.year) + '/' + str(time.month) + '/' + str(time.day)
        newBlog = Blog(header=reqHeader, content=reqContent, cover=reqCover, markdownContent=reqMarkdownContent, time=date, readTimes=0)
        newBlog.save()
        print(newBlog.id)
        return Response({"code": 200, "msg": "博客发布成功"})
    else:
        # 未登录与无效token错误
        return Response({"code": 403, "msg": "请登录"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def get_blogByID_view(request):
    # 没登录无token可以上传，登录后带X-CSRFToken也没问题
    reqArticleID = request.data['articleID']
    queryset = Blog.objects.get(id=reqArticleID)
    queryset.readTimes += 1
    queryset.save()
    print(queryset.readTimes)
    serializer = BlogSerializer(queryset)
    articleTitle = serializer.data['header']
    articleContent = serializer.data['content']
    articleCover = serializer.data['cover']
    articleMarkdownContent = serializer.data['markdownContent']
    articleTime = serializer.data['time']
    return Response({"code": 200, "msg": "success",
                     "article": {
                         "articleTitle": articleTitle,
                         "articleContent": articleContent,
                         "articleCover": articleCover,
                         "articleMarkdownContent": articleMarkdownContent,
                         "articleTime": articleTime
                     }
                     })


@api_view(['GET'])
def get_blogList_view(request):
    querysets = Blog.objects.all()
    print(querysets)
    print(querysets.values())
    querysetsList = querysets.values()
    blogList = []
    for item in querysetsList:
        blog = {"imageSrc": item['cover'], "headline": item["header"], "articleID": item["id"], "articleTime": item["time"]}
        blogList.append(blog)
    # print(dir(querysets))
    # serializer = BlogSerializer(querysets.values(), many=True)
    # print(serializer.data)
    # 直接返回values
    blogList = blogList[::-1]
    return Response({"blogList": blogList})

@api_view(['GET'])
def get_blogList_recently_view(request):
    #返回最后6条
    querysets = Blog.objects.all()
    print(querysets)
    print(querysets.values())
    querysetsList = querysets.values()
    blogList = []
    for item in querysetsList:
        blog = {"imageSrc": item['cover'], "headline": item["header"], "articleID": item["id"], "articleTime": item["time"]}
        blogList.append(blog)
    blogList=blogList[-1:-7:-1]
    return Response({"blogList": blogList})

@api_view(['POST'])
def delete_blog_view(request):
    if request.user.is_authenticated:
        reqArticleID = request.data['articleID']
        blog = Blog.objects.get(pk=reqArticleID)
        result = blog.delete()
        print(result)
        return Response({"code": 200, "msg": "删除成功"})
    else:
        # 未登录与无效token错误
        return Response({"code": 403, "msg": "请登录"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def edit_blog_view(request):
    if request.user.is_authenticated:
        reqArticleID = request.data['articleID']
        reqArticleContent = request.data['content']
        reqArticleCover = request.data['cover']
        reqArticleTitle = request.data['header']
        reqMarkdownContent = request.data['markdownContent']
        queryset = Blog.objects.get(id=reqArticleID)
        queryset.header = reqArticleTitle
        queryset.cover = reqArticleCover
        queryset.content = reqArticleContent
        queryset.markdownContent = reqMarkdownContent
        queryset.save()
        return Response({'code': 200, 'msg': "编辑成功"})
    else:
        return Response({'code': 403, 'msg': "请登录"}, status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(['GET', 'POST'])
def test_view(request):
    return Response({'code': 200})
