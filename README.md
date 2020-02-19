##### @version: v1.1
##### @date: 2.16
# --- For Developer ---
## Tasks
| Task | Engineer | Deadline |
| ------ | ------ | ------ |
| 后端API | cyy, zwk, zc | 2.17 |
| 爬虫&nlp集成 | zwk, zc | 2.18 |
| 后端架构及工具类 | cyy | 2.18 |
| 前端开发 | zh | 2.18 |
| 部署，测试 | cyy, zwk, zc | 2.20 |

## Easy Start
以下操作在项目根目录(epiheadquarter\)下，使用终端或命令行输入
1. 安装依赖：`>pip install -r requirements.txt`
2. 修改数据库参数: [config.py](backend/utils/config.py)
3. 运行：`>flask run`
4. 若本地数据库表未建好，可访问`http://127.0.0.1:5000/create`自动建表
5. Swagger接口管理页：`http://127.0.0.1:5000/apidocs`

## Projection Structure
### 1. Backend
- 项目启动入口： [wsgi.py](/main.py)
- 各模块（蓝图）：[blueprints/](backend/api)
- 配置文件: [config.py](backend/utils/config.py)
- 常量库: [const.py](backend/utils/const.py)
- 表单：[forms.py](backend/forms.py)
- 数据类型（数据库orm）: [models.py](backend/models.py)
- 插件: [extensions.py](backend/utils/extensions.py)
- 其他工具：[utils.py](backend/utils/helper.py)
### 2. Frontend
- 客户端 [main.js](myapp/web/src) 

    - 使用

      ```bash
      npm i && npm run serve
      ```

      

- 后台管理 [main.js](myapp/admin/src) 
  
  - 使用 
  
    ```bash
    npm i && npm run serve
    ```
  
    
  
  - 测试用后端代码 [index.js](myapp/server/) 
  
    - 使用
  
      ```bash
      npm i && npm run serve
      ```
  
      
  
- 静态资源 [static](myapp/admin/dist)

- 静态资源 [static](myapp/web/dist)
    - 客户端首页 [dist/index.html](myapp/web/dist)
    - 后台管理首页 [dist/index.html](myapp/admin/dist)

## Development Guide
### 1. Web Operations
#### 1) 落脚点操作:
参考：[blueprints/manager.py](backend/api/manager.py) 尾部
- 渲染当前页面，后面紧跟的是传参: `return render_template('user/marks.html', article=article)`
- 跳转到上一个页面: `return redirect_back()`
- 跳转到其他页面: `return redirect('/account/edit')`
- 跳转到某个函数所在页面: `return redirect(url_for('news.home_article'))`
### 2. Swagger API 
在函数体中写注释来启动该API的swagger调试功能
url：http://127.0.0.1:5000/apidocs/
#### 1) 模板: 

    """
            注册用户API
            ---
            parameters:
              - name: article_id
                in: query
                type: integer
                required: true
                description: 当前文章id
        """
#### 2) 参数说明：
- ##### parameters: 
    - ##### in:
    | 字段 | 说明 | 示例 |
    | ------ | ------ | ----- |
    |path   |   以地址的形式提交数据  | /users/{id}
    |query  |   参数（包括表单）完成自动映射赋值    |  /users?role=admin
    |header |   参数在request headers 里边提交 | X-MyHeader: Value
    |cookie   |   以流的形式提交 仅支持POST | Cookie: debug=0; csrftoken=BUSe35dohU3O1MZvDCU
    
### 3. Database Operations
#### 1) CRUD:
参考：sqlalchemy增删改查操作 https://www.cnblogs.com/shangerzhong/articles/10381793.html

### 4. Form
参考：Flask表单入门 https://www.cnblogs.com/senlinyang/p/8376452.html

# --- For User ---
