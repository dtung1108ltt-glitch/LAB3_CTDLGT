# Lab 3 - Mini E-commerce Core (Giai doan 3)
Xu ly luong nghiep vu voi **Xep chong (Stack)** va **Hang doi (Queue)**. Ngon ngu: Python 3.8+ (khong can thu vien ngoai).

Ke thua tu:
- Lab 1: https://github.com/dtung1108ltt-glitch/Lab1_CTDL-GT.git
- Lab 2: https://github.com/dtung1108ltt-glitch/LAB2_CTDT-GT.git

## Cach chay
```bash
python main.py          # demo Buoc 1-4 + menu tuong tac
python main.py --demo   # chi demo
python test_lab3.py     # kiem thu tu dong (Overflow/Underflow/LIFO/FIFO/Undo/Checkout)
```

## Cau truc & nguon goc tung file
| File | Nguon | Noi dung |
|---|---|---|
| `product.py` | **Lab 1 (nguyen ban)** | `Product`, `init_product`, `print_product`, `MAX_PRODUCTS` |
| `inventory.py` | **Lab 2 (nguyen ban)** | `build_inventory` (cong thuc sinh du lieu seed=42 cua Lab 1) |
| `linked_list.py` | **Lab 2** + 1 ham moi | `Node`, `SinglyLinkedList`; **them `remove_head()`** |
| `stack.py` | **Moi (Lab 3)** | `Stack` ke thua `SinglyLinkedList` |
| `queue_ds.py` | **Moi (Lab 3)** | `Queue` ke thua `SinglyLinkedList` |
| `cart.py` | **Lab 2 + nang cap** | `Cart` giu ham Lab 2, them `DeletedItems`, ghi de `remove_from_cart`, them `undo` |
| `order.py` | **Moi (Lab 3)** | `Order`, `create_order`, `checkout`, `process_orders` |
| `main.py` | **Moi** (cau truc theo Lab 2) | Demo 4 buoc, do Big-O, menu |
| `test_lab3.py` | **Moi** | Kiem thu tu dong |

## Cac ham / thuat toan KE THUA
| Ham / lop | Nguon | Thuat toan / phuong phap | Do phuc tap | Dung o dau trong Lab 3 |
|---|---|---|---|---|
| `Product`, `init_product`, `print_product` | Lab 1 | ADT (dataclass), High Cohesion/Low Coupling | O(1) | Phan tu cua Gio hang, Order, DeletedItems |
| Cong thuc sinh du lieu (`SanPham_i`, gia 1.000-5.000.000, ton 0-1000, `Random(42)`) | Lab 1 -> `inventory.py` Lab 2 | Sinh du lieu gia co seed co dinh | O(n) | Kho hang de khach "mua" |
| `time.perf_counter()` do thoi gian | Lab 1 / Lab 2 | Do thuc nghiem Big-O | - | Buoc 4: do Push/Pop/Enqueue/Dequeue |
| `Node` | Lab 2 | Nut danh sach lien ket (data + next) | O(1) | Nut cua Stack/Queue |
| `SinglyLinkedList.insert_head` | Lab 2 | Chen dau: `new.next=head; head=new` | O(1) | `Stack.push` |
| `SinglyLinkedList.insert_tail` | Lab 2 | Chen cuoi nho con tro **Tail** | O(1) | `Queue.enqueue`, `Cart.undo`, `add_to_cart` |
| `SinglyLinkedList.find_by_id` | Lab 2 | Duyet tuan tu (Linear Search, y tuong Lab 1) | O(n) | `remove_from_cart`, `add_to_cart` |
| `SinglyLinkedList.delete_by_id` | Lab 2 | Tim Node truoc + ngat lien ket an toan + `del` | O(n) | `Cart.remove_from_cart` |
| `SinglyLinkedList.to_list` | Lab 2 | Duyet danh sach xuat ra list | O(n) | `create_order` |
| `is_empty()`, `size()` | Lab 2 | Kiem tra `head is None`, bo dem `_size` | O(1) | Chong Underflow/Overflow |
| `Cart(SinglyLinkedList)`, `add_to_cart` (`deepcopy`), `calculate_total`, `print_cart` | Lab 2 | Ke thua (inheritance), sao chep sau (deep copy), cong don | O(n) | Gio hang cua moi khach |

## Cac ham / thuat toan MOI o Lab 3
| Ham | Thuat toan | Do phuc tap |
|---|---|---|
| `SinglyLinkedList.remove_head()` | Go Node dau: `head=head.next`; neu can thi `tail=None`; ngat lien ket + `del` | O(1) |
| `Stack.push / pop / top / is_empty / is_full` | LIFO tren dau danh sach (dinh = Head); tu choi khi day/rong | O(1) |
| `Queue.enqueue / dequeue / front / is_empty / is_full` | FIFO: them o Tail, lay o Head; reset Tail khi can | O(1) |
| `Cart.remove_from_cart` (ghi de) | `find_by_id` -> `DeletedItems.push` -> `delete_by_id` | O(n) |
| `Cart.undo` | `DeletedItems.pop` -> `insert_tail` | O(1) |
| `create_order` | Chup (deepcopy) toan bo Gio hang + `calculate_total` | O(n) |
| `checkout` | `create_order` -> `OrderQueue.enqueue` -> don gio, xoa lich su Undo | O(n) |
| `process_orders` | Vong lap `while not is_empty()`: `dequeue` roi xu ly (FIFO) | O(k) cho k don |

## Giai thich quyet dinh thiet ke
1. **Ke thua SinglyLinkedList thay vi viet lai**: tai su dung Node/Head/Tail cua Lab 2 (khuyen khich trong de bai Buoc 1).
2. **Dinh Stack = Head**: Push/Pop o dau danh sach la O(1); lay Tail lam dinh thi Pop thanh O(n) vi danh sach don khong co `prev`.
3. **Queue: enqueue o Tail, dequeue o Head**: giu con tro Tail (da co tu Lab 2) nen ca hai deu O(1).
4. **Chong Overflow/Underflow**: `max_size` tuy chon; `push/enqueue` tra `False` khi day, `pop/dequeue/top/front` tra `None` khi rong, khong nem exception, khong crash.
5. **Xoa gio hang khong "giai phong ngay"**: `remove_from_cart` Push **tham chieu Product** vao `DeletedItems` truoc khi go Node; Node bi `del` nhung Product van song nho Stack giu tham chieu. Neu Stack day thi huy thao tac xoa de khong mat du lieu.
6. **Han che da biet**: `undo()` dua san pham ve **cuoi** Gio hang (khong nho vi tri cu). `calculate_total` giu cach tinh cua Lab 2 (chi cong `price`, khong nhan so luong).

## Danh gia Buoc 4
- **Big-O**: Push, Pop, Enqueue, Dequeue deu **O(1)** (Queue can giu Tail; neu khong, Enqueue thanh O(n)). Do thuc nghiem trong `main.py`: thoi gian cho n thao tac tang tuyen tinh theo n.
- **Vi sao khong dung Stack thay Queue o xu ly don hang**: Stack la LIFO nen don den sau bi xu ly truoc, don den dau phai cho cuoi (co the khong bao gio duoc xu ly - starvation). Flash Sale can cong bang "den truoc phuc vu truoc" = FIFO. Nguoc lai, Undo can LIFO nen Buoc 2 dung Stack. `main.py` co demo xu ly cung don bang Stack de thay thu tu bi dao nguoc.
