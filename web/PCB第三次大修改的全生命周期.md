PCB 预审核第三次大修改 - 接口与前端改动记录

1. 企业总体生产情况 - 三个表格（近三年产品产量、企业近三年合格率、企业近三年产值情况）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ProductionInfoForm.vue`
- 后端实现：
  - Schema：`app/schemas/pcb_production.py`
  - Controller：`app/controllers/pcb_production.py`
  - API路由：`app/api/v1/pcb_production.py`

### 1.1 近三年产品产量

- 新增能力：
  - 可选择年份范围（如`2022-2024`），动态生成三年列：`output_2022`、`output_2023`、`output_2024`
  - 自动计算“总计”列，为三年产量求和
  - 保持原有字段不变：`type`（类型）、`mainProduct`（主要产品）、`unit`（单位）、`layers`（层数）
  - 每个表格左下角有独立的“提交”按钮

- 已实现接口：
  - 保存企业近三年产品产量
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/production/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "type": "rigid",
            "main_product": "rigid_double",
            "unit": "m2",
            "layers": 2,
            "output_2022": 1000,
            "output_2023": 1200,
            "output_2024": 1500
          }
        ]
      }
    - 响应：200，标准成功结构 `{"code": 200, "data": {"count": 1}, "msg": "保存成功"}`

  - 获取企业近三年产品产量
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/production/three-years?year_range=2022-2024`
    - 响应体示例同保存请求体的`items`结构，字段名保持camelCase（前端格式）

### 1.2 企业近三年合格率

- 新增能力：
  - 年份范围与“近三年产品产量”联动（保持一致）
  - 表格显示年份和合格率（百分比）
  - 每个表格左下角有独立的“提交”按钮

- 已实现接口：
  - 保存企业近三年合格率
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/qualification-rate/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          { "year": "2022", "rate": 95.5 },
          { "year": "2023", "rate": 96.0 },
          { "year": "2024", "rate": 97.2 }
        ]
      }
    - 响应：200，标准成功结构

  - 获取企业近三年合格率
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/qualification-rate/three-years?year_range=2022-2024`
    - 响应体示例同保存请求体的`items`结构

### 1.3 企业近三年产值情况

- 新增能力：
  - 年份范围与“近三年产品产量”联动（保持一致）
  - 表格显示年份、单位（万元）、年产值、所得税
  - 每个表格左下角有独立的“提交”按钮
  - 重要：正确处理0值（0是有效数值，不会被误判为null）

- 已实现接口：
  - 保存企业近三年产值
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/output-value/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "year": "2022",
            "unit": "wan_yuan",
            "annualOutputValue": 1234.56,
            "incomeTax": 67.89
          },
          {
            "year": "2023",
            "unit": "wan_yuan",
            "annualOutputValue": 1456.78,
            "incomeTax": 78.90
          },
          {
            "year": "2024",
            "unit": "wan_yuan",
            "annualOutputValue": 1678.90,
            "incomeTax": 89.01
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据
    - 注意：前端字段名为camelCase（`annualOutputValue`、`incomeTax`），后端Schema使用`PCBOutputValueThreeYearsItem`支持camelCase字段

  - 获取企业近三年产值
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/output-value/three-years?year_range=2022-2024`
    - 响应体示例同保存请求体的`items`结构，字段名为camelCase格式

- 技术要点：
  1. **字段名映射**：前端使用camelCase（`annualOutputValue`、`incomeTax`），后端Schema `PCBOutputValueThreeYearsItem` 支持camelCase，使用 `model_config = {"populate_by_name": True}` 确保兼容
  2. **0值处理**：前后端都正确处理0值，避免0被误判为null：
     - 前端：使用显式判断 `=== null` 或 `=== undefined`，而不是 `||`
     - 后端：使用 `is None` 检查，而不是 `if value`
  3. **数据保存**：使用 `batch_upsert` 方法，根据企业ID和年份进行更新或插入
  4. **数据读取**：后端确保返回完整的年份数据（即使某年份没有数据也返回空记录），前端自动补充缺失年份

- 数据库表：
  - `pcb_product_output`：产品产量表（支持动态年份字段）
  - `pcb_qualification_rate`：合格率表
  - `pcb_output_value`：产值情况表（字段：`year`、`unit`、`annual_output_value`、`income_tax`）

备注：三个表格的年份范围保持一致，由第一个表格（近三年产品产量）的选择器控制，其他两个表格自动联动。每个表格都有独立的“提交”按钮，位于表格左下角，提交成功后会自动刷新数据。



2. 原辅材料使用情况（新版）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/RawMaterialForm.vue`
- 后端实现：
  - Schema：`app/schemas/pcb_production.py`
  - Controller：`app/controllers/pcb_raw_material.py`、`app/controllers/pcb_production.py`
  - API路由：`app/api/v1/pcb_production.py`
  - Model：`app/models/pcb_raw_material.py`

- 新增能力：
  - 表头右上角新增"年份范围"选择器（如`2022-2024`），动态生成三年列
  - 列顺序：产品类型、产品名称、产品产量(m²)、原辅材料、单位（kg/m²/L）、分组年度列
  - 双层表头（减少无效空间）：
    - 年消耗量：下挂三年列（如"2022 年"、"2023 年"、"2024 年"），对应字段：`amount_2022`、`amount_2023`、`amount_2024`
    - 单位产品消耗量/m²：下挂三年列（如"2022 年"、"2023 年"、"2024 年"），对应字段：`unitConsumption_2022`、`unitConsumption_2023`、`unitConsumption_2024`
  - 新增行默认继承上一行的产品类型、产品名称、产品产量（用户可手动修改）
  - 与"1. 近三年产品产量"的类型与主要产品枚举保持一致（`type`：刚性/挠性；`mainProduct`：刚性/挠性系列）
  - 表格左下角有独立的"提交"按钮（移除了表头右上角的"暂存"按钮）

- 已实现接口：
  - 保存企业原辅材料三年用量
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/raw-materials/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "type": "rigid",
            "mainProduct": "rigid_double",
            "productOutput": 5000,
            "materialName": "硫酸",
            "unit": "kg",
            "amount_2022": 1200.5,
            "amount_2023": 1300,
            "amount_2024": 1100.25,
            "unitConsumption_2022": 0.2401,
            "unitConsumption_2023": 0.2600,
            "unitConsumption_2024": 0.2201
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据
    - 注意：前端字段名为camelCase（`mainProduct`、`productOutput`、`materialName`），后端Schema支持camelCase字段

  - 获取企业原辅材料三年用量
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/raw-materials/three-years?year_range=2022-2024`
    - 响应体示例（同保存请求体的`items`结构），字段名为camelCase格式

字段说明
- `type`：产品类型，枚举`rigid`/`flexible`
- `mainProduct`：产品名称，与类型联动的枚举（如`rigid_double`等），前端使用camelCase
- `productOutput`：产品产量（数值，单位固定为m²），前端使用camelCase
- `materialName`：原辅材料名称，前端使用camelCase
- `unit`：计量单位，枚举`kg`/`m²`/`L`
- `amount_YYYY`：对应年份的原辅材料年消耗量
- `unitConsumption_YYYY`：对应年份的单位产品消耗量（/m²）

- 技术要点：
  1. **字段名映射**：前端使用camelCase（`mainProduct`、`productOutput`、`materialName`），后端Schema `PCBRawMaterialUsageThreeYearsItem` 使用字段别名（alias）和 `model_config = {"extra": "allow", "populate_by_name": True}` 支持camelCase字段
     - `main_product` 使用别名 `alias="mainProduct"`
     - `product_output` 使用别名 `alias="productOutput"`
     - `material_name` 使用别名 `alias="materialName"`
     - `populate_by_name: True` 允许通过别名或原字段名填充数据
  2. **0值处理**：前后端都正确处理0值，避免0被误判为null（参考产值数据的处理方式）
  3. **数据保存**：使用 `batch_upsert` 方法，根据企业ID、类型、主要产品和材料名称进行更新或插入
  4. **数据读取**：后端返回所有记录，前端根据年份范围筛选并显示对应年份的数据
  5. **数据库表**：`pcb_raw_material_usage`，支持2020-2024年的动态字段
  6. **循环依赖处理**：在 `PCBProductionDataController.__init__()` 中使用延迟导入避免循环依赖问题

- API错误分析与修复（422 Unprocessable Entity）：
  - **错误原因**：
    1. 前端发送的字段名为camelCase格式（`mainProduct`、`productOutput`、`materialName`）
    2. 后端Schema `PCBRawMaterialUsageThreeYearsItem` 初始定义使用snake_case格式（`main_product`、`product_output`、`material_name`），且未配置字段别名
    3. Pydantic验证时无法识别camelCase字段名，导致必填字段验证失败，返回422错误
    
  - **修复方法**：
    1. **Schema修改**（`app/schemas/pcb_production.py`）：
       - 为 `main_product`、`product_output`、`material_name` 添加字段别名（alias）
       - 设置 `model_config = {"extra": "allow", "populate_by_name": True}`
       - 保持必填字段的必填约束（`Field(...)`）
       
       ```python
       class PCBRawMaterialUsageThreeYearsItem(BaseModel):
           """近三年原辅材料使用项Schema - 支持前端camelCase字段名"""
           type: str = Field(..., description="类型(rigid/flexible)")
           main_product: str = Field(..., alias="mainProduct", description="主要产品")
           product_output: Optional[float] = Field(None, alias="productOutput", description="产品产量(m²)")
           material_name: str = Field(..., alias="materialName", description="原辅材料名称")
           unit: str = Field(..., description="单位")
           model_config = {"extra": "allow", "populate_by_name": True}
       ```
    
    2. **API端点修改**（`app/api/v1/pcb_production.py`）：
       - 使用 `model_dump(by_alias=True)` 保留camelCase别名格式
       - 确保传递给controller的数据格式为camelCase，与前端一致
       
       ```python
       # 使用 by_alias=True 来保留camelCase别名（mainProduct, productOutput, materialName）
       item_dict = item.model_dump(by_alias=True)
       ```
    
    3. **Controller延迟导入**（`app/controllers/pcb_production.py`）：
       - 在 `PCBProductionDataController.__init__()` 中使用延迟导入避免循环依赖
       
       ```python
       def __init__(self):
           # 延迟导入避免循环依赖
           from app.controllers.pcb_raw_material import pcb_raw_material_usage_controller
           self.raw_material_usage_controller = pcb_raw_material_usage_controller
       ```

- 数据库表：
  - `pcb_raw_material_usage`：原辅材料使用情况表（字段：`enterprise_id`、`type`、`main_product`、`product_output`、`material_name`、`unit`、`amount_2020~2024`、`unitConsumption_2020~2024`）
  - 唯一约束：(`enterprise_id`, `type`, `main_product`, `material_name`)

- 迁移脚本：
  - `migrations/create_pcb_raw_material_usage_table.py`：用于创建数据库表的迁移脚本

备注：
1. 原辅材料表必须至少存在一行原辅材料为"覆铜板"的记录（前端会自动添加）。
2. 原辅材料字段支持两种方式：
   - 从枚举中直接选择"覆铜板"（前端内置选项）
   - 手动输入任意材料名称（选择器支持手动输入/创建）
3. 年份范围变化时会自动重新获取数据。
4. 提交按钮位于表格左下角，提交成功后会自动刷新数据。
5. **重要**：Schema字段别名配置确保前端camelCase格式与后端snake_case格式的正确映射，避免422验证错误。
6. **单位产品消耗量自动计算**：单位产品消耗量/m² = 年消耗量 / 产品产量，保留两位小数。该字段为只读，当用户输入年消耗量或修改产品产量时自动计算。字段显示为灰色背景，提示"自动计算"。


