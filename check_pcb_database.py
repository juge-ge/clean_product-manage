"""
PCB数据库内容检查脚本
用于查看数据库中的数据和表结构
"""
import asyncio

from tortoise import Tortoise

from app.models.pcb import (
    PCBAuditReport,
    PCBAuditResult,
    PCBEnterprise,
    PCBEnterpriseScheme,
    PCBIndicator,
    PCBIndicatorSchemeRelation,
    PCBPreAuditData,
    PCBScheme,
)
from app.settings import settings


async def check_database():
    """检查数据库内容"""
    # 初始化数据库连接
    await Tortoise.init(config=settings.TORTOISE_ORM)

    print("=" * 80)
    print("PCB数据库内容检查")
    print("=" * 80)

    # 检查企业表
    print("\n【1. PCB企业表 (pcb_enterprise)】")
    enterprises = await PCBEnterprise.all()
    print(f"总记录数: {len(enterprises)}")
    if enterprises:
        print("\n企业列表:")
        for idx, ent in enumerate(enterprises[:10], 1):  # 只显示前10条
            print(f"  {idx}. ID: {ent.id}, 名称: {ent.name}, 地区: {ent.region}, 状态: {ent.audit_status}")
    else:
        print("  暂无企业数据")

    # 检查指标表
    print("\n【2. PCB指标表 (pcb_indicator)】")
    indicators = await PCBIndicator.all()
    print(f"总记录数: {len(indicators)}")
    if indicators:
        print("\n指标分类统计:")
        categories = {}
        for ind in indicators:
            categories[ind.category] = categories.get(ind.category, 0) + 1
        for category, count in sorted(categories.items()):
            print(f"  - {category}: {count}项")
        
        print("\n前5项指标:")
        for ind in indicators[:5]:
            print(f"  指标{ind.indicator_id}: {ind.name} ({ind.category})")
        
        # 检查限定性指标
        limiting_indicators = [ind for ind in indicators if ind.is_limiting]
        print(f"\n限定性指标数量: {len(limiting_indicators)}")
        if limiting_indicators:
            for ind in limiting_indicators:
                print(f"  指标{ind.indicator_id}: {ind.name}")
    else:
        print("  暂无指标数据")

    # 检查审核结果表
    print("\n【3. PCB审核结果表 (pcb_audit_result)】")
    audit_results = await PCBAuditResult.all()
    print(f"总记录数: {len(audit_results)}")
    if audit_results:
        print("\n前10条审核结果:")
        for idx, result in enumerate(audit_results[:10], 1):
            print(f"  {idx}. 企业ID: {result.enterprise_id}, 指标ID: {result.indicator_id}, "
                  f"评级: {result.level}, 得分: {result.score}")
    else:
        print("  暂无审核结果数据")

    # 检查方案表
    print("\n【4. PCB方案表 (pcb_scheme)】")
    schemes = await PCBScheme.all()
    print(f"总记录数: {len(schemes)}")
    if schemes:
        print("\n方案列表:")
        for idx, scheme in enumerate(schemes[:10], 1):  # 只显示前10条
            print(f"  {idx}. 方案{scheme.scheme_id}: {scheme.name} ({scheme.scheme_type})")
    else:
        print("  暂无方案数据")

    # 检查指标方案关联表
    print("\n【5. PCB指标方案关联表 (pcb_indicator_scheme_relation)】")
    relations = await PCBIndicatorSchemeRelation.all()
    print(f"总记录数: {len(relations)}")
    if relations:
        print("\n前10条关联关系:")
        for idx, rel in enumerate(relations[:10], 1):
            print(f"  {idx}. 指标ID: {rel.indicator_id} -> 方案ID: {rel.scheme_id} "
                  f"(关联度: {rel.relevance_score})")
    else:
        print("  暂无关联关系数据")

    # 检查企业方案记录表
    print("\n【6. PCB企业方案记录表 (pcb_enterprise_scheme)】")
    enterprise_schemes = await PCBEnterpriseScheme.all()
    print(f"总记录数: {len(enterprise_schemes)}")
    if enterprise_schemes:
        print("\n前10条企业方案记录:")
        for idx, es in enumerate(enterprise_schemes[:10], 1):
            print(f"  {idx}. 企业ID: {es.enterprise_id}, 方案ID: {es.scheme_id}, 状态: {es.status}")
    else:
        print("  暂无企业方案记录")

    # 检查预审核数据表
    print("\n【7. PCB预审核数据表 (pcb_pre_audit_data)】")
    pre_audit_data = await PCBPreAuditData.all()
    print(f"总记录数: {len(pre_audit_data)}")
    if pre_audit_data:
        print("\n预审核数据列表:")
        for idx, pad in enumerate(pre_audit_data[:10], 1):
            print(f"  {idx}. 企业ID: {pad.enterprise_id}, 状态: {pad.status}")
    else:
        print("  暂无预审核数据")

    # 检查审核报告表
    print("\n【8. PCB审核报告表 (pcb_audit_report)】")
    reports = await PCBAuditReport.all()
    print(f"总记录数: {len(reports)}")
    if reports:
        print("\n审核报告列表:")
        for idx, report in enumerate(reports[:10], 1):
            print(f"  {idx}. 企业ID: {report.enterprise_id}, 总分: {report.total_score}, "
                  f"等级: {report.overall_level}, 状态: {report.status}")
    else:
        print("  暂无审核报告")

    print("\n" + "=" * 80)
    print("数据库检查完成！")
    print("=" * 80)

    # 关闭数据库连接
    await Tortoise.close_connections()


