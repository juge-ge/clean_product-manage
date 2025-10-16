# PCB前后端交互问题及解决方案

## 问题概述

在PCB审核模块从Mock数据切换到真实数据库的过程中，遇到了多个前后端交互问题，导致用户无法通过前端界面正常创建企业信息。本文档详细记录了问题的发现、分析和解决过程。

## 问题时间线

- **初始状态**: PCB模块使用Mock数据，前端功能正常
- **切换目标**: 将PCB模块从Mock数据切换到真实数据库API
- **遇到问题**: 前端表单数据无法正确提交到后端，出现多种错误
- **解决过程**: 逐步排查并修复前端数据获取、字段映射、后端权限、API调用等问题
- **最终结果**: 成功实现前后端交互，用户可以正常创建企业信息

## 问题详细分析

### 1. 前端表单数据获取问题

**问题描述**: 
- 用户填写表单后点击保存，控制台显示 `raw from child = {}` (空对象)
- 前端无法正确获取子组件中的表单数据

**根本原因**: 
- 在 `web/src/views/cloud-audit/pcb/index.vue` 的 `handleSave` 函数中，访问子组件数据的方式错误
- 使用了 `formRef.value?.formData?.value` 而不是 `formRef.value?.formData`

**解决方案**:
```javascript
// 修改前 (错误)
const raw = { ...(formRef.value?.formData?.value || {}) };

// 修改后 (正确)
const raw = { ...(formRef.value?.formData || {}) };
```

### 2. 字段映射问题

**问题描述**: 
- 前端表单字段名与后端API期望的字段名不匹配
- 前端使用 `city`, `county` 等字段名，后端期望 `region`, `district`

**解决方案**:
在 `handleSave` 函数中添加字段映射逻辑：
```javascript
const payload = {
  name: trim(raw.name),                         // 企业名称
  region: trim(raw.city),                       // 地市 ← UI: city
  district: trim(raw.county),                   // 区县 ← UI: county
  address: trim(raw.address),                   // 注册地址
  legal_representative: trim(raw.legalRepresentative), // 法人代表
  contact_person: trim(raw.contact),            // 联系人
  contact_phone: raw.phone ? String(raw.phone).trim() : undefined // 联系电话
};
```

### 3. 组件语法错误

**问题描述**: 
- `web/src/components/table/CrudModal.vue` 缺少 `computed` 导入
- 导致组件无法正常工作

**解决方案**:
```javascript
// 添加导入
import { computed } from 'vue'
```

### 4. 后端API权限问题

**问题描述**: 
- 后端返回500错误，提示权限不足
- 数据库中没有PCB相关的API权限记录

**根本原因**: 
- PCB API路由被注册，但数据库中没有对应的权限记录
- 用户角色没有访问PCB API的权限

**解决方案**:
1. 修复 `app/controllers/api.py` 中的错误：
```python
# 修复前 (错误)
tags = list(route.tags)[0]

# 修复后 (正确)
tags = list(route.tags)[0] if route.tags else "default"
```

2. 初始化PCB API权限：
```python
# 调用API权限刷新方法
await api_controller.refresh_api()
```

3. 将PCB API权限分配给管理员角色：
```python
# 获取所有PCB API
pcb_apis = await Api.filter(path__startswith='/api/v1/pcb').all()

# 分配给管理员角色
admin_role = await Role.filter(name='管理员').first()
await admin_role.apis.add(*pcb_apis)
```

### 5. CRUD方法调用错误

**问题描述**: 
- 后端API调用 `CRUDBase.create()` 方法时参数错误
- 导致500内部服务器错误

**根本原因**: 
- `CRUDBase.create()` 方法期望参数为 `obj_in`，但代码中使用了 `obj=enterprise`

**解决方案**:
```python
# 修改前 (错误)
new_enterprise = await pcb_enterprise_controller.create(obj=enterprise)

# 修改后 (正确)
new_enterprise = await pcb_enterprise_controller.create(enterprise)
```

## 修改文件清单

### 前端文件修改

1. **web/src/views/cloud-audit/pcb/index.vue**
   - 修复 `handleSave` 函数中的表单数据获取方式
   - 添加字段映射逻辑
   - 添加调试日志输出

2. **web/src/components/table/CrudModal.vue**
   - 添加 `computed` 导入
   - 修复组件响应式逻辑

### 后端文件修改

1. **app/controllers/api.py**
   - 修复 `refresh_api` 方法中的 `tags` 索引错误
   - 添加空值检查

2. **app/api/v1/pcb.py**
   - 修复 `create_enterprise` 函数中的CRUD方法调用参数

## 测试验证

### 测试步骤
1. 启动后端服务器
2. 初始化PCB API权限
3. 分配权限给管理员角色
4. 测试前端企业创建功能

### 测试结果
- ✅ 前端表单数据正确获取
- ✅ 字段映射正确
- ✅ 后端API权限正常
- ✅ 企业创建成功，返回200状态码
- ✅ 数据正确保存到数据库

## 技术要点总结

### 前端技术要点
1. **Vue 3 Composition API**: 正确使用 `ref` 和 `defineExpose`
2. **组件通信**: 父子组件数据传递的正确方式
3. **表单验证**: Naive UI表单组件的使用
4. **数据映射**: 前端字段到后端字段的转换

### 后端技术要点
1. **FastAPI路由**: 正确注册API路由
2. **权限系统**: 基于角色的访问控制(RBAC)
3. **数据库ORM**: Tortoise ORM的使用
4. **CRUD操作**: 基础CRUD方法的正确调用

### 调试技巧
1. **前端调试**: 使用浏览器开发者工具查看网络请求和控制台日志
2. **后端调试**: 查看服务器日志和数据库状态
3. **API测试**: 使用Python脚本直接测试API接口
4. **权限检查**: 验证用户角色和API权限的分配

## 预防措施

### 开发规范
1. **前后端字段统一**: 建立字段命名规范，避免前后端字段名不一致
2. **API权限管理**: 新增API时及时更新权限记录
3. **错误处理**: 完善前后端错误处理机制
4. **测试覆盖**: 确保关键功能有完整的测试覆盖

### 部署检查清单
1. ✅ 数据库连接正常
2. ✅ API权限已初始化
3. ✅ 用户角色权限已分配
4. ✅ 前后端字段映射正确
5. ✅ 错误处理机制完善

## 总结

通过系统性的问题排查和修复，成功解决了PCB模块前后端交互的所有问题。主要解决了：

1. **前端数据获取问题** - 修复了子组件数据访问方式
2. **字段映射问题** - 建立了前后端字段映射机制
3. **组件语法错误** - 修复了Vue组件导入问题
4. **后端权限问题** - 初始化了API权限并分配给用户角色
5. **CRUD调用错误** - 修复了方法调用参数问题

最终实现了用户可以通过前端界面正常创建企业信息，数据正确保存到数据库中，前后端交互完全正常。

## 相关文档

- [PCB审核模块数据库与交互设计方案.md](./PCB审核模块数据库与交互设计方案.md)
- [PCB数据库和API检查指南.md](./PCB数据库和API检查指南.md)
- [PCB模块技术方案.md](./PCB模块技术方案.md)

---

**文档创建时间**: 2025-10-14  
**问题解决时间**: 2025-10-14  
**状态**: ✅ 已解决

