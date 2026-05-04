import sqlite3
conn = sqlite3.connect('C:/Users/Aldair/Documents/Proyectos/Zentory/backend/zentory.db')
cur = conn.cursor()

# Fix tipos to lowercase
print("=== FIXING TIPOS ===")

cur.execute("UPDATE movimientos SET tipo = 'ingreso' WHERE tipo = 'INGRESO'")
print(f"Fixed INGRESO: {cur.rowcount}")

cur.execute("UPDATE movimientos SET tipo = 'entrega' WHERE tipo = 'ENTREGA'")
print(f"Fixed ENTREGA: {cur.rowcount}")

conn.commit()

# Verify
print("\n=== VERIFY ===")
cur.execute("SELECT DISTINCT tipo FROM movimientos")
for row in cur.fetchall():
    print(f"tipo: {row[0]}")

conn.close()
print("Done!")