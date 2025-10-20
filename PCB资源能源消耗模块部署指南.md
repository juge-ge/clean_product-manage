# PCB资源能源消耗模块部署指南

## 📋 模块概述

本模块重新设计了PCB预审核模块中的资源能源消耗部分，包含三个统计表：
1. **企业近三年用水情况统计** - 分组卡片+动态表格布局
2. **企业近三年用电情况统计** - 顶部筛选区+模块卡片+动态表格
3. **企业近三年天然气情况统计** - 年份范围选择器+动态表头

## 🚀 部署步骤

### 第一步：创建数据库表

运行数据库迁移脚本创建新的表结构：

```bash
python migrations/create_resource_consumption_tables.py
```

这将创建以下表：
- `pcb_water_consumption_category` - 用水类型分类表
- `pcb_water_consumption_record` - 用水消耗记录表
- `pcb_electricity_consumption_record` - 用电消耗记录表
- `pcb_gas_consumption_record` - 天然气消耗记录表
- `pcb_resource_consumption_summary` - 资源能源消耗汇总表

### 第二步：启动后端服务器

```bash
python run.py
```

服务器将在 `http://localhost:8000` 启动。

### 第三步：启动前端服务器

```bash
cd web
npm run dev
```

前端将在 `http://localhost:3100` 启动。

### 第四步：验证部署

运行API测试脚本：

```bash
python test_resource_consumption_api.py
```

## 📁 文件结构

### 后端文件

```
app/
├── models/
│   └── resource_consumption.py          # 数据模型
├── schemas/
│   └── resource_consumption.py          # 数据验证模式
├── controllers/
│   └── resource_consumption.py          # 业务逻辑控制器
└── api/v1/
    └── resource_consumption.py          # API接口
```

### 前端文件

```
web/src/
├── views/cloud-audit/pcb/enterprise-detail/
│   └── components/
│       └── ResourceConsumptionForm.vue  # 资源能源消耗表单组件
└── api/
    └── pcb.js                          # API配置（已更新）
```

### 迁移和测试文件

```
migrations/
└── create_resource_consumption_tables.py  # 数据库迁移脚本

test_resource_consumption_api.py           # API测试脚本
```

## 🔧 功能特性

### 1. 企业用水情况统计

**界面特性：**
- 分组卡片布局，每个卡片对应不同用水统计维度
- 支持动态增删用水分类
- 表格包含：年份、用水类型、单位、用水量、用水来源、备注
- 智能单位推荐：根据用水类型自动推荐单位
- 实时数据验证和错误提示

**数据维度：**
- 企业总体用水
- 分项目用水
- 分部位用水

### 2. 企业用电情况统计

**界面特性：**
- 顶部筛选区：年份多选 + 数据维度切换标签
- 模块卡片：区域用电分布 / 近三年用电趋势
- 动态表格：根据选择的年份自动调整列
- 自动占比计算：用电量 ÷ 总计 × 100%
- 推荐单位标签显示

**数据维度：**
- 区域用电分布（按区域统计）
- 近三年用电趋势（按类型统计）

### 3. 天然气情况统计

**界面特性：**
- 年份范围选择器：支持不同年份范围
- 动态表头：根据选择的年份范围自动生成列
- 项目下拉选择：锅炉天然气、工业煤气等
- 单位下拉选择：m³、吨等
- 底部操作按钮：添加行、提交

## 🔌 API接口

### 主要接口

```
GET    /api/v1/resource-consumption/enterprise/{id}/all-data
POST   /api/v1/resource-consumption/enterprise/{id}/all-data
DELETE /api/v1/resource-consumption/enterprise/{id}/all-data

# 用水相关
GET    /api/v1/resource-consumption/enterprise/{id}/water-categories
POST   /api/v1/resource-consumption/enterprise/{id}/water-categories
GET    /api/v1/resource-consumption/enterprise/{id}/water-records

# 用电相关
GET    /api/v1/resource-consumption/enterprise/{id}/electricity-records
POST   /api/v1/resource-consumption/enterprise/{id}/electricity-records

# 天然气相关
GET    /api/v1/resource-consumption/enterprise/{id}/gas-records
POST   /api/v1/resource-consumption/enterprise/{id}/gas-records

# 汇总数据
GET    /api/v1/resource-consumption/enterprise/{id}/summary
POST   /api/v1/resource-consumption/enterprise/{id}/summary/calculate
```

