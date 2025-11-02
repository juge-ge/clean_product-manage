"""
PCB企业工艺装备数据控制器
"""
from typing import List, Dict, Any
from app.core.crud import CRUDBase
from app.models.process_equipment import PCBEquipmentRecord, PCBEquipmentCategory
from app.schemas.process_equipment import (
    PCBEquipmentRecordCreate,
    PCBEquipmentRecordUpdate,
    PCBEquipmentCategoryCreate,
    PCBEquipmentCategoryUpdate,
    PCBEquipmentDataRequest,
    PCBEquipmentDataResponse
)


class PCBEquipmentRecordController(CRUDBase[PCBEquipmentRecord, PCBEquipmentRecordCreate, PCBEquipmentRecordUpdate]):
    """设备记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBEquipmentRecord]:
        """获取企业的所有设备记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('equipment_name')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBEquipmentRecord]:
        """批量更新或插入设备记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有设备记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 转换前端camelCase字段名为后端snake_case，允许空值
            record_data = {
                "enterprise_id": enterprise_id,
                "equipment_name": item.get("equipmentName") or item.get("equipment_name") or "",
                "equipment_model": item.get("equipmentModel") or item.get("equipment_model") or "",
                "motor_model": item.get("motorModel") or item.get("motor_model") or "",
                "power": item.get("power"),
                "quantity": item.get("quantity", 1),
                "process": item.get("process") or "",
                "status": item.get("status") or "良好",
                "remark": item.get("remark")
            }
            
            # 移除必填字段验证，允许空字段提交
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBEquipmentCategoryController(CRUDBase[PCBEquipmentCategory, PCBEquipmentCategoryCreate, PCBEquipmentCategoryUpdate]):
    """设备分类控制器"""
    
    async def get_all_categories(self) -> List[PCBEquipmentCategory]:
        """获取所有设备分类"""
        return await self.model.all().order_by('sort_order')


class PCBEquipmentDataController:
    """设备数据控制器"""
    
    def __init__(self):
        self.equipment_controller = PCBEquipmentRecordController(PCBEquipmentRecord)
        self.category_controller = PCBEquipmentCategoryController(PCBEquipmentCategory)
    
    async def get_all_data(self, enterprise_id: int) -> List[Dict[str, Any]]:
        """获取企业的所有设备数据，返回前端camelCase格式"""
        equipment_records = await self.equipment_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表，使用camelCase字段名
        equipment_data = []
        for record in equipment_records:
            equipment_data.append({
                "id": record.id,
                "equipmentName": record.equipment_name,
                "equipmentModel": record.equipment_model,
                "motorModel": record.motor_model,
                "power": float(record.power) if record.power else None,
                "quantity": record.quantity,
                "process": record.process,
                "status": record.status,
                "remark": record.remark
            })
        
        return equipment_data
    
    async def save_all_data(self, enterprise_id: int, items: List[Dict]) -> int:
        """保存企业的所有设备数据，使用批量upsert"""
        results = await self.equipment_controller.batch_upsert(enterprise_id, items)
        return len(results)
    
    async def delete_all_data(self, enterprise_id: int) -> bool:
        """删除企业的所有设备数据"""
        try:
            await PCBEquipmentRecord.filter(enterprise_id=enterprise_id).delete()
            return True
        except Exception as e:
            print(f"删除设备数据失败: {str(e)}")
            return False


# 创建控制器实例
equipment_record_controller = PCBEquipmentRecordController(PCBEquipmentRecord)
equipment_category_controller = PCBEquipmentCategoryController(PCBEquipmentCategory)
equipment_data_controller = PCBEquipmentDataController()