3. 主要工艺及装备使用（新版）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ProcessEquipmentForm.vue`
- 后端实现：
  - Schema：`app/schemas/process_equipment.py`
  - Controller：`app/controllers/process_equipment.py`
  - API路由：`app/api/v1/pcb_production.py`
  - Model：`app/models/process_equipment.py`

- 改动说明：
  - 将以下字段改为手动输入（取消枚举、与库解耦）：
    - 设备名称（`equipmentName`）
    - 设备型号（`equipmentModel`）
    - 电机型号（`motorModel`）
    - 应用工艺（`process`）
  - 以下字段保持原有类型与交互：
    - 功率（`power`，数值）
    - 数量（`quantity`，整数）
    - 运行状况（`status`，枚举：良好/正常/一般/需维护/故障）
  - 移除了表头右上角的"暂存"按钮，在表格左下角添加独立的"提交"按钮

- 已实现接口：
  - 保存企业设备信息
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/equipment`
    - 请求体示例：
      {
        "items": [
          {
            "equipmentName": "蚀刻机",
            "equipmentModel": "G-1200",
            "motorModel": "MAV21325A-02",
            "power": 15.5,
            "quantity": 2,
            "process": "蚀刻工艺",
            "status": "良好"
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据
    - 注意：前端字段名为camelCase（`equipmentName`、`equipmentModel`、`motorModel`），后端Schema支持camelCase字段

  - 获取企业设备信息
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/equipment`
    - 响应体示例（同保存请求体的`items`结构），字段名为camelCase格式

字段说明
- `equipmentName`：设备名称（字符串），前端使用camelCase
- `equipmentModel`：设备型号（字符串），前端使用camelCase
- `motorModel`：电机型号（字符串），前端使用camelCase
- `power`：功率（数值，kW）
- `quantity`：数量（整数）
- `process`：应用工艺（字符串）
- `status`：运行状况（枚举：良好/正常/一般/需维护/故障）

- 技术要点：
  1. **字段名映射**：前端使用camelCase（`equipmentName`、`equipmentModel`、`motorModel`），后端Schema `PCBEquipmentRecordBase` 使用字段别名（alias）和 `model_config = {"extra": "allow", "populate_by_name": True}` 支持camelCase字段
  2. **数据保存**：使用 `batch_upsert` 方法，先删除该企业的所有设备记录，再批量创建新记录，确保删除功能正常工作
  3. **数据读取**：后端返回所有记录，字段名为camelCase格式
  4. **数据库表**：`pcb_equipment_record`，存储设备基本信息

- 数据库表：
  - `pcb_equipment_record`：设备记录表（字段：`enterprise_id`、`equipment_name`、`equipment_model`、`motor_model`、`power`、`quantity`、`process`、`status`、`remark`）

备注：为保证前后端解耦，该模块不再依赖任何后端返回的枚举集，均为自由输入，仅保留运行状况为前端固定枚举。提交按钮位于表格左下角，提交成功后会自动刷新数据。


4. 资源能源消耗（用水/用电/天然气）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ResourceConsumptionForm.vue`
- 后端实现：
  - Schema：`app/schemas/resource_consumption.py`
  - Controller：`app/controllers/resource_consumption.py`
  - API路由：`app/api/v1/pcb_production.py`（资源消耗相关路由）
  - Model：`app/models/resource_consumption.py`

- 改动说明（用水部分）：
  - 年份范围默认与"1. 企业总体生产情况"一致（如`2022-2024`），表头右上角选择器沿用原交互
  - 用水"项目"枚举仅保留：`生产用水`、`生活用水`
  - 在"项目"后新增"使用车间"（自由输入）
  - 保持每年动态列，并在表尾始终展示三条总计：
    - `生产用水总计`：对所有项目为"生产用水"的行，逐年求和
    - `生活用水总计`：对所有项目为"生活用水"的行，逐年求和
    - `总用水量`：上述两类逐年之和
  - 总计行不可编辑，仅显示逐年累计结果
  - 移除了模块顶部的"暂存"按钮，在表格左下角添加独立的"提交"按钮

- 已实现接口：
  - 保存企业近三年用水情况
    - 方法：POST
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/consumption/water/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "project": "生产用水",
            "workshop": "电镀车间",
            "unit": "m³",
            "amount_2022": 1200.25,
            "amount_2023": 1350,
            "amount_2024": 1400.5
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据

  - 获取企业近三年用水情况
    - 方法：GET
    - 路径：`/api/v1/pcb/enterprise/{enterpriseId}/consumption/water/three-years?year_range=2022-2024`
    - 响应体示例（同保存请求体的`items`结构），字段名为camelCase格式

- 用电：与用水相同的年份范围与动态列机制；项目仅保留`生产用电`、`非直接生产用电`，新增"使用车间"，表尾固定三条总计（生产用电总计、非直接生产用电总计、总用电量），总计及其逐年数加粗显示。
  - 已实现接口：
    - 用电保存：POST `/api/v1/pcb/enterprise/{enterpriseId}/consumption/electricity/three-years`
    - 用电获取：GET `/api/v1/pcb/enterprise/{enterpriseId}/consumption/electricity/three-years?year_range=2022-2024`
    - 字段：`project`（生产用电/非直接生产用电）、`workshop`、`unit`（kWh）、`amount_YYYY`

- 天然气：与用水相同的年份范围与动态列机制；项目仅保留`生产用气`、`非直接生产用气`，新增"使用车间"，表尾固定三条总计（生产用气总计、非直接生产用气总计、总用气量），总计及其逐年数加粗显示。
  - 已实现接口：
    - 天然气保存：POST `/api/v1/pcb/enterprise/{enterpriseId}/consumption/gas/three-years`
    - 天然气获取：GET `/api/v1/pcb/enterprise/{enterpriseId}/consumption/gas/three-years?year_range=2022-2024`
  - 字段：`project`（生产用气/非直接生产用气）、`workshop`、`unit`（m³/吨/kg/L）、`amount_YYYY`

- 技术要点：
  1. **字段名映射**：前端使用camelCase，后端Schema使用`model_config = {"extra": "allow", "populate_by_name": True}`支持动态年份字段和camelCase字段。
  2. **数据保存**：使用 `batch_upsert` 方法，先删除该企业的所有记录，再批量创建新记录，确保删除功能正常工作。
  3. **数据读取**：后端返回所有记录，前端根据年份范围筛选并显示对应年份的数据。
  4. **数据库表**：
     - `pcb_water_consumption_record`：用水消耗记录表（包含`workshop`字段）
     - `pcb_electricity_consumption_record`：用电消耗记录表（包含`workshop`字段）
     - `pcb_gas_consumption_record`：天然气消耗记录表（包含`workshop`字段）

- 数据库迁移：
  - 迁移脚本：`migrations/add_workshop_column_to_resource_consumption.py`
  - 该脚本为三个资源消耗表添加`workshop`列（VARCHAR(200)）

字段说明（用水）
- `project`：枚举，仅`生产用水`/`生活用水`
- `workshop`：使用车间（字符串）
- `unit`：单位（如`m³`）
- `amount_YYYY`：各年份用量

备注：总计行为前端即时计算用于展示，未参与提交；每个表格都有独立的"提交"按钮，位于表格左下角，提交成功后会自动刷新数据。


5. 污染防治（三个表格）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/PollutionControlForm.vue`
- 后端实现：
  - Schema：`app/schemas/pollution_control.py`
  - Controller：`app/controllers/pollution_control.py`
  - API路由：`app/api/v1/pollution_control.py`
  - Model：`app/models/pollution_control.py`

- 改动说明：
  - 移除了模块顶部的"暂存"按钮，三个表格都在表格左下角添加独立的"提交"按钮
  - 三个表格：废水产生分析、企业近三年废水情况统计、废气产生情况

### 5.1 废水产生分析

- 已实现接口：
  - 批量保存废水产生分析
    - 方法：POST
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/wastewater-analysis/batch`
    - 请求体示例：
      {
        [
          {
            "category": "电镀废水",
            "source": "电镀工序",
            "pollutants": "铜、镍",
            "disposal": "化学沉淀+过滤"
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据

  - 获取废水产生分析
    - 方法：GET
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/wastewater-analysis`
    - 响应体示例（同保存请求体结构），字段名为camelCase格式

### 5.2 企业近三年废水情况统计

- 改动说明：
  - 样式与交互复用"4.资源能源消耗-企业近三年用水情况统计"，仅将"用水"替换为"废水"
  - 年份范围选择与"1.企业总体生产情况"一致（如`2022-2024`）
  - 列：项目（仅`生产废水`/`生活废水`）、使用车间（自由输入）、单位（m³ 等）、逐年用量动态列
  - 表尾固定三条总计：`生产废水总计`、`生活废水总计`、`总废水量`；名称与逐年数值加粗，仅展示不可编辑

- 已实现接口：
  - 保存企业近三年废水情况统计
    - 方法：POST
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/wastewater-stat/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "project": "生产废水",
            "workshop": "电镀车间",
            "unit": "m³",
            "amount_2022": 1200.25,
            "amount_2023": 1350,
            "amount_2024": 1400.5
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据

  - 获取企业近三年废水情况统计
    - 方法：GET
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/wastewater-stat/three-years?year_range=2022-2024`
    - 响应体示例（同保存请求体的`items`结构），字段名为camelCase格式

### 5.3 废气产生情况

- 已实现接口：
  - 批量保存废气产生情况
    - 方法：POST
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/waste-gas-analysis/batch`
    - 请求体示例：
      {
        [
          {
            "type": "有机废气",
            "pollutants": "VOCs",
            "location": "印刷工序",
            "treatment": "活性炭吸附"
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据

  - 获取废气产生情况
    - 方法：GET
    - 路径：`/api/v1/pollution-control/enterprise/{enterpriseId}/waste-gas-analysis`
    - 响应体示例（同保存请求体结构），字段名为camelCase格式

- 技术要点：
  1. **字段名映射**：前端使用camelCase（废气表使用`type`字段），后端Schema支持camelCase字段，废气表的`type`字段映射到数据库的`gas_type`字段。
  2. **数据保存**：使用 `batch_upsert` 方法，先删除该企业的所有记录，再批量创建新记录，确保删除功能正常工作。
  3. **数据读取**：后端返回所有记录，前端直接显示。
  4. **前端交互**：移除顶部暂存，添加底部提交按钮，实现数据获取和提交逻辑。

- 数据库表：
  - `pcb_wastewater_analysis`：废水产生分析表
  - `pcb_wastewater_stat_record`：近三年废水情况统计记录表（包含`workshop`字段）
  - `pcb_waste_gas_analysis`：废气产生情况表

- 数据库迁移：
  - 迁移脚本：`migrations/create_pollution_control_tables.py`（推荐使用，一次性创建所有表）
  - 或使用单独脚本：`migrations/create_pcb_wastewater_stat_record_table.py`（仅创建废水统计表）
  - `create_pollution_control_tables.py`会创建以下三个表：
    - `pcb_wastewater_analysis`：废水产生分析表
    - `pcb_waste_gas_analysis`：废气产生情况表
    - `pcb_wastewater_stat_record`：近三年废水情况统计记录表（包含`project`、`workshop`、`unit`和动态年份字段`amount_2020`到`amount_2024`）

字段说明
- 废水产生分析：`category`（废水类别）、`source`（来源）、`pollutants`（主要污染物）、`disposal`（处置方式）
- 近三年废水情况统计：`project`（枚举，仅`生产废水`/`生活废水`）、`workshop`（使用车间，字符串）、`unit`（单位，如`m³`）、`amount_YYYY`（各年份用量）
- 废气产生情况：`type`（种类，前端camelCase）、`pollutants`（主要污染物）、`location`（产生部位）、`treatment`（处理方法）

备注：三个表格都有独立的"提交"按钮，位于表格左下角，提交成功后会自动刷新数据。总计行前端计算，不参与提交。


6. 工业固体废物管理（已实现前后端交互）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/SolidWasteForm.vue`
- 后端实现：
  - Schema：`app/schemas/solid_waste.py`
  - Controller：`app/controllers/solid_waste.py`
  - API路由：`app/api/v1/solid_waste.py`
  - Model：`app/models/solid_waste.py`

- 表格结构：
  - 列：类别、名称、单位、处置方式、年份范围动态列（如`2022年用量`、`2023年用量`、`2024年用量`）、操作（删除）
  - 年份范围选择：支持`2020-2022`、`2021-2023`、`2022-2024`三种范围，默认`2022-2024`
  - 类别选项：一般废物、生活垃圾、危险废物
  - 单位选项：吨、kg、m³
  - 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 获取企业近三年固体废物情况
    - 方法：GET
    - 路径：`/api/v1/solid-waste/enterprise/{enterpriseId}/three-years?year_range=2022-2024`
    - 响应体示例：
      {
        "code": 200,
        "msg": "获取成功",
        "data": [
          {
            "id": 1,
            "category": "危险废物",
            "name": "含铜污泥",
            "unit": "吨",
            "disposal_method": "委托处置",
            "amount_2022": 120.5,
            "amount_2023": 135.2,
            "amount_2024": 140.8
          }
        ]
      }

  - 保存企业近三年固体废物情况
    - 方法：POST
    - 路径：`/api/v1/solid-waste/enterprise/{enterpriseId}/three-years`
    - 请求体示例：
      {
        "year_range": "2022-2024",
        "items": [
          {
            "category": "危险废物",
            "name": "含铜污泥",
            "unit": "吨",
            "disposal_method": "委托处置",
            "amount_2022": 120.5,
            "amount_2023": 135.2,
            "amount_2024": 140.8
          }
        ]
      }
    - 响应：200，标准成功结构，包含保存后的验证数据

- 技术要点：
  1. **动态年份字段**：前端根据选择的年份范围动态生成列，后端模型支持`amount_2020`到`amount_2024`字段
  2. **数据保存**：使用 `batch_upsert` 方法，先删除该企业的所有固体废物记录，再批量创建新记录，确保删除功能正常工作
  3. **数据读取**：后端返回所有记录，字段名为snake_case格式（如`amount_2022`），与前端一致
  4. **字段处理**：对于空值或空字符串，数据库存储为`NULL`；对于数值，转换为`Decimal`类型存储

- 数据库表：
  - `pcb_solid_waste_record`：固体废物记录表
    - 字段：`enterprise_id`、`category`、`name`、`unit`、`disposal_method`、`amount_2020`到`amount_2024`、`remark`

备注：表格有独立的"提交"按钮，位于表格左下角，提交成功后会自动刷新数据。支持完整的增删改查操作，年份范围变化时自动重新加载数据。


7. 自行监测情况（已实现前后端交互）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/SelfMonitoringForm.vue`
- 后端实现：
  - Schema：`app/schemas/self_monitoring.py`
  - Controller：`app/controllers/self_monitoring.py`
  - API路由：`app/api/v1/self_monitoring.py`
  - Model：`app/models/self_monitoring.py`

### 7.1 有组织废气检测表

- 表头顺序：监测时间、监测地点、监测项目及化验结果（单位 mg/m³）
- 监测项目以分组两层表头呈现；新增监测因子 VOCs
- 数值输入移除加减按钮（showButton: false）
- 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 批量获取有组织废气检测记录
    - 方法：GET
    - 路径：`/api/v1/self-monitoring/enterprise/{enterpriseId}/organized-gas/batch`
    - 响应体示例：
      {
        "code": 200,
        "msg": "获取成功",
        "data": [
          {
            "id": 1,
            "monitoringPoint": "G1",
            "monitoringTime": "2024-01-01",
            "result_氮氧化物": 12.3,
            "result_氯化氢": 5.6,
            "result_VOCs": 1.2,
            ...
          }
        ]
      }

  - 批量保存有组织废气检测记录
    - 方法：POST
    - 路径：`/api/v1/self-monitoring/enterprise/{enterpriseId}/organized-gas/batch`
    - 请求体示例：
      [
        {
          "monitoringPoint": "G1",
          "monitoringTime": "2024-01-01",
          "result_氮氧化物": 12.3,
          "result_氯化氢": 5.6,
          "result_VOCs": 1.2,
          ...
        }
      ]
    - 响应：200，标准成功结构，包含保存后的验证数据

### 7.2 无组织废气检测表

- 表格包含：采样时间、采样点位、监测因子、排放浓度（mg/m³）、排放浓度限值（mg/m³）、达标情况
- 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 批量获取无组织废气检测记录：GET `/api/v1/self-monitoring/enterprise/{enterpriseId}/unorganized-gas/batch`
  - 批量保存无组织废气检测记录：POST `/api/v1/self-monitoring/enterprise/{enterpriseId}/unorganized-gas/batch`
  - 请求体字段：`samplingTime`、`samplingPoint`、`monitoringFactor`、`emissionConcentration`、`emissionLimit`、`compliance`

### 7.3 废水排放监测情况表

- 表头顺序：监测时间、监测地点、监测项目（单位 mg/L）
- 监测项目（分组两层表头）包含：pH、氨氮、总氮、COD、镍、铜、总磷、总氰化物、镍（镍排口）
- 数值输入移除加减按钮（showButton: false）
- 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 批量获取废水排放监测记录：GET `/api/v1/self-monitoring/enterprise/{enterpriseId}/wastewater/batch`
  - 批量保存废水排放监测记录：POST `/api/v1/self-monitoring/enterprise/{enterpriseId}/wastewater/batch`
  - 请求体字段：`monitoringTime`、`monitoringPoint`、`result_pH`、`result_COD`、`result_氨氮`、`result_总氮`、`result_总磷`、`result_铜`、`result_镍`、`result_总氰化物`、`result_镍（镍排口）`

### 7.4 废气排放监测情况表

- 表格包含：检测点位、检测项目、检测结果、许可排放浓度限值、排气筒高（m）
- 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 批量获取废气排放监测记录：GET `/api/v1/self-monitoring/enterprise/{enterpriseId}/gas-emission/batch`
  - 批量保存废气排放监测记录：POST `/api/v1/self-monitoring/enterprise/{enterpriseId}/gas-emission/batch`
  - 请求体字段：`detectionPoint`、`detectionItem`、`detectionResult`、`permittedEmissionLimit`、`stackHeight`

### 7.5 近三年厂界噪声监测情况表

- 表格包含：监测时间、监测点位、检测结果 Leq（dB（A））昼间、检测结果 Leq（dB（A））夜间、排放标准 Leq（dB（A））昼间、排放标准 Leq（dB（A））夜间
- 表格左下角有独立的"提交"按钮

- 已实现接口：
  - 批量获取噪声监测记录：GET `/api/v1/self-monitoring/enterprise/{enterpriseId}/noise/batch`
  - 批量保存噪声监测记录：POST `/api/v1/self-monitoring/enterprise/{enterpriseId}/noise/batch`
  - 请求体字段：`monitoringTime`、`monitoringPoint`、`daytimeResult`、`nighttimeResult`、`daytimeStandard`、`nighttimeStandard`

字段说明
- 有组织废气：`monitoringTime`、`monitoringPoint`、`result_<监测因子名>`（mg/m³），监测因子包括：氮氧化物、氯化氢、氰化氢、硫酸雾、铬酸雾、氟化物、酚类、非甲烷总烃、苯、甲苯、二甲苯、甲苯与二甲苯合计、VOCs
- 废水监测：`monitoringTime`、`monitoringPoint`、`result_<项目名>`（mg/L），项目包括：pH、COD、氨氮、总氮、总磷、铜、镍、总氰化物、镍（镍排口）
- 无组织废气：`samplingTime`、`samplingPoint`、`monitoringFactor`、`emissionConcentration`、`emissionLimit`、`compliance`
- 废气排放：`detectionPoint`、`detectionItem`、`detectionResult`、`permittedEmissionLimit`、`stackHeight`
- 噪声监测：`monitoringTime`、`monitoringPoint`、`daytimeResult`、`nighttimeResult`、`daytimeStandard`、`nighttimeStandard`

- 技术要点：
  1. **字段名映射**：前端使用camelCase（如`monitoringPoint`、`monitoringTime`），后端使用snake_case（如`monitoring_point`、`monitoring_time`），Controller中进行字段名转换
  2. **动态字段映射**：有组织废气和废水表格使用`result_<监测因子/项目名>`格式，Controller需要将这些动态字段名映射到数据库固定字段名
  3. **数据保存**：所有表格都使用 `batch_upsert` 方法，先删除该企业的所有记录，再批量创建新记录，确保删除功能正常工作
  4. **数据读取**：后端返回所有记录，字段名为camelCase格式，与前端一致
  5. **数据库表**：
     - `pcb_organized_gas_monitoring`：有组织废气检测表（包含`vocs`字段）
     - `pcb_unorganized_gas_monitoring`：无组织废气检测表
     - `pcb_wastewater_monitoring`：废水排放监测表（包含`monitoring_point`、`nickel`、`nickel_outlet`字段）
     - `pcb_gas_emission_monitoring`：废气排放监测表
     - `pcb_noise_monitoring`：噪声监测表

- 数据库迁移：
  - 迁移脚本：`migrations/add_vocs_and_wastewater_fields.py`
  - 该脚本为`pcb_organized_gas_monitoring`表添加`vocs`字段
  - 为`pcb_wastewater_monitoring`表添加`monitoring_point`、`nickel`、`nickel_outlet`字段

备注：5个表格都有独立的"提交"按钮，位于表格左下角，提交成功后会自动刷新数据。所有表格都支持完整的增删改查操作。


8. 生产工艺与装备要求（完整6项二级指标）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ProcessEquipmentRequirement.vue`
- 二级指标：
  1. **基本要求**（I、II、III级）
     - Ⅲ级：不采用已淘汰高耗能设备；生产场所整洁，符合安全技术、工业卫生的要求
     - Ⅱ级：工厂布局合理，图形形成、板面清洗、蚀刻和电镀与化学镀有水电计量装置
     - Ⅰ级：工厂有全面节能节水措施并有效实施；工厂布局先进，生产设备自动化程度高，有安全、节能工效
     - 选择规则：需先满足Ⅲ级，方可选择Ⅱ级；需满足Ⅱ/Ⅲ级，方可选择Ⅰ级
  2. **机械加工及辅助设施**（I、II、III级）
     - Ⅲ级：有安全防护装置；有吸尘装置
     - Ⅱ级：有集尘系统回收粉尘；废边料分类回收利用
     - Ⅰ级：高噪声区隔音吸声处理；或有防噪声措施
     - 选择规则：同上（需先Ⅲ后Ⅱ，再Ⅰ）
  3. **线路与阻焊图形形成 (印刷或感光工艺)**（I、III级，跳过II级）
     - Ⅲ级：用水溶性抗蚀剂、弱碱显影阻焊剂；废料分类、回收
     - Ⅰ级：用光固化抗蚀剂、阻焊剂；显影、去膜设备附有有机膜处理装置；配置排气或废气处理系统
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级（直接跳过II级）
  4. **板面清洗**（I、III级，跳过II级）
     - Ⅲ级：不使用有机清洗剂，清洗液不含络合物
     - Ⅰ级：建设生产系统数字化体系，拥有覆盖全厂的信息化控制网络和视频监控系统，搭建实时数据库，实现集生产、能源、环境等于一体的数字化管理
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级
  5. **蚀刻**（I、III级，跳过II级）
     - Ⅲ级：应用封闭式自动传送蚀刻装置，蚀刻液不含铬、铁化合物及螯合物，废液集中存放并回收
     - Ⅰ级：蚀刻机有自动控制与添加、再生循环系统；蚀刻清洗水多级逆流清洗；蚀刻清洗溶液补充添加于蚀刻液中或回收；蚀刻机密封，无溶液与气体泄漏，排风管有阀门；排气有吸收处理装置，控制效果好
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级
  6. **电镀与化学镀**（I、III级，跳过II级）
     - Ⅲ级：废液集中存放并回收。配置排气和处理系统
     - Ⅰ级：除电镀金与化学镀金外，均采用无氰电镀液。除产品特定要求外，不采用铅合金电镀与含氟络合物的电镀液，不采用含铅的焊锡涂层。设备有自动控制装置，清洗水多级逆流回用。配置废气收集和处理系统
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级

- 通用规则：
  - 所有指标均可选择“均不符合”（与其他选项互斥）
  - 选择规则仅在第一个“基本要求”上方统一展示提示

- 预留接口（仅占位，未接入）：
  - 保存：POST `/api/pcb/enterprise/{enterpriseId}/process-requirement`
    - 请求体示例：
      {
        "basic_requirements": ["level3", "level2", "level1"] 或 ["none"],
        "mechanical_facilities": ["level3", "level2", "level1"] 或 ["none"],
        "printing_process": ["level3", "level1"] 或 ["none"],
        "cleaning": ["level3", "level1"] 或 ["none"],
        "etching": ["level3", "level1"] 或 ["none"],
        "plating": ["level3", "level1"] 或 ["none"]
      }
  - 获取：GET `/api/pcb/enterprise/{enterpriseId}/process-requirement`
    - 响应体示例同上


9. 温室气体排放（3项二级指标）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/GreenhouseGasEmission.vue`
- 二级指标：
  1. **碳减排管理**（I、III级，跳过II级）
     - Ⅲ级：定期开展碳盘查
     - Ⅰ级：定期开展主要产品碳足迹评价和碳盘查
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级
  2. **单位产值碳排放量**（I、II、III级）
     - Ⅲ级：识别、计算并提供改进方案
     - Ⅱ级：与上年度相比指标改善
     - Ⅰ级：近三年指标持续改善
     - 选择规则：需先Ⅲ→II→I
  3. **碳排放强度**（I、II、III级）
     - Ⅲ级：2.677 t/万元
     - Ⅱ级：1.71 t/万元
     - Ⅰ级：0.628 t/万元
     - 选择规则：需先Ⅲ→II→I

- 通用规则：
  - 所有指标均可选择“均不符合”（与其他选项互斥）
  - 选择规则已在第8模块上方统一展示，本模块不重复

- 预留接口（仅占位，未接入）：
  - 保存：POST `/api/pcb/enterprise/{enterpriseId}/greenhouse-gas-emission`
    - 请求体示例：
      {
        "carbon_management": ["level3", "level1"] 或 ["none"],
        "emission_per_output": ["level3", "level2", "level1"] 或 ["none"],
        "emission_intensity": ["level3", "level2", "level1"] 或 ["none"]
      }
  - 获取：GET `/api/pcb/enterprise/{enterpriseId}/greenhouse-gas-emission`
    - 响应体示例同上


10. 产品特征（4项二级指标）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ProductCharacteristics.vue`
- 说明：本模块所有指标仅包含“Ⅰ级”和“不符合”两个选项（原表格中Ⅲ级内容已作为Ⅰ级要求）
- 二级指标：
  1. **使用无毒无害或低毒低害的生产辅助材料**（只有Ⅰ级和不符合）
     - Ⅰ级：不得使用氢氟氯化碳(HCFCs)、1,1,1-三氯乙烷(C2H3Cl3)、三氯乙烯(C2HCl3)、溴丙烷(C3H7Br)、二氯乙烷(CH3CHCl2)、二氯甲烷(CH2Cl2)、三氯甲烷(CHCl3)、四氯化碳(CCl4)、正己烷(C6H14)、甲苯(C7H8)、二甲苯(C6H4(CH3)2)等物质作为清洗剂。使用光固化抗蚀剂、阻焊剂除电镀金、银与化学镀金外,均采用无氰电镀液除产品特定要求外,不使用铅合金电镀与含氟络合物的电镀液,不采用含铅的焊锡涂层原辅材料中有害物质应满足《电器电子产品有害物质限制使用管理办法》要求。
     - 不符合
  2. **包装**（只有Ⅰ级和不符合）
     - Ⅰ级：不得使用氢氟氯化碳(HCFCs)作为发泡剂;符合GB/T 16716.1 关于包装的通用要求, 包括包装的减量化、重复使用、回收利用、重金属含量和最终处理方面的要求, 并满足GB/T 31268 关于限制商品过度包装的要求。
     - 不符合
  3. **有害物质限制使用**（只有Ⅰ级和不符合）
     - Ⅰ级：铅及其化合物(Pb) ≤1000mg/kg；镉及其化合物(Cd) ≤100mg/kg；汞及其化合物(Hg) ≤1000mg/kg；六价铬化合物(Cr(VI)) ≤1000mg/kg；多溴联苯(PBB) ≤1000mg/kg；多溴二苯醚(PBDE) ≤1000mg/kg；邻苯二甲酸二(2-乙基己基)酯(DEHP) ≤1000mg/kg；邻苯二甲酸丁苄酯(BBP) ≤1000mg/kg；邻苯二甲酸二丁酯(DBP) ≤1000mg/kg；邻苯二甲酸二异丁酯(DIBP) ≤1000mg/kg
     - 不符合
  4. **产品性能**（只有Ⅰ级和不符合）
     - Ⅰ级：应达到或超过产品规定的技术要求。
     - 不符合

- 选择规则：
  - 每个指标仅有两个互斥选项：Ⅰ级 或 不符合
  - 选择规则已在第8模块上方统一展示，本模块不重复

- 预留接口（仅占位，未接入）：
  - 保存：POST `/api/pcb/enterprise/{enterpriseId}/product-characteristics`
    - 请求体示例：
      {
        "auxiliary_material": ["level1"] 或 ["none"],
        "packaging": ["level1"] 或 ["none"],
        "hazardous_substance": ["level1"] 或 ["none"],
        "product_performance": ["level1"] 或 ["none"]
      }
  - 获取：GET `/api/pcb/enterprise/{enterpriseId}/product-characteristics`
    - 响应体示例同上

字段说明
- 所有字段均为单选（数组仅包含一个值）：`["level1"]` 或 `["none"]`


11. 清洁生产管理（11项二级指标）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/CleanProductionManagement.vue`
- 二级指标：
  1. **环保法律法规执行情况**（只有Ⅰ级和不符合）
     - Ⅰ级：符合国家和地方有关环境法律、法规,企业污染物排放总量及能源消耗总量满足国家及地方政府相关标准,满足环评批复、环保"三同时"制度、总量控制和排污许可证管理要求。
     - 不符合
  2. **产业政策符合性**（只有Ⅰ级和Ⅲ级，跳过II级）
     - Ⅲ级：生产规模符合国家和地方。不采用国家明令淘汰类的生产工艺、装备,不生产国家禁止类产品。
     - Ⅰ级：生产规模符合国家和地方相关产业政策,不采用国家限制、淘汰类的生产工艺、装备,不生产国家限制、淘汰类的产品。
     - 选择规则：需先满足Ⅲ级，方可选择Ⅰ级
     - 均不符合
  3. **清洁生产管理**（只有Ⅰ级和不符合）
     - Ⅰ级：按照GB/T 24001建立并运行环境管理体系,建有专门负责清洁生产的领导机构,各成员单位及主管人员职责分工明确;有健全的清洁生产管理制度和奖励管理办法,有执行情况检查记录;制定有清洁生产工作规划及年度工作计划,对规划、计划提出的目标、指标、清洁生产方案,认真组织落实;资源、能源、环保设施运行统计台账齐全;建立、制定环境突发性事件应急预案(预案要通过相应环保部门备案)并定期演练。按行业无组织排放监管的相关政策要求,加强对无组织排放的防控措施,减少生产过程无组织排放。
     - 不符合
  4. **清洁生产审核**（Ⅰ、Ⅱ、Ⅲ级）
     - Ⅲ级：按政府规定要求,制订清洁生产审核工作计划,原料及生产全流程中部分生产工序定期开展清洁生产审核活动,中、高费方案实施率≥50%。
     - Ⅱ级：按政府规定要求,制订清洁生产审核工作计划,对原料及生产全流程定期开展清洁生产审核活动,中、高费方案实施率≥60%。
     - Ⅰ级：按政府规定要求,制订清洁生产审核工作计划,对原料及生产全流程定期开展清洁生产审核活动,中、高费方案实施率≥80%。
     - 选择规则：需先Ⅲ→II→I
     - 均不符合
  5. **节能管理**（Ⅰ、Ⅱ、Ⅲ级）
     - Ⅲ级：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥50%。
     - Ⅱ级：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥70%。
     - Ⅰ级：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥90%。
     - 选择规则：需先Ⅲ→II→I
     - 均不符合
  6. **污染物排放监测**（只有Ⅰ级和不符合）
     - Ⅰ级：满足国家相关监测技术规范要求;按照排污许可证规定的自行监测方案自行或委托第三方监测机构开展监测工作,安排专人专职对监测数据进行记录、整理、统计和分析,公开自行监测信息。
     - 不符合
  7. **危险化学品管理**（只有Ⅰ级和不符合）
     - Ⅰ级：符合《危险化学品安全管理条例》相关要求。
     - 不符合
  8. **计量器具配备情况**（只有Ⅰ级和不符合）
     - Ⅰ级：计量器具配备满足符合国家标准GB17167、GB24789三级计量配备要求。
     - 不符合
  9. **固体废物处理处置**（只有Ⅰ级和不符合）
     - Ⅰ级：通过当地环保主管部门组织的危险废物规范化管理考核,综合评估结果为"达标"。按照GB 18599 相关规定对暂时不利用或者不能利用的一般工业固体废物进行贮存或处置。
     - 不符合
  10. **土壤污染隐患排查**（只有Ⅰ级和不符合）
      - Ⅰ级：属于土壤污染重点监管单位的企业应参照国家有关技术规范,建立土壤污染隐患排查制度,保证持续有效防止有毒有害物质渗漏、流失、扬散。
      - 不符合
  11. **运输方式**（Ⅰ、Ⅱ、Ⅲ级）
      - Ⅲ级：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)，或新能源汽车比例不低于50%，其他车辆达到国四排放标准；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械比例不低于50%。
      - Ⅱ级：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)，或新能源汽车比例不低于70%，其他车辆达到国四排放标准；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械比例不低于70%。
      - Ⅰ级：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)或新能源汽车；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械。
      - 选择规则：需先Ⅲ→II→I
      - 均不符合

- 通用规则：
  - 所有指标均可选择"均不符合"或"不符合"（与其他选项互斥）
  - 有层级关系的指标遵循先低后高的选择规则
  - 选择规则已在第8模块上方统一展示，本模块不重复

- 预留接口（仅占位，未接入）：
  - 保存：POST `/api/pcb/enterprise/{enterpriseId}/clean-production-management`
    - 请求体示例：
      {
        "environmental_law": ["level1"] 或 ["none"],
        "industrial_policy": ["level3", "level1"] 或 ["none"],
        "clean_production_management": ["level1"] 或 ["none"],
        "clean_production_audit": ["level3", "level2", "level1"] 或 ["none"],
        "energy_management": ["level3", "level2", "level1"] 或 ["none"],
        "emission_monitoring": ["level1"] 或 ["none"],
        "chemical_management": ["level1"] 或 ["none"],
        "measurement_equipment": ["level1"] 或 ["none"],
        "solid_waste_disposal": ["level1"] 或 ["none"],
        "soil_pollution_risk": ["level1"] 或 ["none"],
        "transport_mode": ["level3", "level2", "level1"] 或 ["none"]
      }
  - 获取：GET `/api/pcb/enterprise/{enterpriseId}/clean-production-management`
    - 响应体示例同上


12. 能源、水、原/辅材料的消耗利用和污染物的排放

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ResourceUtilization.vue`
- 表格说明：
  1. **能源消耗**（第一个表格）
     - 表格列：
       - 类型（枚举）：刚性/挠性，与"1.企业总体生产情况-近三年产品产量"的逻辑一致
       - 产品名称（枚举）：根据类型动态显示（刚性单面板、刚性双面板等），与"1.企业总体生产情况"一致
       - 层数（枚举）：1-30层，与"1.企业总体生产情况"一致，部分产品有默认层数
       - 产量（m²）：用户输入，移除+ -符号，允许输入正数（包括小数，精度2位）
       - 耗电量：用户输入，移除+ -符号，允许输入正数（包括小数，精度2位）
       - 单位产品消耗量：自动计算（耗电量/产量），保留四位有效数字，只读显示
       - 评定等级：多选复选框，包含Ⅰ级、Ⅱ级、Ⅲ级和"均不符合"选项
         - 选择规则："均不符合"与其他选项互斥（选择"均不符合"时清除其他选项，选择其他选项时清除"均不符合"）
       - 操作：删除按钮
     - 功能：
       - 支持新增行
       - 类型选择后，产品名称选项自动更新
       - 产品名称选择后，层数自动填充（如有默认值）或允许手动选择
       - 单位产品消耗量根据产量和耗电量实时计算

- 预留接口（仅占位，未接入）：
  - 保存能源消耗数据
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/energy-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "type": "rigid",
            "main_product": "rigid_double",
            "layers": 2,
            "output": 5000.50,
            "electricity": 2500.25,
            "unit_consumption": 0.5001,
            "rating": ["level1", "level2", "level3"] 或 ["none"]
          }
        ]
      }
    - 响应：200，标准成功结构

  - 获取能源消耗数据
    - 方法：GET
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/energy-consumption`
    - 响应体示例同保存请求体的`items`结构

字段说明
- `type`：产品类型，枚举`rigid`（刚性）/`flexible`（挠性）
- `main_product`：产品名称，与类型联动的枚举（如`rigid_single`、`rigid_double`等）
- `layers`：层数，整数（1-30）
- `output`：产量，数值（m²），精度2位
- `electricity`：耗电量，数值，精度2位
- `unit_consumption`：单位产品消耗量，数值（耗电量/产量），保留四位有效数字，前端自动计算
- `rating`：评定等级，字符串，单选：`"level1"`、`"level2"`、`"level3"` 或 `"none"`（均不符合）

  2. **新鲜水耗**（第二个表格）
     - 表格列：产品名称（单面板、双面板、多层板(2+n)层、HDI板(2+n)层）、层数、产量（m²）、新鲜水耗（m³）、单位产品新鲜水耗（m³/m²）、评定等级、操作
     - 交互与规则：单面板/双面板自动默认层数1/2，多层板和HDI板用户输入；数字输入移除+ -按钮；单位产品新鲜水耗=新鲜水耗/产量，保留四位有效数字
     - 判断标准：点击"判断标准"按钮，查看单位产品耗水标准（根据产品类型和层数）

  3. **废水总量**（第三个表格）
     - 表格列：产品名称、层数、产量（m²）、废水总量（m³）、单位产品废水量（m³/m²）、评定等级、操作
     - 交互与规则：同上；单位产品废水量=废水总量/产量，保留四位有效数字
     - 判断标准：点击"判断标准"按钮，查看废水产生量标准

  4. **废水中总铜浓度**（第四个表格）
     - 表格列：产品名称、层数、产量（m²）、废水中总铜浓度（g/m²）、单位产品废水铜产生量（g/m²）、评定等级、操作
     - 交互与规则：同上；单位产品废水铜产生量=废水中总铜浓度/产量，保留四位有效数字
     - 判断标准：点击"判断标准"按钮，查看废水中铜产生量标准

  5. **废水中COD浓度**（第五个表格）
     - 表格列：产品名称、层数、产量（m²）、废水中总COD浓度（g/m²）、单位产品COD产生量（g/m²）、评定等级、操作
     - 交互与规则：同上；单位产品COD产生量=废水中总COD浓度/产量，保留四位有效数字
     - 判断标准：点击"判断标准"按钮，查看废水中COD产生量标准

- 预留接口（仅占位，未接入）：
  - 保存新鲜水耗数据
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/fresh-water-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "product": "single|double|multilayer|hdi",
            "layers": 2,
            "output": 5000.5,
            "fresh_water": 1200.25,
            "unit_fresh_water": 0.2401,
            "rating": "level1" 或 "level2" 或 "level3" 或 "none"
          }
        ]
      }

  - 保存废水总量数据
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/wastewater-total-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "product": "single|double|multilayer|hdi",
            "layers": 2,
            "output": 5000.5,
            "wastewater_total": 950.1,
            "unit_wastewater": 0.1900,
            "rating": "level1" 或 "level2" 或 "level3" 或 "none"
          }
        ]
      }

  - 保存废水中总铜浓度数据
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/wastewater-cu-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "product": "single|double|multilayer|hdi",
            "layers": 2,
            "output": 5000.5,
            "wastewater_cu": 2.3456,
            "unit_cu": 0.0005,
            "rating": "level1" 或 "level2" 或 "level3" 或 "none"
          }
        ]
      }

  - 保存废水中COD浓度数据
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/wastewater-cod-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "product": "single|double|multilayer|hdi",
            "layers": 2,
            "output": 5000.5,
            "wastewater_cod": 8.7654,
            "unit_cod": 0.0018,
            "rating": "level1" 或 "level2" 或 "level3" 或 "none"
          }
        ]
      }

  - 获取接口：GET `/api/pcb/enterprise/{enterpriseId}/resource-utilization/{type}`，其中type为：fresh-water-consumption、wastewater-total-consumption、wastewater-cu-consumption、wastewater-cod-consumption
    - 响应体示例同对应保存请求体的`items`结构

字段说明（水资源消耗表格）
- `product`：产品名称，枚举：`single`（单面板）、`double`（双面板）、`multilayer`（多层板）、`hdi`（HDI板）
- `layers`：层数，整数；单面板默认1，双面板默认2，多层板和HDI板需用户输入
- `output`：产量，数值（m²），精度2位
- 各表格总量字段：
  - 新鲜水耗：`fresh_water`（m³），精度4位
  - 废水总量：`wastewater_total`（m³），精度4位
  - 废水中总铜浓度：`wastewater_cu`（g/m²），精度4位
  - 废水中总COD浓度：`wastewater_cod`（g/m²），精度4位
- 单位产品计算字段：各总量/产量，保留四位有效数字，前端自动计算
- `rating`：评定等级，字符串，单选：`"level1"`、`"level2"`、`"level3"` 或 `"none"`（均不符合）

备注：仅前端实现，保持前后端解耦；单位产品消耗量为前端实时计算，后端保存时可包含计算结果；每个表格都有独立的判断标准弹窗；后续计划继续扩展原/辅材料消耗与污染物排放表格。

---

**重要更新（2024年修改）：**

已完成"12. 能源、水、原/辅材料的消耗利用和污染物的排放"模块的6个表格的后端实现：

### 已实现表格：

1. **能源消耗**（已完成前后端交互）
2. **新鲜水耗**（已完成前后端交互）
3. **废水总量**（已完成前后端交互）
4. **废水中总铜浓度**（已完成前后端交互）
5. **废水中COD浓度**（已完成前后端交互）
6. **原/辅料消耗（覆铜板）**（已完成前后端交互）

### 后端实现：

- **Model**: `app/models/resource_utilization.py`
  - `PCBEnergyConsumption`
  - `PCBFreshWaterConsumption`
  - `PCBWastewaterTotalConsumption`
  - `PCBWastewaterCuConsumption`
  - `PCBWastewaterCODConsumption`
  - `PCBRawMaterialConsumption`

- **Schema**: `app/schemas/resource_utilization.py`
  - 为每个表格定义了Create、Update、Response Schema

- **Controller**: `app/controllers/resource_utilization.py`
  - 6个Controller，每个都实现了`get_by_enterprise`和`batch_upsert`方法
  - 使用"先删除后创建"策略，确保删除功能正常工作
  - 安全处理Decimal类型转换，避免类型错误

- **API路由**: `app/api/v1/resource_utilization.py`
  - 每个表格都有GET和POST批量操作端点
  - 使用`Body(...)`明确指定列表请求体，避免中间件500错误
  - 正确处理camelCase和snake_case字段名转换

### 已实现接口：

1. **能源消耗**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/energy-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/energy-consumption`

2. **新鲜水耗**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/fresh-water-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/fresh-water-consumption`

3. **废水总量**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-total-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-total-consumption`

4. **废水中总铜浓度**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-cu-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-cu-consumption`

5. **废水中COD浓度**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-cod-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/wastewater-cod-consumption`

6. **原/辅料消耗（覆铜板）**：
   - GET `/api/v1/resource-utilization/enterprise/{enterpriseId}/raw-material-consumption`
   - POST `/api/v1/resource-utilization/enterprise/{enterpriseId}/raw-material-consumption`

### 前端实现：

- **组件**: `web/src/views/cloud-audit/pcb/enterprise-detail/components/ResourceUtilization.vue`
  - 添加了`enterpriseId` props
  - 为每个表格在底部添加了"提交"按钮（使用`<template #footer>`）
  - 实现了6个表格的数据加载函数（`loadEnergyData`, `loadFreshWaterData`, `loadWastewaterTotalData`, `loadWastewaterCuData`, `loadWastewaterCODData`, `loadRawMaterialData`）
  - 实现了6个表格的数据提交函数（`submitEnergyData`, `submitFreshWaterData`, `submitWastewaterTotalData`, `submitWastewaterCuData`, `submitWastewaterCODData`, `submitRawMaterialData`）
  - 添加了6个独立的`loading`状态
  - 在`onMounted`和`watch enterpriseId`时自动加载数据
  - 提交成功后自动刷新数据

- **API调用**: `web/src/api/pcb.js`
  - 新增`pcbResourceUtilizationApi`对象，包含所有6个表格的GET和POST方法
  - 已添加到`pcbApi`的`resourceUtilization`属性中

- **父组件**: `web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue`
  - 移除了"12. 能源、水、原/辅材料的消耗利用和污染物的排放"模块的暂存按钮
  - 传递`enterpriseId`给`ResourceUtilization`组件

### 数据库迁移：

- **迁移脚本**: `migrations/create_resource_utilization_tables.py`
  - 创建了6个数据库表，每个表都包含必要的字段和索引
  - 表结构完全符合Tortoise ORM模型定义

### 技术要点：

1. **字段名映射**：前端使用camelCase（如`mainProduct`、`unitConsumption`），后端Controller正确映射到数据库snake_case字段（如`main_product`、`unit_consumption`）

2. **数据保存策略**：使用`batch_upsert`方法，先删除该企业的所有记录，再批量创建新记录，确保删除功能正常工作

3. **请求体处理**：API端点使用`List[Dict[str, Any]] = Body(...)`明确指定请求体类型，避免中间件500错误（参考Bug修复记录4.1）

4. **Decimal类型安全**：Controller中使用`get_decimal_value`辅助函数安全地处理Decimal类型转换，避免`ValueError`或`TypeError`

5. **前后端数据同步**：提交成功后自动刷新数据，确保前端显示与数据库一致

### 注意事项：

- 所有6个表格都在表格左下角有独立的"提交"按钮
- 提交成功后会自动刷新数据，确保前端显示与数据库一致
- 支持完整的增删改查操作
- 前端自动计算字段（如单位产品消耗量）为只读显示，不参与后端存储
- 企业ID变化时会自动重新加载所有表格数据

  6. **原/辅料消耗（覆铜板利用率）**（第六个表格）
     - 表格列：类型、产品名称、层数、产量（m²）、覆铜板消耗量（m²）、覆铜板利用率（%）、评定等级、操作
     - 交互与规则：
       - 类型/产品/层数逻辑与“能源消耗”一致
       - 覆铜板利用率= 覆铜板消耗量/产量×100，保留两位有效数字，显示为百分比
       - 评定等级单选：Ⅰ、Ⅱ、Ⅲ、均不符合
       - 提供“判断标准”弹窗（20-27条）

  - 保存原/辅料消耗（覆铜板）
    - 方法：POST
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/raw-material-consumption`
    - 请求体示例：
      {
        "items": [
          {
            "type": "rigid|flexible",
            "main_product": "rigid_double|...",
            "layers": 2,
            "output": 5000.5,
            "ccl_consumption": 4800.2,
            "ccl_utilization": 96.01,
            "rating": "level1" 或 "level2" 或 "level3" 或 "none"
          }
        ]
      }
    - 响应：200

  - 获取原/辅料消耗（覆铜板）
    - 方法：GET
    - 路径：`/api/pcb/enterprise/{enterpriseId}/resource-utilization/raw-material-consumption`
    - 响应体示例同上

13. 资源综合利用（选项型）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/components/ResourceReutilization.vue`
- 二级指标与规则：
  1. 水资源重复利用率（Ⅰ、Ⅱ、Ⅲ级，数值阈值：Ⅲ≥45%，Ⅱ≥55%，Ⅰ≥65%）
  2. 蚀刻液回收率（Ⅰ、Ⅱ、Ⅲ级：Ⅲ≥80%，Ⅱ≥88%，Ⅰ≥95%）
  3. 一般工业固体废物综合利用率（Ⅰ、Ⅱ、Ⅲ级：Ⅲ≥65%，Ⅱ≥73%，Ⅰ≥90%）
  4. 废水收集与处理（只有“符合(Ⅰ级)”或“不符合”）
  5. 废气收集与处理（只有“符合(Ⅰ级)”或“不符合”）
  6. 一般固体废物收集与处理（只有“符合(Ⅰ级)”或“不符合”）
  7. 危险废物收集与处理（只有“符合(Ⅰ级)”或“不符合”）
  8. 噪声（只有“符合(Ⅰ级)”或“不符合”）

- 选择逻辑：
  - 具有Ⅰ/Ⅱ/Ⅲ级的指标：Ⅲ→Ⅱ→Ⅰ逐级满足；“均不符合”与其它互斥
  - 只有Ⅰ级的指标：单选“符合(Ⅰ级)”或“不符合”

- 预留接口：
  - 保存：POST `/api/pcb/enterprise/{enterpriseId}/resource-reutilization`
    - 请求体示例：
      {
        "water_reuse": ["level3", "level2", "level1"] 或 ["none"],
        "etching_recovery": ["level3", "level2", "level1"] 或 ["none"],
        "general_solid_util": ["level3", "level2", "level1"] 或 ["none"],
        "wastewater_collection": ["level1"] 或 ["none"],
        "waste_gas_treatment": ["level1"] 或 ["none"],
        "general_solid_collection": ["level1"] 或 ["none"],
        "hazardous_waste_collection": ["level1"] 或 ["none"],
        "noise": ["level1"] 或 ["none"]
      }
  - 获取：GET `/api/pcb/enterprise/{enterpriseId}/resource-reutilization`
    - 响应体示例同上


14. 问题及清洁生产方案（已完成前后端交互）

- 前端实现：`web/src/views/cloud-audit/pcb/enterprise-detail/problem-solution.vue`
- 后端实现：
  - Schema：`app/schemas/pcb_problem_solution.py`
  - Controller：`app/controllers/pcb_problem_solution.py`
  - API路由：`app/api/v1/pcb_problem_solution.py`
  - Model：`app/models/pcb_problem_solution.py`

- 界面分为四部分：
  1) **问题清单**：自动汇聚"审核"模块中评定为Ⅱ级及以下的指标，支持问题描述、整改建议、责任部门/人、整改期限等字段编辑；支持暂存。
  2) **权重总和计分排序**：记录用户录入的新增因素和新增审核重点以及输入的数据及结果，自动计算总分并排序。
  3) **无/低费方案库**：展示可选方案列表，支持新建自定义方案和从方案库选择；支持多选并关联到问题清单。
  4) **中高费方案库**：展示可选方案列表；支持新建/编辑自定义方案并保存；独立数据表，与无/低费方案不共用。

