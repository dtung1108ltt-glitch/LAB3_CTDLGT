"""
queue_ds.py   (dat ten queue_ds de khong trung module `queue` co san cua Python)
-----------------------------------------------------------------------
BUOC 1 (Lab 3) - phan 2: Hien thuc cau truc HANG DOI (Queue - FIFO).

Cach hien thuc : Danh sach lien ket don (Chuong 4.3) - KE THUA class
                 SinglyLinkedList cua Lab 2.
Nguyen ly      : FIFO (First In, First Out) - vao truoc, ra truoc.
Quy uoc        : DAU hang (Front) = HEAD ; CUOI hang (Rear) = TAIL.
                 - Enqueue them o TAIL  -> O(1) NHO con tro Tail
                   (Lab 2 da giu san Tail de insert_tail dat O(1)).
                 - Dequeue lay o HEAD   -> O(1).

Bang tai su dung tu Lab 2:
    enqueue()   -> goi insert_tail()   [KE THUA Lab 2, O(1) nho Tail]
    dequeue()   -> goi remove_head()   [BO SUNG Lab 3 trong linked_list.py, O(1)]
    front()     -> doc self.head.data  [O(1)]
    is_empty()/size() -> KE THUA nguyen ban

Kiem soat loi:
    - Overflow  : enqueue() tra ve False khi da dat max_size.
    - Underflow : dequeue()/front() tra ve None khi rong.
    - remove_head() reset Tail ve None khi hang can -> Enqueue lai sau khi
      can van dung (khong bi Tail "treo").
-----------------------------------------------------------------------
"""

from typing import Optional, Any

from linked_list import SinglyLinkedList


class Queue(SinglyLinkedList):
    """Queue FIFO ke thua SinglyLinkedList (Lab 2)."""

    def __init__(self, max_size: int = 0):
        super().__init__()
        self.max_size: int = max_size

    def is_full(self) -> bool:
        return self.max_size > 0 and self.size() >= self.max_size

    def enqueue(self, item: Any) -> bool:
        """Them `item` vao CUOI hang. O(1). Day -> tra ve False (chong Overflow)."""
        if self.is_full():
            print("[Loi] Queue day (Overflow) - khong the Enqueue them.")
            return False
        self.insert_tail(item)
        return True

    def dequeue(self) -> Optional[Any]:
        """Lay phan tu o DAU hang ra va tra ve. O(1). Rong -> None (chong Underflow)."""
        if self.is_empty():
            print("[Loi] Queue rong (Underflow) - khong co gi de Dequeue.")
            return None
        return self.remove_head()

    def front(self) -> Optional[Any]:
        """Xem phan tu dau hang ma KHONG lay ra. O(1). Rong -> None."""
        return None if self.is_empty() else self.head.data
