"""
PCB企业自行监测数据控制器
"""
from typing import List, Dict, Any
from app.core.crud import CRUDBase
from app.models.self_monitoring import (
    PCBOrganizedGasMonitoring,
    PCBUnorganizedGasMonitoring,
    PCBWastewaterMonitoring,
    PCBGasEmissionMonitoring,
    PCBNoiseMonitoring
)
from app.schemas.self_monitoring import (
    PCBOrganizedGasMonitoringCreate,
    PCBOrganizedGasMonitoringUpdate,
    PCBUnorganizedGasMonitoringCreate,
    PCBUnorganizedGasMonitoringUpdate,
    PCBWastewaterMonitoringCreate,
    PCBWastewaterMonitoringUpdate,
    PCBGasEmissionMonitoringCreate,
    PCBGasEmissionMonitoringUpdate,
    PCBNoiseMonitoringCreate,
    PCBNoiseMonitoringUpdate,
    PCBSelfMonitoringDataRequest,
    PCBSelfMonitoringDataResponse
)


class PCBOrganizedGasMonitoringController(CRUDBase[PCBOrganizedGasMonitoring, PCBOrganizedGasMonitoringCreate, PCBOrganizedGasMonitoringUpdate]):
    """有组织废气检测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBOrganizedGasMonitoring]:
        """获取企业的所有有组织废气检测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('monitoring_point')


class PCBUnorganizedGasMonitoringController(CRUDBase[PCBUnorganizedGasMonitoring, PCBUnorganizedGasMonitoringCreate, PCBUnorganizedGasMonitoringUpdate]):
    """无组织废气检测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBUnorganizedGasMonitoring]:
        """获取企业的所有无组织废气检测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('sampling_point')


class PCBWastewaterMonitoringController(CRUDBase[PCBWastewaterMonitoring, PCBWastewaterMonitoringCreate, PCBWastewaterMonitoringUpdate]):
    """废水监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterMonitoring]:
        """获取企业的所有废水监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('sampling_date')


class PCBGasEmissionMonitoringController(CRUDBase[PCBGasEmissionMonitoring, PCBGasEmissionMonitoringCreate, PCBGasEmissionMonitoringUpdate]):
    """废气排放监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBGasEmissionMonitoring]:
        """获取企业的所有废气排放监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('detection_point')


class PCBNoiseMonitoringController(CRUDBase[PCBNoiseMonitoring, PCBNoiseMonitoringCreate, PCBNoiseMonitoringUpdate]):
    """噪声监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBNoiseMonitoring]:
        """获取企业的所有噪声监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('monitoring_point')


class PCBSelfMonitoringDataController:
    """自行监测数据控制器"""
    
    def __init__(self):
        self.organized_gas_controller = PCBOrganizedGasMonitoringController(PCBOrganizedGasMonitoring)
        self.unorganized_gas_controller = PCBUnorganizedGasMonitoringController(PCBUnorganizedGasMonitoring)
        self.wastewater_controller = PCBWastewaterMonitoringController(PCBWastewaterMonitoring)
        self.gas_emission_controller = PCBGasEmissionMonitoringController(PCBGasEmissionMonitoring)
        self.noise_controller = PCBNoiseMonitoringController(PCBNoiseMonitoring)
    
    async def get_all_data(self, enterprise_id: int) -> Dict[str, Any]:
        """获取企业的所有自行监测数据"""
        organized_gas_records = await self.organized_gas_controller.get_by_enterprise(enterprise_id)
        unorganized_gas_records = await self.unorganized_gas_controller.get_by_enterprise(enterprise_id)
        wastewater_records = await self.wastewater_controller.get_by_enterprise(enterprise_id)
        gas_emission_records = await self.gas_emission_controller.get_by_enterprise(enterprise_id)
        noise_records = await self.noise_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        organized_gas_data = [await record.to_dict() for record in organized_gas_records]
        unorganized_gas_data = [await record.to_dict() for record in unorganized_gas_records]
        wastewater_data = [await record.to_dict() for record in wastewater_records]
        gas_emission_data = [await record.to_dict() for record in gas_emission_records]
        noise_data = [await record.to_dict() for record in noise_records]
        
        return {
            "organizedGas": organized_gas_data,
            "unorganizedGas": unorganized_gas_data,
            "wastewater": wastewater_data,
            "gasEmission": gas_emission_data,
            "noise": noise_data
        }
    
    async def save_all_data(self, enterprise_id: int, data: PCBSelfMonitoringDataRequest) -> Dict[str, Any]:
        """保存企业的所有自行监测数据"""
        try:
            # 保存有组织废气检测记录
            saved_organized_gas = []
            for gas_data in data.organizedGas:
                gas_data.enterprise_id = enterprise_id
                gas = await self.organized_gas_controller.create(gas_data)
                saved_organized_gas.append(gas)
            
            # 保存无组织废气检测记录
            saved_unorganized_gas = []
            for gas_data in data.unorganizedGas:
                gas_data.enterprise_id = enterprise_id
                gas = await self.unorganized_gas_controller.create(gas_data)
                saved_unorganized_gas.append(gas)
            
            # 保存废水监测记录
            saved_wastewater = []
            for water_data in data.wastewater:
                water_data.enterprise_id = enterprise_id
                water = await self.wastewater_controller.create(water_data)
                saved_wastewater.append(water)
            
            # 保存废气排放监测记录
            saved_gas_emission = []
            for emission_data in data.gasEmission:
                emission_data.enterprise_id = enterprise_id
                emission = await self.gas_emission_controller.create(emission_data)
                saved_gas_emission.append(emission)
            
            # 保存噪声监测记录
            saved_noise = []
            for noise_data in data.noise:
                noise_data.enterprise_id = enterprise_id
                noise = await self.noise_controller.create(noise_data)
                saved_noise.append(noise)
            
            return {
                'success': True,
                'message': '自行监测数据保存成功',
                'data': {
                    'organized_gas_count': len(saved_organized_gas),
                    'unorganized_gas_count': len(saved_unorganized_gas),
                    'wastewater_count': len(saved_wastewater),
                    'gas_emission_count': len(saved_gas_emission),
                    'noise_count': len(saved_noise)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'自行监测数据保存失败: {str(e)}',
                'data': None
            }
    
    async def delete_all_data(self, enterprise_id: int) -> bool:
        """删除企业的所有自行监测数据"""
        try:
            await PCBOrganizedGasMonitoring.filter(enterprise_id=enterprise_id).delete()
            await PCBUnorganizedGasMonitoring.filter(enterprise_id=enterprise_id).delete()
            await PCBWastewaterMonitoring.filter(enterprise_id=enterprise_id).delete()
            await PCBGasEmissionMonitoring.filter(enterprise_id=enterprise_id).delete()
            await PCBNoiseMonitoring.filter(enterprise_id=enterprise_id).delete()
            return True
        except Exception as e:
            print(f"删除自行监测数据失败: {str(e)}")
            return False


# 创建控制器实例
organized_gas_monitoring_controller = PCBOrganizedGasMonitoringController(PCBOrganizedGasMonitoring)
unorganized_gas_monitoring_controller = PCBUnorganizedGasMonitoringController(PCBUnorganizedGasMonitoring)
wastewater_monitoring_controller = PCBWastewaterMonitoringController(PCBWastewaterMonitoring)
gas_emission_monitoring_controller = PCBGasEmissionMonitoringController(PCBGasEmissionMonitoring)
noise_monitoring_controller = PCBNoiseMonitoringController(PCBNoiseMonitoring)
self_monitoring_data_controller = PCBSelfMonitoringDataController()
