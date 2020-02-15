##### @version: v1.0
##### @date: 2.15
# For Development
## Tasks
| Task | Engineer | Deadline |
| ------ | ------ | ------ |
| 后端API | cyy, zwk, zc | 2.17 |
| 爬虫&nlp集成 | zwk, zc | 2.18 |
| 后端架构及工具类 | cyy | 2.18 |
| 前端开发 | zh | 2.18 |
| 部署，测试 | cyy, zwk, zc | 2.20 |

## Easy Start
##### 启动项目：
(Terminal) 在项目根路径输入"flask run"
`epiheadquarter >flask run` 
## Projection Structure
### 1. Backend
- 项目启动入口： [wsgi.py](/wsgi.py)
- 样例和测试API（整体启动后）: [blueprints/auth.py](epihq/blueprints/auth.py)(在末尾)
- 配置文件: [config.py](epihq/config.py)
- 常量库: [const.py](epihq/const.py)
- 表单：[forms.py](epihq/forms.py)
- 数据类型（数据库orm）: [models.py](epihq/models.py)
- 插件: [extensions.py](epihq/extensions.py)
### 2. Frontend
- 首页 [templates/index.html](epihq/templates/index.html)
- 错误页面 [templates/errors](epihq/templates/errors)

## Development Guide
### Backend API Develop
#### 1. 落脚点操作:
- 渲染当前页面，后面紧跟的是传参: `return render_template('user/marks.html', article=article)`
- 跳转到上一个页面: `return redirect_back()`
- 跳转到其他页面: `return redirect('/account/edit')`
- 跳转到某个函数所在页面: `return redirect(url_for('news.home_article'))`
### Database
#### 1 CRUD:
参考：https://www.cnblogs.com/shangerzhong/articles/10381793.html


# For User
