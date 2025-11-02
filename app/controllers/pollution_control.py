"""
PCB企业污染防治数据控制器
"""
from typing import List, Dict, Any
from decimal import Decimal
from app.core.crud import CRUDBase
from app.models.pollution_control import PCBWastewaterAnalysis, PCBWasteGasAnalysis, PCBWastewaterStatRecord
from app.schemas.pollution_control import (
    PCBWastewaterAnalysisCreate,
    PCBWastewaterAnalysisUpdate,
    PCBWasteGasAnalysisCreate,
    PCBWasteGasAnalysisUpdate,
    PCBWastewaterStatRecordCreate,
    PCBWastewaterStatRecordUpdate,
    PCBPollutionControlDataRequest,
    PCBPollutionControlDataResponse
)


class PCBWastewaterAnalysisController(CRUDBase[PCBWastewaterAnalysis, PCBWastewaterAnalysisCreate, PCBWastewaterAnalysisUpdate]):
    """废水产生分析控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterAnalysis]:
        """获取企业的所有废水分析记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('category')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterAnalysis]:
        """批量更新或插入废水分析记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水分析记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for idx, item in enumerate(items):
            try:
                # 安全地获取字段值，数据库和Schema都有默认值，所以可以安全处理
                def safe_str(value):
                    """安全地将值转换为字符串，None或空值返回空字符串"""
                    if value is None:
                        return ""
                    return str(value).strip()
                
                record_data = {
                    "enterprise_id": enterprise_id,
                    "category": safe_str(item.get("category")),
                    "source": safe_str(item.get("source")),
                    "pollutants": safe_str(item.get("pollutants")),
                    "disposal": safe_str(item.get("disposal"))
                }
                
                # 验证必填字段
                if not record_data["category"]:
                    print(f"[WARN] 跳过第 {idx+1} 条记录：category为空")
                    continue
                
                print(f"[DEBUG] 创建废水分析记录 {idx+1}: {record_data}")
                new_record = await self.model.create(**record_data)
                results.append(new_record)
            except Exception as e:
                print(f"[ERROR] 创建废水分析记录 {idx+1} 失败: {str(e)}")
                print(f"[ERROR] 原始数据: {item}")
                import traceback
                traceback.print_exc()
                # 不抛出异常，继续处理下一条记录，但记录错误
                # 如果所有记录都失败，results为空列表，调用方可以检查
                continue
        
        # 如果所有记录都失败了，抛出异常
        if not results and items:
            raise ValueError("所有废水分析记录创建失败，请检查数据格式和必填字段")
        
        return results


class PCBWasteGasAnalysisController(CRUDBase[PCBWasteGasAnalysis, PCBWasteGasAnalysisCreate, PCBWasteGasAnalysisUpdate]):
    """废气产生情况控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWasteGasAnalysis]:
        """获取企业的所有废气分析记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('gas_type')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWasteGasAnalysis]:
        """批量更新或插入废气分析记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废气分析记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for idx, item in enumerate(items):
            try:
                # 安全地获取字段值，数据库和Schema都有默认值，所以可以安全处理
                def safe_str(value):
                    """安全地将值转换为字符串，None或空值返回空字符串"""
                    if value is None:
                        return ""
                    return str(value).strip()
                
                record_data = {
                    "enterprise_id": enterprise_id,
                    "gas_type": safe_str(item.get("type")),
                    "pollutants": safe_str(item.get("pollutants")),
                    "location": safe_str(item.get("location")),
                    "treatment": safe_str(item.get("treatment"))
                }
                
                # 验证必填字段
                if not record_data["gas_type"]:
                    print(f"[WARN] 跳过第 {idx+1} 条记录：gas_type为空")
                    continue
                
                print(f"[DEBUG] 创建废气分析记录 {idx+1}: {record_data}")
                new_record = await self.model.create(**record_data)
                results.append(new_record)
            except Exception as e:
                print(f"[ERROR] 创建废气分析记录 {idx+1} 失败: {str(e)}")
                print(f"[ERROR] 原始数据: {item}")
                import traceback
                traceback.print_exc()
                # 不抛出异常，继续处理下一条记录，但记录错误
                # 如果所有记录都失败，results为空列表，调用方可以检查
                continue
        
        # 如果所有记录都失败了，抛出异常
        if not results and items:
            raise ValueError("所有废气分析记录创建失败，请检查数据格式和必填字段")
        
        return results


class PCBWastewaterStatRecordController(CRUDBase[PCBWastewaterStatRecord, PCBWastewaterStatRecordCreate, PCBWastewaterStatRecordUpdate]):
    """近三年废水情况统计记录控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterStatRecord]:
        """获取企业的所有废水统计记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('project')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterStatRecord]:
        """批量更新或插入废水统计记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水统计记录，确保删除功能正常工作
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 构建记录数据
            record_data = {
                "enterprise_id": enterprise_id,
                "project": item.get("project", ""),
                "workshop": item.get("workshop"),
                "unit": item.get("unit", "")
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
            if not record_data["project"] or not record_data["unit"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBPollutionControlDataController:
    """污染防治数据控制器"""
    
    def __init__(self):
        self.wastewater_controller = PCBWastewaterAnalysisController(PCBWastewaterAnalysis)
        self.waste_gas_controller = PCBWasteGasAnalysisController(PCBWasteGasAnalysis)
        self.wastewater_stat_controller = PCBWastewaterStatRecordController(PCBWastewaterStatRecord)
    
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
wastewater_stat_record_controller = PCBWastewaterStatRecordController(PCBWastewaterStatRecord)
pollution_control_data_controller = PCBPollutionControlDataController()
