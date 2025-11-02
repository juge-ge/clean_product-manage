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
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBOrganizedGasMonitoring]:
        """批量更新或插入有组织废气检测记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有有组织废气检测记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 定义辅助函数，安全地获取值（支持ND字符串或数字）
            def get_string_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                # 如果是ND字符串，直接返回
                if str(value).upper() == 'ND':
                    return 'ND'
                # 如果是数字，转换为字符串（保留原格式）
                try:
                    # 尝试转换为数字并保留精度
                    num_value = float(value)
                    # 如果是整数，返回整数字符串；否则返回原字符串格式
                    if num_value == int(num_value):
                        return str(int(num_value))
                    else:
                        return str(value).strip()
                except (ValueError, TypeError):
                    # 如果不是数字也不是ND，返回原值（字符串）
                    return str(value).strip()
            
            record_data = {
                "enterprise_id": enterprise_id,
                "monitoring_point": item.get("monitoringPoint") or item.get("monitoring_point") or "",
                "monitoring_time": item.get("monitoringTime") or item.get("monitoring_time") or "",
                "nitrogen_oxides": get_string_value("result_氮氧化物"),
                "hydrogen_chloride": get_string_value("result_氯化氢"),
                "hydrogen_cyanide": get_string_value("result_氰化氢"),
                "sulfuric_acid_mist": get_string_value("result_硫酸雾"),
                "chromic_acid_mist": get_string_value("result_铬酸雾"),
                "fluoride": get_string_value("result_氟化物"),
                "phenol": get_string_value("result_酚类"),
                "non_methane_hydrocarbons": get_string_value("result_非甲烷总烃"),
                "benzene": get_string_value("result_苯"),
                "toluene": get_string_value("result_甲苯"),
                "xylene": get_string_value("result_二甲苯"),
                "toluene_xylene_total": get_string_value("result_甲苯与二甲苯合计"),
                "vocs": get_string_value("result_VOCs"),
            }
            
            # 验证必填字段
            if not record_data["monitoring_point"] or not record_data["monitoring_time"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBUnorganizedGasMonitoringController(CRUDBase[PCBUnorganizedGasMonitoring, PCBUnorganizedGasMonitoringCreate, PCBUnorganizedGasMonitoringUpdate]):
    """无组织废气检测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBUnorganizedGasMonitoring]:
        """获取企业的所有无组织废气检测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('sampling_point')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBUnorganizedGasMonitoring]:
        """批量更新或插入无组织废气检测记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有无组织废气检测记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        from decimal import Decimal
        for item in items:
            # 定义辅助函数，安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            # 定义辅助函数，获取字符串值（支持ND）
            def get_string_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                # 如果是ND字符串，直接返回
                if str(value).upper() == 'ND':
                    return 'ND'
                # 如果是数字，转换为字符串（保留原格式）
                try:
                    num_value = float(value)
                    if num_value == int(num_value):
                        return str(int(num_value))
                    else:
                        return str(value).strip()
                except (ValueError, TypeError):
                    return str(value).strip()
            
            record_data = {
                "enterprise_id": enterprise_id,
                "sampling_time": item.get("samplingTime") or item.get("sampling_time") or "",
                "sampling_point": item.get("samplingPoint") or item.get("sampling_point") or "",
                "monitoring_factor": item.get("monitoringFactor") or item.get("monitoring_factor") or "",
                "emission_concentration": get_string_value("emissionConcentration"),
                "emission_limit": get_decimal_value("emissionLimit"),
                "compliance": item.get("compliance") or "",
            }
            
            # 验证必填字段
            if not record_data["sampling_time"] or not record_data["sampling_point"] or not record_data["monitoring_factor"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBWastewaterMonitoringController(CRUDBase[PCBWastewaterMonitoring, PCBWastewaterMonitoringCreate, PCBWastewaterMonitoringUpdate]):
    """废水监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterMonitoring]:
        """获取企业的所有废水监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('sampling_date')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterMonitoring]:
        """批量更新或插入废水监测记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水监测记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        from decimal import Decimal
        for item in items:
            # 定义辅助函数，安全地获取并转换值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "sampling_date": item.get("monitoringTime") or item.get("sampling_date") or "",
                "monitoring_point": item.get("monitoringPoint") or item.get("monitoring_point") or "",
                "ph": get_decimal_value("result_pH"),
                "cod": get_decimal_value("result_COD"),
                "ammonia_nitrogen": get_decimal_value("result_氨氮"),
                "total_nitrogen": get_decimal_value("result_总氮"),
                "total_phosphorus": get_decimal_value("result_总磷"),
                "total_copper": get_decimal_value("result_铜"),
                "nickel": get_decimal_value("result_镍"),
                "total_cyanide": get_decimal_value("result_总氰化物"),
                "nickel_outlet": get_decimal_value("result_镍（镍排口）"),
            }
            
            # 验证必填字段
            if not record_data["sampling_date"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBGasEmissionMonitoringController(CRUDBase[PCBGasEmissionMonitoring, PCBGasEmissionMonitoringCreate, PCBGasEmissionMonitoringUpdate]):
    """废气排放监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBGasEmissionMonitoring]:
        """获取企业的所有废气排放监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('detection_point')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBGasEmissionMonitoring]:
        """批量更新或插入废气排放监测记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废气排放监测记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        from decimal import Decimal
        for item in items:
            # 定义辅助函数，安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            # 定义辅助函数，获取字符串值（不限制用户输入内容，直接接受任意字符串）
            def get_string_value(key):
                value = item.get(key)
                if value is None:
                    return None
                # 直接转换为字符串，不做任何类型判断或转换，允许用户输入任意内容
                return str(value).strip() if str(value).strip() else None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "detection_point": item.get("detectionPoint") or item.get("detection_point") or "",
                "detection_item": item.get("detectionItem") or item.get("detection_item") or "",
                "emission_rate": get_decimal_value("emissionRate"),
                "benchmark_flow": get_decimal_value("benchmarkFlow"),
                "detection_result": get_string_value("detectionResult"),
                "permitted_emission_limit": get_decimal_value("permittedEmissionLimit"),
                "stack_height": get_decimal_value("stackHeight"),
            }
            
            # 验证必填字段
            if not record_data["detection_point"] or not record_data["detection_item"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBNoiseMonitoringController(CRUDBase[PCBNoiseMonitoring, PCBNoiseMonitoringCreate, PCBNoiseMonitoringUpdate]):
    """噪声监测控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBNoiseMonitoring]:
        """获取企业的所有噪声监测记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('monitoring_point')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBNoiseMonitoring]:
        """批量更新或插入噪声监测记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有噪声监测记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        from decimal import Decimal
        for item in items:
            # 定义辅助函数，安全地获取并转换值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "monitoring_time": item.get("monitoringTime") or item.get("monitoring_time") or "",
                "monitoring_point": item.get("monitoringPoint") or item.get("monitoring_point") or "",
                "daytime_result": get_decimal_value("daytimeResult"),
                "nighttime_result": get_decimal_value("nighttimeResult"),
                "daytime_standard": get_decimal_value("daytimeStandard"),
                "nighttime_standard": get_decimal_value("nighttimeStandard"),
            }
            
            # 验证必填字段
            if not record_data["monitoring_time"] or not record_data["monitoring_point"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


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