- 已实现接口：
  - 获取Ⅱ级及以下问题清单
    - 方法：GET
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/issues`
    - 响应示例：
      {
        "code": 200,
        "msg": "获取成功",
        "data": [
          {
            "indicator_id": 1,
            "primary_indicator": "资源消耗利用",
            "primary_weight": 0.25,
            "secondary_indicator": "单位产品电耗",
            "secondary_weight": 0.1,
            "current_level": "II级",
            "problem": "",
            "advice": "",
            "department": "",
            "owner": "",
            "deadline": ""
          }
        ]
      }
    - 说明：从审核模块（PCBAuditResult）中查询level为"II级"、"III级"、"不达标"的指标，关联指标表（PCBIndicator）获取指标详情

  - 暂存问题清单
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/issues`
    - 请求体示例：
      [
        {
          "indicator_id": 1,
          "problem": "单位电耗偏高",
          "advice": "优化工艺参数",
          "department": "生产部",
          "owner": "张三",
          "deadline": "2025-12-31"
        }
      ]
    - 响应：200，标准成功结构
    - 说明：将问题描述保存到审核结果的comment字段

  - 获取权重计分配置
    - 方法：GET
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/scoring-config`
    - 响应示例：
      {
        "code": 200,
        "msg": "获取成功",
        "data": {
        "factors": [{ "key": "waste_amount", "name": "废弃物量", "weight": 10 }],
          "focuses": [{ "id": 1, "name": "二车间" }],
          "scores": {
            "1": {
              "waste_amount": { "r": 5, "rw": 50 }
            }
          },
          "ranking": [{ "id": 1, "name": "二车间", "score": 500 }]
        }
      }

  - 保存权重计分配置
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/scoring-config`
    - 请求体示例：
      {
        "factors": [{ "key": "waste_amount", "name": "废弃物量", "weight": 10 }],
        "focuses": [{ "id": 1, "name": "二车间" }],
        "scores": {
          "1": {
            "waste_amount": { "r": 5, "rw": 50 }
          }
        }
      }
    - 响应：200，标准成功结构，包含自动计算的排序结果
    - 说明：前端可自定义新增/移除"因素(含权重)"与"审核重点(名称)"，保存为企业侧配置；后端自动计算总分（Σ R*W）并排序

  - 获取无/低费方案列表
    - 方法：GET
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/low-cost-schemes`
    - 响应示例：
      {
        "code": 200,
        "msg": "获取成功",
        "data": [
          {
            "id": 1,
            "name": "优化喷淋压力与流量",
            "intro": "通过优化喷淋参数降低新鲜水耗",
            "economic_benefit": "年节约用水费用12万",
            "environment_benefit": "减少废水12000m³/年",
            "scheme_id": 1,
            "is_custom": false,
            "related_indicator_ids": [30, 34],
            "status": "selected"
          }
        ]
      }
    - 说明：如果方案为空，会自动从方案库（根据Ⅱ级及以下指标关联）导入推荐方案

  - 批量保存无/低费方案
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/low-cost-schemes`
    - 请求体示例：
      [
        {
          "name": "优化喷淋压力与流量",
          "intro": "通过优化喷淋参数降低新鲜水耗",
          "economic_benefit": "年节约用水费用12万",
          "environment_benefit": "减少废水12000m³/年",
          "is_custom": true,
          "status": "selected"
        }
      ]
    - 响应：200，标准成功结构
    - 说明：使用"先删除后创建"策略，确保删除功能正常工作

  - 从方案库导入无/低费方案
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/low-cost-schemes/import`
    - 响应：200，标准成功结构
    - 说明：根据企业的Ⅱ级及以下指标，从方案库（PCBIndicatorSchemeRelation）查找关联的方案，自动导入

  - 获取中/高费方案列表
    - 方法：GET
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/medium-high-cost-schemes`
    - 响应示例：同无/低费方案，但包含`cost_level`字段（middle/high）
    - 说明：如果方案为空，会自动从方案库导入推荐方案

  - 批量保存中/高费方案
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/medium-high-cost-schemes`
    - 请求体示例：
      [
        {
          "name": "引入闭路循环冷却系统",
          "intro": "建设循环冷却水站并分区计量",
          "economic_benefit": "年节约电费30万",
          "environment_benefit": "减少废水45000m³/年",
          "cost_level": "middle",
          "is_custom": true,
          "status": "selected"
        }
      ]
    - 响应：200，标准成功结构
    - 说明：使用独立的数据表（pcb_problem_solution_medium_high_cost_scheme），与无/低费方案不共用

  - 从方案库导入中/高费方案
    - 方法：POST
    - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/medium-high-cost-schemes/import`
    - 响应：200，标准成功结构
    - 说明：根据企业的Ⅱ级及以下指标，从方案库查找关联的方案，自动导入

