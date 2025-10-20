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
    
    async def get_all_data(self, enterprise_id: int) -> Dict[str, Any]:
        """获取企业的所有设备数据"""
        equipment_records = await self.equipment_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        equipment_data = [await record.to_dict() for record in equipment_records]
        
        return {
            "equipment": equipment_data
        }
    
    async def save_all_data(self, enterprise_id: int, data: PCBEquipmentDataRequest) -> Dict[str, Any]:
        """保存企业的所有设备数据"""
        try:
            # 保存设备记录
            saved_equipment = []
            for equipment_data in data.equipment:
                equipment_data.enterprise_id = enterprise_id
                equipment = await self.equipment_controller.create(equipment_data)
                saved_equipment.append(equipment)
            
            return {
                'success': True,
                'message': '设备数据保存成功',
                'data': {
                    'equipment_count': len(saved_equipment)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'设备数据保存失败: {str(e)}',
                'data': None
            }
    
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
