from typing import List, Dict, Optional
from app.core.crud import CRUDBase
from app.models.raw_material import RawMaterial, EnterpriseRawMaterialUsage
from app.schemas.raw_material import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialInDB
)

class RawMaterialController(CRUDBase[RawMaterial, RawMaterialCreate, RawMaterialUpdate]):
    def __init__(self):
        super().__init__(model=RawMaterial)

    async def get_materials_by_keyword(self, keyword: Optional[str] = None) -> List[RawMaterial]:
        """根据关键词获取材料"""
        if keyword:
            return await self.model.filter(name__icontains=keyword).limit(10).all()
        return await self.model.all()

    async def get_material_by_name(self, name: str) -> Optional[RawMaterial]:
        """根据名称获取材料"""
        return await self.model.filter(name=name).first()

# 创建控制器实例
raw_material_controller = RawMaterialController()
