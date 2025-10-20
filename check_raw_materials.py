#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.models.raw_material import RawMaterial
from app.settings import settings


async def check():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    materials = await RawMaterial.all()
    print(f"Total materials: {len(materials)}")
    for m in materials:
        print(f"  ID={m.id}: {m.name} ({m.default_unit})")
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check())