async def check_specific_enterprise(enterprise_id: int):
    """检查特定企业的详细信息"""
    await Tortoise.init(config=settings.TORTOISE_ORM)

    print("\n" + "=" * 80)
    print(f"企业 ID {enterprise_id} 的详细信息")
    print("=" * 80)

    # 获取企业信息
    enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
    if not enterprise:
        print(f"❌ 未找到ID为 {enterprise_id} 的企业")
        await Tortoise.close_connections()
        return

    print(f"\n【企业基本信息】")
    print(f"  名称: {enterprise.name}")
    print(f"  地区: {enterprise.region} {enterprise.district}")
    print(f"  联系人: {enterprise.contact_person}")
    print(f"  联系电话: {enterprise.contact_phone}")
    print(f"  审核状态: {enterprise.audit_status}")
    print(f"  当前步骤: {enterprise.current_step}")

    # 获取预审核数据
    pre_audit = await PCBPreAuditData.get_or_none(enterprise_id=enterprise_id)
    print(f"\n【预审核数据】")
    if pre_audit:
        print(f"  状态: {pre_audit.status}")
        print(f"  提交时间: {pre_audit.submitted_at}")
    else:
        print("  暂无预审核数据")

    # 获取审核结果
    audit_results = await PCBAuditResult.filter(enterprise_id=enterprise_id).all()
    print(f"\n【审核结果】")
    print(f"  已审核指标数: {len(audit_results)}")
    if audit_results:
        level_count = {}
        for result in audit_results:
            level_count[result.level] = level_count.get(result.level, 0) + 1
        print("  评级分布:")
        for level, count in sorted(level_count.items()):
            print(f"    {level}: {count}项")

    # 获取选择的方案
    enterprise_schemes = await PCBEnterpriseScheme.filter(enterprise_id=enterprise_id).all()
    print(f"\n【选择的方案】")
    print(f"  总数: {len(enterprise_schemes)}")
    if enterprise_schemes:
        status_count = {}
        for es in enterprise_schemes:
            status_count[es.status] = status_count.get(es.status, 0) + 1
        print("  状态分布:")
        for status, count in sorted(status_count.items()):
            print(f"    {status}: {count}项")

    # 获取审核报告
    report = await PCBAuditReport.get_or_none(enterprise_id=enterprise_id)
    print(f"\n【审核报告】")
    if report:
        print(f"  总分: {report.total_score}")
        print(f"  综合等级: {report.overall_level}")
        print(f"  待改进项数: {report.improvement_items}")
        print(f"  限定性指标数: {report.limiting_indicators_count}")
        print(f"  报告状态: {report.status}")
    else:
        print("  暂无审核报告")

    print("\n" + "=" * 80)

    await Tortoise.close_connections()


async def show_table_structure():
    """显示所有PCB表的结构"""
    await Tortoise.init(config=settings.TORTOISE_ORM)

    print("\n" + "=" * 80)
    print("PCB模块数据库表结构")
    print("=" * 80)

    tables_info = {
        "pcb_enterprise": "企业基本信息表",
        "pcb_indicator": "审核指标表（64项指标）",
        "pcb_audit_result": "审核结果表",
        "pcb_scheme": "清洁生产方案表（130项方案）",
        "pcb_indicator_scheme_relation": "指标方案关联表",
        "pcb_enterprise_scheme": "企业方案记录表",
        "pcb_pre_audit_data": "预审核数据表",
        "pcb_audit_report": "审核报告表",
    }

    for table_name, description in tables_info.items():
        print(f"\n【{table_name}】 - {description}")

    print("\n" + "=" * 80)

    await Tortoise.close_connections()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "structure":
            # 显示表结构
            asyncio.run(show_table_structure())
        elif command == "enterprise" and len(sys.argv) > 2:
            # 检查特定企业
            enterprise_id = int(sys.argv[2])
            asyncio.run(check_specific_enterprise(enterprise_id))
        else:
            print("用法:")
            print("  python check_pcb_database.py              # 检查所有表")
            print("  python check_pcb_database.py structure    # 显示表结构")
            print("  python check_pcb_database.py enterprise 1 # 检查特定企业")
    else:
        # 检查所有表
        asyncio.run(check_database())



