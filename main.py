"""
main.py
-----------------------------------------------------------------------
BAI LAB 3 - Mini E-commerce Core (Giai doan 3)
Xu ly luong nghiep vu voi Xep chong (Stack) va Hang doi (Queue).

Quy trinh (bam sat 4 Buoc trong de bai):
    Buoc 1: Stack + Queue (ke thua SinglyLinkedList Lab 2) -> stack.py, queue_ds.py
    Buoc 2: Undo gio hang bang Stack DeletedItems           -> cart.py
    Buoc 3: Flash Sale: OrderQueue + xu ly FIFO             -> order.py
    Buoc 4: Danh gia Big-O + giai thich Stack vs Queue      -> cuoi file nay

CACH CHAY:
    python main.py            (demo + do Big-O, sau do vao menu tuong tac)
    python main.py --demo     (chi chay demo, khong hoi menu)
-----------------------------------------------------------------------
"""

import io
import sys
import time
import random
import contextlib

from product import Product, init_product                  # Lab 1
from inventory import build_inventory                      # Lab 2 (cong thuc sinh du lieu Lab 1)
from cart import Cart                                      # Lab 2 + Lab 3
from stack import Stack
from queue_ds import Queue
from order import checkout, process_orders


def header(text: str) -> None:
    print(f"\n===== {text} =====")


# =======================================================================
# BUOC 1: KIEM THU STACK & QUEUE (LIFO / FIFO / Overflow / Underflow)
# =======================================================================
def demo_buoc1() -> None:
    header("BUOC 1: Kiem thu Stack (LIFO) va Queue (FIFO)")

    s = Stack(max_size=3)
    print("Stack rong?", s.is_empty())
    print("Pop khi rong     ->", s.pop())
    for x in (1, 2, 3):
        s.push(x)
    print("Push thu 4 (day) ->", s.push(4))
    print("Top =", s.top(), "| size =", s.size())
    print("Thu tu Pop (LIFO):", [s.pop() for _ in range(3)])

    q = Queue(max_size=3)
    print("\nDequeue khi rong ->", q.dequeue())
    for x in (1, 2, 3):
        q.enqueue(x)
    print("Enqueue thu 4 (day) ->", q.enqueue(4))
    print("Front =", q.front(), "| size =", q.size())
    print("Thu tu Dequeue (FIFO):", [q.dequeue() for _ in range(3)])
    q.enqueue(9)   # kiem tra Tail da duoc reset dung sau khi can
    print("Enqueue lai sau khi can: Front =", q.front())


# =======================================================================
# BUOC 2: UNDO GIO HANG
# =======================================================================
def demo_buoc2(inventory) -> None:
    header("BUOC 2: Hoan tac (Undo) Gio hang bang Stack DeletedItems")
    cart = Cart()
    for pid in (5, 20, 100):
        cart.add_to_cart(inventory, pid)
    cart.print_cart()

    print("\nXoa ID=20 roi ID=5:")
    cart.remove_from_cart(20)
    cart.remove_from_cart(5)
    cart.print_cart()
    print(f"(DeletedItems dang giu {cart.DeletedItems.size()} san pham, "
          f"dinh stack = ID {cart.DeletedItems.top().id})")

    print("\nUndo lan 1 (khoi phuc cai xoa SAU CUNG = ID 5):")
    cart.undo(); cart.print_cart()
    print("\nUndo lan 2 (khoi phuc ID 20):")
    cart.undo(); cart.print_cart()
    print("\nUndo lan 3 khi het gi de hoan tac:")
    cart.undo()


# =======================================================================
# BUOC 3: FLASH SALE - HANG DOI XU LY DON HANG
# =======================================================================
CUSTOMERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K"]


def demo_buoc3(inventory) -> list:
    header("BUOC 3: Flash Sale - OrderQueue xu ly don hang theo FIFO")
    rng = random.Random()
    OrderQueue = Queue()                      # Queue ten OrderQueue theo de bai
    num_orders = rng.randint(5, 10)           # ngau nhien 5..10 don
    print(f"Flash Sale: {num_orders} khach bam 'Thanh toan' cung luc.\n")

    for i in range(num_orders):
        cart = Cart()                         # moi khach 1 gio rieng
        with contextlib.redirect_stdout(io.StringIO()):   # an log add_to_cart cho gon
            for _ in range(rng.randint(1, 3)):
                cart.add_to_cart(inventory, rng.randint(0, inventory.size() - 1))
        if checkout(cart, OrderQueue, CUSTOMERS[i], 1000 + i):
            o = OrderQueue.tail.data
            print(f"  + Enqueue don #{o.order_id} cua khach {o.customer} "
                  f"({len(o.items)} san pham, {o.total:,.0f})")

    print(f"\nHang doi dang co {OrderQueue.size()} don. Backend bat dau xu ly (FIFO):\n")
    arrival = [CUSTOMERS[i] for i in range(num_orders)]
    process_orders(OrderQueue)
    print(f"\nHang doi sau xu ly: {OrderQueue.size()} don. "
          f"Thu tu den: {' '.join(arrival)} (xu ly dung thu tu).")
    return arrival


