import threading
import time
import random

def test2():
    process_id = random.randint(1000, 9999)
    print(f"Process ID: {process_id}")

    time.sleep(30+random.randint(0, 10))

    print("Process completed")
    return process_id

def test():
    thread = threading.Thread(target=test2)
    thread.start()
    return True

def main():
    for _ in range(100):
        result = test()
    print(f"Return value from test(): {result}")

if __name__ == "__main__":
    main()
