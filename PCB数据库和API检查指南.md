# PCB数据库和API检查指南

本指南提供多种方法来检查数据库内容和验证API调用。

## 📋 目录

1. [快速开始](#快速开始)
2. [检查数据库内容](#检查数据库内容)
3. [测试API调用](#测试api调用)
4. [使用Swagger UI](#使用swagger-ui)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 第一步：初始化数据

如果是首次运行，需要先初始化数据库：

```bash
# 初始化64项指标和示例方案数据
python migrations/init_pcb_data.py
```

### 第二步：启动应用

```bash
# 启动FastAPI应用
python run.py
```

应用启动后会显示：
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🗄️ 检查数据库内容

### 方法一：使用数据库检查脚本（推荐）

我已经为你创建了一个专用的数据库检查脚本 `check_pcb_database.py`

#### 1. 查看所有表的数据

```bash
python check_pcb_database.py
```

这将显示：
- 企业表的数据统计
- 64项指标的分类统计
- 审核结果数据
- 方案数据
- 各表关联关系
- 等等...

**示例输出**：
```
================================================================================
PCB数据库内容检查
================================================================================

【1. PCB企业表 (pcb_enterprise)】
总记录数: 5
企业列表:
  1. ID: 1, 名称: 深圳某某电路板有限公司, 地区: 深圳市, 状态: pending
  2. ID: 2, 名称: 东莞PCB制造厂, 地区: 东莞市, 状态: in_progress
  ...

【2. PCB指标表 (pcb_indicator)】
总记录数: 64
指标分类统计:
  - 生产工艺与装备要求: 6项
  - 能源消耗: 8项
  - 水资源消耗: 5项
  ...
```

#### 2. 查看特定企业的详细信息

```bash
python check_pcb_database.py enterprise 1
```

这将显示ID为1的企业的：
- 基本信息
- 预审核数据状态
- 审核结果统计
- 已选择的方案
- 审核报告

#### 3. 查看表结构

```bash
python check_pcb_database.py structure
```

### 方法二：使用SQLite可视化工具

#### DB Browser for SQLite（推荐）

1. **下载安装**
   - 官网: https://sqlitebrowser.org/
   - Windows/Mac/Linux都有对应版本

2. **打开数据库**
   - 启动DB Browser
   - 点击"打开数据库"
   - 选择项目目录下的 `db.sqlite3` 文件

3. **查看数据**
   - 在"浏览数据"标签页选择表
   - 可以看到所有PCB相关的8张表：
     - `pcb_enterprise`
     - `pcb_indicator`
     - `pcb_audit_result`
     - `pcb_scheme`
     - `pcb_indicator_scheme_relation`
     - `pcb_enterprise_scheme`
     - `pcb_pre_audit_data`
     - `pcb_audit_report`

4. **执行SQL查询**
   ```sql
   -- 查询所有企业
   SELECT * FROM pcb_enterprise;
   
   -- 查询指标分类统计
   SELECT category, COUNT(*) as count 
   FROM pcb_indicator 
   GROUP BY category;
   
   -- 查询某企业的审核结果
   SELECT * FROM pcb_audit_result 
   WHERE enterprise_id = 1;
   ```

#### VS Code SQLite插件

如果使用VS Code编辑器：

1. 安装插件：`SQLite` 或 `SQLite Viewer`
2. 在项目中右键点击 `db.sqlite3`
3. 选择 "Open Database"
4. 可以直接查看和查询数据

### 方法三：使用Python直接查询

创建一个临时脚本：

```python
import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBEnterprise, PCBIndicator
from app.settings import settings

async def quick_check():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    # 查询企业数量
    enterprise_count = await PCBEnterprise.all().count()
    print(f"企业总数: {enterprise_count}")
    
    # 查询指标数量
    indicator_count = await PCBIndicator.all().count()
    print(f"指标总数: {indicator_count}")
    
    # 查询所有企业
    enterprises = await PCBEnterprise.all()
    for ent in enterprises:
        print(f"企业: {ent.name}, 状态: {ent.audit_status}")
    
    await Tortoise.close_connections()

asyncio.run(quick_check())
```

---

## 🔌 测试API调用

### 方法一：使用API测试脚本（推荐）

我已经为你创建了完整的API测试脚本 `test_pcb_api.py`

```bash
# 运行所有API测试
python test_pcb_api.py
```

这个脚本会自动测试：
1. ✅ API连接测试
2. ✅ 获取指标列表
3. ✅ 获取指标树
4. ✅ 创建企业
5. ✅ 获取企业列表
6. ✅ 获取审核结果
7. ✅ 更新审核结果
8. ✅ 获取审核汇总
9. ✅ 获取方案列表

**测试输出示例**：
```
================================================================================
【测试1】获取指标列表
================================================================================
请求URL: GET http://localhost:8000/api/v1/pcb/indicator
状态码: 200
✅ 请求成功
   指标总数: 64
   前3项指标:
     - 指标1: 基本要求
     - 指标2: 机械加工及辅助设施
     - 指标3: 线路与阻焊图形形成(印刷或感光工艺)
```

### 方法二：使用Swagger UI（最推荐）

这是最直观的方式！

1. **启动应用**
   ```bash
   python run.py
   ```

2. **打开Swagger UI**
   - 在浏览器访问: http://localhost:8000/docs
   - 你会看到所有API接口的文档

3. **测试接口**
   - 展开任意接口（如 `GET /api/v1/pcb/indicator`）
   - 点击 "Try it out"
   - 填写参数（如果需要）
   - 点击 "Execute"
   - 查看响应结果

**Swagger UI截图说明**：
```
接口分组：
├─ base - 基础接口（登录等）
├─ pcb - PCB审核模块
   ├─ 企业管理
   │  ├─ GET  /api/v1/pcb/enterprise - 获取企业列表
   │  ├─ POST /api/v1/pcb/enterprise - 创建企业
   │  ├─ GET  /api/v1/pcb/enterprise/{id} - 获取企业详情
   │  └─ ...
   ├─ 指标管理
   │  ├─ GET /api/v1/pcb/indicator - 获取指标列表
   │  ├─ GET /api/v1/pcb/indicator/tree - 获取指标树
   │  └─ ...
   ├─ 审核结果
   │  ├─ GET /api/v1/pcb/enterprise/{id}/audit - 获取审核结果
   │  ├─ PUT /api/v1/pcb/enterprise/{id}/audit/indicator/{indicator_id} - 更新审核结果
   │  └─ ...
   └─ ...
```

### 方法三：使用curl命令

```bash
# 获取指标列表
curl -X GET "http://localhost:8000/api/v1/pcb/indicator"

# 创建企业
curl -X POST "http://localhost:8000/api/v1/pcb/enterprise" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试企业",
    "region": "深圳市",
    "contact_person": "张三"
  }'

# 获取企业列表
curl -X GET "http://localhost:8000/api/v1/pcb/enterprise?page=1&page_size=10"

# 获取审核结果
curl -X GET "http://localhost:8000/api/v1/pcb/enterprise/1/audit"
```

### 方法四：使用Postman

1. 下载安装 Postman: https://www.postman.com/
2. 导入API文档：
   - 访问 http://localhost:8000/openapi.json
   - 在Postman中导入这个JSON文件
3. 逐个测试接口

---

## 📊 使用Swagger UI详细说明

### 1. 访问API文档

启动应用后访问：
- **Swagger UI**: http://localhost:8000/docs （推荐）
- **ReDoc**: http://localhost:8000/redoc （备选）

### 2. 认证设置（如果需要）

如果API需要认证：

1. 先调用登录接口获取token
   ```
   POST /api/v1/base/login
   ```

2. 点击页面右上角的 "Authorize" 按钮
3. 输入token
4. 点击 "Authorize" 保存

### 3. 测试完整流程

#### 步骤1：初始化数据
```bash
python migrations/init_pcb_data.py
```

#### 步骤2：创建企业
在Swagger UI中：
1. 找到 `POST /api/v1/pcb/enterprise`
2. 点击 "Try it out"
3. 填写企业信息：
   ```json
   {
     "name": "测试PCB企业",
     "region": "深圳市",
     "district": "宝安区",
     "contact_person": "张三",
     "contact_phone": "13800138000"
   }
   ```
4. 点击 "Execute"
5. 记录返回的企业ID（假设是 `1`）

#### 步骤3：获取审核结果
1. 找到 `GET /api/v1/pcb/enterprise/{enterprise_id}/audit`
2. 输入企业ID: `1`
3. 点击 "Execute"
4. 查看64项指标的审核结果

#### 步骤4：更新审核结果
1. 找到 `PUT /api/v1/pcb/enterprise/{enterprise_id}/audit/indicator/{indicator_id}`
2. 输入企业ID: `1`，指标ID: `7`
3. 填写更新数据：
   ```json
   {
     "current_value": 115.5,
     "level": "II级",
     "score": 80,
     "comment": "电耗符合II级标准"
   }
   ```
4. 点击 "Execute"

#### 步骤5：获取审核汇总
1. 找到 `GET /api/v1/pcb/enterprise/{enterprise_id}/audit/summary`
2. 输入企业ID: `1`
3. 点击 "Execute"
4. 查看总分、等级等汇总信息

#### 步骤6：获取推荐方案
1. 找到 `GET /api/v1/pcb/enterprise/{enterprise_id}/audit/schemes/{indicator_id}`
2. 输入企业ID: `1`，指标ID: `30`
3. 点击 "Execute"
4. 查看推荐的清洁生产方案

---

## 🔍 监控API调用

### 方法一：查看应用日志

应用运行时会在控制台输出日志：

```
INFO:     127.0.0.1:50000 - "GET /api/v1/pcb/indicator HTTP/1.1" 200 OK
INFO:     127.0.0.1:50001 - "POST /api/v1/pcb/enterprise HTTP/1.1" 200 OK
INFO:     127.0.0.1:50002 - "GET /api/v1/pcb/enterprise/1/audit HTTP/1.1" 200 OK
```

### 方法二：使用审计日志

系统有内置的审计日志表 `audit_log`，会记录所有API调用：

```python
# 查询最近的API调用
import asyncio
from tortoise import Tortoise
from app.models.admin import AuditLog
from app.settings import settings

async def check_audit_log():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    # 查询最近的PCB相关API调用
    logs = await AuditLog.filter(
        path__startswith="/api/v1/pcb"
    ).order_by("-created_at").limit(10)
    
    for log in logs:
        print(f"{log.method} {log.path} - {log.status} - {log.username}")
    
    await Tortoise.close_connections()

asyncio.run(check_audit_log())
```

---

## ❓ 常见问题

### Q1: 如何知道数据是否成功写入数据库？

**方法1**: 使用数据库检查脚本
```bash
python check_pcb_database.py
```

**方法2**: 在Swagger UI中先POST数据，然后GET查询

**方法3**: 使用DB Browser打开 `db.sqlite3` 查看

### Q2: API返回401未授权错误？

如果接口需要认证：
1. 先调用登录接口获取token
2. 在Swagger UI中点击 "Authorize" 设置token
3. 或在curl中添加 `-H "Authorization: Bearer YOUR_TOKEN"`

### Q3: 如何查看某个企业的所有数据？

使用检查脚本：
```bash
python check_pcb_database.py enterprise 1
```

或在Swagger UI中依次调用：
- `GET /api/v1/pcb/enterprise/1` - 基本信息
- `GET /api/v1/pcb/enterprise/1/pre-audit` - 预审核数据
- `GET /api/v1/pcb/enterprise/1/audit` - 审核结果
- `GET /api/v1/pcb/enterprise/1/scheme` - 选择的方案
- `GET /api/v1/pcb/enterprise/1/report` - 审核报告

### Q4: 如何重置数据库？

```bash
# 删除数据库文件
rm db.sqlite3 db.sqlite3-shm db.sqlite3-wal

# 重新启动应用（会自动创建表）
python run.py

# 重新初始化数据
python migrations/init_pcb_data.py
```

### Q5: 如何批量导入测试数据？

可以编写Python脚本：

```python
import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBEnterprise
from app.settings import settings

async def import_test_data():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    # 批量创建企业
    enterprises = [
        {"name": f"测试企业{i}", "region": "深圳市"} 
        for i in range(1, 11)
    ]
    
    for ent_data in enterprises:
        await PCBEnterprise.create(**ent_data)
    
    print(f"导入 {len(enterprises)} 家企业")
    
    await Tortoise.close_connections()

asyncio.run(import_test_data())
```

---

## 📚 推荐工作流程

### 开发和测试时

1. **启动应用**
   ```bash
   python run.py
   ```

2. **在Swagger UI中测试API**
   - 访问 http://localhost:8000/docs
   - 逐个测试接口功能

3. **检查数据库**
   ```bash
   python check_pcb_database.py
   ```

4. **运行自动化测试**
   ```bash
   python test_pcb_api.py
   ```

### 前端集成时

1. 前端开发人员访问 Swagger UI 查看API文档
2. 根据文档调用对应的API接口
3. 使用浏览器开发者工具查看Network请求
4. 后端使用审计日志监控API调用

---

## 📞 快速参考

### 常用命令

```bash
# 启动应用
python run.py

# 初始化数据
python migrations/init_pcb_data.py

# 检查所有表
python check_pcb_database.py

# 检查特定企业
python check_pcb_database.py enterprise 1

# 运行API测试
python test_pcb_api.py
```

### 常用链接

- API文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc
- OpenAPI规范: http://localhost:8000/openapi.json

### 核心API

```
GET    /api/v1/pcb/enterprise           - 企业列表
POST   /api/v1/pcb/enterprise           - 创建企业
GET    /api/v1/pcb/indicator            - 指标列表
GET    /api/v1/pcb/indicator/tree       - 指标树
GET    /api/v1/pcb/enterprise/{id}/audit - 审核结果
PUT    /api/v1/pcb/enterprise/{id}/audit/indicator/{indicator_id} - 更新审核
GET    /api/v1/pcb/scheme               - 方案列表
```

---

**祝使用顺利！如有问题，请查看Swagger UI的接口文档。** 🎉



