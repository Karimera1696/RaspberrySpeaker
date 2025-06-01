import asyncio


async def say_after(delay: float, message: str) -> None:
    await asyncio.sleep(delay)
    print(message)


async def main() -> None:
    # say_after(1, "A") を待たずに開始しておく
    task1 = asyncio.create_task(say_after(1, "1秒後に出るメッセージ"))
    # say_after(0.5, "B") は先に終わる
    task2 = asyncio.create_task(say_after(0.5, "0.5秒後に出るメッセージ"))

    print("ここはすぐに出力される")
    # 両方のタスクを待つ
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
