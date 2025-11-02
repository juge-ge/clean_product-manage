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
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBSolidWasteRecord]:
        """批量更新或插入固体废物记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有固体废物记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        from decimal import Decimal
        for item in items:
            # 构建记录数据
            record_data = {
                "enterprise_id": enterprise_id,
                "category": item.get("category") or "",
                "name": item.get("name") or "",
                "unit": item.get("unit") or "",
                "disposal_method": item.get("disposal_method")
            }
            
            # 添加年份数据
            for year in range(2020, 2025):
                year_key = f"amount_{year}"
                if year_key in item:
                    value = item[year_key]
                    # 确保0值被正确处理
                    if value is None or value == "":
                        record_data[year_key] = None
                    else:
                        record_data[year_key] = Decimal(str(value))
            
            # 验证必填字段
            if not record_data["category"] or not record_data["name"] or not record_data["unit"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


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
