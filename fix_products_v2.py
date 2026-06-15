import re
from collections import Counter

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# استخراج تمام SKUها برای تحلیل
all_skus = re.findall(r"'(sku-\d+)'", content)
sku_counts = Counter(all_skus)

# شناسایی SKUهایی که 4 بار تکرار شده‌اند
duplicate_skus = {sku for sku, count in sku_counts.items() if count == 4}
print(f"تعداد SKUهای با 4 تکرار: {len(duplicate_skus)}")

# تقسیم محتوا به خطوط
lines = content.split('\n')
new_lines = []
sku_occurrence = Counter()

for line in lines:
    # پیدا کردن اولین SKU در این خط
    sku_match = re.search(r"'(sku-\d+)'", line)
    
    if sku_match:
        sku = sku_match.group(1)
        
        # اگر این SKU جزو تکراری‌هاست (4 بار)
        if sku in duplicate_skus:
            sku_occurrence[sku] += 1
            
            # فقط دو occurrence اول را نگه دار
            if sku_occurrence[sku] <= 2:
                new_lines.append(line)
            # else: حذف خط (occurrence سوم و چهارم)
        else:
            # SKUهای غیر تکراری را همیشه نگه دار
            new_lines.append(line)
    else:
        # خطوط بدون SKU (مثل INSERT INTO) را نگه دار
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
remaining_4 = sum(1 for count in fixed_sku_counts.values() if count == 4)

print(f"\n=== نتایج نهایی ===")
print(f"تعداد رکوردهای جدید: {total_records}")
print(f"تعداد SKUهای یکتا: {len(fixed_sku_counts)}")
print(f"SKUهای با 2 تکرار (صحیح): {correct_count}")
print(f"SKUهای با 4 تکرار باقی‌مانده: {remaining_4}")
print(f"SKUهای با تکرار غیر از 2 (خطا): {wrong_count}")
