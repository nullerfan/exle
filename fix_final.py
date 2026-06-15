import re
from collections import defaultdict

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# گروه‌بندی خطوط بر اساس SKU
sku_to_lines = defaultdict(list)

for i, line in enumerate(lines):
    if line.strip().startswith('INSERT'):
        continue
    skus = re.findall(r"'(sku-\d+)'", line)
    if skus:
        sku = skus[0]  # استفاده از اولین SKU به عنوان کلید
        sku_to_lines[sku].append((i, line))

print(f"تعداد SKUهای یکتا: {len(sku_to_lines)}")

# بررسی توزیع
from collections import Counter
line_counts = Counter([len(v) for v in sku_to_lines.values()])
print("توزیع تعداد خطوط برای هر SKU:")
for count, num_skus in sorted(line_counts.items()):
    print(f"  {count} خط: {num_skus} SKU")

# ساخت لیست خطوط برای نگهداری - فقط خط اول برای هر SKU
lines_to_keep = set()

for sku, recs in sku_to_lines.items():
    # فقط اولین رکورد را نگه دار
    first_line_num = recs[0][0]
    lines_to_keep.add(first_line_num)

print(f"\nتعداد خطوط برای نگهداری: {len(lines_to_keep)}")

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

fixed_skus = re.findall(r"'(sku-\d+)'", fixed_content)
fixed_sku_counts = Counter(fixed_skus)

total_records = len([l for l in new_lines if l.strip() and not l.strip().startswith('INSERT')])
wrong_count = sum(1 for count in fixed_sku_counts.values() if count != 2)
correct_count = sum(1 for count in fixed_sku_counts.values() if count == 2)

print(f"\n=== نتایج نهایی ===")
print(f"تعداد رکوردهای جدید: {total_records}")
print(f"تعداد SKUهای یکتا: {len(fixed_sku_counts)}")
print(f"SKUهای با 2 occurrence (صحیح): {correct_count}")
print(f"SKUهای با occurrence غیر از 2 (خطا): {wrong_count}")
