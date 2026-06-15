import re
from collections import Counter, defaultdict

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# تقسیم به خطوط
lines = content.split('\n')

# استخراج تمام رکوردها با SKU اصلی آنها
# هر رکورد یک SKU دارد که در دو فیلد furl و fsku تکرار شده است
records_by_sku = defaultdict(list)

for i, line in enumerate(lines):
    if line.strip().startswith('INSERT'):
        continue
    
    # استخراج SKU از خط (اولین SKU پیدا شده)
    sku_match = re.search(r"'(sku-\d+)'", line)
    
    if sku_match:
        sku = sku_match.group(1)
        records_by_sku[sku].append((i, line))

print(f"تعداد SKUهای یکتا: {len(records_by_sku)}")

# بررسی توزیع تعداد رکوردها برای هر SKU
record_counts = Counter([len(v) for v in records_by_sku.values()])
print("توزیع تعداد رکوردها برای هر SKU:")
for count, num_skus in sorted(record_counts.items()):
    print(f"  {count} رکورد: {num_skus} SKU")

# شناسایی SKUهایی که 4 رکورد دارند (یعنی دو بار تکرار شده‌اند)
duplicate_skus = {sku for sku, recs in records_by_sku.items() if len(recs) == 4}
print(f"\nتعداد SKUهای با 4 رکورد (تکراری): {len(duplicate_skus)}")

# ساخت لیست خطوط برای نگهداری
lines_to_keep = set()

for sku, recs in records_by_sku.items():
    if len(recs) == 4:
        # فقط دو رکورد اول را نگه دار
        for i, line in recs[:2]:
            lines_to_keep.add(i)
    else:
        # همه رکوردها را نگه دار
        for i, line in recs:
            lines_to_keep.add(i)

print(f"تعداد خطوط برای نگهداری: {len(lines_to_keep)}")

# ساخت محتوای جدید
new_lines = []
for i, line in enumerate(lines):
    if line.strip().startswith('INSERT'):
        new_lines.append(line)
    elif i in lines_to_keep:
        new_lines.append(line)

# نوشتن فایل جدید
with open('/workspace/products_fixed.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

# بررسی نهایی
with open('/workspace/products_fixed.sql', 'r', encoding='utf-8') as f:
    fixed_content = f.read()

# استخراج SKUها از فایل جدید
fixed_skus = re.findall(r"'(sku-\d+)'", fixed_content)
fixed_sku_counts = Counter(fixed_skus)

# هر محصول باید دقیقاً 2 occurrence داشته باشد (یکی در furl و یکی در fsku)
total_records = len([l for l in new_lines if l.strip() and not l.strip().startswith('INSERT')])
wrong_count = sum(1 for count in fixed_sku_counts.values() if count != 2)
correct_count = sum(1 for count in fixed_sku_counts.values() if count == 2)

print(f"\n=== نتایج نهایی ===")
print(f"تعداد رکوردهای جدید: {total_records}")
print(f"تعداد SKUهای یکتا: {len(fixed_sku_counts)}")
print(f"SKUهای با 2 occurrence (صحیح): {correct_count}")
print(f"SKUهای با occurrence غیر از 2 (خطا): {wrong_count}")
