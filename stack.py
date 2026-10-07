"""
stack.py
-----------------------------------------------------------------------
BUOC 1 (Lab 3) - phan 1: Hien thuc cau truc XEP CHONG (Stack - LIFO).

Cach hien thuc : Danh sach lien ket don (Chuong 4.3) - KE THUA truc tiep
                 class SinglyLinkedList cua Lab 2 (linked_list.py), tai su
                 dung Node, con tro Head/Tail, is_empty(), size().
Nguyen ly      : LIFO (Last In, First Out) - vao sau, ra truoc.
Quy uoc        : DINH stack = HEAD cua danh sach lien ket.
                 => Push/Pop deu thao tac o DAU danh sach -> O(1).
                 (Neu lay CUOI lam dinh thi Pop phai duyet tim Node ke cuoi
                 vi danh sach don khong co con tro prev -> O(n), sai muc tieu.)

Bang tai su dung tu Lab 2:
    push()      -> goi insert_head()   [KE THUA Lab 2, O(1)]
    pop()       -> goi remove_head()   [BO SUNG Lab 3 trong linked_list.py, O(1)]
    top()       -> doc self.head.data  [truy cap truc tiep con tro Head, O(1)]
    is_empty()  -> KE THUA nguyen ban tu SinglyLinkedList
    size()      -> KE THUA nguyen ban tu SinglyLinkedList

Kiem soat loi:
    - Overflow  (day) : push() tra ve False khi da dat max_size.
    - Underflow (rong): pop()/top() tra ve None, KHONG nem exception.
-----------------------------------------------------------------------
"""

from typing import Optional, Any

from linked_list import SinglyLinkedList


class Stack(SinglyLinkedList):
    """Stack LIFO ke thua SinglyLinkedList (Lab 2)."""

    def __init__(self, max_size: int = 0):
        """max_size: so phan tu toi da; 0 = khong gioi han (chi han che boi RAM)."""
        super().__init__()
        self.max_size: int = max_size

    def is_full(self) -> bool:
        """True neu stack da dat gioi han max_size. O(1)."""
        return self.max_size > 0 and self.size() >= self.max_size

    def push(self, item: Any) -> bool:
        """Day `item` vao DINH stack. O(1).
        Thuat toan: insert_head (newNode.next = head; head = newNode).
        Tra ve False (tu choi an toan) neu stack day -> chong Overflow."""
        if self.is_full():
            print("[Loi] Stack day (Overflow) - khong the Push them.")
            return False
        self.insert_head(item)
        return True

    def pop(self) -> Optional[Any]:
        """Lay phan tu o DINH stack ra khoi stack va tra ve. O(1).
        Thuat toan: remove_head (head = head.next, cat lien ket Node cu).
        Tra ve None neu stack rong -> chong Underflow."""
        if self.is_empty():
            print("[Loi] Stack rong (Underflow) - khong co gi de Pop.")
            return None
        return self.remove_head()

    def top(self) -> Optional[Any]:
        """Xem phan tu o DINH stack ma KHONG lay ra. O(1). Rong -> None."""
        return None if self.is_empty() else self.head.data
