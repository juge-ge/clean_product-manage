#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCB清洁生产审核报告生成器 - Word格式
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from datetime import datetime
from typing import Dict, Any, List
import os


class PCBWordReportGenerator:
    """PCB清洁生产审核报告生成器"""
    
    def __init__(self):
        self.doc = Document()
        self.setup_document_style()
    
    def setup_document_style(self):
        """设置文档样式"""
        # 设置默认字体为宋体
        self.doc.styles['Normal'].font.name = '宋体'
        self.doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        self.doc.styles['Normal'].font.size = Pt(12)
    
    def add_title(self, title: str):
        """添加标题"""
        heading = self.doc.add_heading(title, level=0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = heading.runs[0]
        run.font.name = '黑体'
        run.font.size = Pt(22)
        run.font.bold = True
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    def add_heading(self, text: str, level: int = 1):
        """添加小节标题"""
        heading = self.doc.add_heading(text, level=level)
        run = heading.runs[0]
        run.font.name = '黑体'
        run.font.size = Pt(16 if level == 1 else 14)
        run.font.bold = True
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        return heading
    
    def add_paragraph(self, text: str, indent: bool = False):
        """添加段落"""
        p = self.doc.add_paragraph(text)
        p.paragraph_format.line_spacing = 1.5
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5)
        return p
    
    def add_table(self, headers: List[str], rows: List[List[Any]], col_widths: List[float] = None):
        """添加表格"""
        table = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        table.style = 'Light Grid Accent 1'
        
        # 添加表头
        header_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            header_cells[i].text = header
            # 设置表头格式
            for paragraph in header_cells[i].paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.size = Pt(11)
                    run.font.name = '黑体'
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加数据行
        for row_idx, row_data in enumerate(rows):
            row_cells = table.rows[row_idx + 1].cells
            for col_idx, value in enumerate(row_data):
                row_cells[col_idx].text = str(value) if value is not None else ""
                # 设置数据格式
                for paragraph in row_cells[col_idx].paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(10.5)
                        run.font.name = '宋体'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        
        # 设置列宽
        if col_widths:
            for i, width in enumerate(col_widths):
                for row in table.rows:
                    row.cells[i].width = Inches(width)
        
        return table
    
    def generate_report(self, enterprise_data: Dict[str, Any], 
                       planning_data: Dict[str, Any],
                       preaudit_data: Dict[str, Any],
                       audit_data: Dict[str, Any]) -> str:
        """
        生成完整的审核报告
        
        Args:
            enterprise_data: 企业基本信息
            planning_data: 筹划与组织数据
            preaudit_data: 预审核数据
            audit_data: 审核数据
        
        Returns:
            生成的Word文档路径
        """
        
        # 1. 添加报告标题
        self.add_title("印制电路板行业清洁生产审核报告")
        self.doc.add_paragraph()
        
        # 2. 企业基本信息
        self._add_enterprise_info(enterprise_data)
        
        # 3. 筹划与组织
        self._add_planning_info(planning_data)
        
        # 4. 预审核数据
        self._add_preaudit_info(preaudit_data)
        
        # 5. 审核结果
        self._add_audit_results(audit_data)
        
        # 6. 改进建议
        self._add_improvement_suggestions(audit_data)
        
        # 7. 生成文件
        filename = f"PCB清洁生产审核报告_{enterprise_data['name']}_{datetime.now().strftime('%Y%m%d')}.docx"
        filepath = os.path.join('reports', filename)
        
        # 确保reports目录存在
        os.makedirs('reports', exist_ok=True)
        
        self.doc.save(filepath)
        return filepath
    
    def _add_enterprise_info(self, data: Dict[str, Any]):
        """添加企业基本信息部分"""
        self.add_heading("一、企业基本信息", level=1)
        
        # 基本信息表格
        info_data = [
            ["企业名称", data.get('name', '')],
            ["统一社会信用代码", data.get('unified_social_credit_code', '')],
            ["所属地区", f"{data.get('region', '')} {data.get('district', '')}"],
            ["详细地址", data.get('address', '')],
            ["法人代表", data.get('legal_representative', '')],
            ["联系人", data.get('contact_person', '')],
            ["联系电话", data.get('contact_phone', '')],
            ["注册资本", f"{data.get('capital', '')}万元" if data.get('capital') else ''],
            ["年产能", f"{data.get('capacity', '')}万m²" if data.get('capacity') else ''],
            ["审核状态", data.get('audit_status', '')],
        ]
        
        self.add_table(["项目", "内容"], info_data, col_widths=[2.0, 4.5])
        self.doc.add_paragraph()
    
    def _add_planning_info(self, data: Dict[str, Any]):
        """添加筹划与组织信息"""
        self.add_heading("二、筹划与组织", level=1)
        
        # 2.1 审核领导小组
        self.add_heading("2.1 清洁生产审核领导小组", level=2)
        if data.get('leadership_team'):
            leadership_rows = []
            for member in data['leadership_team']:
                leadership_rows.append([
                    member.get('name', ''),
                    member.get('position', ''),
                    member.get('department', ''),
                    member.get('role', ''),
                    member.get('responsibilities', ''),
                    member.get('phone', '')
                ])
            self.add_table(
                ["姓名", "职位", "部门", "角色", "职责", "联系电话"],
                leadership_rows,
                col_widths=[0.8, 1.0, 1.0, 0.8, 2.0, 1.0]
            )
        self.doc.add_paragraph()
        
        # 2.2 工作小组
        self.add_heading("2.2 清洁生产工作小组", level=2)
        if data.get('work_team'):
            workteam_rows = []
            for member in data['work_team']:
                workteam_rows.append([
                    member.get('name', ''),
                    member.get('position', ''),
                    member.get('department', ''),
                    member.get('role', ''),
                    member.get('responsibilities', ''),
                    member.get('phone', '')
                ])
            self.add_table(
                ["姓名", "职位", "部门", "角色", "职责", "联系电话"],
                workteam_rows,
                col_widths=[0.8, 1.0, 1.0, 0.8, 2.0, 1.0]
            )
        self.doc.add_paragraph()
        
        # 2.3 工作计划
        self.add_heading("2.3 清洁生产审核工作计划", level=2)
        if data.get('work_plans'):
            workplan_rows = []
            for plan in data['work_plans']:
                workplan_rows.append([
                    f"第{plan.get('stage_order', '')}阶段",
                    plan.get('stage', ''),
                    plan.get('work_content', ''),
                    plan.get('planned_start_date', '')[:10] if plan.get('planned_start_date') else '',
                    plan.get('planned_end_date', '')[:10] if plan.get('planned_end_date') else '',
                    plan.get('responsible_department', ''),
                ])
            self.add_table(
                ["阶段", "阶段名称", "工作内容", "计划开始时间", "计划结束时间", "责任部门"],
                workplan_rows,
                col_widths=[0.8, 1.2, 2.0, 1.0, 1.0, 1.0]
            )
        self.doc.add_paragraph()
        
        # 2.4 培训记录
        self.add_heading("2.4 宣传与培训记录", level=2)
        if data.get('training_records'):
            training_rows = []
            for record in data['training_records']:
                training_rows.append([
                    record.get('title', ''),
                    record.get('date', '')[:10] if record.get('date') else '',
                    record.get('duration', ''),
                    record.get('participants', ''),
                    record.get('instructor', ''),
                    record.get('location', '')
                ])
            self.add_table(
                ["培训主题", "培训日期", "时长(分钟)", "参与人数", "讲师", "地点"],
                training_rows,
                col_widths=[2.0, 1.0, 0.8, 0.8, 0.8, 1.2]
            )
        self.doc.add_paragraph()
    
    def _add_preaudit_info(self, data: Dict[str, Any]):
        """添加预审核数据"""
        self.add_heading("三、预审核数据", level=1)
        
        # 3.1 企业总体生产情况
        self.add_heading("3.1 企业总体生产情况", level=2)
        
        # 产品产量表
        if data.get('production', {}).get('productOutput'):
            self.add_paragraph("（1）产品产量统计")
            output_rows = []
            for item in data['production']['productOutput']:
                output_rows.append([
                    item.get('type', ''),
                    item.get('main_product', ''),
                    item.get('layers', ''),
                    item.get('unit', ''),
                    item.get('year', ''),
                    f"{item.get('output', ''):.2f}" if item.get('output') else ''
                ])
            self.add_table(
                ["类型", "主要产品", "层数", "单位", "年份", "产量"],
                output_rows,
                col_widths=[1.0, 1.5, 0.8, 0.8, 0.8, 1.0]
            )
            self.doc.add_paragraph()
        
        # 合格率表
        if data.get('production', {}).get('qualificationRate'):
            self.add_paragraph("（2）产品合格率")
            qual_rows = []
            for item in data['production']['qualificationRate']:
                qual_rows.append([
                    item.get('year', ''),
                    f"{item.get('rate', '')}%" if item.get('rate') else ''
                ])
            self.add_table(
                ["年份", "合格率"],
                qual_rows,
                col_widths=[2.0, 2.0]
            )
            self.doc.add_paragraph()
        
        # 产值表
        if data.get('production', {}).get('outputValue'):
            self.add_paragraph("（3）年产值情况")
            value_rows = []
            for item in data['production']['outputValue']:
                value_rows.append([
                    item.get('year', ''),
                    item.get('unit', ''),
                    f"{item.get('annual_output_value', ''):.2f}" if item.get('annual_output_value') else '',
                    f"{item.get('income_tax', ''):.2f}" if item.get('income_tax') else ''
                ])
            self.add_table(
                ["年份", "单位", "年产值", "所得税"],
                value_rows,
                col_widths=[1.0, 1.0, 1.5, 1.5]
            )
            self.doc.add_paragraph()
        
        # 3.2 原辅材料使用情况
        if data.get('rawMaterials'):
            self.add_heading("3.2 原辅材料使用情况", level=2)
            raw_material_rows = []
            for item in data['rawMaterials']:
                raw_material_rows.append([
                    item.get('year', ''),
                    item.get('name', ''),
                    item.get('unit', ''),
                    item.get('process', ''),
                    f"{item.get('amount', ''):.2f}" if item.get('amount') else '',
                    item.get('state', ''),
                    f"{item.get('voc_content', '')}%" if item.get('voc_content') else ''
                ])
            self.add_table(
                ["年份", "材料名称", "单位", "使用工序", "用量", "状态", "VOC含量"],
                raw_material_rows
            )
            self.doc.add_paragraph()
        
        # 3.3 主要工艺及装备使用
        if data.get('processEquipment', {}).get('equipment'):
            self.add_heading("3.3 主要工艺及装备使用", level=2)
            equipment_rows = []
            for item in data['processEquipment']['equipment']:
                equipment_rows.append([
                    item.get('equipment_name', ''),
                    item.get('equipment_model', ''),
                    item.get('motor_model', ''),
                    f"{item.get('power', '')}kW" if item.get('power') else '',
                    item.get('quantity', ''),
                    item.get('process', ''),
                    item.get('status', '')
                ])
            self.add_table(
                ["设备名称", "设备型号", "电机型号", "功率", "数量", "应用工艺", "运行状况"],
                equipment_rows
            )
            self.doc.add_paragraph()
        
        # 3.4 资源能源消耗
        self.add_heading("3.4 资源能源消耗", level=2)
        
        # 用电情况
        if data.get('resourceConsumption', {}).get('electricity'):
            self.add_paragraph("（1）用电情况统计")
            electricity_rows = []
            for item in data['resourceConsumption']['electricity']:
                electricity_rows.append([
                    item.get('project', ''),
                    item.get('unit', ''),
                    f"{item.get('amount_2022', ''):.2f}" if item.get('amount_2022') else '',
                    f"{item.get('amount_2023', ''):.2f}" if item.get('amount_2023') else '',
                    f"{item.get('amount_2024', ''):.2f}" if item.get('amount_2024') else ''
                ])
            self.add_table(
                ["用电类型", "单位", "2022年", "2023年", "2024年"],
                electricity_rows,
                col_widths=[1.5, 0.8, 1.2, 1.2, 1.2]
            )
            self.doc.add_paragraph()
        
        # 用水情况
        if data.get('resourceConsumption', {}).get('water'):
            self.add_paragraph("（2）用水情况统计")
            water_rows = []
            for item in data['resourceConsumption']['water']:
                water_rows.append([
                    item.get('project', ''),
                    item.get('unit', ''),
                    f"{item.get('amount_2022', ''):.2f}" if item.get('amount_2022') else '',
                    f"{item.get('amount_2023', ''):.2f}" if item.get('amount_2023') else '',
                    f"{item.get('amount_2024', ''):.2f}" if item.get('amount_2024') else '',
                    item.get('source', '')
                ])
            self.add_table(
                ["用水类型", "单位", "2022年", "2023年", "2024年", "来源"],
                water_rows
            )
            self.doc.add_paragraph()
        
        # 天然气情况
        if data.get('resourceConsumption', {}).get('gas'):
            self.add_paragraph("（3）天然气使用情况")
            gas_rows = []
            for item in data['resourceConsumption']['gas']:
                gas_rows.append([
                    item.get('project', ''),
                    item.get('unit', ''),
                    f"{item.get('amount_2022', ''):.2f}" if item.get('amount_2022') else '',
                    f"{item.get('amount_2023', ''):.2f}" if item.get('amount_2023') else '',
                    f"{item.get('amount_2024', ''):.2f}" if item.get('amount_2024') else ''
                ])
            self.add_table(
                ["用途", "单位", "2022年", "2023年", "2024年"],
                gas_rows,
                col_widths=[1.5, 0.8, 1.2, 1.2, 1.2]
            )
            self.doc.add_paragraph()
        
        # 3.5 污染防治
        if data.get('pollutionControl'):
            self.add_heading("3.5 污染防治", level=2)
            
            # 废水处理
            if data['pollutionControl'].get('wastewater'):
                self.add_paragraph("（1）废水处理情况")
                wastewater_rows = []
                for item in data['pollutionControl']['wastewater']:
                    wastewater_rows.append([
                        item.get('category', ''),
                        item.get('source', ''),
                        item.get('pollutants', ''),
                        item.get('disposal', '')
                    ])
                self.add_table(
                    ["废水类别", "来源", "主要污染物", "处置方式"],
                    wastewater_rows
                )
                self.doc.add_paragraph()
            
            # 废气处理
            if data['pollutionControl'].get('wasteGas'):
                self.add_paragraph("（2）废气处理情况")
                wastegas_rows = []
                for item in data['pollutionControl']['wasteGas']:
                    wastegas_rows.append([
                        item.get('gas_type', ''),
                        item.get('pollutants', ''),
                        item.get('location', ''),
                        item.get('treatment', '')
                    ])
                self.add_table(
                    ["废气种类", "主要污染物", "产生部位", "处理方法"],
                    wastegas_rows
                )
                self.doc.add_paragraph()
        
        # 3.6 固体废物管理
        if data.get('solidWaste', {}).get('waste'):
            self.add_heading("3.6 工业固体废物管理", level=2)
            waste_rows = []
            for item in data['solidWaste']['waste']:
                waste_rows.append([
                    item.get('category', ''),
                    item.get('name', ''),
                    item.get('unit', ''),
                    f"{item.get('amount_2022', ''):.2f}" if item.get('amount_2022') else '',
                    f"{item.get('amount_2023', ''):.2f}" if item.get('amount_2023') else '',
                    f"{item.get('amount_2024', ''):.2f}" if item.get('amount_2024') else '',
                    item.get('disposal_method', '')
                ])
            self.add_table(
                ["类别", "名称", "单位", "2022年", "2023年", "2024年", "处置方式"],
                waste_rows
            )
            self.doc.add_paragraph()
        
        # 3.7 自行监测情况
        if data.get('selfMonitoring'):
            self.add_heading("3.7 自行监测情况", level=2)
            
            # 废水监测
            if data['selfMonitoring'].get('wastewater'):
                self.add_paragraph("（1）废水监测情况")
                wastewater_monitoring_rows = []
                for item in data['selfMonitoring']['wastewater']:
                    wastewater_monitoring_rows.append([
                        item.get('sampling_date', ''),
                        f"{item.get('ph', ''):.2f}" if item.get('ph') else '',
                        f"{item.get('cod', ''):.2f}" if item.get('cod') else '',
                        f"{item.get('total_copper', ''):.2f}" if item.get('total_copper') else '',
                        f"{item.get('ammonia_nitrogen', ''):.2f}" if item.get('ammonia_nitrogen') else ''
                    ])
                self.add_table(
                    ["采样日期", "pH", "COD(mg/L)", "总铜(mg/L)", "氨氮(mg/L)"],
                    wastewater_monitoring_rows
                )
                self.doc.add_paragraph()
            
            # 有组织废气监测
            if data['selfMonitoring'].get('organizedGas'):
                self.add_paragraph("（2）有组织废气监测情况")
                gas_monitoring_rows = []
                for item in data['selfMonitoring']['organizedGas']:
                    gas_monitoring_rows.append([
                        item.get('monitoring_point', ''),
                        item.get('monitoring_time', ''),
                        f"{item.get('non_methane_hydrocarbons', ''):.2f}" if item.get('non_methane_hydrocarbons') else '',
                        f"{item.get('sulfuric_acid_mist', ''):.2f}" if item.get('sulfuric_acid_mist') else ''
                    ])
                self.add_table(
                    ["监测点位", "监测时间", "非甲烷总烃(mg/m³)", "硫酸雾(mg/m³)"],
                    gas_monitoring_rows
                )
                self.doc.add_paragraph()
            
            # 噪声监测
            if data['selfMonitoring'].get('noise'):
                self.add_paragraph("（3）厂界噪声监测情况")
                noise_rows = []
                for item in data['selfMonitoring']['noise']:
                    noise_rows.append([
                        item.get('monitoring_point', ''),
                        item.get('monitoring_time', ''),
                        f"{item.get('daytime_result', ''):.1f}" if item.get('daytime_result') else '',
                        f"{item.get('daytime_standard', ''):.1f}" if item.get('daytime_standard') else '',
                        f"{item.get('nighttime_result', ''):.1f}" if item.get('nighttime_result') else '',
                        f"{item.get('nighttime_standard', ''):.1f}" if item.get('nighttime_standard') else ''
                    ])
                self.add_table(
                    ["监测点位", "监测时间", "昼间结果dB(A)", "昼间标准dB(A)", "夜间结果dB(A)", "夜间标准dB(A)"],
                    noise_rows
                )
                self.doc.add_paragraph()
    
    def _add_audit_results(self, data: Dict[str, Any]):
        """添加审核结果"""
        self.add_heading("四、审核结果", level=1)
        
        # 审核汇总
        if data.get('summary'):
            summary = data['summary']
            self.add_paragraph(f"综合得分：{summary.get('total_score', 0):.2f}分")
            self.add_paragraph(f"综合等级：{summary.get('overall_level', '')}")
            self.add_paragraph(f"待改进项：{summary.get('improvement_items', 0)}项")
            self.add_paragraph(f"限定性指标不达标：{summary.get('limiting_indicators', 0)}项")
            self.doc.add_paragraph()
        
        # 详细审核结果表
        if data.get('indicators'):
            self.add_paragraph("详细审核结果如下：")
            
            # 按类别分组显示
            categories = {}
            for indicator in data['indicators']:
                category = indicator.get('indicator', {}).get('category', '未分类')
                if category not in categories:
                    categories[category] = []
                categories[category].append(indicator)
            
            for category, indicators in categories.items():
                self.add_heading(category, level=3)
                indicator_rows = []
                for item in indicators:
                    ind = item.get('indicator', {})
                    indicator_rows.append([
                        ind.get('name', ''),
                        ind.get('unit', ''),
                        f"{item.get('current_value', ''):.2f}" if item.get('current_value') else '-',
                        item.get('level', ''),
                        f"{item.get('score', 0):.2f}" if item.get('score') else '0'
                    ])
                self.add_table(
                    ["指标名称", "单位", "当前值", "评级", "得分"],
                    indicator_rows,
                    col_widths=[2.5, 0.8, 1.0, 0.8, 0.8]
                )
                self.doc.add_paragraph()
    
    def _add_improvement_suggestions(self, data: Dict[str, Any]):
        """添加改进建议"""
        self.add_heading("五、清洁生产改进建议", level=1)
        
        # 收集所有不达标或低等级的指标
        needs_improvement = []
        if data.get('indicators'):
            for item in data['indicators']:
                level = item.get('level', '')
                if level in ['II级', 'III级', '不达标']:
                    needs_improvement.append(item)
        
        if needs_improvement:
            self.add_paragraph(f"根据审核结果，共有{len(needs_improvement)}项指标需要改进。针对这些指标，提出以下改进建议：")
            self.doc.add_paragraph()
            
            for idx, item in enumerate(needs_improvement, 1):
                ind = item.get('indicator', {})
                schemes = item.get('recommended_schemes', [])
                
                self.add_paragraph(f"{idx}. {ind.get('name', '')}（当前评级：{item.get('level', '')}）")
                
                if schemes:
                    self.add_paragraph(f"   推荐方案{len(schemes)}项：")
                    for scheme_idx, scheme in enumerate(schemes, 1):
                        preview = scheme.get('preview', {})
                        self.add_paragraph(f"   方案{scheme_idx}：{scheme.get('label', '')}")
                        if preview.get('problemSolved'):
                            self.add_paragraph(f"      问题描述：{preview['problemSolved'][:100]}...", indent=True)
                        if preview.get('economicBenefit'):
                            self.add_paragraph(f"      经济效益：{preview['economicBenefit'][:100]}...", indent=True)
                        self.doc.add_paragraph()
        else:
            self.add_paragraph("恭喜！所有指标均达到I级标准，无需改进。")
        
        self.doc.add_paragraph()
        
        # 添加报告结尾
        self.add_heading("六、结论", level=1)
        self.add_paragraph("本次清洁生产审核全面评估了企业的生产工艺、资源消耗、污染排放等各方面情况。", indent=True)
        self.add_paragraph("企业应根据本报告提出的改进建议，制定具体的实施计划，持续推进清洁生产工作。", indent=True)
        
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # 添加签章区域
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run(f"审核日期：{datetime.now().strftime('%Y年%m月%d日')}")


# 导出的工具函数
async def generate_pcb_word_report(
    enterprise_data: Dict[str, Any],
    planning_data: Dict[str, Any],
    preaudit_data: Dict[str, Any],
    audit_data: Dict[str, Any]
) -> str:
    """
    生成PCB清洁生产审核Word报告
    
    Returns:
        生成的Word文档路径
    """
    generator = PCBWordReportGenerator()
    filepath = generator.generate_report(
        enterprise_data=enterprise_data,
        planning_data=planning_data,
        preaudit_data=preaudit_data,
        audit_data=audit_data
    )
    return filepath

