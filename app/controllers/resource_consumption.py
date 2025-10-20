"""
PCB企业资源能源消耗数据控制器
实现用水、用电、天然气消耗数据的CRUD操作和业务逻辑
"""
from typing import Dict, List, Optional, Any
from decimal import Decimal

from app.core.crud import CRUDBase
from app.models.resource_consumption import (
    PCBWaterConsumptionRecord,
    PCBElectricityConsumptionRecord,
    PCBGasConsumptionRecord,
    PCBResourceConsumptionSummary
)
from app.schemas.resource_consumption import (
    PCBWaterConsumptionRecordCreate,
    PCBWaterConsumptionRecordUpdate,
    PCBElectricityConsumptionRecordCreate,
    PCBElectricityConsumptionRecordUpdate,
    PCBGasConsumptionRecordCreate,
    PCBGasConsumptionRecordUpdate,
    PCBResourceConsumptionSummaryCreate,
    PCBResourceConsumptionSummaryUpdate,
    PCBResourceConsumptionDataRequest,
    PCBResourceConsumptionDataResponse
)


class PCBWaterConsumptionRecordController(CRUDBase[PCBWaterConsumptionRecord, PCBWaterConsumptionRecordCreate, PCBWaterConsumptionRecordUpdate]):
    """用水消耗记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWaterConsumptionRecord]:
        """获取企业的所有用水记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('project')
    


class PCBElectricityConsumptionRecordController(CRUDBase[PCBElectricityConsumptionRecord, PCBElectricityConsumptionRecordCreate, PCBElectricityConsumptionRecordUpdate]):
    """用电消耗记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBElectricityConsumptionRecord]:
        """获取企业的所有用电记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('project')


