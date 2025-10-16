# PCB筹划与组织的前后端交互方案

## 1. 方案概述

### 1.1 已完成的UI修改总结

#### 1.1.1 工作计划表优化
- 实现了"第X阶段"的显示和编辑功能
- 支持阶段顺序调整和自动重排
- 实现了阶段内容的完整编辑功能
- 优化了表格布局和视觉效果

#### 1.1.2 宣传与培训模块优化
- 添加了会议图片上传功能
- 优化了培训记录的展示效果
- 增强了用户交互体验

### 1.2 数据库设计目标
基于已完成的UI优化，设计新的数据库结构以支持：
- 清洁生产审核领导小组管理
- 清洁生产工作小组管理
- 工作计划表的十个阶段管理
- 宣传与培训记录管理（含会议图片）

## 2. 数据库设计

### 2.1 核心表结构

#### 2.1.1 领导小组表 (pcb_leadership_team)
```sql
CREATE TABLE pcb_leadership_team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,  -- 关联企业ID
    name VARCHAR(100) NOT NULL,      -- 成员姓名
    position VARCHAR(100),           -- 职位
    department VARCHAR(100),         -- 部门
    role VARCHAR(50) NOT NULL,       -- 角色(组长/副组长/成员)
    responsibilities TEXT,           -- 职责描述
    phone VARCHAR(20),              -- 联系电话
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    INDEX idx_enterprise_role (enterprise_id, role)
);
```

#### 2.1.2 工作小组表 (pcb_work_team)
```sql
CREATE TABLE pcb_work_team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,  -- 关联企业ID
    name VARCHAR(100) NOT NULL,      -- 成员姓名
    position VARCHAR(100),           -- 职位
    department VARCHAR(100),         -- 部门
    role VARCHAR(50) NOT NULL,       -- 角色(组长/副组长/成员)
    responsibilities TEXT,           -- 职责描述
    phone VARCHAR(20),              -- 联系电话
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    INDEX idx_enterprise_role (enterprise_id, role)
);
```

#### 2.1.3 工作计划表 (pcb_work_plans)
```sql
CREATE TABLE pcb_work_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,  -- 关联企业ID
    stage_order INTEGER NOT NULL,    -- 阶段顺序(1-10)
    stage VARCHAR(100) NOT NULL,     -- 阶段名称
    work_content TEXT,              -- 工作内容
    planned_start_date DATETIME,    -- 计划开始时间
    planned_end_date DATETIME,      -- 计划结束时间
    responsible_department VARCHAR(100), -- 责任部门
    actual_start_date DATETIME,     -- 实际开始时间
    actual_end_date DATETIME,       -- 实际结束时间
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_enterprise_stage (enterprise_id, stage_order),
    INDEX idx_enterprise (enterprise_id)
);
```

#### 2.1.4 培训记录表 (pcb_training_records)
```sql
CREATE TABLE pcb_training_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,  -- 关联企业ID
    title VARCHAR(200) NOT NULL,     -- 培训标题
    date DATETIME NOT NULL,         -- 培训日期
    duration INTEGER,               -- 培训时长(分钟)
    participants INTEGER,           -- 参与人数
    content TEXT,                   -- 培训内容
    instructor VARCHAR(100),        -- 培训讲师
    location VARCHAR(200),          -- 培训地点
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    INDEX idx_enterprise_date (enterprise_id, date)
);
```

#### 2.1.5 培训图片表 (pcb_training_images)
```sql
CREATE TABLE pcb_training_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_id INTEGER NOT NULL,    -- 关联培训记录ID
    image_path TEXT NOT NULL,        -- 图片路径
    image_name VARCHAR(200),         -- 图片名称
    image_size INTEGER,              -- 图片大小(字节)
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (training_id) REFERENCES pcb_training_records(id) ON DELETE CASCADE,
    INDEX idx_training (training_id)
);
```

## 3. API设计

### 3.1 领导小组API

#### 3.1.1 获取领导小组成员列表
```http
GET /api/v1/pcb/enterprise/{enterprise_id}/leadership-team

响应:
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 5,
        "items": [
            {
                "id": 1,
                "name": "张三",
                "position": "总经理",
                "department": "总经理办公室",
                "role": "组长",
                "responsibilities": "负责清洁生产审核工作的总体协调和决策",
                "phone": "13800138000"
            }
        ]
    }
}
```

#### 3.1.2 添加领导小组成员
```http
POST /api/v1/pcb/enterprise/{enterprise_id}/leadership-team

请求体:
{
    "name": "张三",
    "position": "总经理",
    "department": "总经理办公室",
    "role": "组长",
    "responsibilities": "负责清洁生产审核工作的总体协调和决策",
    "phone": "13800138000"
}
```

### 3.2 工作小组API

#### 3.2.1 获取工作小组成员列表
```http
GET /api/v1/pcb/enterprise/{enterprise_id}/work-team

响应格式同领导小组
```

#### 3.2.2 添加工作小组成员
```http
POST /api/v1/pcb/enterprise/{enterprise_id}/work-team

请求体格式同领导小组
```

### 3.3 工作计划API

