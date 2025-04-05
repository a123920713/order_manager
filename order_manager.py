import json
from typing import List, Dict, Tuple, Optional

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename: str) -> List[Dict]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_orders(filename: str, orders: List[Dict]) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)


def calculate_order_total(order: Dict) -> int:
    return sum(item['price'] * item['quantity'] for item in order['items'])

def add_order(orders: List[Dict]) -> str:
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(order['order_id'] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not name:
            break
        try:
            price = input("請輸入價格：").strip()
            if not price.isdigit() or int(price) < 0:
                raise ValueError("價格錯誤")
            price = int(price)
        except ValueError:
            print("=> 錯誤：價格或數量必須為整數，請重新輸入")
            continue

        try:
            quantity = input("請輸入數量：").strip()
            if not quantity.isdigit() or int(quantity) <= 0:
                raise ValueError("數量錯誤")
            quantity = int(quantity)
        except ValueError:
            print("=> 錯誤：數量必須為正整數，請重新輸入")
            continue

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({"order_id": order_id, "customer": customer, "items": items})
    return f"=> 訂單 {order_id} 已新增！"


def print_order_report(data: List[Dict], title: str = "訂單報表", single: bool = False) -> None:
    if not data:
        return
    print(f"\n{'=' * 20} {title} {'=' * 20}")
    for i, order in enumerate(data, start=1):
        if not single:
            print(f"訂單 #{i}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print("商品名稱\t單價\t數量\t小計")
        print("-" * 50)
        total = 0
        for item in order['items']:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{subtotal}")
        print("-" * 50)
        print(f"訂單總額: {total:,}")
        print("=" * 50)


def process_order(orders: List[Dict]) -> Tuple[str, Optional[Dict]]:
    if not orders:
        return ("=> 沒有待處理的訂單。", None)

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, start=1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("=" * 32)

    choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
    if not choice:
        return ("=> 已取消出餐處理。", None)
    if not choice.isdigit() or not (1 <= int(choice) <= len(orders)):
        return ("=> 錯誤：請輸入有效的數字", None)

    index = int(choice) - 1
    order = orders.pop(index)
    completed_orders = load_data(OUTPUT_FILE)
    completed_orders.append(order)
    save_orders(INPUT_FILE, orders)
    save_orders(OUTPUT_FILE, completed_orders)
    return (f"=> 訂單 {order['order_id']} 已出餐完成", order)


def main() -> None:
    while True:
        print("""
***************選單***************
1. 新增訂單
2. 顯示訂單報表
3. 出餐處理
4. 離開
**********************************
        """)
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        if choice == "":
            break
        elif choice == "1":
            orders = load_data(INPUT_FILE)
            msg = add_order(orders)
            save_orders(INPUT_FILE, orders)
            print(msg)
        elif choice == "2":
            orders = load_data(INPUT_FILE)
            print_order_report(orders)
        elif choice == "3":
            orders = load_data(INPUT_FILE)
            msg, order = process_order(orders)
            print(msg)
            if order:
                print("出餐訂單詳細資料：")
                print_order_report([order], title="出餐訂單", single=True)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")


if __name__ == "__main__":
    main()
