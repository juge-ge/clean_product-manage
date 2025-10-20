"""
PCB企业污染防治数据控制器
"""
from typing import List, Dict, Any
from app.core.crud import CRUDBase
from app.models.pollution_control import PCBWastewaterAnalysis, PCBWasteGasAnalysis
from app.schemas.pollution_control import (
    PCBWastewaterAnalysisCreate,
    PCBWastewaterAnalysisUpdate,
    PCBWasteGasAnalysisCreate,
    PCBWasteGasAnalysisUpdate,
    PCBPollutionControlDataRequest,
    PCBPollutionControlDataResponse
)


class PCBWastewaterAnalysisController(CRUDBase[PCBWastewaterAnalysis, PCBWastewaterAnalysisCreate, PCBWastewaterAnalysisUpdate]):
    """废水产生分析控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterAnalysis]:
        """获取企业的所有废水分析记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('category')


class PCBWasteGasAnalysisController(CRUDBase[PCBWasteGasAnalysis, PCBWasteGasAnalysisCreate, PCBWasteGasAnalysisUpdate]):
    """废气产生情况控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWasteGasAnalysis]:
        """获取企业的所有废气分析记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('gas_type')


class PCBPollutionControlDataController:
    """污染防治数据控制器"""
    
    def __init__(self):
        self.wastewater_controller = PCBWastewaterAnalysisController(PCBWastewaterAnalysis)
        self.waste_gas_controller = PCBWasteGasAnalysisController(PCBWasteGasAnalysis)
    
    async def get_all_data(self, enterprise_id: int) -> Dict[str, Any]:
        """获取企业的所有污染防治数据"""
        wastewater_records = await self.wastewater_controller.get_by_enterprise(enterprise_id)
        waste_gas_records = await self.waste_gas_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        wastewater_data = [await record.to_dict() for record in wastewater_records]
        waste_gas_data = [await record.to_dict() for record in waste_gas_records]
        
        return {
            "wastewater": wastewater_data,
            "wasteGas": waste_gas_data
        }
    
    async def save_all_data(self, enterprise_id: int, data: PCBPollutionControlDataRequest) -> Dict[str, Any]:
        """保存企业的所有污染防治数据"""
        try:
            # 保存废水分析记录
            saved_wastewater = []
            for wastewater_data in data.wastewater.wastewater:
                wastewater_data.enterprise_id = enterprise_id
                wastewater = await self.wastewater_controller.create(wastewater_data)
                saved_wastewater.append(wastewater)
            
            # 保存废气分析记录
            saved_waste_gas = []
            for waste_gas_data in data.wasteGas.wasteGas:
                waste_gas_data.enterprise_id = enterprise_id
                waste_gas = await self.waste_gas_controller.create(waste_gas_data)
                saved_waste_gas.append(waste_gas)
            
            return {
                'success': True,
                'message': '污染防治数据保存成功',
                'data': {
                    'wastewater_count': len(saved_wastewater),
                    'waste_gas_count': len(saved_waste_gas)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'污染防治数据保存失败: {str(e)}',
                'data': None
            }
    
    async def delete_all_data(self, enterprise_id: int) -> bool:
        """删除企业的所有污染防治数据"""
        try:
            await PCBWastewaterAnalysis.filter(enterprise_id=enterprise_id).delete()
            await PCBWasteGasAnalysis.filter(enterprise_id=enterprise_id).delete()
            return True
        except Exception as e:
            print(f"删除污染防治数据失败: {str(e)}")
            return False


# 创建控制器实例
wastewater_analysis_controller = PCBWastewaterAnalysisController(PCBWastewaterAnalysis)
waste_gas_analysis_controller = PCBWasteGasAnalysisController(PCBWasteGasAnalysis)
pollution_control_data_controller = PCBPollutionControlDataController()
