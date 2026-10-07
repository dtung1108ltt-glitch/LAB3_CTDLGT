"""
linked_list.py
-----------------------------------------------------------------------
BUOC 1 (Lab 2): Hien thuc cau truc Danh sach lien ket don
(Singly Linked List) bang ky thuat con tro (Chuong 3.3).

Thanh phan:
    Node        -> "mac xich" gom Data (mot ADT Product cua Lab 1)
                   va Next (con tro/tham chieu toi Node ke tiep)
    SinglyLinkedList -> quan ly danh sach thong qua con tro Head
                   (va Tail de Insert-at-tail dat O(1))

Ghi chu ve quan ly bo nho:
    Python khong co new/delete/malloc/free nhu C++. O day ta MO PHONG
    dung tinh than cua yeu cau de bai:
        - insert_head/insert_tail tuong duong "new Node(...)"
        - delete_by_id chu dong cat lien ket (unlink) VA gan next = None
          + dung tu khoa `del` de "giai phong" tham chieu toi Node bi
          loai bo, giup Garbage Collector thu hoi vung nho ngay lap tuc
          (tuong duong tinh than cua delete/free trong C++), tranh
          truong hop Node "mo coi" (con trong RAM ma khong dung toi)
          -> Memory Leak.
-----------------------------------------------------------------------
"""

from typing import Optional, Callable

from product import Product, print_product


class Node:
    """Mot Node (nut) trong Danh sach lien ket don.

    - data: du lieu thuc te, o day la mot ADT Product (Lab 1)
    - next: con tro/tham chieu toi Node ke tiep (None neu la Node cuoi)
    """

    __slots__ = ("data", "next")

    def __init__(self, data: Product):
        self.data: Product = data
        self.next: Optional["Node"] = None


class SinglyLinkedList:
    """Danh sach lien ket don, quan ly bang con tro Head (va Tail).

    Dung chung cho ca "Kho hang" va "Gio hang" trong Buoc 2, vi ban
    chat ca hai deu la mot Danh sach lien ket don chua cac Product.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    # ---------------------------------------------------------- Thong tin --
    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._size

    # ------------------------------------------------------------- Them ---
    def insert_head(self, product: Product) -> Node:
        """Them mot Node vao DAU danh sach. Do phuc tap: O(1).

        Buoc: (1) tao newNode, (2) newNode.next = head hien tai,
        (3) cap nhat head = newNode. Khong can dich chuyen bat ky
        Node nao khac -> loi the lon nhat so voi Mang (Chuong 3.3).
        """
        new_node = Node(product)
        new_node.next = self.head
        self.head = new_node
        if self.tail is None:  # danh sach vua tu rong -> newNode cung la tail
            self.tail = new_node
        self._size += 1
        return new_node

    def insert_tail(self, product: Product) -> Node:
        """Them mot Node vao CUOI danh sach. Do phuc tap: O(1) nho
        giu san con tro Tail (neu khong giu Tail, phai duyet het
        danh sach de tim Node cuoi -> O(n))."""
        new_node = Node(product)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        return new_node

    # ------------------------------------------------------------ Duyet ---
    def traverse(self, limit: Optional[int] = None, action: Optional[Callable[[Product], None]] = None) -> None:
        """Duyet danh sach tu Head den khi gap None. Do phuc tap: O(n).

        limit: chi in `limit` phan tu dau (de tranh spam console khi
               danh sach co hang tram nghin san pham).
        action: ham xu ly moi Product; mac dinh la print_product.
        """
        act = action or print_product
        current = self.head
        count = 0
        while current is not None:
            act(current.data)
            count += 1
            if limit is not None and count >= limit:
                break
            current = current.next

    def to_list(self) -> list:
        """Xuat danh sach lien ket ra list Python (phuc vu xuat CSV, thong ke...)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    # ----------------------------------------------------------- Tim kiem -
    def find_by_id(self, target_id: int) -> Optional[Node]:
        """Tim Node co Product.id == target_id. Do phuc tap: O(n)
        (khong the truy xuat ngau nhien nhu Mang, phai duyet tuan tu)."""
        current = self.head
        while current is not None:
            if current.data.id == target_id:
                return current
            current = current.next
        return None

    # --------------------------------------------------------------- Xoa --
    def delete_by_id(self, target_id: int) -> bool:
        """Tim va xoa AN TOAN Node co Product.id == target_id.

        An toan o day nghia la: cap nhat lai con tro cua Node DUNG
        TRUOC no de no tro thang qua Node DUNG SAU no truoc khi go bo
        Node muon xoa - tranh lam dut gay phan con lai cua danh sach
        (dung tinh than canh bao o Chuong 3.3, slide "Them vao giua").

        Do phuc tap: O(n) - vi phai duyet de TIM Node truoc do (O(n)),
        rieng thao tac NGAT LIEN KET sau khi da tim thay chi ton O(1).
        """
        if self.head is None:
            return False

        # Truong hop 1: Node can xoa la Head
        if self.head.data.id == target_id:
            removed = self.head
            self.head = self.head.next
            if self.head is None:  # danh sach vua tro thanh rong
                self.tail = None
            removed.next = None  # cat lien ket -> "giai phong" Node
            del removed
            self._size -= 1
            return True

        # Truong hop 2: Node can xoa nam o giua/cuoi -> phai giu Node truoc
        prev = self.head
        current = self.head.next
        while current is not None:
            if current.data.id == target_id:
                prev.next = current.next          # Buoc 1: bo qua current
                if current is self.tail:          # neu xoa dung Node cuoi
                    self.tail = prev
                current.next = None                # Buoc 2: cat lien ket con lai
                del current                        # "giai phong" bo nho cua Node
                self._size -= 1
                return True
            prev = current
            current = current.next

        return False  # khong tim thay ID can xoa

    # ====================================================================
    # [LAB 3 - THEM MOI] remove_head(): go Node o DAU danh sach, tra ve data
    # --------------------------------------------------------------------
    # Lab 2 chi co delete_by_id (O(n) vi phai tim theo ID). Stack.pop va
    # Queue.dequeue deu can "lay phan tu o dau" ma KHONG biet ID (du lieu
    # co the la Order chu khong chi Product) -> bo sung ham nay.
    # Do phuc tap: O(1) - chi doi con tro Head, khong phai duyet.
    # Cac ham/ thuat toan con lai cua Lab 2 giu NGUYEN, khong sua.
    # ====================================================================
    def remove_head(self):
        """Go Node dau danh sach va tra ve du lieu (data) cua no.
        Tra ve None neu danh sach rong (tranh Underflow). O(1)."""
        if self.head is None:
            return None
        removed = self.head
        data = removed.data
        self.head = removed.next
        if self.head is None:      # danh sach vua can -> Tail cung phai ve None
            self.tail = None       # (tranh Tail "treo" tro vao Node da xoa)
        removed.next = None        # cat lien ket -> "giai phong" Node (nhu Lab 2)
        del removed
        self._size -= 1
        return data
