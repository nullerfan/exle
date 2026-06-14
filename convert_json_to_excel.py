import json
import pandas as pd

# خواندن فایل JSON
with open('/workspace/products_price_after.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# استخراج داده‌های اصلی (بخش data از جدول products_price_after)
products_data = []
for item in data:
    if item.get('type') == 'table' and item.get('name') == 'products_price_after':
        products_data = item.get('data', [])
        break

if not products_data:
    print("هیچ داده‌ای پیدا نشد!")
    exit(1)

print(f"تعداد محصولات پیدا شده: {len(products_data)}")

# ایجاد لیست برای ذخیره ردیف‌ها
rows = []

for product in products_data:
    # استخراج اطلاعات پایه
    product_id = product.get('id', '')
    master_product_id = product.get('master_product_id', '')
    name = product.get('name', '')
    image_url = product.get('image_url', '')
    store_detail_str = product.get('store_detail', '{}')
    
    try:
        store_detail = json.loads(store_detail_str)
    except:
        store_detail = {}
    
    # برای هر store در store_detail، یک ردیف ایجاد می‌کنیم
    for store_id, store_info in store_detail.items():
        if store_info is None:
            continue
        
        row = {
            'حذف شده': 0,
            'فعال': 1 if store_info.get('hasQuantity', False) else 0,
            'دانلودی': 0,
            'مجازی': 0,
            'شناسه': product_id,
            'نام': store_info.get('name', name),
            'SKU': f'SKU-{product_id}',
            'تصویر شاخص': store_info.get('imageUrl', image_url),
            'گالری تصاویر': '',
            'نام لاتین': '',
            'توضیحات سئو': f'خرید اینترنتی {store_info.get("name", name)} به همراه مقایسه، بررسی مشخصات و لیست قیمت امروز در فروشگاه اینترنتی فروشگاه اینترنتی هاوند',
            'تایتل اختصاصی': f'قیمت و خرید {store_info.get("name", name)}',
            'کلمات کلیدی': '',
            'لینک': f'sku-{product_id}',
            'دسته‌بندی': '',
            'برند': ''
        }
        rows.append(row)

# اگر هیچ store_info معتبری نبود، از اطلاعات خود محصول استفاده کن
if not rows and products_data:
    for product in products_data:
        product_id = product.get('id', '')
        name = product.get('name', '')
        image_url = product.get('image_url', '')
        
        row = {
            'حذف شده': 0,
            'فعال': 1,
            'دانلودی': 0,
            'مجازی': 0,
            'شناسه': product_id,
            'نام': name,
            'SKU': f'SKU-{product_id}',
            'تصویر شاخص': image_url,
            'گالری تصاویر': '',
            'نام لاتین': '',
            'توضیحات سئو': f'خرید اینترنتی {name} به همراه مقایسه، بررسی مشخصات و لیست قیمت امروز در فروشگاه اینترنتی فروشگاه اینترنتی هاوند',
            'تایتل اختصاصی': f'قیمت و خرید {name}',
            'کلمات کلیدی': '',
            'لینک': f'sku-{product_id}',
            'دسته‌بندی': '',
            'برند': ''
        }
        rows.append(row)

print(f"تعداد ردیف‌های ایجاد شده: {len(rows)}")

# ایجاد DataFrame
df = pd.DataFrame(rows)

# مرتب‌سازی ستون‌ها مطابق با فایل اکسل اصلی
column_order = ['حذف شده', 'فعال', 'دانلودی', 'مجازی', 'شناسه', 'نام', 'SKU', 'تصویر شاخص', 'گالری تصاویر', 'نام لاتین', 'توضیحات سئو', 'تایتل اختصاصی', 'کلمات کلیدی', 'لینک', 'دسته‌بندی', 'برند']
df = df[column_order]

# ذخیره به فایل اکسل
output_file = '/workspace/products_price_after.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"فایل اکسل با موفقیت ایجاد شد: {output_file}")
print(f"تعداد ردیف‌ها: {len(df)}")