class PCBGasConsumptionRecordController(CRUDBase[PCBGasConsumptionRecord, PCBGasConsumptionRecordCreate, PCBGasConsumptionRecordUpdate]):
    """天然气消耗记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBGasConsumptionRecord]:
        """获取企业的所有天然气记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('project')
    
    async def get_by_year_range(self, enterprise_id: int, start_year: int, end_year: int) -> List[PCBGasConsumptionRecord]:
        """获取指定年份范围的天然气记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('project')


class PCBResourceConsumptionSummaryController(CRUDBase[PCBResourceConsumptionSummary, PCBResourceConsumptionSummaryCreate, PCBResourceConsumptionSummaryUpdate]):
    """资源能源消耗汇总控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBResourceConsumptionSummary]:
        """获取企业的所有汇总数据"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('year')
    
    async def get_by_year(self, enterprise_id: int, year: int) -> Optional[PCBResourceConsumptionSummary]:
        """获取指定年份的汇总数据"""
        return await self.model.filter(enterprise_id=enterprise_id, year=year).first()
    
    async def calculate_summary(self, enterprise_id: int, year: int) -> PCBResourceConsumptionSummary:
        """计算指定年份的汇总数据"""
        # 获取用水数据
        water_records = await water_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 获取用电数据
        electricity_records = await electricity_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 获取天然气数据
        gas_records = await gas_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 计算用水汇总
        total_water = 0
        production_water = 0
        domestic_water = 0
        
        for record in water_records:
            year_amount = getattr(record, f'amount_{year}', 0) or 0
            total_water += year_amount
            if '生产' in record.project:
                production_water += year_amount
            elif '生活' in record.project:
                domestic_water += year_amount
        
        # 计算用电汇总
        total_electricity = 0
        production_electricity = 0
        auxiliary_electricity = 0
        office_electricity = 0
        
        for record in electricity_records:
            year_amount = getattr(record, f'amount_{year}', 0) or 0
            total_electricity += year_amount
            if '生产车间' in record.project:
                production_electricity += year_amount
            elif '辅助生产' in record.project:
                auxiliary_electricity += year_amount
            elif '办公' in record.project:
                office_electricity += year_amount
        
        # 计算天然气汇总
        total_gas = 0
        production_gas = 0
        domestic_gas = 0
        
        for record in gas_records:
            year_amount = getattr(record, f'amount_{year}', 0) or 0
            total_gas += year_amount
            if '生产' in record.project:
                production_gas += year_amount
            elif '生活' in record.project:
                domestic_gas += year_amount
        
        # 创建或更新汇总记录
        summary_data = {
            'enterprise_id': enterprise_id,
            'year': year,
            'total_water_consumption': total_water,
            'production_water_consumption': production_water,
            'domestic_water_consumption': domestic_water,
            'total_electricity_consumption': total_electricity,
            'production_electricity_consumption': production_electricity,
            'auxiliary_electricity_consumption': auxiliary_electricity,
            'office_electricity_consumption': office_electricity,
            'total_gas_consumption': total_gas,
            'production_gas_consumption': production_gas,
            'domestic_gas_consumption': domestic_gas
        }
        
        existing_summary = await self.get_by_year(enterprise_id, year)
        if existing_summary:
            return await self.update(existing_summary.id, summary_data)
        else:
            return await self.create(summary_data)


class PCBResourceConsumptionDataController:
    """资源能源消耗数据控制器"""
    
    def __init__(self):
        self.water_record_controller = PCBWaterConsumptionRecordController(PCBWaterConsumptionRecord)
        self.electricity_controller = PCBElectricityConsumptionRecordController(PCBElectricityConsumptionRecord)
        self.gas_controller = PCBGasConsumptionRecordController(PCBGasConsumptionRecord)
        self.summary_controller = PCBResourceConsumptionSummaryController(PCBResourceConsumptionSummary)
    
    async def get_all_data(self, enterprise_id: int) -> Dict[str, Any]:
        """获取企业的所有资源能源消耗数据"""
        # 获取用水数据
        water_records = await self.water_record_controller.get_by_enterprise(enterprise_id)
        
        # 获取用电数据
        electricity_records = await self.electricity_controller.get_by_enterprise(enterprise_id)
        
        # 获取天然气数据
        gas_records = await self.gas_controller.get_by_enterprise(enterprise_id)
        
        # 获取最新年份的汇总数据
        summaries = await self.summary_controller.get_by_enterprise(enterprise_id)
        latest_summary = summaries[-1] if summaries else None
        
        # 转换为字典列表
        water_data = [await record.to_dict() for record in water_records]
        electricity_data = [await record.to_dict() for record in electricity_records]
        gas_data = [await record.to_dict() for record in gas_records]
        summary_data = await latest_summary.to_dict() if latest_summary else None
        
        return {
            "water_records": water_data,
            "electricity_records": electricity_data,
            "gas_records": gas_data,
            "summary": summary_data
        }
    
    async def save_all_data(self, enterprise_id: int, data: PCBResourceConsumptionDataRequest) -> Dict[str, Any]:
        """保存企业的所有资源能源消耗数据"""
        try:
            # 保存用水记录
            saved_water_records = []
            for record_data in data.water.records:
                record_data.enterprise_id = enterprise_id
                record = await self.water_record_controller.create(record_data)
                saved_water_records.append(record)
            
            # 保存用电记录
            saved_electricity_records = []
            for record_data in data.electricity.records:
                record_data.enterprise_id = enterprise_id
                record = await self.electricity_controller.create(record_data)
                saved_electricity_records.append(record)
            
            # 保存天然气记录
            saved_gas_records = []
            for record_data in data.gas.records:
                record_data.enterprise_id = enterprise_id
                record = await self.gas_controller.create(record_data)
                saved_gas_records.append(record)
            
            # 计算汇总数据
            current_year = 2023  # 可以根据需要调整
            summary = await self.summary_controller.calculate_summary(enterprise_id, current_year)
            
            return {
                'success': True,
                'message': '数据保存成功',
                'data': {
                    'water_records': len(saved_water_records),
                    'electricity_records': len(saved_electricity_records),
                    'gas_records': len(saved_gas_records),
                    'summary_id': summary.id if summary else None
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'数据保存失败: {str(e)}',
                'data': None
            }
    
    async def delete_all_data(self, enterprise_id: int) -> bool:
        """删除企业的所有资源能源消耗数据"""
        try:
            # 删除用水记录
            await PCBWaterConsumptionRecord.filter(enterprise_id=enterprise_id).delete()
            
            # 删除用水分类
            await PCBWaterConsumptionCategory.filter(enterprise_id=enterprise_id).delete()
            
            # 删除用电记录
            await PCBElectricityConsumptionRecord.filter(enterprise_id=enterprise_id).delete()
            
            # 删除天然气记录
            await PCBGasConsumptionRecord.filter(enterprise_id=enterprise_id).delete()
            
            # 删除汇总数据
            await PCBResourceConsumptionSummary.filter(enterprise_id=enterprise_id).delete()
            
            return True
        except Exception as e:
            print(f"删除数据失败: {str(e)}")
            return False


# 创建控制器实例
water_consumption_record_controller = PCBWaterConsumptionRecordController(PCBWaterConsumptionRecord)
electricity_consumption_record_controller = PCBElectricityConsumptionRecordController(PCBElectricityConsumptionRecord)
gas_consumption_record_controller = PCBGasConsumptionRecordController(PCBGasConsumptionRecord)
resource_consumption_summary_controller = PCBResourceConsumptionSummaryController(PCBResourceConsumptionSummary)
resource_consumption_data_controller = PCBResourceConsumptionDataController()
