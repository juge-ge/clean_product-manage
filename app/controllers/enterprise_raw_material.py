from typing import List, Optional, Dict, Any
from app.core.crud import CRUDBase
from app.models.raw_material import EnterpriseRawMaterialUsage, RawMaterial
from app.schemas.raw_material import EnterpriseRawMaterialUsageCreate, EnterpriseRawMaterialUsageUpdate
from tortoise.expressions import Q

class EnterpriseRawMaterialController(CRUDBase[EnterpriseRawMaterialUsage, EnterpriseRawMaterialUsageCreate, EnterpriseRawMaterialUsageUpdate]):
    """企业原辅材料使用情况控制器"""
    
    def __init__(self):
        super().__init__(model=EnterpriseRawMaterialUsage)
    
    async def get_by_enterprise(self, enterprise_id: int, year: Optional[str] = None) -> List[EnterpriseRawMaterialUsage]:
        """获取企业的原辅材料使用情况"""
        query = Q(enterprise_id=enterprise_id)
        if year:
            query &= Q(year=year)
        
        usages = await self.model.filter(query).prefetch_related('material_info').all()
        return usages
    
    async def get_by_enterprise_and_year(self, enterprise_id: int, year: str) -> List[EnterpriseRawMaterialUsage]:
        """获取企业指定年份的原辅材料使用情况"""
        usages = await self.model.filter(
            enterprise_id=enterprise_id,
            year=year
        ).prefetch_related('material_info').all()
        return usages
    
    async def save_usage_data(self, enterprise_id: int, year: str, usage_data: List[Dict[str, Any]]) -> List[EnterpriseRawMaterialUsage]:
        """保存企业原辅材料使用数据"""
        # 先删除该企业该年份的现有数据
        await self.model.filter(
            enterprise_id=enterprise_id,
            year=year
        ).delete()
        
        # 批量创建新数据
        usage_list = []
        for data in usage_data:
            # 查找材料ID
            material = await RawMaterial.filter(name=data.get('name')).first()
            if not material:
                continue  # 跳过不存在的材料
            
            usage = await self.model.create(
                enterprise_id=enterprise_id,
                material_id=material.id,
                year=year,
                amount=data.get('amount'),
                unit=data.get('unit'),
                process=data.get('process'),
                state=data.get('state'),
                voc_content=data.get('voc_content')
            )
            usage_list.append(usage)
        
        return usage_list
    
    async def update_usage_data(self, enterprise_id: int, year: str, usage_data: List[Dict[str, Any]]) -> List[EnterpriseRawMaterialUsage]:
        """更新企业原辅材料使用数据"""
        return await self.save_usage_data(enterprise_id, year, usage_data)
    
    async def get_usage_statistics(self, enterprise_id: int, year: Optional[str] = None) -> Dict[str, Any]:
        """获取企业原辅材料使用统计"""
        usages = await self.get_by_enterprise(enterprise_id, year)
        
        total_materials = len(usages)
        completed_materials = len([u for u in usages if u.amount is not None and u.amount > 0])
        
        # 按工序统计
        process_stats = {}
        for usage in usages:
            if usage.process:
                if usage.process not in process_stats:
                    process_stats[usage.process] = 0
                process_stats[usage.process] += 1
        
        return {
            "total_materials": total_materials,
            "completed_materials": completed_materials,
            "completion_rate": (completed_materials / total_materials * 100) if total_materials > 0 else 0,
            "process_statistics": process_stats
        }

# 创建控制器实例
enterprise_raw_material_controller = EnterpriseRawMaterialController()