- 技术要点：
  1. **问题清单获取**：从PCBAuditResult表中查询level为"II级"、"III级"、"不达标"的审核结果，关联PCBIndicator表获取指标详情
  2. **权重计分排序**：用户可自定义因素和审核重点，输入R和RW值，后端自动计算总分（Σ R*W）并按分数降序排序
  3. **方案库关联**：通过PCBIndicatorSchemeRelation表建立指标与方案的映射关系，根据Ⅱ级及以下指标自动推荐关联方案
  4. **数据表独立**：无/低费方案和中/高费方案使用独立的数据表，不共用
  5. **方案来源标识**：方案表中使用`is_custom`字段区分自定义方案和方案库导入的方案；使用`scheme_id`字段关联到方案库的原始方案

- 数据库表：
  - `pcb_problem_solution_scoring`：权重总和计分排序表（字段：`enterprise_id`、`factors`、`focuses`、`scores`、`ranking`）
  - `pcb_problem_solution_low_cost_scheme`：无/低费方案表（字段：`enterprise_id`、`name`、`intro`、`economic_benefit`、`environment_benefit`、`scheme_id`、`is_custom`、`related_indicator_ids`、`status`）
  - `pcb_problem_solution_medium_high_cost_scheme`：中/高费方案表（字段：`enterprise_id`、`name`、`intro`、`economic_benefit`、`environment_benefit`、`scheme_id`、`is_custom`、`cost_level`、`related_indicator_ids`、`status`）

