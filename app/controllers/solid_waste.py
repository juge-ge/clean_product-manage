"""
PCB企业固体废物管理数据控制器
"""
from typing import List, Dict, Any
from app.core.crud import CRUDBase
from app.models.solid_waste import PCBSolidWasteRecord, PCBSolidWasteCategory
from app.schemas.solid_waste import (
    PCBSolidWasteRecordCreate,
    PCBSolidWasteRecordUpdate,
    PCBSolidWasteCategoryCreate,
    PCBSolidWasteCategoryUpdate,
    PCBSolidWasteDataRequest,
    PCBSolidWasteDataResponse
)


class PCBSolidWasteRecordController(CRUDBase[PCBSolidWasteRecord, PCBSolidWasteRecordCreate, PCBSolidWasteRecordUpdate]):
    """固体废物记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBSolidWasteRecord]:
        """获取企业的所有固体废物记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('category', 'name')


class PCBSolidWasteCategoryController(CRUDBase[PCBSolidWasteCategory, PCBSolidWasteCategoryCreate, PCBSolidWasteCategoryUpdate]):
    """固体废物分类控制器"""
    
    async def get_all_categories(self) -> List[PCBSolidWasteCategory]:
        """获取所有固体废物分类"""
        return await self.model.all().order_by('sort_order')


class PCBSolidWasteDataController:
    """固体废物数据控制器"""
    
    def __init__(self):
        self.waste_record_controller = PCBSolidWasteRecordController(PCBSolidWasteRecord)
        self.category_controller = PCBSolidWasteCategoryController(PCBSolidWasteCategory)
    
    async def get_all_data(self, enterprise_id: int) -> Dict[str, Any]:
        """获取企业的所有固体废物数据"""
        waste_records = await self.waste_record_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        waste_data = [await record.to_dict() for record in waste_records]
        
        return {
            "waste": waste_data
        }
    
    async def save_all_data(self, enterprise_id: int, data: PCBSolidWasteDataRequest) -> Dict[str, Any]:
        """保存企业的所有固体废物数据"""
        try:
            # 保存固体废物记录
            saved_waste = []
            for waste_data in data.waste:
                waste_data.enterprise_id = enterprise_id
                waste = await self.waste_record_controller.create(waste_data)
                saved_waste.append(waste)
            
            return {
                'success': True,
                'message': '固体废物数据保存成功',
                'data': {
                    'waste_count': len(saved_waste)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'固体废物数据保存失败: {str(e)}',
                'data': None
            }
    
    async def delete_all_data(self, enterprise_id: int) -> bool:
        """删除企业的所有固体废物数据"""
        try:
            await PCBSolidWasteRecord.filter(enterprise_id=enterprise_id).delete()
            return True
        except Exception as e:
            print(f"删除固体废物数据失败: {str(e)}")
            return False


# 创建控制器实例
solid_waste_record_controller = PCBSolidWasteRecordController(PCBSolidWasteRecord)
solid_waste_category_controller = PCBSolidWasteCategoryController(PCBSolidWasteCategory)
solid_waste_data_controller = PCBSolidWasteDataController()