## 🎨 UI设计特点

### 视觉风格
- **简约专业**：采用卡片式布局，清晰的视觉层次
- **色彩搭配**：主色调为蓝色系，符合企业级应用风格
- **响应式设计**：支持不同屏幕尺寸

### 交互体验
- **智能推荐**：根据选择自动推荐相关选项
- **实时验证**：输入错误时实时标红提示
- **便捷操作**：支持批量操作和快捷按钮
- **数据联动**：不同表格间的数据关联提示

### 组件特性
- **动态表格**：支持动态增删行
- **枚举选择**：丰富的下拉选项
- **年份选择**：灵活的时间范围选择
- **数据格式化**：千分位格式化显示

## 🧪 测试验证

### 1. 功能测试

**用水统计测试：**
- [ ] 创建用水分类
- [ ] 添加用水记录
- [ ] 单位自动推荐
- [ ] 数据验证

**用电统计测试：**
- [ ] 年份多选功能
- [ ] 维度切换
- [ ] 占比自动计算
- [ ] 推荐单位显示

**天然气统计测试：**
- [ ] 年份范围选择
- [ ] 动态表头更新
- [ ] 项目选择
- [ ] 数据提交

### 2. API测试

运行测试脚本验证所有API接口：

```bash
python test_resource_consumption_api.py
```

### 3. 前后端集成测试

1. 启动前后端服务器
2. 访问PCB企业详情页面
3. 进入预审核模块
4. 测试资源能源消耗部分的所有功能

## 🔍 故障排除

### 常见问题

**1. 数据库表创建失败**
```bash
# 检查数据库连接
python check_db.py

# 重新运行迁移脚本
python migrations/create_resource_consumption_tables.py
```

**2. API接口404错误**
```bash
# 检查API路由注册
# 确认 app/api/v1/__init__.py 中已添加资源消耗路由
```

**3. 前端组件加载失败**
```bash
# 检查组件导入路径
# 确认 ResourceConsumptionForm.vue 文件存在
```

**4. 数据保存失败**
```bash
# 检查API权限
# 确认用户有访问资源消耗API的权限
```

### 调试技巧

**1. 查看API文档**
访问 `http://localhost:8000/docs` 查看完整的API文档

**2. 检查数据库**
使用DB Browser for SQLite查看数据是否正确保存

**3. 查看控制台日志**
检查浏览器开发者工具和服务器日志

## 📊 数据流程

```
前端表单 → API接口 → 控制器 → 数据模型 → 数据库
    ↓         ↓        ↓        ↓        ↓
Vue组件 → RESTful → 业务逻辑 → ORM映射 → SQLite
```

## 🎯 使用说明

### 1. 访问模块

1. 登录系统
2. 进入PCB审核模块
3. 选择企业
4. 进入预审核页面
5. 找到"4. 资源能源消耗"模块

### 2. 填写数据

**用水数据：**
1. 点击"新增用水类型"创建分类
2. 在分类卡片中点击"新增行"添加记录
3. 选择年份、用水类型、单位等
4. 填写用水量和来源信息

**用电数据：**
1. 选择年份范围
2. 切换数据维度（区域/趋势）
3. 添加用电记录
4. 系统自动计算占比

**天然气数据：**
1. 选择年份范围
2. 添加项目记录
3. 填写各年份用量
4. 点击提交保存

### 3. 保存数据

- 点击各模块的"暂存"按钮保存当前模块数据
- 点击"保存草稿"保存所有数据
- 点击"提交审核"提交完整数据

## 🚀 后续优化

### 计划功能
- [ ] 数据导入导出功能
- [ ] 数据可视化图表
- [ ] 历史数据对比
- [ ] 数据审核流程
- [ ] 移动端适配

### 性能优化
- [ ] 数据分页加载
- [ ] 缓存机制
- [ ] 批量操作优化
- [ ] 数据压缩

## 📞 技术支持

如遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查相关日志文件
3. 联系技术支持团队

---

**文档版本**: v1.0  
**创建时间**: 2024年  
**最后更新**: 2024年  
**状态**: ✅ 已完成
