"""
product.py
-----------------------------------------------------------------------
Kieu du lieu truu tuong (ADT) mo ta mot San pham (Product) trong he
thong Mini E-commerce Core.

ADT gom:
    - Thuoc tinh    : id, name, price, stock
    - Thao tac co ban:
        init_product() -> Khoi tao thong tin san pham
        print_product() -> In thong tin san pham ra man hinh

Thiet ke tuan thu tieu chi High Cohesion / Low Coupling (Chuong 1,
muc 1.2): ADT 'Product' CHI chua du lieu va hanh vi lien quan truc
tiep den mot san pham, khong xu ly cac nghiep vu khac (thanh toan,
kho van, ...).
-----------------------------------------------------------------------
"""

from dataclasses import dataclass

# Kich thuoc toi da cua kho luu tru - theo yeu cau Buoc 2
MAX_PRODUCTS = 100_000


@dataclass
class Product:
    """ADT San pham - tuong duong 'struct Product' trong C++."""
    id: int = 0
    name: str = ""
    price: float = 0.0
    stock: int = 0


def init_product(p: Product, id_: int, name: str, price: float, stock: int) -> None:
    """Ham khoi tao thong tin san pham (thao tac 'Create')."""
    p.id = id_
    p.name = name
    p.price = price
    p.stock = stock


def print_product(p: Product) -> None:
    """In thong tin san pham ra man hinh (thao tac 'Access')."""
    print(f"ID: {p.id:<6} | Ten: {p.name:<20} | Gia: {p.price:>12,.2f} | Ton kho: {p.stock}")
