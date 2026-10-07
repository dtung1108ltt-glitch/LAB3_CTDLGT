"""
order.py
-----------------------------------------------------------------------
BUOC 3 (Lab 3): Don hang (Order) + luong Thanh toan (Checkout) +
Xu ly don hang bang HANG DOI OrderQueue (FIFO).

Tai su dung:
    Product (Lab 1)            : phan tu cua don hang
    Cart.to_list() (Lab 2)     : xuat gio hang ra list (duyet O(n))
    Cart.calculate_total (Lab 2): tinh tong tien
    Queue (Lab 3 Buoc 1)       : OrderQueue
-----------------------------------------------------------------------
"""

import copy
from dataclasses import dataclass, field
from typing import List

from product import Product
from cart import Cart
from queue_ds import Queue


@dataclass
class Order:
    """Don hang = ban chup (snapshot) toan bo Gio hang luc bam 'Thanh toan'."""
    order_id: int
    customer: str
    items: List[Product] = field(default_factory=list)
    total: float = 0.0


def create_order(cart: Cart, customer: str, order_id: int) -> Order:
    """Dong goi toan bo Gio hang thanh 1 Order. O(n).
    deepcopy de Order doc lap voi Gio hang (giong y tuong add_to_cart Lab 2)."""
    items = [copy.deepcopy(p) for p in cart.to_list()]
    return Order(order_id, customer, items, cart.calculate_total())


def checkout(cart: Cart, order_queue: Queue, customer: str, order_id: int) -> bool:
    """Nghiep vu 'Thanh toan': dong goi Gio hang -> Enqueue vao OrderQueue.
    Gio hang rong hoac OrderQueue day -> khong thuc hien (giu nguyen gio)."""
    if cart.is_empty():
        print("[Loi] Gio hang rong, khong the thanh toan.")
        return False
    order = create_order(cart, customer, order_id)
    if not order_queue.enqueue(order):          # O(1)
        return False
    while not cart.is_empty():                  # don sach gio sau khi chot don
        cart.remove_head()
    while not cart.DeletedItems.is_empty():     # het hieu luc Undo cua don da chot
        cart.DeletedItems.pop()
    return True


def process_orders(order_queue: Queue) -> int:
    """Mo phong backend: lien tuc Dequeue tung don va xu ly theo FIFO.
    Thuat toan: vong lap while (hang doi khong rong) -> dequeue O(1)/don.
    Tong: O(k) cho k don. Tra ve so don da xu ly."""
    processed = 0
    while not order_queue.is_empty():
        order = order_queue.dequeue()
        print(f"Dang xu ly don hang cua khach {order.customer} "
              f"(#{order.order_id}, {len(order.items)} san pham, "
              f"{order.total:,.0f})... Da xu ly xong")
        processed += 1
    return processed
