import re

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن تمام مقادیر INSERT
# هر خط VALUES با یک پرانتز شروع می‌شود و با ); پایان می‌یابد
lines = content.split('\n')
new_lines = []
seen_skus = {}

for line in lines:
    if line.strip().startswith('INSERT'):
        new_lines.append(line)
        continue
    
    # پیدا کردن SKU در این خط (هم در furl و هم در fsku)
    sku_match = re.search(r"'(sku-\d+)'", line)
    if sku_match:
        sku = sku_match.group(1)
        if sku not in seen_skus:
            seen_skus[sku] = 0
        
        seen_skus[sku] += 1
        
        # اگر این سومین یا چهارمین بار است که این SKU را می‌بینیم، آن را رد کن
        if seen_skus[sku] > 2:
            continue
    
    new_lines.append(line)

# نوشتن فایل جدید
with open('/workspace/products_fixed.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f"تعداد SKUهای منحصر به فرد: {len(seen_skus)}")
print(f"تعداد کل رکوردهای اصلی: {len([l for l in lines if not l.strip().startswith('INSERT') and l.strip()])}")
print(f"تعداد رکوردهای جدید: {len([l for l in new_lines if not l.strip().startswith('INSERT') and l.strip()])}")
