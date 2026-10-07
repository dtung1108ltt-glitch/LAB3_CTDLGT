"""
inventory.py
-----------------------------------------------------------------------
BUOC 2 (Lab 2) - phan "Kho hang dong":
Sinh lai du lieu san pham GIONG HET Lab 1 (cung seed=42, cung cong
thuc random) nhung nap vao Danh sach lien ket don thay vi Mang tinh
Product store[100000].

Ke thua truc tiep tu Lab 1:
    - product.py (ADT Product, init_product) -> copy nguyen ban
    - Cong thuc sinh du lieu (SanPham_i, gia [1_000, 5_000_000],
      ton kho [0, 1000]) -> giong het data_generator.py cua Lab 1
      de dam bao du lieu Kho hang nhat quan giua 2 bai lab.
-----------------------------------------------------------------------
"""

import random

from product import Product, init_product
from linked_list import SinglyLinkedList


def build_inventory(n: int, seed: int = 42) -> SinglyLinkedList:
    """Sinh `n` san pham va nap vao mot Danh sach lien ket don (Kho hang).

    Dung insert_tail() de giu dung THU TU ID tang dan 0..n-1 giong nhu
    khi duyet Mang trong Lab 1 (thuan tien doi chieu ket qua giua 2 lab).
    Nho co con tro Tail, insert_tail() van la O(1) cho moi lan them.
    """
    inventory = SinglyLinkedList()
    rng = random.Random(seed)  # seed co dinh giong Lab 1 -> tai lap duoc

    for i in range(n):
        name = f"SanPham_{i}"
        price = rng.uniform(1000.0, 5_000_000.0)
        stock = rng.randint(0, 1000)

        p = Product()
        init_product(p, i, name, price, stock)
        inventory.insert_tail(p)

    return inventory
