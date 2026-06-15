import re

# خواندن فایل
with open('/workspace/products.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن تمام VALUES با regex
# الگو: هر چیزی بین پرانتزها بعد از VALUES
pattern = r"\((\d+),[^)]+'(sku-\d+)',[^)]+'(sku-\d+)'\s*,[^)]*\)"

# پیدا کردن تمام رکوردها
records = []
for match in re.finditer(r"\([^)]+\)", content):
    record_text = match.group(0)
    # استخراج ID و SKU
    id_match = re.search(r'^\((\d+)', record_text)
    sku_matches = re.findall(r"'(sku-\d+)'", record_text)
    
    if id_match and len(sku_matches) >= 2:
        record_id = int(id_match.group(1))
        # SKU باید در furl و fsku یکسان باشد
        sku1 = sku_matches[0]  # furl
        sku2 = sku_matches[1]  # fsku
        
        records.append({
            'id': record_id,
            'sku': sku1,
            'text': record_text,
            'start': match.start(),
            'end': match.end()
        })

print(f"تعداد رکوردهای پیدا شده: {len(records)}")

# شمارش تکرار هر SKU
from collections import Counter
sku_counts = Counter([r['sku'] for r in records])

# پیدا کردن SKUهایی که 4 بار تکرار شده‌اند
duplicate_skus = {sku for sku, count in sku_counts.items() if count == 4}
print(f"تعداد SKUهای با 4 تکرار: {len(duplicate_skus)}")

# نگاشت SKU به رکوردها
sku_to_records = {}
for r in records:
    if r['sku'] not in sku_to_records:
        sku_to_records[r['sku']] = []
    sku_to_records[r['sku']].append(r)

# تعیین کدام رکوردها باید حذف شوند (نیمه دوم برای SKUهای تکراری)
records_to_remove = set()
for sku in duplicate_skus:
    recs = sku_to_records[sku]
    # حذف دو رکورد آخر (نگه داشتن دو رکورد اول)
    for r in recs[2:]:
        records_to_remove.add(r['id'])

print(f"تعداد رکوردهای حذفی: {len(records_to_remove)}")

# ساخت محتوای جدید
new_content_parts = []
last_end = 0

# مرتب‌سازی رکوردها بر اساس موقعیت شروع
sorted_records = sorted(records, key=lambda x: x['start'])

for r in sorted_records:
    if r['id'] in records_to_remove:
        continue
    # اضافه کردن بخش قبل از این رکورد
    new_content_parts.append(content[last_end:r['start']])
    # اضافه کردن خود رکورد
    new_content_parts.append(r['text'])
    last_end = r['end']

# اضافه کردن بخش پایانی
new_content_parts.append(content[last_end:])

new_content = ''.join(new_content_parts)

# نوشتن فایل جدید
with open('/workspace/products_fixed.sql', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("فایل اصلاح شده ذخیره شد.")

# بررسی نهایی
with open('/workspace/products_fixed.sql', 'r', encoding='utf-8') as f:
    fixed_content = f.read()

fixed_sku_counts = Counter(re.findall(r"'(sku-\d+)'", fixed_content))
still_wrong = sum(1 for count in fixed_sku_counts.values() if count != 2)
print(f"تعداد SKUهای با تکرار غیر از 2 در فایل جدید: {still_wrong}")
