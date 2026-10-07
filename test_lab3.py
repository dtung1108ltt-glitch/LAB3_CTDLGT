"""Kiem thu tu dong Lab 3: python test_lab3.py"""
import io, contextlib
from stack import Stack
from queue_ds import Queue
from cart import Cart
from inventory import build_inventory
from order import checkout, process_orders

quiet = lambda: contextlib.redirect_stdout(io.StringIO())

def test_stack():
    s = Stack(max_size=2)
    with quiet():
        assert s.pop() is None and s.top() is None            # Underflow
        assert s.push(1) and s.push(2) and not s.push(3)      # Overflow
    assert s.top() == 2 and s.size() == 2
    assert [s.pop(), s.pop()] == [2, 1]                       # LIFO
    assert s.is_empty() and s.head is None and s.tail is None

def test_queue():
    q = Queue(max_size=2)
    with quiet():
        assert q.dequeue() is None and q.front() is None
        assert q.enqueue("a") and q.enqueue("b") and not q.enqueue("c")
    assert q.front() == "a"
    assert [q.dequeue(), q.dequeue()] == ["a", "b"]            # FIFO
    assert q.tail is None
    q.enqueue("z"); assert q.front() == "z" and q.tail.data == "z"

def test_undo():
    inv = build_inventory(50)
    c = Cart()
    with quiet():
        for i in (1, 2, 3): c.add_to_cart(inv, i)
        c.remove_from_cart(2); c.remove_from_cart(1)
        assert c.size() == 1
        assert c.undo() and c.find_by_id(1) is not None        # khoi phuc cai xoa sau cung
        assert c.undo() and c.find_by_id(2) is not None
        assert not c.undo()                                    # rong -> khong crash
        assert not c.remove_from_cart(99)
    assert c.size() == 3 and inv.size() == 50

def test_checkout_fifo():
    inv = build_inventory(50)
    oq = Queue()
    with quiet():
        for i, name in enumerate("ABC"):
            c = Cart(); c.add_to_cart(inv, i); c.add_to_cart(inv, i + 10)
            assert checkout(c, oq, name, i) and c.is_empty()
        assert not checkout(Cart(), oq, "X", 9)                # gio rong
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert process_orders(oq) == 3
    lines = out.getvalue().splitlines()
    assert [("khach " + n) in l for n, l in zip("ABC", lines)] == [True] * 3
    assert oq.is_empty()

if __name__ == "__main__":
    for f in (test_stack, test_queue, test_undo, test_checkout_fifo):
        f(); print("PASS", f.__name__)