- 数据库迁移：
  - 迁移脚本：`migrations/create_pcb_problem_solution_tables.py`
  - 该脚本创建3个数据库表

- 前端API调用：
  - API对象：`web/src/api/pcb.js` 中的 `pcbProblemSolutionApi`
  - 已添加到 `pcbApi.problemSolution`

字段说明
- `level`：当前评定等级，`II级`/`III级`/`不达标`
- `cost_level`：方案费用等级，`middle`（中费）/`high`（高费）
- `is_custom`：是否自定义方案，`true`（自定义）/`false`（方案库导入）
- `scheme_id`：来源方案库的方案ID（如果是从方案库选择的）
- `related_indicator_ids`：关联的指标ID列表（JSON格式）
- `factors`：因素列表，格式：`[{key, name, weight}]`
- `focuses`：审核重点列表，格式：`[{id, name}]`
- `scores`：评分数据，格式：`{focus_id: {factor_key: {r, rw}}}`

备注：所有接口已实现完整的前后端交互，支持数据的增删改查操作。权重计分排序模块支持自动计算总分并排序。方案库导入功能根据Ⅱ级及以下指标自动推荐关联方案。

### 14.1 功能增强（2024年最新修改）

**新增功能：**
1. **三个表格的提交按钮**：
   - 权重总和计分排序表格左下角添加"提交"按钮
   - 无/低费方案库表格左下角添加"提交"按钮
   - 中/高费方案库表格左下角添加"提交"按钮
   - 点击提交后将数据保存到数据库（使用批量保存，先删除后创建策略）

