"""
cart.py
-----------------------------------------------------------------------
Gio hang (Cart) - KE THUA tu Lab 2, NANG CAP o Lab 3 (BUOC 2: UNDO).

[KE THUA NGUYEN BAN tu Lab 2 - khong sua]
    class Cart(SinglyLinkedList)  : gio hang la Danh sach lien ket don
    add_to_cart()                 : find_by_id O(n) trong Kho + deepcopy +
                                    insert_tail O(1)  => O(n)
    calculate_total()             : duyet Gio hang, cong don Price => O(n)
    print_cart()                  : duyet + print_product (Lab 1)
    delete_by_id() (cua lop cha)  : tim Node + cat lien ket an toan => O(n)

[MO RONG o Lab 3]
    self.DeletedItems (Stack)     : ngan xep luu cac san pham da bi xoa
    remove_from_cart() (GHI DE)   : them buoc Push san pham vao DeletedItems
                                    TRUOC khi go Node khoi gio
    undo()                        : Pop san pham tren cung cua DeletedItems
                                    va dua tro lai Gio hang

Vi sao dung Stack cho Undo? Hoan tac phai khoi phuc thao tac xoa GAN NHAT
truoc (LIFO) -> dung bai toan cua Stack.
-----------------------------------------------------------------------
"""

import copy
from typing import Optional

from linked_list import SinglyLinkedList
from product import Product, print_product
from stack import Stack


class Cart(SinglyLinkedList):

    def __init__(self, undo_capacity: int = 0):
        super().__init__()
        # [LAB 3 - Buoc 2] Stack "DeletedItems" (undo_capacity=0: khong gioi han)
        self.DeletedItems: Stack = Stack(max_size=undo_capacity)

    # ----------------------------------------------- KE THUA Lab 2 (giu nguyen)
    def add_to_cart(self, inventory: SinglyLinkedList, product_id: int) -> bool:
        node = inventory.find_by_id(product_id)
        if node is None:
            print(f"[Loi] Khong tim thay san pham ID={product_id} trong Kho hang.")
            return False
        product_copy = copy.deepcopy(node.data)
        self.insert_tail(product_copy)
        print(f"[OK] Da them '{product_copy.name}' (ID={product_id}) vao Gio hang.")
        return True

    def calculate_total(self) -> float:
        total = 0.0
        current = self.head
        while current is not None:
            total += current.data.price
            current = current.next
        return total

    def print_cart(self) -> None:
        if self.is_empty():
            print("Gio hang dang trong.")
            return
        print(f"--- GIO HANG ({self.size()} san pham) ---")
        current = self.head
        while current is not None:
            print_product(current.data)
            current = current.next
        print(f"{'TONG TIEN':<10}: {self.calculate_total():>15,.2f}")

    # ------------------------------------------------ [LAB 3] GHI DE: xoa + Push
    def remove_from_cart(self, product_id: int) -> bool:
        """Xoa san pham theo ID, nhung KHONG vut du lieu di ma Push vao
        DeletedItems de con hoan tac.

        Thuat toan:
          1. find_by_id(product_id)       [Lab 2, O(n)] - lay Product can xoa
          2. DeletedItems.push(product)   [Lab 3, O(1)] - cat giu doi tuong
          3. delete_by_id(product_id)     [Lab 2, O(n)] - ngat lien ket Node
        Node bi giai phong (del) nhung doi tuong Product van song vi Stack
        con giu tham chieu -> dung yeu cau "khong giai phong ngay".
        Neu Stack day (Overflow) thi TU CHOI xoa de khong mat du lieu.
        Do phuc tap tong: O(n).
        """
        node = self.find_by_id(product_id)
        if node is None:
            print(f"[Loi] Khong tim thay san pham ID={product_id} trong Gio hang.")
            return False
        if not self.DeletedItems.push(node.data):
            print("[Loi] Bo nho hoan tac day - huy thao tac xoa.")
            return False
        self.delete_by_id(product_id)
        print(f"[OK] Da xoa san pham ID={product_id} khoi Gio hang (co the Undo).")
        return True

    # ------------------------------------------------------ [LAB 3] Undo moi
    def undo(self) -> bool:
        """Hoan tac thao tac xoa gan nhat. O(1).
        Thuat toan: Pop dinh DeletedItems -> insert_tail vao Gio hang.
        Luu y: san pham quay lai CUOI gio (khong nho vi tri cu).
        Stack rong -> khong lam gi, tra ve False (chong Underflow)."""
        product: Optional[Product] = self.DeletedItems.pop()
        if product is None:
            print("[Loi] Khong co thao tac xoa nao de hoan tac.")
            return False
        self.insert_tail(product)
        print(f"[OK] Undo: da khoi phuc '{product.name}' (ID={product.id}) vao Gio hang.")
        return True