#### 3.3.1 获取工作计划列表
```http
GET /api/v1/pcb/enterprise/{enterprise_id}/work-plans

响应:
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 10,
        "items": [
            {
                "id": 1,
                "stage_order": 1,
                "stage": "审核准备",
                "work_content": "成立清洁生产审核领导小组和工作小组",
                "planned_start_date": "2024-01-15T00:00:00",
                "planned_end_date": "2024-01-31T00:00:00",
                "responsible_department": "总经理办公室",
                "actual_start_date": "2024-01-15T00:00:00",
                "actual_end_date": "2024-01-30T00:00:00"
            }
        ]
    }
}
```

#### 3.3.2 更新工作计划
```http
PUT /api/v1/pcb/enterprise/{enterprise_id}/work-plans

请求体:
{
    "work_plans": [
        {
            "id": 1,
            "stage_order": 1,
            "stage": "审核准备",
            "work_content": "成立清洁生产审核领导小组和工作小组",
            "planned_start_date": "2024-01-15T00:00:00",
            "planned_end_date": "2024-01-31T00:00:00",
            "responsible_department": "总经理办公室",
            "actual_start_date": "2024-01-15T00:00:00",
            "actual_end_date": "2024-01-30T00:00:00"
        }
    ]
}
```

### 3.4 培训记录API

#### 3.4.1 获取培训记录列表
```http
GET /api/v1/pcb/enterprise/{enterprise_id}/training-records

响应:
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 5,
        "items": [
            {
                "id": 1,
                "title": "清洁生产基础培训",
                "date": "2024-01-20T09:00:00",
                "duration": 120,
                "participants": 30,
                "content": "清洁生产基本概念和方法介绍",
                "instructor": "李四",
                "location": "公司会议室",
                "images": [
                    {
                        "id": 1,
                        "url": "/uploads/training/1.jpg",
                        "name": "培训现场照片1"
                    }
                ]
            }
        ]
    }
}
```

#### 3.4.2 添加培训记录
```http
POST /api/v1/pcb/enterprise/{enterprise_id}/training-records
Content-Type: multipart/form-data

表单字段:
- title: 培训标题
- date: 培训日期
- duration: 培训时长
- participants: 参与人数
- content: 培训内容
- instructor: 培训讲师
- location: 培训地点
- images[]: 培训图片文件（可多个）
```

## 4. 前后端交互注意事项

### 4.1 数据验证
1. **前端验证**:
   - 必填字段检查
   - 日期格式验证
   - 图片大小和格式验证（限制5MB以内，仅支持jpg/png）
   - 阶段顺序范围检查（1-10）

2. **后端验证**:
   - 企业ID有效性验证
   - 数据完整性检查
   - 图片安全性检查
   - 并发操作处理

### 4.2 错误处理
1. **前端错误处理**:
   ```javascript
   try {
     await pcbApi.planning.updateWorkPlans(enterpriseId, workPlans)
     message.success('保存成功')
   } catch (error) {
     console.error('保存失败:', error)
     message.error('保存失败')
   }
   ```

2. **后端错误处理**:
   ```python
   try:
       await work_plan_controller.update(enterprise_id, work_plans)
   except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))
   except Exception as e:
       logger.error(f"更新工作计划失败: {e}")
       raise HTTPException(status_code=500, detail="服务器内部错误")
   ```

### 4.3 性能优化
1. **图片处理**:
   - 前端压缩上传
   - 后端异步处理
   - 使用缓存服务

2. **数据加载**:
   - 分页加载
   - 按需加载
   - 数据缓存

## 5. 部署和测试建议

### 5.1 数据库部署
1. 创建数据库表:
   ```bash
   python migrations/create_planning_tables.py
   ```

2. 初始化基础数据:
   ```bash
   python migrations/init_planning_data.py
   ```

### 5.2 API测试
1. 使用Swagger UI测试所有API接口
2. 编写自动化测试脚本
3. 进行并发测试
4. 验证文件上传功能

### 5.3 前端测试
1. 验证所有表单提交功能
2. 测试图片上传功能
3. 验证数据展示正确性
4. 检查错误提示功能

## 6. 安全性考虑

1. **文件上传安全**:
   - 限制文件类型
   - 限制文件大小
   - 文件名安全处理
   - 存储路径安全配置

2. **数据访问控制**:
   - API认证
   - 企业数据隔离
   - 操作日志记录

## 7. 扩展性考虑

1. **数据结构扩展**:
   - 预留扩展字段
   - 使用JSON字段存储额外属性
   - 支持自定义配置

2. **功能扩展**:
   - 支持更多文件类型
   - 支持更多培训类型
   - 预留API版本升级空间

## 总结

本方案提供了PCB筹划与组织模块的完整数据库设计和API接口方案，重点考虑了：

1. **数据完整性**: 设计合理的数据库结构
2. **接口规范**: 提供标准的RESTful API
3. **安全性**: 包含必要的安全措施
4. **可扩展性**: 预留扩展空间
5. **易用性**: 提供友好的接口调用方式

建议按照以下步骤实施：
1. 创建数据库表
2. 实现API接口
3. 进行接口测试
4. 集成前端功能
5. 进行完整性测试