2. **方案库导入功能改进**：
   - 点击"从方案库导入"按钮后，弹出方案库选择界面
   - 界面中展示根据二级及以下指标关联的所有可用方案
   - 支持通过选择指标进行筛选（多选下拉框）
   - 用户可以勾选需要导入的方案
   - 确认导入后，只导入选中的方案，而不是全部导入
   - 支持无/低费方案和中/高费方案分别导入

**新增API接口：**

- **批量保存无/低费方案**：
  - 方法：POST
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/low-cost-schemes`
  - 请求体：方案列表数组（支持批量保存）
  - 说明：使用先删除后创建策略，确保删除功能正常工作

- **批量保存中/高费方案**：
  - 方法：POST
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/medium-high-cost-schemes`
  - 请求体：方案列表数组（支持批量保存）
  - 说明：使用先删除后创建策略，确保删除功能正常工作

- **获取方案库无/低费方案（支持指标筛选）**：
  - 方法：GET
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/scheme-library/low-cost`
  - 查询参数：`indicator_ids`（可选，指标ID列表，用于筛选）
  - 响应：方案列表，包含方案详情和关联的指标信息

- **获取方案库中/高费方案（支持指标筛选）**：
  - 方法：GET
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/scheme-library/medium-high-cost`
  - 查询参数：
    - `indicator_ids`（可选，指标ID列表，用于筛选）
    - `cost_level`（可选，费用等级：middle/high）
  - 响应：方案列表，包含方案详情和关联的指标信息

- **提交权重计分配置**：
  - 方法：POST（已存在，新增提交按钮调用）
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/scoring-config`
  - 说明：前端添加了提交按钮，用户点击后保存到数据库

**方案库筛选逻辑：**
- 无/低费方案：通过`investment`字段（为空或小于10万）或`scheme_type`字段（包含"低"、"无"）判断
- 中/高费方案：通过`investment`字段（大于等于10万）或`scheme_type`字段（包含"中"、"高"）判断
- 费用等级判断：investment >= 100万为高费，10-100万为中费

**前端改动：**
- 为三个表格添加了`<template #footer>`，在左下角显示提交按钮
- 新增方案库导入弹窗（`showImportModal`），包含：
  - 指标筛选下拉框（多选）
  - 方案列表表格（可勾选）
  - 导入按钮（显示选中数量）
- 修改了`importFromLibrary`函数，改为打开弹窗而不是直接导入
- 新增`loadLibrarySchemes`函数，根据指标筛选加载方案
- 新增`confirmImportSchemes`函数，导入选中的方案
- 新增`submitScoringConfig`、`submitLowCostSchemes`、`submitMediumHighCostSchemes`三个提交函数

**后端改动：**
- Controller新增`batch_upsert`方法（无/低费方案和中/高费方案），实现先删除后创建策略
- API路由修改批量保存接口，支持列表格式请求体
- 新增获取方案库方案的GET接口，支持指标筛选
- 修改导入接口，改为接收方案ID列表而不是指标ID列表

**技术要点：**
1. **批量保存策略**：使用"先删除后创建"策略，确保删除功能正常工作
2. **方案筛选逻辑**：通过`investment`和`scheme_type`字段判断方案的费用等级
3. **指标筛选**：前端支持多选指标，后端根据指标ID列表筛选关联的方案
4. **导入逻辑**：用户可以选择特定方案导入，而不是一股脑全部导入
5. **前后端交互**：所有提交操作都有加载状态和错误提示

### 14.2 功能增强（2024年最新修改 - 删除功能和新建方案简化）

**新增功能：**
1. **方案删除功能**：
   - 无/低费方案库表格的每一行添加"删除"按钮
   - 中/高费方案库表格的每一行添加"删除"按钮
   - 点击删除按钮后弹出确认对话框
   - 确认删除后调用后端API直接删除数据库中的记录
   - 删除成功后自动刷新列表

2. **新建方案表单简化**：
   - 新建自定义方案时，表单只保留4个字段：
     - 方案名称
     - 方案简介
     - 经济效益
     - 环境效益
   - 移除了其他字段：适用问题、方案内容、费用等级、预期效果等
   - 无/低费方案和中/高费方案共用同一个简化的表单
   - 保存后直接写入数据库，无需再点击"提交"按钮

**新增API接口：**

- **删除无/低费方案**（已存在，前端新增调用）：
  - 方法：DELETE
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/low-cost-schemes/{schemeId}`
  - 说明：前端表格中的删除按钮调用此接口

- **删除中/高费方案**（已存在，前端新增调用）：
  - 方法：DELETE
  - 路径：`/api/v1/pcb/problem-solution/enterprise/{enterpriseId}/medium-high-cost-schemes/{schemeId}`
  - 说明：前端表格中的删除按钮调用此接口

**前端改动：**
- 在`lowSchemeColumns`和`mhSchemeColumns`中添加"操作"列，使用`h`函数渲染删除按钮
- 新增`handleDeleteScheme`函数，实现删除确认对话框和删除逻辑
- 修改`editForm`结构，只保留4个字段：`name`、`intro`、`economic_benefit`、`environment_benefit`
- 新增`currentSchemeType`变量，用于区分新建的是无/低费方案还是中/高费方案
- 修改`openCreateLow`函数，简化为只初始化4个字段
- 新增`openCreateMedium`函数，用于打开中/高费方案的新建表单
- 修改`saveCustomScheme`函数：
  - 简化为只保存4个字段
  - 根据`currentSchemeType`判断保存到哪个表
  - 保存成功后直接刷新列表，提示用户已创建成功
- 简化新建方案的模态框，移除不需要的字段输入框

**后端改动：**
- 删除API接口已存在（`delete_low_cost_scheme`和`delete_medium_high_cost_scheme`）
- Controller的`remove`方法已实现，无需修改

**数据清除：**
- 已清除所有现有方案数据（152条记录）
- 清除脚本：`clear_all_schemes.py`
- 脚本会清除`pcb_low_cost_scheme`和`pcb_medium_high_cost_scheme`表中的所有记录

**技术要点：**
1. **删除功能**：使用确认对话框防止误删，删除后自动刷新列表
2. **表单简化**：新建方案时只保留必要的4个字段，简化用户操作
3. **即时保存**：新建方案保存后直接写入数据库，无需额外的提交步骤
4. **类型区分**：通过`currentSchemeType`区分无/低费方案和中/高费方案，但共用同一个表单
5. **前后端交互**：删除操作有确认提示和错误处理，用户体验良好

**注意事项：**
- 删除操作不可恢复，请谨慎操作
- 新建方案时，无/低费方案和中/高费方案使用相同的表单字段
- 中/高费方案保存时会自动设置`cost_level`为"middle"（中费）
- 方案创建成功后会自动刷新列表，无需手动刷新


---

## Bug修复记录

### 1. 删除功能修复（2024年修改）

**问题描述：**
- 三个模块（1.企业总体生产情况、2.原辅材料使用情况、3.主要工艺及装备使用）共五个表格的删除按钮无法正常删除数据库中的数据
- 前端删除行后，提交时数据库仍然保留已删除的记录

**影响范围：**
- `ProductionInfoForm` 的三个表格：近三年产品产量、企业近三年合格率、企业近三年产值情况
- `RawMaterialForm`：原辅材料使用情况
- `ProcessEquipmentForm`：主要工艺及装备使用

**修复方案：**
修改后端Controller的保存方法，采用"先删除后创建"的策略：
1. **产品产量**（`save_three_years_product_output`）：
   - 先删除该年份范围内的所有产品产量数据
   - 再批量创建新记录
   
2. **合格率**（`save_three_years_qualification_rate`）：
   - 先删除该年份范围内的所有合格率数据
   - 再批量创建新记录

3. **产值情况**（`save_three_years_output_value`）：
   - 先删除该年份范围内的所有产值数据
   - 再批量创建新记录

4. **原辅材料使用情况**（`save_three_years_raw_material_usage`）：
   - 先删除该企业的所有原辅材料数据
   - 再批量创建新记录

5. **主要工艺及装备使用**（`batch_upsert` in `PCBEquipmentRecordController`）：
   - 先删除该企业的所有设备记录
   - 再批量创建新记录

**技术实现：**
```python
# 示例：产品产量保存方法
async def save_three_years_product_output(self, enterprise_id: int, year_range: str, items: List[Dict]) -> int:
    # 解析年份范围
    start_year, end_year = map(int, year_range.split('-'))
    years = [str(y) for y in range(start_year, end_year + 1)]
    
    # 先删除该年份范围内的所有数据，确保删除功能正常工作
    await self.product_output_controller.model.filter(
        enterprise_id=enterprise_id,
        year__in=years
    ).delete()
    
    # 批量创建新记录
    results = []
    for data_item in data_list:
        new_record = await self.product_output_controller.model.create(
            enterprise_id=enterprise_id,
            **data_item
        )
        results.append(new_record)
    
    return len(results)
```

**修复文件：**
- `app/controllers/pcb_production.py`：修改了三个保存方法
- `app/controllers/process_equipment.py`：已实现先删除后创建（无需修改）

**效果：**
- 前端删除行后，提交时会同步删除数据库中的对应记录
- 确保前端显示的数据与数据库保持一致

---

### 2. 单位产品消耗量自动计算功能（2024年修改）

**问题描述：**
- 原辅材料使用情况表格中，单位产品消耗量/m²字段需要手动输入
- 要求根据消耗量/产品产量自动计算，保留两位小数

**修复方案：**
在前端 `RawMaterialForm.vue` 中实现自动计算功能：

1. **添加计算函数**：
   ```javascript
   const calculateUnitConsumption = (row, year) => {
     const amount = row[`amount_${year}`]
     const productOutput = row.productOutput
     
     if (amount != null && amount !== '' && productOutput != null && productOutput !== '' && productOutput > 0) {
       const amountNum = typeof amount === 'number' ? amount : parseFloat(amount)
       const outputNum = typeof productOutput === 'number' ? productOutput : parseFloat(productOutput)
       
       if (!isNaN(amountNum) && !isNaN(outputNum) && outputNum > 0) {
         const unitConsumption = (amountNum / outputNum).toFixed(2)
         row[`unitConsumption_${year}`] = parseFloat(unitConsumption)
       } else {
         row[`unitConsumption_${year}`] = null
       }
     } else {
       row[`unitConsumption_${year}`] = null
     }
   }
   ```

2. **修改年消耗量输入框**：
   - 当用户输入年消耗量时，自动触发计算对应年份的单位产品消耗量

3. **修改产品产量输入框**：
   - 当产品产量变化时，重新计算所有年份的单位产品消耗量

4. **修改单位产品消耗量列**：
   - 将字段改为只读（`readonly: true`）
   - 显示灰色背景（`backgroundColor: '#f5f5f5'`）
   - 占位符改为"自动计算"
   - 精度从6位改为2位（保留两位小数）

5. **数据加载时自动计算**：
   - 如果后端没有单位产品消耗量值，自动根据消耗量和产品产量计算

**计算公式：**
```
单位产品消耗量/m² = 年消耗量 / 产品产量（保留两位小数）
```

**修复文件：**
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/RawMaterialForm.vue`

