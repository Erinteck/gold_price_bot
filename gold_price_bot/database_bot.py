import aiosqlite

DB_PATH = "settings.db"

async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                buy_offset INTEGER DEFAULT 0,
                sell_offset INTEGER DEFAULT 0,
                source_channel TEXT DEFAULT ''
            )
        ''')
        await db.execute('INSERT OR IGNORE INTO settings (id) VALUES (1)')
        await db.commit()

async def update_offsets(buy_offset, sell_offset):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE settings SET buy_offset = ?, sell_offset = ? WHERE id = 1', (buy_offset, sell_offset))
        await db.commit()

async def get_offsets():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT buy_offset, sell_offset FROM settings WHERE id = 1') as cursor:
            row = await cursor.fetchone()
            return row if row else (0, 0)

async def update_source_channel(source_channel):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE settings SET source_channel = ? WHERE id = 1', (source_channel,))
        await db.commit()

async def get_source_channel():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT source_channel FROM settings WHERE id = 1') as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None
