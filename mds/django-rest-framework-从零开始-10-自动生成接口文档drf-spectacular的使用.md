django-rest-framework-从零开始-10-自动生成接口文档drf-spectacular的使用

## 1、前言

我们和前端对接，或者其他同事对接，需要一个API文档，这里对于drf项目，推荐使用`drf-spectacular`这个第三方库来进行生成。以后就不用每次修改代码都修改自己写的API文档了，简直就是省事又省力。当然，对于一些自定义的视图，需要补充一些信息，毕竟`drf-spectacular`并不是神，无法对于不属于drf基本规范的生成的CRUD外的接口也能表达出来，但官网已经举例了，可以参考[drf-spectacular](https://drf-spectacular.readthedocs.io/en/stable/readme.html)

## 2、使用步骤

### （1）下载第三方库`drf-spectacular`

```
python -m pip install drf-spectacular
```

### （2）注册到`tutorial/settings.py`的INSTALLED_APPS中

![image-20230320201400917](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230320203510805-1513358590.png)

### （3）设置REST_FRAMEWORK的默认配置

在`tutorial/settings.py`中添加以下代码

```
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Student-Manager API接口文档',
    'DESCRIPTION': 'Student-Manager 项目详情介绍',
    'VERSION': '1.0.0',
    # OTHER SETTINGS
} 
```

图示

![image-20230320201924599](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230320203511343-197759250.png)

### （4）设置路由

在`tutorial/tutorial/urls.py`中添加路由

```python
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger接口文档
path('api-doc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc接口文档
```

图示

![image-20230320202824751](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230320203511772-1938823495.png)

## 3、启动服务验证

启动服务

```
python.exe manage.py runserver 0.0.0.0:9000
```

访问http://127.0.0.1:9000/api/schema/ 则会直接下载文档

访问http://127.0.0.1:9000/api-ui/ 则如下

![image-20230320203113694](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230320203512142-2020555983.png)

访问http://127.0.0.1:9000/api-doc/则如下

![image-20230320203227036](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230320203512500-627903018.png)

github：https://github.com/rainbow-tan/learn-drf