**效果：**
- 用户输入年消耗量或修改产品产量时，单位产品消耗量自动计算并显示
- 字段为只读，防止手动修改导致的数据不一致
- 保留两位小数，符合业务需求

---

### 3. 数据库迁移修复（2024年修改）

**问题描述：**
- "4. 资源能源消耗"模块的三个表格（用水、用电、天然气）在提交数据时报告500错误：`table pcb_water_consumption_record has no column named workshop`
- "5. 污染防治"模块的"企业近三年废水情况统计"表格在加载/提交数据时报告500错误：`no such table: pcb_wastewater_stat_record`
- 原因是数据库表结构与模型定义不一致，缺少`workshop`列和新表

**修复方案：**
1. **添加`workshop`列到资源消耗表**：
   - 创建迁移脚本：`migrations/add_workshop_column_to_resource_consumption.py`
   - 为以下三个表添加`workshop`列（VARCHAR(200)）：
     - `pcb_water_consumption_record`
     - `pcb_electricity_consumption_record`
     - `pcb_gas_consumption_record`

2. **创建`pcb_wastewater_stat_record`表**：
   - 更新迁移脚本：`migrations/create_pcb_wastewater_stat_record_table.py`
   - 使用Tortoise ORM的`generate_schemas()`方法自动创建表结构
   - 表包含字段：`enterprise_id`、`project`、`workshop`、`unit`、`amount_2020`到`amount_2024`、`remark`

**技术实现：**
```python
# 添加workshop列的迁移脚本示例
def add_workshop_column():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    
    tables = [
        "pcb_water_consumption_record",
        "pcb_electricity_consumption_record",
        "pcb_gas_consumption_record"
    ]
    
    for table_name in tables:
        if not check_column_exists(cursor, table_name, "workshop"):
            cursor.execute(f"""
                ALTER TABLE {table_name} 
                ADD COLUMN workshop VARCHAR(200)
            """)
    
    conn.commit()
```

```python
# 创建废水统计表的迁移脚本示例
async def create_table():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()  # 根据模型定义自动生成表结构
    await Tortoise.close_connections()
```

**修复文件：**
- `migrations/add_workshop_column_to_resource_consumption.py`：添加workshop列的迁移脚本
- `migrations/create_pcb_wastewater_stat_record_table.py`：创建废水统计表的迁移脚本

**效果：**
- 资源消耗表的`workshop`列已添加，可以正常保存和读取车间信息
- 废水统计表已创建，可以正常进行数据的增删改查操作
- 所有数据库表结构与模型定义保持一致

**注意事项：**
- 运行迁移脚本时需要注意Windows编码问题（GBK vs UTF-8），脚本中应避免使用Unicode字符
- 迁移脚本应在数据库操作前运行，确保表结构正确

### 4. 污染防治表缺失修复（2024年修改）

**问题描述：**
- "5. 污染防治"模块的"废水产生分析"和"废气产生情况"表格在提交数据时报告500错误
- 错误信息：`Request failed with status code 500`
- 原因是数据库表中 `pcb_wastewater_analysis` 和 `pcb_waste_gas_analysis` 表不存在，或者表结构不正确（NOT NULL字段没有默认值）

**根本原因：**
- 数据库表的 `source`、`pollutants`、`disposal`、`location`、`treatment` 字段定义为 `NOT NULL` 但没有 `DEFAULT ''`
- 当前端发送的数据中这些字段为 `None` 或缺失时，数据库拒绝插入
- 与能正常工作的"企业近三年废水情况统计"表相比，该表的 `workshop` 字段允许 `NULL`，因此能正常工作

**修复方案：**
1. **重新创建数据库表（关键修复）**：
   - 创建迁移脚本 `migrations/recreate_pollution_analysis_tables.py`
   - 删除旧的 `pcb_wastewater_analysis` 和 `pcb_waste_gas_analysis` 表
   - 重新创建表，确保 `NOT NULL` 字段都有 `DEFAULT ''`：
     - `pcb_wastewater_analysis`：`source TEXT NOT NULL DEFAULT ''`、`pollutants TEXT NOT NULL DEFAULT ''`、`disposal TEXT NOT NULL DEFAULT ''`
     - `pcb_waste_gas_analysis`：`pollutants VARCHAR(200) NOT NULL DEFAULT ''`、`location TEXT NOT NULL DEFAULT ''`、`treatment TEXT NOT NULL DEFAULT ''`
   - 这样可以确保即使前端发送 `None` 或缺失字段，数据库也能正常插入

2. **修复Schema定义**：
   - 在 `app/schemas/pollution_control.py` 中为 `PCBWastewaterAnalysisBase` 和 `PCBWasteGasAnalysisBase` 的字段添加默认值：
     - `source: str = Field(default="", ...)`
     - `pollutants: str = Field(default="", ...)`
     - `disposal: str = Field(default="", ...)`
     - `location: str = Field(default="", ...)`
     - `treatment: str = Field(default="", ...)`

3. **修复FastAPI请求体参数问题**：
   - 使用 `Body(...)` 明确指定请求体参数类型
   - 在API端点中添加数据预处理，确保所有字段都是字符串

4. **简化Controller逻辑**：
   - 由于数据库和Schema都有默认值，可以简化字段处理逻辑
   - 保留错误处理和调试日志

**技术实现：**
```python
# 创建表的迁移脚本
async def create_tables():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    # 导入模型以确保它们被注册
    from app.models.pollution_control import (
        PCBWastewaterAnalysis,
        PCBWasteGasAnalysis,
        PCBWastewaterStatRecord
    )
    
    # 生成数据库表
    await Tortoise.generate_schemas()
```

```python
# API端点修复 - 使用Body(...)指定请求体
@router.post("/enterprise/{enterprise_id}/wastewater-analysis/batch")
async def batch_save_wastewater_analysis(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水分析记录列表"),
    current_user=DependAuth
):
    # ... 处理逻辑
```

**修复文件：**
- `migrations/recreate_pollution_analysis_tables.py`：重新创建污染防治分析表的迁移脚本（带默认值）
- `app/schemas/pollution_control.py`：更新Schema定义，添加字段默认值
- `app/api/v1/pollution_control.py`：修复API端点，使用`Body(...)`指定请求体参数，添加数据预处理
- `app/controllers/pollution_control.py`：简化字段处理逻辑（因为数据库和Schema都有默认值）

**效果：**
- 数据库表结构正确，所有 `NOT NULL` 字段都有 `DEFAULT ''`
- Schema定义与数据库表一致，都有默认值
- API端点正确识别请求体参数，批量保存功能恢复正常
- "废水产生分析"和"废气产生情况"表格的提交功能正常工作

**技术要点：**
- **数据库表结构**：`NOT NULL` 字段必须搭配 `DEFAULT ''`，否则插入 `None` 或缺失字段时会失败
- **Schema默认值**：确保即使前端未发送某些字段，也能正常工作
- **对比能正常工作的表**："企业近三年废水情况统计"的 `workshop` 字段允许 `NULL`，因此能正常工作，但其他表的所有字段都是 `NOT NULL`，必须提供默认值

**注意事项：**
- 运行迁移脚本会删除现有数据，请先备份
- FastAPI中，对于列表类型的请求体参数，必须使用 `Body(...)` 明确指定
- 修复后需要重启后端服务器才能生效

---

### 4.1 中间件处理列表请求体错误修复（2024年修改）

**问题描述：**
- "5. 污染防治"模块的"废水产生分析"和"废气产生情况"表格在提交数据时仍然报告500错误
- 错误信息：`ValueError: dictionary update sequence element #0 has length 4; 2 is required`
- 错误发生在 `app/core/middlewares.py` 的 `HttpAuditLogMiddleware.get_request_args` 方法中

**根本原因：**
- `HttpAuditLogMiddleware` 中间件在记录审计日志时，尝试解析请求体并更新到 `args` 字典中
- 代码使用 `args.update(body)`，期望 `body` 是字典类型
- 但批量操作API（如废水产生分析、废气产生情况）的请求体是列表格式：`[{category: "123", ...}]`
- 当 `body` 是列表时，`dict.update()` 方法会尝试将列表元素作为键值对更新，导致 `ValueError`
- 这是因为 `dict.update()` 对于列表会期望每个元素是长度为2的元组 `(key, value)`，但实际收到的是字典

**修复方案：**
在 `app/core/middlewares.py` 的 `get_request_args` 方法中添加类型检查：

```python
# 修复前
body = await request.json()
args.update(body)  # 如果body是列表会报错

# 修复后
body = await request.json()
# 只有当body是字典时才更新args，如果是列表（如批量操作），则跳过
if isinstance(body, dict):
    args.update(body)
# 如果是列表，为了审计日志记录，可以添加一个标记
elif isinstance(body, list):
    args["_batch_data"] = True
    args["_batch_count"] = len(body)
```

**技术实现：**
- 检查请求体的类型（字典或列表）
- 如果是字典，正常更新 `args`（保持原有功能）
- 如果是列表，跳过更新但添加标记信息，便于审计日志记录批量操作的特征
- 不影响FastAPI的请求处理，只是中间件在准备审计日志参数时的处理逻辑

**修复文件：**
- `app/core/middlewares.py`：修复 `HttpAuditLogMiddleware.get_request_args` 方法

**效果：**
- 中间件可以正确处理字典和列表两种格式的请求体
- 批量操作API（列表格式请求体）不再报错
- 审计日志仍然可以记录请求信息（包括批量操作的标记）
- "废水产生分析"和"废气产生情况"表格的提交功能正常工作

**技术要点：**
- **中间件处理**：中间件在处理请求体时需要区分不同的数据类型，不能假设所有请求体都是字典
- **批量操作支持**：批量操作的API通常使用列表作为请求体，中间件需要特殊处理
- **向后兼容**：修复后仍然支持字典格式的请求体，不影响现有功能

**注意事项：**
- 此修复影响所有使用列表作为请求体的API端点，不仅限于污染防治模块
- 修复后需要重启后端服务器才能生效
- 其他批量操作API（如自行监测、固体废物管理等）也会受益于此修复

---

### 5. 工业固体废物管理模块实现（2024年修改）

**问题描述：**
- "6. 工业固体废物管理"模块需要实现正常的前后端交互，支持年份范围选择和批量CRUD操作
- 需要移除表头右上角的"暂存"按钮，在表格左下角添加"提交"按钮

**修复方案：**
1. **后端实现**：
   - 在`PCBSolidWasteRecordController`中添加`batch_upsert`方法，实现"先删除后创建"策略
   - 在`app/api/v1/solid_waste.py`中添加三年数据交互端点：
     - GET `/api/v1/solid-waste/enterprise/{enterprise_id}/three-years?year_range=2022-2024`
     - POST `/api/v1/solid-waste/enterprise/{enterprise_id}/three-years`
   - 创建`PCBSolidWasteThreeYearsItem`和`PCBSolidWasteThreeYearsRequest` Schema，支持动态年份字段

2. **前端实现**：
   - 修改`SolidWasteForm.vue`：
     - 移除表头右上角的"暂存"按钮
     - 在表格左下角添加"提交"按钮
     - 实现`loadSolidWasteData`和`submitSolidWasteData`函数
     - 添加`loading`状态管理
     - 在`onMounted`和年份范围变化时自动加载数据
   - 修改`pre-audit.vue`：移除"6. 工业固体废物管理"模块的暂存按钮
   - 更新`web/src/api/pcb.js`：添加`getThreeYearsSolidWaste`和`saveThreeYearsSolidWaste`方法

**技术实现：**
```python
# Controller中的batch_upsert方法
async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBSolidWasteRecord]:
    # 先删除该企业的所有固体废物记录，确保删除功能正常工作
    await self.model.filter(enterprise_id=enterprise_id).delete()
    
    # 创建新记录
    results = []
    for item in items:
        record_data = {
            "enterprise_id": enterprise_id,
            "category": item.get("category") or "",
            "name": item.get("name") or "",
            "unit": item.get("unit") or "",
        }
        
        # 添加年份数据
        for year in range(2020, 2025):
            year_key = f"amount_{year}"
            if year_key in item:
                value = item[year_key]
                if value is None or value == "":
                    record_data[year_key] = None
                else:
                    record_data[year_key] = Decimal(str(value))
        
        new_record = await self.model.create(**record_data)
        results.append(new_record)
    
    return results
```

