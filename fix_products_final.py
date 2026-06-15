import re
from collections import Counter

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# تقسیم به خطوط
lines = content.split('\n')

# استخراج تمام رکوردها با ID و SKU
records = []
for i, line in enumerate(lines):
    if line.strip().startswith('INSERT'):
        continue
    
    # استخراج ID و SKU
    id_match = re.match(r'\((\d+),', line)
    sku_match = re.search(r"'(sku-\d+)'", line)
    
    if id_match and sku_match:
        record_id = int(id_match.group(1))
        sku = sku_match.group(1)
        records.append({
            'line_num': i,
            'id': record_id,
            'sku': sku,
            'content': line
        })

print(f"تعداد رکوردهای پیدا شده: {len(records)}")

# شمارش تکرار هر SKU
sku_counts = Counter([r['sku'] for r in records])
print(f"تعداد SKUهای یکتا: {len(sku_counts)}")

# SKUهایی که 4 بار تکرار شده‌اند (یعنی دو رکورد اضافی دارند)
duplicate_skus = {sku for sku, count in sku_counts.items() if count == 4}
print(f"تعداد SKUهای با 4 تکرار: {len(duplicate_skus)}")

# برای هر SKU تکراری، فقط دو رکورد اول را نگه دار
lines_to_keep = set()
sku_seen_count = Counter()

for r in records:
    sku = r['sku']
    
    if sku in duplicate_skus:
        sku_seen_count[sku] += 1
        # فقط دو occurrence اول را نگه دار
        if sku_seen_count[sku] <= 2:
            lines_to_keep.add(r['line_num'])
    else:
        # SKUهای غیر تکراری را همیشه نگه دار
        lines_to_keep.add(r['line_num'])

print(f"تعداد خطوط برای نگهداری: {len(lines_to_keep)}")

# ساخت محتوای جدید
new_lines = []
for i, line in enumerate(lines):
    if line.strip().startswith('INSERT'):
        new_lines.append(line)
    elif i in lines_to_keep:
        new_lines.append(line)
    # else: حذف خط تکراری

# نوشتن فایل جدید
with open('/workspace/products_fixed.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

# بررسی نهایی
with open('/workspace/products_fixed.sql', 'r', encoding='utf-8') as f:
    fixed_content = f.read()

fixed_skus = re.findall(r"'(sku-\d+)'", fixed_content)
fixed_sku_counts = Counter(fixed_skus)

total_records = len([l for l in new_lines if l.strip() and not l.strip().startswith('INSERT')])
wrong_count = sum(1 for count in fixed_sku_counts.values() if count != 2)
correct_count = sum(1 for count in fixed_sku_counts.values() if count == 2)

print(f"\n=== نتایج نهایی ===")
print(f"تعداد رکوردهای جدید: {total_records}")
print(f"تعداد SKUهای یکتا: {len(fixed_sku_counts)}")
print(f"SKUهای با 2 تکرار (صحیح): {correct_count}")
print(f"SKUهای با تکرار غیر از 2 (خطا): {wrong_count}")
