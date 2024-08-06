# 系统部署文档

## 修改数据库并迁移

```python

command = Command(tortoise_config=APP_SETTINGS.TORTOISE_ORM, app="app_system")
try:
    await command.init_db(safe=True)
except FileExistsError:
    pass
await command.migrate()
```