# =======================================================================
# BUOC 4: DO THUC NGHIEM BIG-O + SO SANH STACK vs QUEUE
# =======================================================================
def demo_buoc4(arrival: list) -> None:
    header("BUOC 4: Danh gia do phuc tap & so sanh Stack vs Queue")
    p = Product(); init_product(p, 0, "SP", 1000.0, 1)
    print(f"{'n':>9} | {'Push(ms)':>10} {'Pop(ms)':>10} | {'Enqueue(ms)':>12} {'Dequeue(ms)':>12}")
    for n in (10_000, 100_000, 200_000):
        st, qu = Stack(), Queue()
        t = time.perf_counter()
        for _ in range(n): st.push(p)
        t_push = (time.perf_counter() - t) * 1000
        t = time.perf_counter()
        for _ in range(n): st.pop()
        t_pop = (time.perf_counter() - t) * 1000
        t = time.perf_counter()
        for _ in range(n): qu.enqueue(p)
        t_enq = (time.perf_counter() - t) * 1000
        t = time.perf_counter()
        for _ in range(n): qu.dequeue()
        t_deq = (time.perf_counter() - t) * 1000
        print(f"{n:>9,} | {t_push:>10.2f} {t_pop:>10.2f} | {t_enq:>12.2f} {t_deq:>12.2f}")
    print("-> Tong thoi gian n thao tac tang TUYEN TINH theo n => moi thao tac O(1).")

    print("\nNeu xu ly don bang STACK thay vi QUEUE (sai nghiep vu):")
    s = Stack()
    for c in arrival:
        s.push(c)
    order_out = []
    while not s.is_empty():
        order_out.append(s.pop())
    print(f"  Thu tu den        : {' '.join(arrival)}")
    print(f"  Thu tu xu ly (LIFO): {' '.join(order_out)}  <- khach den dau bi xu ly CUOI!")


# =======================================================================
# MENU TUONG TAC
# =======================================================================
def interactive_menu(inventory, cart: Cart) -> None:
    OrderQueue = Queue()
    order_id = 2000
    menu = """
========== QUAN LY GIO HANG & DON HANG (Lab 3) ==========
1. Xem Gio hang + Tong tien       5. Thanh toan (dua vao OrderQueue)
2. Them san pham (nhap ID)        6. Xu ly toan bo OrderQueue (FIFO)
3. Xoa san pham (nhap ID)         7. Xem so don dang cho
4. Hoan tac (Undo) lan xoa cuoi   8. Thoat
Lua chon: """
    while True:
        try:
            c = input(menu).strip()
        except EOFError:
            break
        try:
            if c == "1": cart.print_cart()
            elif c == "2": cart.add_to_cart(inventory, int(input("Nhap ID can them: ")))
            elif c == "3": cart.remove_from_cart(int(input("Nhap ID can xoa: ")))
            elif c == "4": cart.undo()
            elif c == "5":
                name = input("Ten khach hang: ").strip() or "Khach"
                if checkout(cart, OrderQueue, name, order_id):
                    print(f"[OK] Da dua don #{order_id} vao OrderQueue."); order_id += 1
            elif c == "6": process_orders(OrderQueue)
            elif c == "7": print(f"Dang co {OrderQueue.size()} don cho xu ly.")
            elif c == "8": print("Tam biet!"); break
            else: print("[Loi] Lua chon khong hop le (1-8).")
        except ValueError:
            print("[Loi] ID khong hop le.")


def main() -> None:
    N = 100_000
    inventory = build_inventory(N)            # Kho hang Lab 2 (seed=42, giong Lab 1)
    print(f"Kho hang: {inventory.size()} san pham (ke thua Lab 1 + Lab 2).")

    demo_buoc1()
    demo_buoc2(inventory)
    arrival = demo_buoc3(inventory)
    demo_buoc4(arrival)
    print("\n===== KET THUC PHAN DEMO TU DONG =====\n")

    if "--demo" not in sys.argv:
        interactive_menu(inventory, Cart())


# =======================================================================
# BUOC 4 - DANH GIA & SO SANH (Chuong 4)
# -----------------------------------------------------------------------
# 1. Do phuc tap thoi gian (hien thuc bang Danh sach lien ket don + Tail):
#      Stack.push    : O(1) - insert_head, chi doi 2 con tro
#      Stack.pop     : O(1) - remove_head
#      Queue.enqueue : O(1) - insert_tail, nho giu con tro Tail
#      Queue.dequeue : O(1) - remove_head
#    Luu y: neu Queue khong giu Tail thi enqueue la O(n) (phai duyet het
#    danh sach). Neu hien thuc bang Mang, dequeue ngay tho (xoa phan tu 0
#    + don cac phan tu con lai) la O(n) - can mang vong de dat O(1).
#    Do phuc tap khong gian: O(n) cho n phan tu dang luu.
#
# 2. Vi sao KHONG the dung Stack thay Queue o Buoc 3?
#    Stack la LIFO: don den SAU duoc xu ly TRUOC, don den DAU phai cho
#    toi cuoi (co the khong bao gio duoc xu ly neu don moi lien tuc
#    den - "doi"/starvation). Xu ly don hang can cong bang "den truoc,
#    phuc vu truoc" = FIFO = ban chat cua Queue. Nguoc lai, Undo can
#    LIFO (huy thao tac gan nhat truoc) nen Buoc 2 dung Stack la dung.
# =======================================================================

if __name__ == "__main__":
    main()
