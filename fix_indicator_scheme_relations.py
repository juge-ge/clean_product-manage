import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBIndicatorSchemeRelation, PCBIndicator, PCBScheme

async def fix_indicator_scheme_relations():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    print('=== 修正指标与方案关联关系 ===')
    
    # 根据pcb指标关联表.md的关联关系
    relations_data = [
        # 方案1: 废水处理系统升级改造
        {"scheme_id": 1, "indicator_ids": [30, 34, 38, 42, 59, 62]},
        # 方案2: 废水分类收集与防泄漏系统改造
        {"scheme_id": 2, "indicator_ids": [30, 34, 38, 42, 59, 62, 63]},
        # 方案3: 镀铜生产线智能化改造
        {"scheme_id": 3, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案4: 有机废气收集处理系统优化
        {"scheme_id": 4, "indicator_ids": [43, 59]},
        # 方案5: 蚀刻线设备更新改造
        {"scheme_id": 5, "indicator_ids": [1, 5, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案6: 文字自动喷印系统改造
        {"scheme_id": 6, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案7: 自动化清洁生产线改造
        {"scheme_id": 7, "indicator_ids": [1, 7, 9, 12, 15, 19, 20, 30]},
        # 方案8: 废水深度处理回用系统改造
        {"scheme_id": 8, "indicator_ids": [15, 19, 30, 42, 59]},
        # 方案9: 磨板废水处理回用系统
        {"scheme_id": 9, "indicator_ids": [15, 19, 30, 34, 42]},
        # 方案10: 危废减量化系统改造
        {"scheme_id": 10, "indicator_ids": [44, 45, 62]},
        # 方案11: 电镀线自动化升级改造
        {"scheme_id": 11, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案12: 自动化蚀刻线改造
        {"scheme_id": 12, "indicator_ids": [1, 5, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案13: 防焊工艺设备升级
        {"scheme_id": 13, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案14: 表面处理自动化改造
        {"scheme_id": 14, "indicator_ids": [1, 7, 9, 12, 15, 19, 30, 34, 38]},
        # 方案15: 废水在线监测系统改造
        {"scheme_id": 15, "indicator_ids": [42, 59]},
        # 方案16: 危废智能管理系统改造
        {"scheme_id": 16, "indicator_ids": [44, 45, 62]},
        # 方案17: 阻焊显影线升级改造
        {"scheme_id": 17, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案18: 沉铜线智能化改造
        {"scheme_id": 18, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案19: 磨板线节水改造
        {"scheme_id": 19, "indicator_ids": [15, 19, 28, 30, 34]},
        # 方案20: 污泥减量化系统改造
        {"scheme_id": 20, "indicator_ids": [44, 62]},
        # 方案21: 内层蚀刻线智能化改造
        {"scheme_id": 21, "indicator_ids": [1, 5, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案22: 外层蚀刻线自动化升级
        {"scheme_id": 22, "indicator_ids": [1, 5, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案23: 钻孔废水处理系统改造
        {"scheme_id": 23, "indicator_ids": [15, 30, 34, 42]},
        # 方案24: 化学铜线升级改造
        {"scheme_id": 24, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案25: 棕化线工艺优化改造
        {"scheme_id": 25, "indicator_ids": [1, 7, 9, 12, 20, 28, 30, 38]},
        # 方案26: 退膜线自动化改造
        {"scheme_id": 26, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案27: 阻焊印刷自动化改造
        {"scheme_id": 27, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案28: 文字喷印系统改造
        {"scheme_id": 28, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案29: 清洗水回用系统改造
        {"scheme_id": 29, "indicator_ids": [15, 19, 30, 42]},
        # 方案30: 废气处理设施改造
        {"scheme_id": 30, "indicator_ids": [43, 59]},
        # 方案31: 黑孔处理线智能化改造
        {"scheme_id": 31, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案32: 沉镍金生产线改造
        {"scheme_id": 32, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43, 50]},
        # 方案33: 压合工序节能改造
        {"scheme_id": 33, "indicator_ids": [1, 7, 47, 48, 49]},
        # 方案34: 防焊前处理系统改造
        {"scheme_id": 34, "indicator_ids": [3, 7, 9, 12, 15, 19, 30]},
        # 方案35: 图形电镀线升级
        {"scheme_id": 35, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案36: 研磨清洗系统改造
        {"scheme_id": 36, "indicator_ids": [15, 19, 30, 34]},
        # 方案37: 显影系统优化改造
        {"scheme_id": 37, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案38: 除胶渣处理改造
        {"scheme_id": 38, "indicator_ids": [44, 62]},
        # 方案39: 中水回用系统改造
        {"scheme_id": 39, "indicator_ids": [15, 19, 30]},
        # 方案40: 除尘系统升级改造
        {"scheme_id": 40, "indicator_ids": [2, 44, 62]},
        # 方案41: 微蚀线自动化改造
        {"scheme_id": 41, "indicator_ids": [1, 5, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案42: 磨板线集尘系统改造
        {"scheme_id": 42, "indicator_ids": [2, 44, 62]},
        # 方案43: 检测线智能化改造
        {"scheme_id": 43, "indicator_ids": [12, 53, 56]},
        # 方案44: 化学铜线节能改造
        {"scheme_id": 44, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案45: 电镀铜添加剂回收系统
        {"scheme_id": 45, "indicator_ids": [20, 28, 30, 34, 38]},
        # 方案46: 棕化线废水处理改造
        {"scheme_id": 46, "indicator_ids": [30, 34, 38, 42, 59, 62]},
        # 方案47: 废气洗涤塔改造
        {"scheme_id": 47, "indicator_ids": [43, 59]},
        # 方案48: 电镀铜退镀液处理
        {"scheme_id": 48, "indicator_ids": [28, 30, 34, 38]},
        # 方案49: 高浓度有机废水处理
        {"scheme_id": 49, "indicator_ids": [38, 42, 59]},
        # 方案50: 含镍废水处理系统改造
        {"scheme_id": 50, "indicator_ids": [30, 34, 38, 42, 59]},
        # 方案51: 曝光线智能化改造
        {"scheme_id": 51, "indicator_ids": [1, 7, 9, 12, 53, 56]},
        # 方案52: 退膜工艺优化改造
        {"scheme_id": 52, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案53: 阻焊烘干系统改造
        {"scheme_id": 53, "indicator_ids": [7, 12, 43, 47, 48, 49]},
        # 方案54: 沉铜前处理改造
        {"scheme_id": 54, "indicator_ids": [1, 6, 7, 9, 12, 15, 20, 28, 30, 34, 38]},
        # 方案55: 喷墨打印系统改造
        {"scheme_id": 55, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案56: 钻孔除尘系统改造
        {"scheme_id": 56, "indicator_ids": [2, 44, 62]},
        # 方案57: 清洗水循环利用改造
        {"scheme_id": 57, "indicator_ids": [15, 19, 30, 42]},
        # 方案58: 蚀刻液回收系统改造
        {"scheme_id": 58, "indicator_ids": [5, 20, 28, 30, 34, 38, 62]},
        # 方案59: 油墨废气处理改造
        {"scheme_id": 59, "indicator_ids": [43, 50, 59]},
        # 方案60: 电镀废水零排放改造
        {"scheme_id": 60, "indicator_ids": [30, 34, 38, 42, 47, 48, 49, 62]},
        # 方案61: 热风整平系统改造
        {"scheme_id": 61, "indicator_ids": [1, 7, 12, 43, 47, 48, 49]},
        # 方案62: 丝印线自动化改造
        {"scheme_id": 62, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案63: 去毛刺线改造
        {"scheme_id": 63, "indicator_ids": [2, 44, 62]},
        # 方案64: 电镀锡自动线改造
        {"scheme_id": 64, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43, 50]},
        # 方案65: 酸性蚀刻线改造
        {"scheme_id": 65, "indicator_ids": [5, 20, 28, 30, 34, 38, 43]},
        # 方案66: 化学沉金线改造
        {"scheme_id": 66, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43, 50]},
        # 方案67: 显影系统升级改造
        {"scheme_id": 67, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案68: 冲孔废料回收系统
        {"scheme_id": 68, "indicator_ids": [29, 44, 62]},
        # 方案69: 废水浓缩液处理
        {"scheme_id": 69, "indicator_ids": [30, 34, 38, 42, 62]},
        # 方案70: 电镀铜自动线改造
        {"scheme_id": 70, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案71: 棕化线智能化改造
        {"scheme_id": 71, "indicator_ids": [1, 7, 9, 12, 20, 28, 30, 38]},
        # 方案72: 酸再生系统改造
        {"scheme_id": 72, "indicator_ids": [5, 20, 28, 62]},
        # 方案73: 高压水清洗改造
        {"scheme_id": 73, "indicator_ids": [15, 19, 30, 42]},
        # 方案74: 镀层测厚系统改造
        {"scheme_id": 74, "indicator_ids": [12, 53]},
        # 方案75: 自动光学检测改造
        {"scheme_id": 75, "indicator_ids": [12, 53, 56]},
        # 方案76: 钻孔粉尘处理改造
        {"scheme_id": 76, "indicator_ids": [2, 44, 62]},
        # 方案77: 压合前处理改造
        {"scheme_id": 77, "indicator_ids": [1, 7, 9, 12, 53]},
        # 方案78: 沉铜药液过滤改造
        {"scheme_id": 78, "indicator_ids": [6, 20, 28, 30, 34, 38]},
        # 方案79: 碱性蚀刻改造
        {"scheme_id": 79, "indicator_ids": [5, 20, 28, 30, 34, 38, 43]},
        # 方案80: 防焊阻焊改造
        {"scheme_id": 80, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案81: 水平电镀线改造
        {"scheme_id": 81, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43]},
        # 方案82: 铣边加工改造
        {"scheme_id": 82, "indicator_ids": [2, 44, 62]},
        # 方案83: 表面处理线改造
        {"scheme_id": 83, "indicator_ids": [1, 7, 9, 12, 15, 19, 30, 34, 38]},
        # 方案84: 化学沉铜改造
        {"scheme_id": 84, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38]},
        # 方案85: 除胶渣系统改造
        {"scheme_id": 85, "indicator_ids": [44, 62]},
        # 方案86: 废水蒸发系统改造
        {"scheme_id": 86, "indicator_ids": [30, 34, 38, 42, 62]},
        # 方案87: 干膜显影改造
        {"scheme_id": 87, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案88: 退锡系统改造
        {"scheme_id": 88, "indicator_ids": [28, 30, 34, 38, 43]},
        # 方案89: 除油清洗改造
        {"scheme_id": 89, "indicator_ids": [15, 19, 30, 38, 42, 43, 50]},
        # 方案90: 纯水制备改造
        {"scheme_id": 90, "indicator_ids": [15, 19, 30]},
        # 方案91: 抗氧化线改造
        {"scheme_id": 91, "indicator_ids": [1, 7, 9, 12, 30, 34, 38, 43]},
        # 方案92: 沉铜预处理改造
        {"scheme_id": 92, "indicator_ids": [1, 6, 7, 9, 12, 15, 20, 28, 30, 34, 38]},
        # 方案93: 钻靶机改造
        {"scheme_id": 93, "indicator_ids": [2, 44, 62]},
        # 方案94: 网印机改造
        {"scheme_id": 94, "indicator_ids": [3, 7, 9, 12, 43, 50]},
        # 方案95: 树脂塞孔改造
        {"scheme_id": 95, "indicator_ids": [2, 44, 62, 50]},
        # 方案96: 磨刷线改造
        {"scheme_id": 96, "indicator_ids": [2, 44, 62, 30, 34]},
        # 方案97: 定位系统改造
        {"scheme_id": 97, "indicator_ids": [12, 53]},
        # 方案98: 层压系统改造
        {"scheme_id": 98, "indicator_ids": [1, 7, 9, 12, 53, 47, 48, 49]},
        # 方案99: 测试系统改造
        {"scheme_id": 99, "indicator_ids": [12, 53]},
        # 方案100: 清洁线改造
        {"scheme_id": 100, "indicator_ids": [15, 19, 30, 42]},
        # 方案101: 碱性除胶改造
        {"scheme_id": 101, "indicator_ids": [44, 62]},
        # 方案102: 铜球研磨改造
        {"scheme_id": 102, "indicator_ids": [2, 44, 62, 28]},
        # 方案103: 外层蚀刻改造
        {"scheme_id": 103, "indicator_ids": [5, 20, 28, 30, 34, 38, 43]},
        # 方案104: 废液回收改造
        {"scheme_id": 104, "indicator_ids": [28, 29, 62]},
        # 方案105: 喷锡线改造
        {"scheme_id": 105, "indicator_ids": [1, 7, 12, 28, 30, 34, 38, 43]},
        # 方案106: 激光打标改造
        {"scheme_id": 106, "indicator_ids": [12, 53]},
        # 方案107: 半固化片处理改造
        {"scheme_id": 107, "indicator_ids": [44, 62, 50]},
        # 方案108: 气刀改造
        {"scheme_id": 108, "indicator_ids": [2, 7, 44, 62]},
        # 方案109: 自动包装改造
        {"scheme_id": 109, "indicator_ids": [51, 44, 62]},
        # 方案110: 冷却水系统改造
        {"scheme_id": 110, "indicator_ids": [15, 19, 30]},
        # 方案111: 化学镍金改造
        {"scheme_id": 111, "indicator_ids": [1, 6, 7, 9, 12, 20, 28, 30, 34, 38, 43, 50]},
        # 方案112: 钻孔定位改造
        {"scheme_id": 112, "indicator_ids": [12, 53]},
        # 方案113: 制程检查改造
        {"scheme_id": 113, "indicator_ids": [12, 53, 56]},
        # 方案114: 蚀刻液净化改造
        {"scheme_id": 114, "indicator_ids": [5, 28, 30, 34, 38, 62]},
        # 方案115: 回流焊改造
        {"scheme_id": 115, "indicator_ids": [7, 12, 47, 48, 49]},
        # 方案116: AOI检测改造
        {"scheme_id": 116, "indicator_ids": [12, 53, 56]},
        # 方案117: 废气治理改造
        {"scheme_id": 117, "indicator_ids": [43, 59]},
        # 方案118: 纯水回用改造
        {"scheme_id": 118, "indicator_ids": [15, 19, 30]},
        # 方案119: 抗氧化处理改造
        {"scheme_id": 119, "indicator_ids": [1, 7, 9, 12, 30, 34, 38, 43]},
        # 方案120: 电镀铜添加剂改造
        {"scheme_id": 120, "indicator_ids": [6, 20, 28, 30, 34, 38]},
        # 方案121: 制程参数优化改造
        {"scheme_id": 121, "indicator_ids": [1, 7, 9, 12, 56]},
        # 方案122: 设备预防维护改造
        {"scheme_id": 122, "indicator_ids": [1, 7, 56]},
        # 方案123: 工艺过程监控改造
        {"scheme_id": 123, "indicator_ids": [1, 7, 12, 56]},
        # 方案124: 废水在线监测改造
        {"scheme_id": 124, "indicator_ids": [42, 59]},
        # 方案125: 危废精细化管理
        {"scheme_id": 125, "indicator_ids": [45, 62]},
        # 方案126: 原辅料管控改造
        {"scheme_id": 126, "indicator_ids": [20, 24, 29, 56]},
        # 方案127: 生产调度优化改造
        {"scheme_id": 127, "indicator_ids": [1, 7, 9, 56]},
        # 方案128: 清洗水质控制改造
        {"scheme_id": 128, "indicator_ids": [15, 19, 30, 42, 56]},
        # 方案129: 药液分析改造
        {"scheme_id": 129, "indicator_ids": [6, 20, 28, 30, 34, 38, 56]},
        # 方案130: 自动加药系统改造
        {"scheme_id": 130, "indicator_ids": [6, 20, 28, 30, 34, 38, 56]}
    ]
    
    # 删除所有现有关联关系
    print('删除现有关联关系...')
    await PCBIndicatorSchemeRelation.all().delete()
    
    # 创建新的关联关系
    print('创建新的关联关系...')
    total_relations = 0
    
    for relation_data in relations_data:
        scheme_id = relation_data["scheme_id"]
        indicator_ids = relation_data["indicator_ids"]
        
        # 获取方案对象
        scheme = await PCBScheme.filter(scheme_id=scheme_id).first()
        if not scheme:
            print(f'警告: 方案编号{scheme_id}不存在')
            continue
        
            for indicator_id in indicator_ids:
            # 获取指标对象
            indicator = await PCBIndicator.filter(indicator_id=indicator_id).first()
            if not indicator:
                print(f'警告: 指标编号{indicator_id}不存在')
                continue
            
            # 创建关联关系
                await PCBIndicatorSchemeRelation.create(
                indicator_id=indicator.id,
                scheme_id=scheme.id,
                relevance_score=1.0  # 默认关联度为1.0
            )
            total_relations += 1
    
    print(f'已创建{total_relations}个指标方案关联关系')
    
    # 验证关联关系
    print('\n=== 验证关联关系 ===')
    relations = await PCBIndicatorSchemeRelation.all()
    print(f'总关联关系数: {len(relations)}')
    
    # 统计每个方案的关联指标数
    scheme_relations = {}
    for relation in relations:
        scheme = await PCBScheme.get(id=relation.scheme_id)
        if scheme.scheme_id not in scheme_relations:
            scheme_relations[scheme.scheme_id] = 0
        scheme_relations[scheme.scheme_id] += 1
    
    print('\n前10个方案的关联指标数:')
    for scheme_id in sorted(scheme_relations.keys())[:10]:
        scheme = await PCBScheme.filter(scheme_id=scheme_id).first()
        print(f'方案{scheme_id}({scheme.name}): {scheme_relations[scheme_id]}个指标')
    
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(fix_indicator_scheme_relations())