**修复文件：**
- `app/controllers/solid_waste.py`：添加`batch_upsert`方法
- `app/api/v1/solid_waste.py`：添加三年数据交互端点
- `app/schemas/solid_waste.py`：添加`PCBSolidWasteThreeYearsItem`和`PCBSolidWasteThreeYearsRequest` Schema
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/SolidWasteForm.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue`：移除暂存按钮
- `web/src/api/pcb.js`：添加API方法

**效果：**
- 固体废物管理表格支持年份范围选择和动态列生成
- 数据可以正常保存、读取和删除
- 提交按钮位于表格左下角，提交成功后自动刷新数据

---

### 6. 自行监测情况模块实现（2024年修改）

**问题描述：**
- "7. 自行监测情况"模块包含5个表格，需要实现正常的前后端交互：
  - 有组织废气检测表
  - 无组织废气检测表
  - 废水排放监测情况表
  - 废气排放监测情况表
  - 近三年厂界噪声监测情况表
- 需要为每个表格移除表头右上角的"暂存"按钮，在表格左下角添加"提交"按钮
- 有组织废气检测表需要支持VOCs字段
- 废水排放监测情况表需要支持monitoring_point、nickel、nickel_outlet字段

**修复方案：**
1. **模型和Schema更新**：
   - 在`PCBOOrganizedGasMonitoring`模型中添加`vocs`字段
   - 在`PCBWastewaterMonitoring`模型中添加`monitoring_point`、`nickel`、`nickel_outlet`字段
   - 更新对应的Schema定义

2. **后端实现**：
   - 在5个Controller中都添加`batch_upsert`方法，实现"先删除后创建"策略
   - 在`app/api/v1/self_monitoring.py`中为每个表格添加批量保存和获取端点：
     - 有组织废气：GET/POST `/api/v1/self-monitoring/enterprise/{enterprise_id}/organized-gas/batch`
     - 无组织废气：GET/POST `/api/v1/self-monitoring/enterprise/{enterprise_id}/unorganized-gas/batch`
     - 废水排放：GET/POST `/api/v1/self-monitoring/enterprise/{enterprise_id}/wastewater/batch`
     - 废气排放：GET/POST `/api/v1/self-monitoring/enterprise/{enterprise_id}/gas-emission/batch`
     - 噪声监测：GET/POST `/api/v1/self-monitoring/enterprise/{enterprise_id}/noise/batch`

3. **前端实现**：
   - 修改`SelfMonitoringForm.vue`：
     - 为每个表格移除表头右上角的"添加列"按钮（有组织废气和废水表格）
     - 为每个表格在左下角添加"提交"按钮
     - 实现5个表格的数据加载和提交函数
     - 添加5个独立的`loading`状态
     - 在`onMounted`时自动加载所有表格数据
   - 修改`pre-audit.vue`：移除"7. 自行监测情况"模块的暂存按钮
   - 更新`web/src/api/pcb.js`：添加所有5个表格的批量保存和获取方法

4. **数据字段映射**：
   - 有组织废气检测：前端使用`result_<监测因子名>`格式（如`result_氮氧化物`、`result_VOCs`），后端转换为对应的数据库字段（如`nitrogen_oxides`、`vocs`）
   - 废水排放监测：前端使用`result_<项目名>`格式（如`result_pH`、`result_COD`），后端转换为对应的数据库字段（如`ph`、`cod`）

**技术实现：**
```python
# Controller中的batch_upsert方法示例（有组织废气）
async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBOrganizedGasMonitoring]:
    # 先删除该企业的所有有组织废气检测记录
    await self.model.filter(enterprise_id=enterprise_id).delete()
    
    # 创建新记录
    results = []
    for item in items:
        record_data = {
            "enterprise_id": enterprise_id,
            "monitoring_point": item.get("monitoringPoint") or "",
            "monitoring_time": item.get("monitoringTime") or "",
            "nitrogen_oxides": Decimal(str(item["result_氮氧化物"])) if item.get("result_氮氧化物") else None,
            "vocs": Decimal(str(item["result_VOCs"])) if item.get("result_VOCs") else None,
            # ... 其他字段
        }
        new_record = await self.model.create(**record_data)
        results.append(new_record)
    
    return results
```

**修复文件：**
- `app/models/self_monitoring.py`：添加`vocs`、`monitoring_point`、`nickel`、`nickel_outlet`字段
- `app/schemas/self_monitoring.py`：更新Schema定义，添加新字段
- `app/controllers/self_monitoring.py`：为5个Controller都添加`batch_upsert`方法
- `app/api/v1/self_monitoring.py`：添加5个表格的批量保存和获取端点
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/SelfMonitoringForm.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue`：移除暂存按钮
- `web/src/api/pcb.js`：添加API方法

**数据库迁移：**
- 迁移脚本：`migrations/add_vocs_and_wastewater_fields.py`
- 该脚本为`pcb_organized_gas_monitoring`表添加`vocs`字段
- 为`pcb_wastewater_monitoring`表添加`monitoring_point`、`nickel`、`nickel_outlet`字段

**效果：**
- 5个表格都可以正常进行数据的增删改查操作
- 每个表格都有独立的提交按钮，位于表格左下角
- 提交成功后自动刷新数据，确保前端显示与数据库一致
- 字段映射正确，前端camelCase格式与后端snake_case格式正确转换

**注意事项：**
- 有组织废气检测表和废水排放监测情况表使用动态字段名（`result_<监测因子/项目名>`），需要正确映射到数据库字段
- 所有表格都采用"先删除后创建"策略，确保删除功能正常工作
- 运行迁移脚本后需要重启后端服务器才能生效

---

### 7. 审核选项型数据模块实现（2024年修改）

**问题描述：**
- "8. 生产工艺与装备要求"、"9. 温室气体排放"、"10. 产品特征"、"11. 清洁生产管理"、"13. 资源综合利用"这5个模块都是复选框型数据，需要实现正常的前后端交互
- 每个模块包含多个二级指标，每个指标可以选择多个选项（如`level1`、`level2`、`level3`、`none`）
- 需要移除每个模块右上角的"暂存"按钮，在模块左下角添加"提交"按钮
- 需要确保数据能够正常保存、读取和更新

**修复方案：**
1. **数据库表设计**：
   - 为每个模块创建一个独立的表，存储该模块的所有二级指标选择
   - 每个表使用`enterprise_id`作为唯一索引，确保每个企业只有一条记录
   - 二级指标字段使用`JSONField`类型，存储数组格式（如`["level1", "level2", "level3"]`）

2. **后端实现**：
   - 创建5个模型类（`app/models/pcb_audit_options.py`）：
     - `PCBProcessEquipmentRequirement`：6个二级指标（基本要求、机械加工及辅助设施、线路与阻焊图形形成、板面清洗、蚀刻、电镀与化学镀）
     - `PCBGreenhouseGasEmission`：3个二级指标（碳减排管理、单位产值碳排放量、碳排放强度）
     - `PCBProductCharacteristics`：4个二级指标（使用无毒无害或低毒低害的生产辅助材料、包装、有害物质限制使用、产品性能）
     - `PCBCleanProductionManagement`：11个二级指标（环保法律法规执行情况、产业政策符合性、清洁生产管理、清洁生产审核、节能管理、污染物排放监测、危险化学品管理、计量器具配备情况、固体废物处理处置、土壤污染隐患排查、运输方式）
     - `PCBResourceReutilization`：8个二级指标（水资源重复利用率、蚀刻液回收率、一般工业固体废物综合利用率、废水收集与处理、废气收集与处理、一般固体废物收集与处理、危险废物收集与处理、噪声）
   - 创建5个Controller（`app/controllers/pcb_audit_options.py`），每个Controller实现：
     - `get_by_enterprise`：获取企业的记录（如果没有则返回空）
     - `upsert`：更新或创建记录（使用`update_or_create`模式，处理camelCase到snake_case的字段名转换）
   - 创建API路由（`app/api/v1/pcb_audit_options.py`）：
     - 每个模块有2个端点：GET（获取）和POST（保存）
     - GET端点：`/api/v1/pcb/enterprise/{enterprise_id}/{module_name}`
     - POST端点：`/api/v1/pcb/enterprise/{enterprise_id}/{module_name}`
     - API层负责字段名的转换（前端camelCase ↔ 后端snake_case）

3. **前端实现**：
   - 修改5个组件（`ProcessEquipmentRequirement.vue`、`GreenhouseGasEmission.vue`、`ProductCharacteristics.vue`、`CleanProductionManagement.vue`、`ResourceReutilization.vue`）：
     - 添加`enterpriseId` prop（必需）
     - 在组件底部添加"提交"按钮
     - 实现`loadData`函数：在`onMounted`和`enterpriseId`变化时调用API获取数据
     - 实现`submitData`函数：将当前选择的数据提交到后端，成功后重新加载数据
     - 添加`loading`状态管理
   - 修改`pre-audit.vue`：
     - 移除5个模块右上角的"暂存"按钮
     - 为5个组件传递`enterprise-id` prop
   - 更新`web/src/api/pcb.js`：添加`pcbAuditOptionsApi`对象，包含5个模块的获取和保存方法

4. **数据格式**：
   - 前端发送的格式（camelCase）：
     ```json
     {
       "basicRequirements": ["level1", "level2", "level3"],
       "mechanicalFacilities": ["level3"],
       "printingProcess": ["none"]
     }
     ```
   - 后端存储的格式（snake_case）：
     ```json
     {
       "basic_requirements": ["level1", "level2", "level3"],
       "mechanical_facilities": ["level3"],
       "printing_process": ["none"]
     }
     ```

**技术实现：**
```python
# Controller中的upsert方法示例（生产工艺与装备要求）
async def upsert(self, enterprise_id: int, data: Dict) -> PCBProcessEquipmentRequirement:
    existing = await self.get_by_enterprise(enterprise_id)
    
    if existing:
        # 更新现有记录（处理camelCase到snake_case的转换）
        await self.model.filter(id=existing.id).update(
            basic_requirements=data.get("basicRequirements") or data.get("basic_requirements"),
            mechanical_facilities=data.get("mechanicalFacilities") or data.get("mechanical_facilities"),
            # ... 其他字段
        )
        return await self.model.get(id=existing.id)
    else:
        # 创建新记录
        return await self.model.create(
            enterprise_id=enterprise_id,
            basic_requirements=data.get("basicRequirements") or data.get("basic_requirements"),
            # ... 其他字段
        )
```

```javascript
// 前端组件示例（ProcessEquipmentRequirement.vue）
const loadData = async () => {
  if (!props.enterpriseId) return
  
  loading.value = true
  try {
    const response = await api.auditOptions.getProcessRequirement(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        basicRequirements: response.data.basicRequirements || [],
        mechanicalFacilities: response.data.mechanicalFacilities || [],
        // ... 其他字段
      })
    }
  } catch (error) {
    message.error('加载数据失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const submitData = async () => {
  loading.value = true
  try {
    await api.auditOptions.saveProcessRequirement(props.enterpriseId, {
      basicRequirements: props.modelValue?.basicRequirements || [],
      mechanicalFacilities: props.modelValue?.mechanicalFacilities || [],
      // ... 其他字段
    })
    message.success('保存成功')
    await loadData() // 重新加载数据
  } catch (error) {
    message.error('保存失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}
```

**修复文件：**
- `app/models/pcb_audit_options.py`：创建5个模型类
- `app/schemas/pcb_audit_options.py`：创建5个模块的Schema（Base、Create、Update、Response）
- `app/controllers/pcb_audit_options.py`：创建5个Controller，实现`get_by_enterprise`和`upsert`方法
- `app/api/v1/pcb_audit_options.py`：创建API路由，包含5个模块的GET和POST端点
- `app/models/__init__.py`：导入新模型
- `app/api/v1/__init__.py`：注册新路由
- `web/src/api/pcb.js`：添加`pcbAuditOptionsApi`对象
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/ProcessEquipmentRequirement.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/GreenhouseGasEmission.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/ProductCharacteristics.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/CleanProductionManagement.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/components/ResourceReutilization.vue`：添加数据加载和提交功能
- `web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue`：移除5个模块的暂存按钮，传递`enterprise-id` prop

**数据库迁移：**
- 迁移脚本：`migrations/create_pcb_audit_options_tables.py`
- 该脚本创建5个新表：
  - `pcb_process_equipment_requirement`
  - `pcb_greenhouse_gas_emission`
  - `pcb_product_characteristics`
  - `pcb_clean_production_management`
  - `pcb_resource_reutilization`
- 每个表使用`enterprise_id`作为唯一索引，二级指标字段使用`TEXT`类型存储JSON字符串

**API端点列表：**
- 生产工艺与装备要求：
  - GET `/api/v1/pcb/enterprise/{enterprise_id}/process-requirement`
  - POST `/api/v1/pcb/enterprise/{enterprise_id}/process-requirement`
- 温室气体排放：
  - GET `/api/v1/pcb/enterprise/{enterprise_id}/greenhouse-gas-emission`
  - POST `/api/v1/pcb/enterprise/{enterprise_id}/greenhouse-gas-emission`
- 产品特征：
  - GET `/api/v1/pcb/enterprise/{enterprise_id}/product-characteristics`
  - POST `/api/v1/pcb/enterprise/{enterprise_id}/product-characteristics`
- 清洁生产管理：
  - GET `/api/v1/pcb/enterprise/{enterprise_id}/clean-production-management`
  - POST `/api/v1/pcb/enterprise/{enterprise_id}/clean-production-management`
- 资源综合利用：
  - GET `/api/v1/pcb/enterprise/{enterprise_id}/resource-reutilization`
  - POST `/api/v1/pcb/enterprise/{enterprise_id}/resource-reutilization`

**效果：**
- 5个模块都可以正常进行数据的保存和读取操作
- 每个模块都有独立的提交按钮，位于模块左下角
- 提交成功后自动刷新数据，确保前端显示与数据库一致
- 字段映射正确，前端camelCase格式与后端snake_case格式正确转换
- 复选框选择逻辑保持不变（层级选择规则、互斥规则等）

**注意事项：**
- 所有模块都采用`upsert`模式（更新或创建），确保每个企业只有一条记录
- Controller中需要同时支持camelCase和snake_case字段名，以确保兼容性
- JSON字段存储的是字符串数组，前端发送和接收的都是数组格式
- 运行迁移脚本后需要重启后端服务器才能生效

---