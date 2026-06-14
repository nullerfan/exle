import os
import pytest


def test_prud_json_exists():
    """بررسی وجود فایل prud.json"""
    assert os.path.exists("prud.json"), "فایل prud.json وجود ندارد"


def test_products_xlsx_exists():
    """بررسی وجود فایل Products.xlsx"""
    assert os.path.exists("Products.xlsx"), "فایل Products.xlsx وجود ندارد"


def test_prud_xlsx_exists():
    """بررسی وجود فایل خروجی prud.xlsx"""
    assert os.path.exists("prud.xlsx"), "فایل prud.xlsx وجود ندارد"


def test_prud_xlsx_not_empty():
    """بررسی خالی نبودن فایل prud.xlsx"""
    file_size = os.path.getsize("prud.xlsx")
    assert file_size > 0, "فایل prud.xlsx خالی است"
